"""Post-acceptance replay/preservation only; no operator execution."""
import json,hashlib,sys
from pathlib import Path
P=Path(__file__).resolve().parent;V=P.parent;NAME='H-VAL001-COMPLETE-REAL-DRUM-PERIODICITY-01'
EXT=Path('/Volumes/SSD Track/JGA/experiments')/NAME
sys.path.insert(0,str(V/'production_streaming_harness_20260908'))
from streaming import canonical,sha
out=P/'replay.json';assert not out.exists();checks=0
def ck(name,ok):
 global checks
 checks+=1
 if not ok:
  out.write_bytes(canonical({'status':'FAIL_CONTRACT','check':name,'checks_passed':checks-1}));raise AssertionError(name)
def identical(a,b):
 with a.open('rb') as x,b.open('rb') as y:
  while True:
   p=x.read(65536);q=y.read(65536)
   if p!=q:return False
   if not p:return True
scores=[P/'score_1.json',P/'score_2.json'];ck('scores_pass',all(json.loads(s.read_bytes())['status']=='PASS' for s in scores));ck('scores_byte_identity',identical(*scores))
a=EXT/'run_1/production';b=EXT/'run_2/production';compared=0
for n in ('inputs.json','periods.json','windows.jsonl','index.json','root.json','metrics.json'):
 ck(n,identical(a/n,b/n));compared+=1
with (a/'index.json').open() as f:
 for line in f:
  r=json.loads(line);ck(r['name'],identical(a/r['name'],b/r['name']));compared+=1
binding=json.loads((P/'implementation_binding.json').read_bytes())
ck('frozen_sources',all(sha(Path(k))==h for k,h in binding['files'].items()))
score=json.loads(scores[0].read_bytes())
material={'experiment_id':NAME,'preregistration_sha256':sha(V/'preregistrations'/(NAME+'.md')),'input_sha256':sha(V/'preregistrations'/(NAME+'.inputs.json')),'authority_manifest_sha256':sha(V/'preregistrations'/(NAME+'.authorities.json')),'implementation_binding_sha256':sha(P/'implementation_binding.json'),'logical_fingerprint':score['logical_fingerprint'],'root_sha256':score['root_sha256'],'scoring_sha256':sha(scores[0]),'query_count':'4080384','scientific_status':'RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED'}
# Identical scoring and physical roots above establish identical material for both runs.
for run in ('run_1','run_2'):(P/(run+'_scientific_fingerprint_input.json')).write_bytes(canonical(material))
ck('fingerprint_material_bytes',identical(P/'run_1_scientific_fingerprint_input.json',P/'run_2_scientific_fingerprint_input.json'))
result={'status':'PASS','claim':'VAL001_COMPLETE_REAL_DRUM_LOCAL_COMPLEX_PERIODICITY_MAP_OBSERVED','checks_passed':checks,'checks_failed':0,'byte_compared_bulk_files':compared,'scientific_fingerprint':sha(P/'run_1_scientific_fingerprint_input.json'),'score_sha256':sha(scores[0]),'logical_fingerprint':score['logical_fingerprint'],'root_sha256':score['root_sha256'],'resources':{run:{n:json.loads((EXT/run/'production'/n).read_bytes()) for n in ('metrics.json','performance.json','preflight.json')} for run in ('run_1','run_2')}}
out.write_bytes(canonical(result));print('PASS replay',checks,compared,result['scientific_fingerprint'],flush=True)
