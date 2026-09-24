from pathlib import Path
import json,hashlib,csv,re,numpy as np,datetime
W=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();D=W/'development';H=W/'holdout'
sp=json.loads((W/'TAKE_SPLIT.json').read_text());assert not(set(sp['development'])&set(sp['holdout']));assert len(sp['development'])==8 and len(sp['holdout'])==4;assert sha(W/'TAKE_SPLIT.json')==json.loads((W/'SPLIT_FREEZE.json').read_text())['sha256']
for base,freeze in [(D,D/'output/SELECTOR_FREEZE.json'),(H,H/'output/PREDICTIONS_FREEZE.json'),(W,W/'EVALUATION_FREEZE.json')]:
 f=json.loads(freeze.read_text());assert all(sha(base/p)==h for p,h in f['files'].items())
for phase in [D,H]:
 checks=json.loads((phase/'output/ISOLATION_CHECKS.json').read_text());assert len(checks)==3 and all(c['read_denied'] for c in checks)
 for m in json.loads((phase/'input/MANIFEST.json').read_text()):assert sha(phase/'input'/m['audio'])==m['sha256']
assert not list((H/'input').glob('*GT*'));gt=json.loads((D/'input/GT_DEVELOPMENT.json').read_text());assert len(gt)==80 and all(g['take_id'] in sp['development'] for g in gt)
records={r['BP']['native_note_id']:r for r in json.loads((H/'output/BLIND_CANDIDATES.json').read_text())};pred=json.loads((H/'output/BLIND_PREDICTIONS.json').read_text());assert len(pred)==288
for p in pred:
 r=records[p['BP_id']];assert len(p['probabilities'])==len(r['candidates']);assert p['status'] in ['ATTACK_SELECTED','ABSTAIN_AMBIGUOUS','NO_CANDIDATE']
 if p['status']=='ATTACK_SELECTED':assert p['selected_s'] in [c['time_s'] for c in r['candidates']]
 for c in r['candidates']:
  assert r['search_start_s']<=c['time_s']<=r['search_end_s'];sample=c['time_s']*44100;assert abs((sample-512)/44-round((sample-512)/44))<1e-8;assert np.isfinite(c['features']).all()
rows=list(csv.DictReader((W/'HOLDOUT_ATTACK_SELECTIONS.csv').open()));assert len(rows)==40 and len({r['GT_ID'] for r in rows})==40
for r in rows:
 if r['selected_candidate']:assert abs((float(r['selected_candidate'])-float(r['GT_onset']))*1000-float(r['signed_error_ms']))<1e-9
G=W.parent/'JGA_GALLEGATI_CONTINUOUS_FISHMAN_GT_120_20260924/GROUND_TRUTH';assert sha(G/'GT_FREEZE.json')=='535e3d3d930db323320a5959da3999bc605ba278234671d0540d04b281b3ebd7';assert sha(G/'GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1.json')=='a4047bf252f28fa3289279bdcaa5e90226dcf0af994a51e0dd5df05174484631'
B=W.parent/'JGA_NATIVE_BP_GT_120_20260924/inference/output';f=json.loads((B/'TRANSCRIPTION_COMPLETE.json').read_text());assert all(sha(B/p)==h for p,h in f['files'].items())
pages={p.name:len(re.findall(rb'/Type /Page\b',p.read_bytes())) for p in W.glob('*.pdf')};assert sorted(pages.values())==[1,3,40]
times=[json.loads(p.read_text())['utc'] for p in [W/'SPLIT_FREEZE.json',D/'output/SELECTOR_FREEZE.json',H/'output/PREDICTIONS_FREEZE.json',W/'GT_REVEAL_RECORD.json',W/'EVALUATION_FREEZE.json']];assert times==sorted(times)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','original_GT_and_native_BP_unchanged':True,'all_freeze_hashes_verified':True,'disjoint_take_split':True,'negative_read_isolation_checks':6,'chronological_freeze_order_verified':times,'native_candidate_coordinates_preserved':True,'holdout_queries':288,'GT_rows':40,'PDF_pages':pages,'development_table_sha256_matches':sha(W/'DEVELOPMENT_CANDIDATES.csv')==sha(D/'output/DEVELOPMENT_CANDIDATES.csv')};(W/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
