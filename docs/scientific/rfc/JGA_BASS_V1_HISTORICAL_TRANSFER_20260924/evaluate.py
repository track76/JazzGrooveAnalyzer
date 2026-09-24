from pathlib import Path
import json,csv,hashlib,datetime,collections,numpy as np
W=Path(__file__).resolve().parent;I=W/'inference';R=W.parent;ROOT=R.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
f=json.loads((I/'output/HISTORICAL_ACOUSTIC_FREEZE.json').read_text());assert all(sha(I/p)==h for p,h in f['files'].items())
raw=R/'JGA_V1_OPERATIONAL_PLP_QUARTER_NEAREST_001_20260922/PLP_REFERENCE.csv';metric=ROOT/'docs/historical_reports/JGA_HISTORICAL_REPORT_001/FINAL_SCORE_V1/METRIC_REFERENCE.csv'
assert sha(raw)=='b6ed2a669b4e7d9b9fbcdd43618d0c801f5d4bfd60225b54e81415edee8e1666';assert sha(metric)=='15aca782227893092b962fe8b9ea9d67e2194f9f967a6634f80b2fbf92b00fd6'
if not (W/'PLP_REVEAL.json').exists():save(W/'PLP_REVEAL.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'acoustic_freeze_sha256':sha(I/'output/HISTORICAL_ACOUSTIC_FREEZE.json'),'raw_PLP_sha256':sha(raw),'metric_mapping_sha256':sha(metric)})
plp=list(csv.DictReader(raw.open()));mapping=list(csv.DictReader(metric.open()));times=np.array([float(q['time_seconds']) for q in plp]);assert len(times)==len(mapping)
for j,q in enumerate(mapping):assert float(q['reference_time'])==times[j]
def nearest(t):
 j=int(np.argmin(abs(times-t)));q=mapping[j];return {'nearest_PLP_quarter':q['quarter_label'],'quarter_index':j+1,'measure':int(q['measure_id'].removeprefix('M')) if q['measure_id'] else None,'beat':int(q['metric_beat']) if q['metric_beat'] else None,'PLP_time_s':float(times[j]),'delta_B_ms':(t-times[j])*1000}
att=json.loads((I/'output/UNIQUE_ACOUSTIC_ATTACKS.json').read_text());eps=json.loads((I/'output/EPISODE_DECISIONS.json').read_text());em={e['episode_id']:e for e in eps};qs=json.loads((I/'output/QUERY_DECISIONS.json').read_text());notes={n['native_note_id']:n for n in json.loads((I/'input/NOTES.json').read_text())}
for a in att:a.update(nearest(a['selected_s']))
counts=collections.Counter(a['nearest_PLP_quarter'] for a in att)
for a in att:a['quarter_multiplicity']=counts[a['nearest_PLP_quarter']]
quarter=[]
for j,q in enumerate(mapping):
 if q['measure_id'] and 33<=int(q['measure_id'].removeprefix('M'))<=48:quarter.append({'quarter':q['quarter_label'],'quarter_index':j+1,'measure':int(q['measure_id'].removeprefix('M')),'beat':int(q['metric_beat']),'PLP_time_s':float(q['reference_time']),'count':counts[q['quarter_label']],'classification':'ZERO' if counts[q['quarter_label']]==0 else 'ONE' if counts[q['quarter_label']]==1 else 'MULTIPLE','attack_ids':[a['attack_id'] for a in att if a['nearest_PLP_quarter']==q['quarter_label']]})
assert len(quarter)==64
unresolved=[]
for e in eps:
 if e['selected_s'] is None:unresolved.append({**e,'display_context':nearest(e['frozen_root_onset_s']),'display_qualification':'Native BP-root location only; no acoustic timestamp or measured delta assigned.'})
rows=[]
for a in att:
 ids=a['hypothesis_ids'];rows.append({'attack_event_id':a['attack_id'],'source_episode_ids':';'.join(a['episode_ids']),'hypothesis_ids':';'.join(ids),'pitch_hypotheses':json.dumps(a['pitch_hypotheses']),'route':';'.join(a['routes']),'BP_native_onsets_s':json.dumps({k:notes[k]['onset_local_s'] for k in ids}),'search_windows_s':json.dumps({k:[qs[k]['search_start_s'],qs[k]['search_end_s']] for k in ids}),'candidate_count':sum(qs[k]['candidate_count'] for k in ids),'selector_status':';'.join(em[e]['status'] for e in a['episode_ids']),'selected_acoustic_timestamp_s':a['selected_s'],'timing_provenance':a['timing_provenance'],'shared_attack':a['shared_attack'],'nearest_PLP_quarter':a['nearest_PLP_quarter'],'measure':a['measure'],'beat':a['beat'],'PLP_time_s':a['PLP_time_s'],'delta_B_ms':a['delta_B_ms'],'quarter_multiplicity':a['quarter_multiplicity'],'abstention_reason':'','notes':'JGA-estimated historical Bass-stem attack coordinate; not historical physical GT.'})
for e in unresolved:
 ids=e['hypothesis_ids'];rows.append({'attack_event_id':'UNRESOLVED_'+e['episode_id'],'source_episode_ids':e['episode_id'],'hypothesis_ids':';'.join(ids),'pitch_hypotheses':json.dumps([e['fundamental_midi']]),'route':e['route'],'BP_native_onsets_s':json.dumps({k:notes[k]['onset_local_s'] for k in ids}),'search_windows_s':json.dumps({k:[qs[k]['search_start_s'],qs[k]['search_end_s']] for k in ids}),'candidate_count':sum(qs[k]['candidate_count'] for k in ids),'selector_status':e['status'],'selected_acoustic_timestamp_s':None,'timing_provenance':e['timing_provenance'],'shared_attack':False,'nearest_PLP_quarter':'','measure':'','beat':'','PLP_time_s':None,'delta_B_ms':None,'quarter_multiplicity':None,'abstention_reason':e['status'],'notes':'No measured timing. BP context shown separately in figures; not an attack-to-quarter assignment.'})
with (W/'JGA_BASS_V1_EXACTLY_LIKE_YOU_ATTACKS.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def stats(aa):
 x=np.array([a['delta_B_ms'] for a in aa]);n=len(x)
 if not n:return {'N':0}
 return {'N':n,'median_ms':float(np.median(x)),'mean_ms':float(np.mean(x)),'IQR_ms':float(np.percentile(x,75)-np.percentile(x,25)),'P95_absolute_ms':float(np.percentile(abs(x),95)),'before_count':int(sum(x<0)),'after_count':int(sum(x>0)),'exact_count':int(sum(x==0)),'before_pct':float(100*np.mean(x<0)),'after_pct':float(100*np.mean(x>0)),'exact_pct':float(100*np.mean(x==0)),'beat_medians':{str(b):float(np.median([a['delta_B_ms'] for a in aa if a['beat']==b])) if any(a['beat']==b for a in aa) else None for b in [1,2,3,4]},'within_ms_counts':{str(k):int(sum(abs(x)<=k)) for k in [10,20,30,50,100]}}
result={'processed_episodes':63,'native_hypotheses':98,'selected_unique_attacks':len(att),'abstentions':len(unresolved),'shared_unique_attacks':sum(a['shared_attack'] for a in att),'quarters':64,'quarter_counts':dict(collections.Counter(q['classification'] for q in quarter)),'outside_target_quarters':sum(not(33<=a['measure']<=48) for a in att),'combined':stats(att),'routes':{route:{'episodes':sum(e['route']==route for e in eps),'selected_episodes':sum(e['route']==route and e['selected_s'] is not None for e in eps),'abstain_episodes':sum(e['route']==route and e['selected_s'] is None for e in eps),'abstention_rate_pct':100*sum(e['route']==route and e['selected_s'] is None for e in eps)/sum(e['route']==route for e in eps),'unique_attack_stats':stats([a for a in att if route in a['routes']])} for route in ['SECURE_ROUTE','AMBIGUOUS_ROUTE']}}
save(W/'MAPPED_UNIQUE_ATTACKS.json',att);save(W/'QUARTER_COUNTS.json',quarter);save(W/'UNRESOLVED_CONTEXT.json',unresolved);save(W/'RESULTS.json',result)
save(W/'PLP_EVALUATION_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{p:sha(W/p) for p in ['JGA_BASS_V1_EXACTLY_LIKE_YOU_ATTACKS.csv','MAPPED_UNIQUE_ATTACKS.json','QUARTER_COUNTS.json','UNRESOLVED_CONTEXT.json','RESULTS.json','evaluate.py']},'acoustic_freeze_sha256':sha(I/'output/HISTORICAL_ACOUSTIC_FREEZE.json')});print(json.dumps(result,indent=2))
