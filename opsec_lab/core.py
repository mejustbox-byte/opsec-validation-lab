"""Offline scenario verification; never executes manifest commands."""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
from opsec_reports.core import ReportError, load, validate, make_report
from opsec_reports.adapters import result

VERSION = '0.1.0a1'
MAX_CASES = 256
ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$')
HASH = re.compile(r'^[a-f0-9]{64}$')

def require(condition):
    if not condition:
        raise ReportError('invalid_manifest')

def exact(obj, keys):
    require(isinstance(obj, dict) and set(obj) == set(keys))

def manifest(data):
    exact(data, ['schema_version', 'suite_id', 'cases'])
    require(data['schema_version'] == 'lab-1.0' and isinstance(data['suite_id'], str) and ID.fullmatch(data['suite_id']))
    cases = data['cases']
    require(isinstance(cases, list) and 0 < len(cases) <= MAX_CASES)
    ids = set()
    for case in cases:
        exact(case, ['id', 'kind', 'report', 'sha256', 'producer', 'expected', 'provenance'])
        require(isinstance(case['id'], str) and ID.fullmatch(case['id']) and case['id'] not in ids)
        ids.add(case['id'])
        require(case['kind'] in ['synthetic', 'live'])
        require(isinstance(case['report'], str) and len(case['report']) <= 160)
        require(case['report'] == '' or (not case['report'].startswith('.') and '/' not in case['report'] and '\\' not in case['report'] and ':' not in case['report'] and case['report'].endswith('.json')))
        require(isinstance(case['sha256'], str) and (HASH.fullmatch(case['sha256']) or case['sha256'] == ''))
        require(bool(case['report']) == bool(case['sha256']))
        exact(case['producer'], ['name', 'version', 'ruleset'])
        require(all(isinstance(v, str) and 0 < len(v) <= 128 for v in case['producer'].values()))
        require(isinstance(case['expected'], list) and 0 < len(case['expected']) <= 10000)
        pairs = set()
        for expected in case['expected']:
            exact(expected, ['check_id', 'asset_id', 'status'])
            require(all(isinstance(expected[k], str) and 0 < len(expected[k]) <= 256 for k in ['check_id', 'asset_id']))
            require(expected['status'] in ['pass', 'fail', 'not_tested', 'not_applicable'])
            pair = expected['check_id'], expected['asset_id']
            require(pair not in pairs)
            pairs.add(pair)
        exact(case['provenance'], ['platform', 'platform_version', 'execution_id', 'sanitization_reviewed'])
        require(all(isinstance(case['provenance'][k], str) and len(case['provenance'][k]) <= 128 for k in ['platform', 'platform_version', 'execution_id']))
        require(type(case['provenance']['sanitization_reviewed']) is bool)
    return data

def read_report(root, name, digest):
    path = root / name
    # One regular file in the manifest directory; parents must also be ordinary directories.
    for parent in [root, *root.parents]:
        if parent.is_symlink():
            raise ReportError('unsafe_input')
    data = load(path)
    # Hash check is a consistency check, not a signature or provenance proof.
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_BINARY', 0)
    try:
        with os.fdopen(os.open(path, flags), 'rb') as stream:
            require(stat.S_ISREG(os.fstat(stream.fileno()).st_mode))
            raw = stream.read(8 * 1024 * 1024 + 1)
        require(hashlib.sha256(raw).hexdigest() == digest)
        require(json.loads(raw.decode('utf-8')) == data)
    except (OSError, UnicodeError, ValueError):
        raise ReportError('invalid_input') from None
    return validate(data)

def evaluate(data, root, observed_at):
    manifest(data)
    records = []
    details = []
    for case in data['cases']:
        states = {f'LAB-00{i}': 'not_tested' for i in range(1, 5)}
        reason = 'unavailable'
        report = None
        if case['report']:
            try:
                report = read_report(root, case['report'], case['sha256'])
            except ReportError:
                reason = 'invalid_evidence'
        if report is not None:
            actual = {(r['check_id'], r['asset_id']): r['status'] for r in report['results']}
            expected = {(r['check_id'], r['asset_id']): r['status'] for r in case['expected']}
            states['LAB-001'] = 'pass' if actual == expected else 'fail'
            states['LAB-002'] = 'pass' if report['producer'] == case['producer'] and case['provenance']['platform'] and case['provenance']['platform_version'] else 'fail'
            states['LAB-003'] = 'pass' if report['run']['synthetic'] == (case['kind'] == 'synthetic') else 'fail'
            if case['kind'] == 'live' and not case['provenance']['execution_id']:
                states['LAB-003'] = 'not_tested'
            states['LAB-004'] = 'pass' if case['provenance']['sanitization_reviewed'] else 'not_tested'
            reason = 'verified_assertions'
        for check, status in states.items():
            record = result(check, case['id'], status, 'high' if status == 'fail' else 'info')
            record['message'] = 'Scenario assertion ' + status
            records.append(record)
        details.append({'case_id': case['id'], 'kind': case['kind'], 'evidence_state': reason, 'checks': states})
    # Lab result itself is an offline synthetic assessment of supplied assertions.
    report = make_report('opsec-validation-lab', VERSION, 'lab-1.0', data['suite_id'], observed_at, True, records)
    return {'schema_version': 'lab-result-1.0', 'assessment': report, 'cases': details}
