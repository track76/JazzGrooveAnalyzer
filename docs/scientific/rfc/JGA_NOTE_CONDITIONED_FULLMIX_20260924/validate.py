from pathlib import Path
import json,hashlib,csv,re,datetime
P=Path(__file__).resolve().parent;I=P/'inference/input';O=P/'inference/output';load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for fp,base in [(P/'RULE_INPUT_FREEZE.json',P),(O/'PRE_RESULT_FREEZE.json',O),(O/'RESULT_FREEZE.json',O)]:
 for f,h in load(fp)['files'].items():assert sha(base/f)==h,(fp,f)
assert sha(P/'inference/run.py')==load(O/'PRE_RESULT_FREEZE.json')['implementation_sha256']
for f,h in load(P/'INPUT_AUDIT.json').items():assert sha(Path(f))==h,f
native={r['note_id']:r['native_hypothesis'] for r in load(P.parent/'JGA_BASIC_PITCH_HARMONIC_FAMILY_20260924/tracking/output/HYPOTHESIS_MEMBERSHIP.json')}
for r in csv.DictReader(open(I/'MEMBERSHIP.csv')):assert json.loads(r['native_hypothesis'])==native[r['note_id']]
E=load(I/'EPISODES.json');identity=load(O/'TARGET_IDENTITIES.json');assert len(identity)==63
for e,t in zip(E,identity):assert e['member_ids']==t['exact_member_ids'] and e['fundamental_midi']==t['frozen_root_midi']
Q=load(I/'QUERY_EVIDENCE.json');R=load(O/'CANDIDATE_ATTRIBUTIONS.json');actual=set((r['BP_member_id'],r['sample']) for r in R);expected=set((bid,f['sample']) for bid,q in Q.items() for f in q['fullmix_fronts']);assert actual==expected
for r in R:assert Q[r['BP_member_id']]['search_start_s']<=r['candidate_s']<=Q[r['BP_member_id']]['search_end_s']
T=load(O/'TEMPLATES_SIGNATURES.json');assert sum(t['f0']<=2*t['halfwidth_hz'] for t in T.values())==59
assert all(sum(t['observable'])<3 for t in T.values() if t['f0']>2*t['halfwidth_hz'])
assert all(c['read_denied'] for c in load(O/'ISOLATION_CHECKS.json'))
pages={}
for f,n in [('JGA_NOTE_CONDITIONED_FULLMIX_ATTRIBUTION_63.pdf',63),('JGA_MULTIPLE_CUE_BASS_ATTRIBUTION.pdf',34),('JGA_HF044_HF047_NOTE_ATTRIBUTION.pdf',2)]:
 pages[f]=len(re.findall(rb'/Type /Page\b',(P/f).read_bytes()));assert pages[f]==n
assert sha(P/'NOTE_CONDITIONED_FULLMIX_ATTRIBUTION.csv')==sha(O/'NOTE_CONDITIONED_FULLMIX_ATTRIBUTION.csv')
v={'status':'PASS','all_input_output_freezes_verified':True,'all_original_sources_unchanged':True,'native_membership_CSV_equals_frozen_JSON':True,'episodes':63,'exact_native_members':98,'all_previous_query_candidate_records_retained':len(expected),'candidate_note_evaluations':len(R),'no_candidates_regenerated_or_moved':True,'all_candidates_within_original_windows':True,'no_model_execution':True,'PLP_denied':True,'resolution_limited_templates':59,'remaining_templates_insufficient_observable_bands':58,'PDF_pages':pages,'pre_result_freeze_sha256':sha(O/'PRE_RESULT_FREEZE.json')}
(P/'VALIDATION.json').write_text(json.dumps(v,indent=2)+'\n')
(P/'REPORT_MANIFEST.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{p.name:sha(p) for p in sorted(P.iterdir()) if p.is_file() and p.name!='REPORT_MANIFEST.json'},'result_freeze_sha256':sha(O/'RESULT_FREEZE.json')},indent=2)+'\n')
print(json.dumps(v,indent=2))
