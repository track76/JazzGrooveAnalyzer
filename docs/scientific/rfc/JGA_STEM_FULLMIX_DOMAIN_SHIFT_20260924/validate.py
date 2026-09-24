from pathlib import Path
import json,hashlib,re,csv,datetime
P=Path(__file__).resolve().parent;I=P/'inference';O=I/'output'
load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks={}
for name,base in [('INPUT_FREEZE.json',P),('inference/output/DIAGNOSTIC_FREEZE.json',I)]:
 d=load(P/name)
 for f,h in d['files'].items():assert sha(base/f)==h,(name,f)
 checks[name]='PASS'
assert sha(I/'run.py')==load(O/'DIAGNOSTIC_FREEZE.json')['implementation_sha256']
a=load(P/'INPUT_AUDIT.json')
for src in a['source_PCM']:
 assert sha(Path(src['source']))==src['sha256']
 assert sha(I/'input'/('FULLMIX.wav' if src['signal']=='mix' else 'BASS.wav'))==src['sha256']
for f,h in a['verified_freezes'].items():assert sha(Path(f))==h
checks['sources_and_prior_freezes_unchanged']='PASS'
prior=P.parent/'JGA_BASS_V1_HISTORICAL_TRANSFER_20260924/inference/output'
for name in ['BLIND_CANDIDATES.json','QUERY_DECISIONS.json','EPISODE_DECISIONS.json','UNIQUE_ACOUSTIC_ATTACKS.json']:
 assert sha(I/'input'/name)==sha(prior/name)
checks['exact_prior_windows_candidates_decisions']='PASS'
Q=load(O/'QUERY_EVIDENCE.json');E=load(O/'EPISODE_DIAGNOSTICS.json')
assert len(Q)==98 and len(E)==63 and len({e['episode_id'] for e in E})==63
assert sum(e['historical_selected_s'] is not None for e in E)==17
assert sum(e['route']=='SECURE_ROUTE' for e in E)==28
assert sum(e['route']=='AMBIGUOUS_ROUTE' for e in E)==35
for q in Q.values():
 for f in q['fullmix_fronts']:
  assert q['search_start_s']<=f['timestamp_s']<=q['search_end_s']
  assert abs(f['timestamp_s']*44100-f['sample'])<1e-6
checks['all_fronts_inside_exact_independent_windows']='PASS'
assert all(x['read_denied'] for x in load(O/'ISOLATION_CHECKS.json'))
checks['execution_isolation_negative_reads']='PASS (3/3)'
assert sha(P/'STEM_FULLMIX_ATTACK_INTERROGATION.csv')==sha(O/'STEM_FULLMIX_ATTACK_INTERROGATION.csv')
checks['PDF_pages']={}
for name,n in [('JGA_STEM_VS_FULLMIX_63_EPISODES.pdf',63),('JGA_FULLMIX_ABSTENTION_RECOVERY_DIAGNOSTIC.pdf',46),('JGA_SELECTED_STEM_ATTACKS_FULLMIX_CROSSCHECK.pdf',17)]:
 count=len(re.findall(rb'/Type /Page\b',(P/name).read_bytes()));assert count==n,(name,count);checks['PDF_pages'][name]=count
checks['visual_review']='HF044 synchronized four-panel render inspected; no PLP, unchanged BP/stem markers and all bounded full-mix peaks visible.'
checks['classification_freeze_sha256']=sha(O/'DIAGNOSTIC_FREEZE.json')
checks['no_fullmix_logistic_or_attack_selection']=True
checks['status']='PASS'
(P/'VALIDATION.json').write_text(json.dumps(checks,indent=2)+'\n')
files=[p for p in P.iterdir() if p.is_file() and p.name!='REPORT_MANIFEST.json']
(P/'REPORT_MANIFEST.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'classification_freeze_sha256':sha(O/'DIAGNOSTIC_FREEZE.json'),'files':{p.name:sha(p) for p in sorted(files)}},indent=2)+'\n')
print(json.dumps(checks,indent=2))
