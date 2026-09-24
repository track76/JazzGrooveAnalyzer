from pathlib import Path
import json,csv,hashlib,datetime,collections
from stats import metrics
W=Path(__file__).resolve().parent;O=W/'inference/output';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
c=json.loads((O/'TRANSCRIPTION_COMPLETE.json').read_text());assert all(sha(O/f)==h for f,h in c['files'].items())
G=W.parent/'JGA_GALLEGATI_CONTINUOUS_FISHMAN_GT_120_20260924/GROUND_TRUTH';assert sha(G/'GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1.json')=='a4047bf252f28fa3289279bdcaa5e90226dcf0af994a51e0dd5df05174484631'
gt=json.loads((G/'GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1.json').read_text())['events']; sources={r['source_wav']:r for r in json.loads((W/'SOURCE_MAP.json').read_text())};notes=json.loads((O/'ALL_NATIVE_NOTES.json').read_text()); rows=[];associated=set();audit=[]
for source,m in sources.items():
 events=sorted([g for g in gt if g['source_wav']==source],key=lambda g:float(g['final_center_s']));ns=[n for n in notes if n['clip_id']==m['clip_id']]
 for i,g in enumerate(events):
  t=float(g['final_center_s']);lo=float(g['final_earliest_s']);hi=float(g['final_latest_s']); left=(float(events[i-1]['final_center_s'])+t)/2 if i else 0;right=(float(events[i+1]['final_center_s'])+t)/2 if i+1<len(events) else m['duration'];pitch=g['midi_pitch']
  cand=[n for n in ns if left<=n['onset_local_s']<right and n['offset_local_s']>=lo]
  exact=[n for n in cand if n['midi_pitch']==pitch];octave=[n for n in cand if n['midi_pitch']!=pitch and (n['midi_pitch']-pitch)%12==0]; tier=exact or octave or cand
  cls='MISSED' if not tier else 'MULTIPLE_BP_CANDIDATES' if len(tier)>1 else 'CORRECT_PITCH_MATCH' if exact else 'OCTAVE_EQUIVALENT' if octave else 'WRONG_PITCH'
  selected=tier[0] if len(tier)==1 else None
  associated.update(n['native_note_id'] for n in cand)
  error=(selected['onset_local_s']-t)*1000 if selected else None
  r={'GT_event_id':g['event_id'],'take':g['take_id'],'string':g['string'],'condition':{'f':'forte','COMFORTABLE_NATURAL':'comfortable-natural'}.get(g['dynamic'],g['dynamic']),'expected_pitch':pitch,'GT_onset':t,'GT_lower_bound':lo,'GT_upper_bound':hi,'matched_BP_event_id':selected['native_note_id'] if selected else '', 'BP_MIDI_pitch':selected['midi_pitch'] if selected else None,'BP_onset':selected['onset_local_s'] if selected else None,'BP_offset':selected['offset_local_s'] if selected else None,'match_classification':cls,'signed_error_ms':error,'absolute_error_ms':abs(error) if error is not None else None,'interval_relation':('BEFORE' if selected['onset_local_s']<lo else 'AFTER' if selected['onset_local_s']>hi else 'INSIDE') if selected else '', 'notes':f'{len(exact)} exact-pitch, {len(octave)} octave-equivalent, {len(cand)} total persistent hypotheses; no timing-error ranking','candidate_ids':';'.join(n['native_note_id'] for n in tier),'source_wav':source,'clip_id':m['clip_id']}
  rows.append(r)
  for n in ns:
   if left<=n['onset_local_s']<right:audit.append({**n,'GT_event_id':g['event_id'],'candidate':n in cand,'highest_pitch_tier':n in tier,'selected':n==selected,'onset_minus_GT_ms':(n['onset_local_s']-t)*1000,'ends_before_GT_interval':n['offset_local_s']<lo})
assert len(rows)==120 and len({r['GT_event_id'] for r in rows})==120
with (W/'GALLEGATI_NATIVE_BP_VS_GT_120.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
save(W/'EVENT_RESULTS.json',rows);save(W/'ALL_HYPOTHESES_ASSOCIATION_AUDIT.json',audit)
extra=[n for n in notes if n['native_note_id'] not in associated];save(W/'ADDITIONAL_UNASSOCIATED_BP_NOTES.json',extra)
result={'native_hypotheses':len(notes),'GT_events':120,'counts':dict(collections.Counter(r['match_classification'] for r in rows)),'additional_unassociated_notes':len(extra),'ambiguous_associated_hypotheses':sum(len(r['candidate_ids'].split(';')) for r in rows if r['match_classification']=='MULTIPLE_BP_CANDIDATES'),'pooled':metrics(rows),'by_string':{v:metrics([r for r in rows if r['string']==v]) for v in ['E','A','D','G']},'by_condition':{v:metrics([r for r in rows if r['condition']==v]) for v in ['mf','comfortable-natural','forte']},'by_take':{v:metrics([r for r in rows if r['take']==v]) for v in sorted({r['take'] for r in rows})}}
save(W/'RESULTS.json',result)
save(W/'RAW_RESULTS_FREEZE.json',{'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_output_freeze_sha256':sha(O/'TRANSCRIPTION_COMPLETE.json'),'protocol_sha256':sha(W/'MATCHING_PROTOCOL.json'),'GT_unchanged_sha256':sha(G/'GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1.json'),'files':{f:sha(W/f) for f in ['GALLEGATI_NATIVE_BP_VS_GT_120.csv','EVENT_RESULTS.json','ALL_HYPOTHESES_ASSOCIATION_AUDIT.json','ADDITIONAL_UNASSOCIATED_BP_NOTES.json','RESULTS.json']}})
print(json.dumps(result,indent=2))
