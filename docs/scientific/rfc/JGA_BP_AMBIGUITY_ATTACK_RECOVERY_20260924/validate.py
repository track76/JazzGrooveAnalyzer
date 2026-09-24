from pathlib import Path
import json,hashlib,csv,re,datetime
W=Path(__file__).resolve().parent;P=W.parent/'JGA_LEARNED_LOCAL_ATTACK_SELECTOR_20260924';I=W/'inference';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for base,fp in [(W,W/'INPUT_FREEZE.json'),(I,I/'output/RECOVERY_FREEZE.json'),(W,W/'EVALUATION_FREEZE.json'),(P/'development',P/'development/output/SELECTOR_FREEZE.json'),(P/'holdout',P/'holdout/output/PREDICTIONS_FREEZE.json')]:
 f=json.loads(fp.read_text());assert all(sha(base/p)==h for p,h in f['files'].items())
for a,b in [('selector.py','development/selector.py'),('morphology.py','development/morphology.py'),('input/MODEL.joblib','development/output/MODEL.joblib'),('input/SELECTOR_RULE.json','development/output/SELECTOR_RULE.json')]:assert sha(I/a)==sha(P/b)
checks=json.loads((I/'output/ISOLATION_CHECKS.json').read_text());assert len(checks)==3 and all(c['read_denied'] for c in checks)
records=json.loads((I/'input/CANDIDATES.json').read_text());assert len(records)==760;recordmap={r['BP']['native_note_id']:r for r in records};groups=json.loads((I/'output/PREDICTIONS.json').read_text());ids=[i for g in groups for i in g['BP_ids']];assert len(ids)==len(set(ids))==760
for g in groups:
 cand=[c for b in g['BP_ids'] for c in recordmap[b]['candidates']];assert g['candidate_context_count']==len(cand)
 if g['selected_s'] is not None:assert any(c['time_s']==g['selected_s'] and c['candidate_id']==g['selected_id'] for c in cand);assert any(lo<=g['selected_s']<=hi for lo,hi in g['search_intervals'])
rows=json.loads((W/'EVENT_RESULTS.json').read_text());assert len(rows)==48;assert sum(r['cohort']=='natural_ambiguous' for r in rows)==13;assert sum(r['cohort']=='masked_holdout' for r in rows)==35
for r in rows:
 if r['selected_timestamp'] is not None:assert abs((r['selected_timestamp']-r['GT_onset'])*1000-r['signed_error_ms'])<1e-9
raw=json.loads((W/'RAW_60_SELECTION_AUDIT.json').read_text());assert len(raw)==len({r['BP_id'] for r in raw})==60
G=W.parent/'JGA_GALLEGATI_CONTINUOUS_FISHMAN_GT_120_20260924/GROUND_TRUTH';assert sha(G/'GT_FREEZE.json')=='535e3d3d930db323320a5959da3999bc605ba278234671d0540d04b281b3ebd7';assert sha(G/'GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1.json')=='a4047bf252f28fa3289279bdcaa5e90226dcf0af994a51e0dd5df05174484631'
B=W.parent/'JGA_NATIVE_BP_GT_120_20260924/inference/output';f=json.loads((B/'TRANSCRIPTION_COMPLETE.json').read_text());assert all(sha(B/p)==h for p,h in f['files'].items())
times=[json.loads(p.read_text())['utc'] for p in [W/'INPUT_FREEZE.json',I/'output/REGIONS_HASH.json',I/'output/RECOVERY_FREEZE.json',W/'GT_REVEAL.json',W/'EVALUATION_FREEZE.json']];assert times==sorted(times)
pages={p.name:len(re.findall(rb'/Type /Page\b',p.read_bytes())) for p in W.glob('*.pdf')};assert sorted(pages.values())==[4,13]
v={'status':'PASS','GT_BP_and_parent_selector_hashes_unchanged':True,'new_freeze_hashes_verified':True,'isolation_negative_checks':3,'native_queries':760,'union_groups':137,'population_rows':48,'raw_selection_audit_rows':60,'selected_coordinates_unchanged':True,'prediction_before_GT_order':times,'PDF_pages':pages};(W/'VALIDATION.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v,indent=2))
