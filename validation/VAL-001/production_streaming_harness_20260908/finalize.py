"""Preservation checks only. Does not invoke workers or scorers."""
import json,hashlib
from pathlib import Path
P=Path(__file__).parent;ext=Path(json.loads((P/'source_freeze.json').read_bytes())['external_run_root'])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def identical(a,b):
 with a.open('rb') as x,b.open('rb') as y:
  while True:
   u=x.read(65536);v=y.read(65536)
   if u!=v:return False
   if not u:return True
checks=[]
def ck(name,ok):
 checks.append({'check':name,'pass':bool(ok)})
 if not ok:
  (P/'preservation_failure.json').write_text(json.dumps(checks,sort_keys=True,separators=(',',':')))
  raise RuntimeError('FAIL '+name)
results={};resources={};roots={};scores={};compared=0
freeze=json.loads((P/'source_freeze.json').read_bytes())
ck('frozen_sources',all(sha(P/n)==h for n,h in freeze['files'].items()))
ck('frozen_preregistration',sha(P.parent/'preregistrations/H-VAL001-PRODUCTION-STREAMING-HARNESS-01.md')==freeze['preregistration_sha256'])
for fixture in ('E','C','S'):
 s1=P/f'score_1_{fixture}.json';s2=P/f'score_2_{fixture}.json'
 s=json.loads(s1.read_bytes());ck(fixture+':run_scores_pass',s['status']=='PASS' and json.loads(s2.read_bytes())['status']=='PASS')
 ck(fixture+':score_bytes',identical(s1,s2));scores[fixture]=sha(s1)
 for mode in ('reference','production'):
  a=ext/'run_1'/mode/fixture;b=ext/'run_2'/mode/fixture
  fixed=['metrics.json']+(['logical.jsonl'] if mode=='reference' else ['inputs.json','periods.json','windows.jsonl','index.json','root.json'])
  if fixture=='E':fixed.append('templates.json')
  for name in fixed:ck(fixture+':'+mode+':'+name,identical(a/name,b/name));compared+=1
  if mode=='production':
   with (a/'index.json').open() as f:
    for line in f:
     row=json.loads(line);ck(fixture+':'+row['name'],identical(a/row['name'],b/row['name']));compared+=1
   roots[fixture]={'root':json.loads((a/'root.json').read_bytes()),'root_sha256':sha(a/'root.json')}
  for run in ('run_1','run_2'):
   loc=ext/run/mode/fixture;resources[f'{run}/{mode}/{fixture}']={'performance':json.loads((loc/'performance.json').read_bytes()),'metrics':json.loads((loc/'metrics.json').read_bytes())}
 results[fixture]=s
summary={'status':'PASS','claim':'PRODUCTION_STREAMING_PERIODICITY_HARNESS_VALIDATED','scores':results,'score_sha256':scores,'replay_checks':checks,'byte_compared_files':str(compared),'scoring_checks_per_run':str(sum(int(s['checks_passed']) for s in results.values())),'scoring_checks_total':str(2*sum(int(s['checks_passed']) for s in results.values())),'roots':roots,'preregistration_sha256':freeze['preregistration_sha256'],'scope':'Only frozen synthetic numerical fixtures and transport stress; no real-data authority.'}
for name,obj in [('result.json',summary),('resources.json',resources)]:
 (P/name).write_text(json.dumps(obj,sort_keys=True,separators=(',',':')))
print('PASS final preservation',len(checks),'checks;',compared,'files byte-compared',flush=True)
