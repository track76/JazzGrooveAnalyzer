from pathlib import Path
import json,hashlib,csv,shutil,datetime
W=Path(__file__).resolve().parent;R=W.parent;P=R/'JGA_LEARNED_LOCAL_ATTACK_SELECTOR_20260924';C=R/'JGA_CONTAINED_BP_FALLBACK_20260924';H=R/'JGA_BASIC_PITCH_HARMONIC_FAMILY_20260924';I=W/'inference';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
checks=[]
for base,fp in [(P/'development',P/'development/output/SELECTOR_FREEZE.json'),(C/'inference',C/'inference/output/PREDICTION_FREEZE.json'),(H/'tracking/output',H/'tracking/output/EPISODE_FREEZE.json')]:
 f=json.loads(fp.read_text());assert all(sha(base/p)==v for p,v in f['files'].items());checks.append({'path':str(fp),'sha256':sha(fp),'files_verified':True})
f=json.loads((H/'tracking/output/EPISODE_FREEZE.json').read_text());assert all(sha(H/'tracking/input'/p)==v for p,v in f['input_hashes'].items())
eps=json.loads((H/'tracking/output/FUNDAMENTAL_EPISODES.json').read_text());native=list(csv.DictReader((H/'tracking/input/notes.csv').open()));nmap={n['note_id']:n for n in native};routes=[]
for e in eps:
 ids=e['member_ids'] if e['ambiguity'] else e['root_note_ids'];assert e['ambiguity'] or len(ids)==1;assert all(k in nmap for k in ids)
 routes.append({'episode_id':e['episode_id'],'route':'AMBIGUOUS_ROUTE' if e['ambiguity'] else 'SECURE_ROUTE','frozen_flag':'FLAGGED' if e['ambiguity'] else 'UNFLAGGED','hypothesis_ids':ids,'frozen_member_ids':e['member_ids'],'root_ids':e['root_note_ids'],'frozen_root_onset_s':e['root_onset_s'],'fundamental_midi':e['fundamental_midi'],'frozen_flags':e['flags']})
assert len(routes)==63 and sum(r['route']=='SECURE_ROUTE' for r in routes)==28 and sum(r['route']=='AMBIGUOUS_ROUTE' for r in routes)==35
assert all(r['hypothesis_ids']==r['frozen_member_ids'] for r in routes if r['route']=='AMBIGUOUS_ROUTE')
save(W/'ROUTING_AUTHORITY.json',{'authority':'Explicit PI approval in current conversation','scope':'Operational Bass-v1 historical routing; not GT-correct identity','rule':'28 frozen UNFLAGGED → SECURE_ROUTE, native root only.35 frozen FLAGGED → AMBIGUOUS_ROUTE, exact frozen family members independently. No outcome-dependent changes.','excluded_inputs':['PLP','Report001 timing','PI-selected attack timestamps','historical acoustic outcomes'],'routing_inputs':'Frozen episode identity/flags/member IDs only','timing_source':'Unchanged preserved Demucs Bass PCM; original mix is PLP source, not a replacement attack coordinate. No independent Demucs latency validation.'})
save(I/'input/ROUTING.json',routes)
with (W/'ROUTING_TABLE.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(routes[0]));w.writeheader();w.writerows([{k:json.dumps(v) if isinstance(v,list) else v for k,v in r.items()} for r in routes])
save(W/'ROUTING_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{str(p.relative_to(W)):sha(p) for p in [W/'ROUTING_AUTHORITY.json',W/'ROUTING_TABLE.csv',I/'input/ROUTING.json']},'episodes':63,'SECURE_ROUTE':28,'AMBIGUOUS_ROUTE':35})
# Routing frozen before audio processing. Copy full native stem so unchanged generator uses original source coordinates/grid.
align=json.loads((R/'JGA_CROSS_REPRESENTATION_TRANSIENT_ATTRIBUTION_20260924/ALIGNMENT_AUDIT.json').read_text());source=[]
for s in align['signals']:
 if s['signal'] in ['mix','bass']:
  assert sha(Path(s['source']))==s['sha256'];source.append(s)
  if s['signal']=='bass':shutil.copyfile(s['source'],I/'input/BASS.wav');basshash=s['sha256']
F=R/'JGA_BP_FRAGMENT_REARTICULATION_20260924';ff=json.loads((F/'CLASSIFICATION_FREEZE.json').read_text());assert sha(F/'CLASSIFICATIONS.json')==ff['classification_sha256'];checks.append({'path':str(F/'CLASSIFICATION_FREEZE.json'),'sha256':sha(F/'CLASSIFICATION_FREEZE.json'),'classification_verified':True,'used_to_change_routing':False})
notes=[]
for n in native:
 notes.append({'clip_id':'BASS','native_note_id':n['note_id'],'onset_local_s':float(n['onset_s']),'offset_local_s':float(n['offset_s']),'duration_s':float(n['offset_s'])-float(n['onset_s']),'midi_pitch':int(n['midi_pitch']),'amplitude':float(n['amplitude']),'pitch_bends':json.loads(n['pitch_bends'])})
save(I/'input/NOTES.json',notes);save(I/'input/MANIFEST.json',[{'clip_id':'BASS','audio':'BASS.wav','notes':'NOTES.json','sha256':basshash}])
for f in ['selector.py','morphology.py']:shutil.copyfile(P/'development'/f,I/f)
for f in ['MODEL.joblib','SELECTOR_RULE.json']:shutil.copyfile(P/'development/output'/f,I/'input'/f)
save(W/'INPUT_AUDIT.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verified_authorities':checks,'source_pcm':source,'source_origin_s':0,'source_sample_rate':44100,'native_BP_hypotheses':98,'episodes':63,'original_source_alignment':'Full stem preserves original sample coordinates; no crop-origin shift, no time or amplitude normalization added. Native frozen generator downmixes stereo by arithmetic mean exactly as during controlled study.','scope':'PROCESS-BLINDED RESTART AFTER INVESTIGATOR PLP EXPOSURE. No claim of investigator blindness. No PLP loaded during preparation.','upstream_rerun':False})
save(W/'INFERENCE_INPUT_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{str(p.relative_to(W)):sha(p) for p in [I/'input/NOTES.json',I/'input/MANIFEST.json',I/'input/MODEL.joblib',I/'input/SELECTOR_RULE.json',I/'selector.py',I/'morphology.py',W/'INPUT_AUDIT.json']}})
s='(version 1)\n(allow default)\n(deny network*)\n(deny file-read* (subpath "/Users") (subpath "/Volumes") (subpath "/private/tmp"))\n'
for p in [str(I),str(Path('.venv').resolve())]:s+=f'(allow file-read* (subpath "{p}"))\n'
(W/'isolation.sb').write_text(s+'(allow file-read-metadata)\n');print('Routing frozen:28/35; all authority and PCM hashes verified; isolated inputs ready.')
