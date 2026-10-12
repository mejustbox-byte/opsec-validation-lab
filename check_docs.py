from pathlib import Path
import re
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parent
ru={p.name for p in (ROOT/'docs/ru').glob('*.md')};en={p.name for p in (ROOT/'docs/en').glob('*.md')};assert ru==en
for p in ROOT.rglob('*.md'):
 if any(x in {'build','dist'} or x.endswith('.egg-info') for x in p.parts):continue
 text=p.read_text(encoding='utf-8');assert text.count('```')%2==0
 for target in re.findall(r'\]\(([^)]+)\)',text):
  if '://' not in target:assert (p.parent/target).exists(),target
for name in ru:
 blocks=lambda lang:re.findall(r'```\w*\n(.*?)```',(ROOT/'docs'/lang/name).read_text(encoding='utf-8'),re.S)
 assert blocks('ru')==blocks('en')
with tempfile.TemporaryDirectory() as tmp:
 for fixture,status in [('suite.synthetic.json',0),('live-unexecuted.json',2)]:
  r=subprocess.run([sys.executable,'-m','opsec_lab','verify',str(ROOT/'examples'/fixture),'--observed-at','2026-10-12T00:00:00Z','--output',str(Path(tmp)/fixture)],cwd=ROOT,capture_output=True,text=True)
  assert r.returncode==status,r.stdout+r.stderr
print(f'OK: {len(ru)} bilingual page pairs and executable examples')
