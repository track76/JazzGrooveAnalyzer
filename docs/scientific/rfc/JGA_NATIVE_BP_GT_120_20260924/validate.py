from pathlib import Path
import json,hashlib,csv,numpy as np,datetime,re
W=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();o=W/'inference/output'
f=json.loads((o/'TRANSCRIPTION_COMPLETE.json').read_text());assert f['clips']==12 and f['GT_read']==False
for n,h in f['files'].items():assert sha(o/n)==h
for p in o.glob('*MODEL_OUTPUT.npz'):
 z=np.load(p);assert all(np.isfinite(z[k]).all() for k in z.files)
f2=json.loads((W/'RAW_RESULTS_FREEZE.json').read_text())
for n,h in f2['files'].items():assert sha(W/n)==h
rows=list(csv.DictReader((W/'GALLEGATI_NATIVE_BP_VS_GT_120.csv').open()));assert len(rows)==120 and len({r['GT_event_id'] for r in rows})==120
ns={r['native_note_id']:r for r in json.loads((o/'ALL_NATIVE_NOTES.json').read_text())};ids=[]
for r in rows:
 if r['matched_BP_event_id']:
  n=ns[r['matched_BP_event_id']];assert float(r['BP_onset'])==n['onset_local_s'];assert abs(float(r['signed_error_ms'])-(n['onset_local_s']-float(r['GT_onset']))*1000)<1e-9;ids.append(r['matched_BP_event_id'])
assert len(ids)==len(set(ids))==107
G=W.parent/'JGA_GALLEGATI_CONTINUOUS_FISHMAN_GT_120_20260924/GROUND_TRUTH';assert sha(G/'GT_FREEZE.json')=='535e3d3d930db323320a5959da3999bc605ba278234671d0540d04b281b3ebd7';assert sha(G/'GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1.json')=='a4047bf252f28fa3289279bdcaa5e90226dcf0af994a51e0dd5df05174484631'
pages={p.name:len(re.findall(rb'/Type /Page\b',p.read_bytes())) for p in W.glob('*.pdf')};assert sorted(pages.values())==[1,1,6]
(W/'VALIDATION.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'GT_hashes_unchanged':True,'complete_take_outputs':12,'native_hypotheses':760,'all_model_values_finite':True,'all_output_and_result_hashes_verified':True,'unique_GT_rows':120,'unique_unmoved_native_matches':107,'PDF_pages':pages,'no_timing_correction':True},indent=2)+'\n');print(pages)
