from pathlib import Path
import json,hashlib,csv,re,datetime,numpy as np
W=Path(__file__).resolve().parent;I=W/'inference';R=W.parent;P=R/'JGA_LEARNED_LOCAL_ATTACK_SELECTOR_20260924';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for base,fp in [(W,W/'ROUTING_FREEZE.json'),(W,W/'INFERENCE_INPUT_FREEZE.json'),(I,I/'output/HISTORICAL_ACOUSTIC_FREEZE.json'),(W,W/'PLP_EVALUATION_FREEZE.json'),(P/'development',P/'development/output/SELECTOR_FREEZE.json')]:
 f=json.loads(fp.read_text());assert all(sha(base/p)==h for p,h in f['files'].items())
for local,old in [('selector.py','selector.py'),('morphology.py','morphology.py'),('input/MODEL.joblib','output/MODEL.joblib'),('input/SELECTOR_RULE.json','output/SELECTOR_RULE.json')]:assert sha(I/local)==sha(P/'development'/old)
routes=json.loads((I/'input/ROUTING.json').read_text());ep=json.loads((I/'output/EPISODE_DECISIONS.json').read_text());orig=json.loads((R/'JGA_BASIC_PITCH_HARMONIC_FAMILY_20260924/tracking/output/FUNDAMENTAL_EPISODES.json').read_text());om={e['episode_id']:e for e in orig};assert len(routes)==len(ep)==63
for r in routes:
 o=om[r['episode_id']];assert r['hypothesis_ids']==(o['member_ids'] if o['ambiguity'] else o['root_note_ids']);assert r['route']==('AMBIGUOUS_ROUTE' if o['ambiguity'] else 'SECURE_ROUTE')
assert sum(r['route']=='SECURE_ROUTE' for r in routes)==28
records={r['BP']['native_note_id']:r for r in json.loads((I/'output/BLIND_CANDIDATES.json').read_text())};qs=json.loads((I/'output/QUERY_DECISIONS.json').read_text());assert len(records)==len(qs)==98
for k,q in qs.items():
 r=records[k];assert len(q['probabilities'])==len(r['candidates'])
 if q['selected_s'] is not None:assert q['selected_s'] in [c['time_s'] for c in r['candidates']];assert r['search_start_s']<=q['selected_s']<=r['search_end_s']
 for c in r['candidates']:assert np.isfinite(c['features']).all();sample=c['time_s']*44100;assert abs((sample-512)/44-round((sample-512)/44))<1e-8
att=json.loads((W/'MAPPED_UNIQUE_ATTACKS.json').read_text());assert len(att)==len({a['native_sample_coordinate'] for a in att})==17
for a in att:assert abs((a['selected_s']-a['PLP_time_s'])*1000-a['delta_B_ms'])<1e-9
q=json.loads((W/'QUARTER_COUNTS.json').read_text());assert len(q)==64;assert sum(x['count']==0 for x in q)==47;assert sum(x['count']==1 for x in q)==17;assert sum(x['count']>1 for x in q)==0
rows=list(csv.DictReader((W/'JGA_BASS_V1_EXACTLY_LIKE_YOU_ATTACKS.csv').open()));assert len(rows)==63;assert sum(bool(x['selected_acoustic_timestamp_s']) for x in rows)==17;assert sum(not x['selected_acoustic_timestamp_s'] for x in rows)==46
assert all(c['read_denied'] for c in json.loads((I/'output/ISOLATION_CHECKS.json').read_text()))
times=[json.loads(p.read_text())['utc'] for p in [W/'ROUTING_FREEZE.json',W/'INFERENCE_INPUT_FREEZE.json',I/'output/HISTORICAL_ACOUSTIC_FREEZE.json',W/'PLP_REVEAL.json',W/'PLP_EVALUATION_FREEZE.json']];assert times==sorted(times)
pages={p.name:len(re.findall(rb'/Type /Page\b',p.read_bytes())) for p in W.glob('*.pdf')};assert sorted(pages.values())==[1,1,6,63]
# Prove original historical tracker, source PCM and reference authorities remain unchanged.
h=R/'JGA_BASIC_PITCH_HARMONIC_FAMILY_20260924';f=json.loads((h/'tracking/output/EPISODE_FREEZE.json').read_text());assert all(sha(h/'tracking/output'/p)==v for p,v in f['files'].items());assert all(sha(h/'tracking/input'/p)==v for p,v in f['input_hashes'].items())
audit=json.loads((W/'INPUT_AUDIT.json').read_text());assert all(sha(Path(s['source']))==s['sha256'] for s in audit['source_pcm']);assert sha(R/'JGA_V1_OPERATIONAL_PLP_QUARTER_NEAREST_001_20260922/PLP_REFERENCE.csv')==json.loads((W/'PLP_REVEAL.json').read_text())['raw_PLP_sha256']
result={'status':'PASS','model_features_generator_thresholds_unchanged':True,'approved_routing_63_28_35_verified':True,'exact_frozen_flagged_members_verified':True,'source_PCM_and_historical_tracker_unchanged':True,'PLP_unchanged':True,'isolated_queries':98,'episodes':63,'unique_selected_attacks':17,'abstentions':46,'quarter_counts':[47,17,0],'timing_coordinates_native_and_unshifted':True,'freeze_sequence':times,'PDF_pages':pages,'scope':'Technical validation, not independent historical timing/identity validation.'};(W/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
report_files=['JGA_BASS_V1_HISTORICAL_REPORT.md','JGA_BASS_V1_HISTORICAL_REPORT.pdf','JGA_BASS_V1_EXACTLY_LIKE_YOU_GROOVE.pdf','JGA_BASS_V1_MEASURE_BY_MEASURE.pdf','JGA_BASS_V1_HISTORICAL_ATTACK_AUDIT.pdf','NATIVE_HYPOTHESIS_PROVENANCE.csv','FINAL_GATE.json','REPORT001_COMPARISON.json','VALIDATION.json','render.py'];(W/'HISTORICAL_REPORT_FREEZE.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'PI-authorized historical report artifact only; NOT Bass-v1 canonical milestone closure','files':{p:sha(W/p) for p in report_files},'parents':{p:sha(W/p) for p in ['ROUTING_FREEZE.json','INFERENCE_INPUT_FREEZE.json','inference/output/HISTORICAL_ACOUSTIC_FREEZE.json','PLP_EVALUATION_FREEZE.json']}},indent=2)+'\n');print(json.dumps(result,indent=2))
