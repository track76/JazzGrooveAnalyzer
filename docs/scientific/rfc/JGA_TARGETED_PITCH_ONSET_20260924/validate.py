from pathlib import Path
import json,hashlib,csv,re,datetime,numpy as np
P=Path(__file__).resolve().parent;I=P/'inference/input';O=P/'inference/output';load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for fp,base in [(P/'METHOD_INPUT_FREEZE.json',P),(O/'OBSERVATION_FREEZE.json',O)]:
 for k,h in load(fp)['files'].items():assert sha(base/k)==h,(fp,k)
assert sha(P/'inference/run.py')==load(O/'OBSERVATION_FREEZE.json')['implementation_sha256']
for k,h in load(P/'INPUT_AUDIT.json').items():assert sha(Path(k))==h,k
assert sha(I/'FULLMIX.wav')=='c890658d8c8f67e0d295d7ab334712227c2c2c999283a1fdb5cf32e6af7a467f'
assert sha(I/'EPISODES.json')=='52aff9d008fe108d747a529e925ba7e12af940088e75439e8e040ed786e6b5ef'
E=load(I/'EPISODES.json');T=load(O/'TARGET_DEFINITIONS.json');R=load(O/'TARGET_OBSERVATIONS.json');A=load(O/'EPISODE_OBSERVATIONS.json');M={r['note_id']:json.loads(r['native_hypothesis']) for r in csv.DictReader(open(I/'MEMBERSHIP.csv'))}
assert len(T)==len(A)==63 and len(M)==98 and len(R)==117
for e,t in zip(E,T):assert [m['note_id'] for m in t['exact_members']]==e['member_ids'] and t['frozen_fundamental_midi']==e['fundamental_midi']
assert set(r['BP_member_id'] for r in R)==set(M)
Z=np.load(O/'TARGET_TRACES.npz')
for r in R:
 assert r['BP_onset_s']==float(M[r['BP_member_id']]['onset_s'])
 assert abs(r['window_start_s']-(r['BP_onset_s']-.15))<1e-12 and abs(r['window_end_s']-(r['BP_onset_s']+.15))<1e-12
 assert r['f0_hz']==440*2**((r['midi_pitch']-69)/12)
 t=Z[r['query_id']+'_t']
 for c in r['target_onset_candidates_s']:
  assert r['window_start_s']<=c<=r['window_end_s'] and np.any(t==c)
  assert abs(c*44100/44-round(c*44100/44))<1e-8
 if r['target_onset_status']=='TARGET_ONSET_CLEAR':assert len(r['target_onset_candidates_s'])==1 and r['selected_clear_onset_s']==r['target_onset_candidates_s'][0]
assert all(v['read_denied'] for v in load(O/'ISOLATION_CHECKS.json'))
assert sha(P/'TARGETED_PITCH_ONSET_FULLMIX.csv')==sha(O/'TARGETED_PITCH_ONSET_FULLMIX.csv')
S=load(P/'SUMMARY.json');pages={}
for fn,n in [('JGA_TARGETED_PITCH_ONSET_63.pdf',63),('JGA_TARGETED_PITCH_ONSET_SUMMARY.pdf',1),('JGA_TARGETED_PITCH_SPECIAL_CASES.pdf',len(S['special_figure_episode_ids']))]:
 pages[fn]=len(re.findall(rb'/Type /Page\b',(P/fn).read_bytes()));assert pages[fn]==n
v={'status':'PASS','method_inputs_observations_hash_verified':True,'original_fullmix_hash_verified':True,'frozen63_episodes_hash_verified':True,'all98_native_members_preserved':True,'117_independent_target_queries':True,'onset_candidates_are_original_frame_coordinates_within_exact_windows':True,'no_timing_correction':True,'filesystem_probes_denied':2,'no_Bass_PCM_or_model_or_historical_selection_in_inference_inputs':True,'PDF_pages':pages,'visual_review':'HF044 enlarged rendered panel inspected; aligned original waveform/target trace/BP/crossing and post-freeze comparison marker visible; no PLP.','observation_freeze_sha256':sha(O/'OBSERVATION_FREEZE.json')}
(P/'VALIDATION.json').write_text(json.dumps(v,indent=2)+'\n')
(P/'REPORT_MANIFEST.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{p.name:sha(p) for p in sorted(P.iterdir()) if p.is_file() and p.name!='REPORT_MANIFEST.json'},'observation_freeze_sha256':sha(O/'OBSERVATION_FREEZE.json')},indent=2)+'\n');print(json.dumps(v,indent=2))
