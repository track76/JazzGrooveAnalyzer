from analyze import P,A,B,p1,p2,meta,sha,read,out,D
import json,collections,datetime
import soundfile as sf
G=P.parent/'JGA_BASIC_PITCH_GALLEGATI_TIMING_VALIDATION_20260924/GROUND_TRUTH';F=P/'GROUND_TRUTH';F.mkdir(exist_ok=True)
assert not (F/'GT_FREEZE.json').exists(),'Do not rewrite a freeze.'
assert json.loads((P/'REPEATABILITY_SUMMARY.json').read_text())['GT_construction_allowed']
assert sha(G/'GT_FREEZE.json')=='7b62b71cf41051c73eee85590c4f4a88b42030c2dfd618c302dc39ac88a75832'
for n,h in json.loads((G/'GT_FREEZE.json').read_text())['files'].items():assert sha(G/n)==h
old=json.loads((G/'GALLEGATI_FISHMAN_OBSERVABLE_ONSET_GT_V1.json').read_text())['events'];oldmap={x['event_id']:x for x in old};oldcsv={x['event_id']:x for x in read(G/'GALLEGATI_FISHMAN_OBSERVABLE_ONSET_GT_V1.csv')}
canonical={x['EVENT_ID']:x for x in read(P.parent/'DOUBLE_BASS_GALLEGATI_EVENT_RESOLUTION_20260919/EVENT_RESOLUTION_MANIFEST.csv') if x['SESSION_DATE']=='2026-09-14'}
rows=[];provenance={}
for o in old:
 row=dict(o);row.update(repetition=int(canonical[o['event_id']]['REPETITION']),reference_class='EXISTING_GT36_UNCHANGED');rows.append(row)
 provenance[o['event_id']]={'parent_GT_file':str(G/'GALLEGATI_FISHMAN_OBSERVABLE_ONSET_GT_V1.json'),'parent_GT_freeze_sha256':sha(G/'GT_FREEZE.json'),'original_record':o}
for eid in sorted(p1):
 a=p1[eid];v=a['values'];assert not a['raw']['uncertain'];assert v['earliest']<=v['center']<=v['latest'];x=meta[eid]
 if eid in p2:
  b=p2[eid];w=b['values'];center=(v['center']+w['center'])/2;earliest=min(v['earliest'],w['earliest']);latest=max(v['latest'],w['latest']);kind='NEW_TWO_PASS_MIDPOINT_OUTER_ENVELOPE'
 else:w=None;center=v['center'];earliest=v['earliest'];latest=v['latest'];kind='NEW_PRIMARY_ONLY_COHORT_AUDITED'
 row={'event_id':eid,'source_wav':x['source_wav'],'source_sha256':x['source_sha256'],'take_id':x['take'],'string':x['string'],'pitch':x['pitch'],'midi_pitch':{'E':28,'A':33,'D':38,'G':43}[x['string']],'dynamic':x['dynamic'],'articulation':'pizzicato','status':'FINAL','final_center_s':float(center),'final_earliest_s':float(earliest),'final_latest_s':float(latest),'uncertainty_width_ms':float((latest-earliest)*1000),**{'pass1_'+k+'_s':float(v[k]) for k in ['center','earliest','latest']},**{'pass2_'+k+'_s':float(w[k]) if w else None for k in ['center','earliest','latest']},'adjudication_item':None,'final_provenance':kind,'decision_detail':'Current PI-authorized conditional construction; FINAL_REFERENCE_RULE.json recorded before Pass2 comparison','reason':'No adjudication trigger; source coordinates restored from native crop offsets','repetition':int(x['repetition']),'reference_class':kind}
 rows.append(row);provenance[eid]={'pass1':a,'pass2':p2.get(eid),'restoration':'crop_start_sample/sample_rate + local exported seconds','reference_class':kind}
rows.sort(key=lambda x:(x['take_id'],x['repetition']))
assert len(rows)==len({r['event_id'] for r in rows})==120 and {r['event_id'] for r in rows}==set(canonical)
counts=collections.Counter(r['take_id'] for r in rows);assert len(counts)==12 and set(counts.values())=={10}
sources={}
for r in rows:
 e=canonical[r['event_id']];assert r['take_id']==e['SOURCE_TRIPLET_ID'] and r['string']==e['STRING_GT'] and r['pitch']==e['PITCH_GT'] and r['dynamic']==e['DYNAMIC_GT'] and r['repetition']==int(e['REPETITION'])
 from pathlib import Path
 path=Path(r['source_wav'])
 if str(path) not in sources:
  assert sha(path)==r['source_sha256'];info=sf.info(path);assert info.samplerate==44100 and info.subtype=='PCM_24' and info.channels==1;sources[str(path)]={'sha256':r['source_sha256'],'duration':info.duration}
 assert 0<=float(r['final_earliest_s'])<=float(r['final_center_s'])<=float(r['final_latest_s'])<=sources[str(path)]['duration']
 if r['event_id'] in oldmap:
  for k,v in oldmap[r['event_id']].items():assert r[k]==v
name='GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1'
definition='Channel-specific observable onset in the Fishman Full Circle pickup signal; NOT physical string-release Ground Truth.'
payload={'artifact':name,'definition':definition,'scope':'September14 controlled validation artifact only','time_basis':'Seconds from start of original continuous source WAV','precision':'1ms human marker steps; no sub-ms human accuracy claim','population':{'existing_unchanged':36,'new_primary_only':60,'new_two_pass':24,'total':120,'takes':12},'events':rows}
(F/(name+'.json')).write_text(json.dumps(payload,indent=2)+'\n')
# Preserve literal old CSV field strings, too.
csvrows=[]
for r in rows:
 z=dict(r)
 if r['event_id'] in oldcsv:z.update(oldcsv[r['event_id']])
 csvrows.append(z)
out(F/(name+'.csv'),csvrows)
def serial(x):
 if isinstance(x,D):return str(x)
 raise TypeError(type(x))
(F/'ANNOTATION_PROVENANCE.json').write_text(json.dumps(provenance,indent=2,default=serial)+'\n')
(F/'README.md').write_text('# '+name+'\n\n'+definition+'\n\n120 unique September-14 events; 12 continuous Fishman takes × 10 notes. Native source coordinates, no snapping or detector-derived reference. Original 36 records and their final values preserved exactly. New 60 primary-only references retain primary values; new 24 repeated references use the precomparison midpoint/outer-envelope rule, preserving both passes. Primary-only records are not individually repeat-validated.\n\nSame-rater reproducibility does not establish physical accuracy or cross-rater agreement. The 1 ms interface step prevents claims of sub-ms human accuracy from fractional coordinates. Individual plausible intervals, including wide original adjudicated intervals, remain relevant to subsequent validation.\n\nThis is a controlled Fishman validation artifact, not JGA canonical methodology or physical string-release GT. Ready for a prospective take-level split, not an executed detector study. All previously analyzed takes have prior isolated-event exposure; a future take-level holdout can test new continuous logic but is not wholly unseen audio.\n')
parents=[G/'GT_FREEZE.json',P/'FINAL_REFERENCE_RULE.json',P/'REPEATABILITY_SUMMARY.json',P/'EVENT_REPEATABILITY.csv',B/'SELECTION_RULE_FREEZE.json',B/'SELECTION_RULE.json',A/'TECHNICAL/PRIVATE_EXCERPT_MANIFEST.csv',B/'TECHNICAL/PASS2_PRIVATE_MANIFEST.csv',P.parent/'DOUBLE_BASS_GALLEGATI_EVENT_RESOLUTION_20260919/EVENT_RESOLUTION_MANIFEST.csv']
for base,passno in [(P,2),(B,1)]:
 for suffix in ['RESPONSES','RECEIPT']:parents.append(base/f'ORIGINAL_EXPORTS/PI_FISHMAN_CONTINUOUS_GT_PASS{passno}_{suffix}.json')
freeze={'artifact':name,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'PI-authorized validation artifact only','definition':definition,'included':120,'excluded':0,'uncertain':0,'files':{p.name:sha(p) for p in sorted(F.iterdir()) if p.is_file()},'parents':{str(p):sha(p) for p in parents},'sources':sources,'validation':{'unique_events':120,'takes':dict(counts),'all_metadata_and_bounds_verified':True,'old36_JSON_values_exact':True,'old36_CSV_field_strings_exact':True,'source_hashes_verified':12,'no_detector_executed':True}}
(F/'GT_FREEZE.json').write_text(json.dumps(freeze,indent=2)+'\n')
print('GT JSON SHA256',sha(F/(name+'.json')));print('GT FREEZE SHA256',sha(F/'GT_FREEZE.json'))
