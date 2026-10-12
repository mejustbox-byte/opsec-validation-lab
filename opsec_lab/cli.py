import argparse
import json
from pathlib import Path
from opsec_reports.core import ReportError, load, outcome, write_new
from .core import evaluate, manifest

def main():
    parser = argparse.ArgumentParser(prog='opsec-lab')
    commands = parser.add_subparsers(dest='command', required=True)
    check = commands.add_parser('check-manifest'); check.add_argument('input')
    run = commands.add_parser('verify'); run.add_argument('input'); run.add_argument('--observed-at', required=True); run.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        data = load(args.input); manifest(data)
        if args.command == 'check-manifest':
            print('valid_manifest'); return 0
        result = evaluate(data, Path(args.input).absolute().parent, args.observed_at)
        write_new(args.output, json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        print('lab_result_written'); return outcome(result['assessment'])
    except ReportError:
        print('invalid_input_or_output'); return 3
    except OSError:
        print('input_or_output_unavailable'); return 3
