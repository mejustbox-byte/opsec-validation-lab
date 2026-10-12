import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from opsec_reports.core import ReportError, outcome
from opsec_lab.core import manifest, evaluate
ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-12T00:00:00Z'
class LabTests(unittest.TestCase):
 def setUp(self):
  self.data=json.loads((ROOT/'examples/suite.synthetic.json').read_text(encoding='utf-8'))
 def assess(self):
  return evaluate(self.data,ROOT/'examples',DATE)
 def test_positive_matrix(self):
  r=self.assess();self.assertEqual(outcome(r['assessment']),0);self.assertEqual(set(r['cases'][0]['checks'].values()),{'pass'})
 def test_wrong_expected_status(self):
  self.data['cases'][0]['expected'][0]['status']='fail';self.assertEqual(self.assess()['cases'][0]['checks']['LAB-001'],'fail')
 def test_missing_expected_result_is_mismatch(self):
  self.data['cases'][0]['expected'][0]['asset_id']='other';self.assertEqual(self.assess()['cases'][0]['checks']['LAB-001'],'fail')
 def test_wrong_version(self):
  self.data['cases'][0]['producer']['version']='other';self.assertEqual(self.assess()['cases'][0]['checks']['LAB-002'],'fail')
 def test_absent_platform(self):
  self.data['cases'][0]['provenance']['platform_version']='';self.assertEqual(self.assess()['cases'][0]['checks']['LAB-002'],'fail')
 def test_synthetic_cannot_be_live(self):
  self.data['cases'][0]['kind']='live';self.assertEqual(self.assess()['cases'][0]['checks']['LAB-003'],'fail')
 def test_live_missing_execution(self):
  self.data['cases'][0]['kind']='live';self.data['cases'][0]['provenance']['execution_id']='';self.assertEqual(self.assess()['cases'][0]['checks']['LAB-003'],'not_tested')
 def test_review_is_attestation(self):
  self.data['cases'][0]['provenance']['sanitization_reviewed']=False;self.assertEqual(self.assess()['cases'][0]['checks']['LAB-004'],'not_tested')
 def test_invalid_evidence_never_pass(self):
  self.data['cases'][0]['sha256']='0'*64;r=self.assess();self.assertEqual(outcome(r['assessment']),2);self.assertEqual(set(r['cases'][0]['checks'].values()),{'not_tested'})
 def test_unavailable_live_never_pass(self):
  d=json.loads((ROOT/'examples/live-unexecuted.json').read_text(encoding='utf-8'));self.assertEqual(outcome(evaluate(d,ROOT/'examples',DATE)['assessment']),2)
 def test_unsafe_paths(self):
  for name in ['../report.json','/report.json','C:report.json','sub/report.json','sub\\report.json']:
   self.data['cases'][0]['report']=name
   with self.assertRaises(ReportError):manifest(self.data)
 def test_strict_manifest(self):
  for value in [None,[],{'schema_version':'lab-1.0'},dict(self.data,extra=True)]:
   with self.assertRaises(ReportError):manifest(value)
 def test_duplicates(self):
  self.data['cases'].append(copy.deepcopy(self.data['cases'][0]))
  with self.assertRaises(ReportError):manifest(self.data)
 def test_types(self):
  for field,value in [('sanitization_reviewed',1),('platform',[]),('execution_id',{})]:
   self.data['cases'][0]['provenance'][field]=value
   with self.assertRaises(ReportError):manifest(self.data)
   self.setUp()
 def test_invalid_report(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'bad.json';p.write_text('{"x":NaN}',encoding='utf-8');self.data['cases'][0].update(report=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest());self.assertEqual(outcome(evaluate(self.data,Path(tmp),DATE)['assessment']),2)
 def test_cli_no_overwrite(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'output.json';args=[sys.executable,'-m','opsec_lab','verify',str(ROOT/'examples/suite.synthetic.json'),'--observed-at',DATE,'--output',str(p)]
   for status in [0,3]:
    r=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,timeout=20);self.assertEqual(r.returncode,status,r.stdout+r.stderr)
if __name__=='__main__':unittest.main()
