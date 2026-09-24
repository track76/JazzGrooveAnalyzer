from pathlib import Path
import json,hashlib,datetime,shutil
W=Path(__file__).resolve().parent;R=W.parent;P=R/'JGA_LEARNED_LOCAL_ATTACK_SELECTOR_20260924';B=R/'JGA_NATIVE_BP_GT_120_20260924';I=W/'inference';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
checks={}
for base,fp in [(P/'development',P/'development/output/SELECTOR_FREEZE.json'),(P/'holdout',P/'holdout/output/PREDICTIONS_FREEZE.json')]:
 f=json.loads(fp.read_text());assert all(sha(base/p)==h for p,h in f['files'].items());checks[str(fp)]=sha(fp)
G=R/'JGA_GALLEGATI_CONTINUOUS_FISHMAN_GT_120_20260924/GROUND_TRUTH'
for name,h in [('GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1.json','a4047bf252f28fa3289279bdcaa5e90226dcf0af994a51e0dd5df05174484631'),('GT_FREEZE.json','535e3d3d930db323320a5959da3999bc605ba278234671d0540d04b281b3ebd7')]:assert sha(G/name)==h;checks[name]=h
nf=json.loads((B/'inference/output/TRANSCRIPTION_COMPLETE.json').read_text());assert all(sha(B/'inference/output'/p)==h for p,h in nf['files'].items())
# Population projection copied WITHOUT reference coordinates, kept outside inference sandbox.
old=json.loads((B/'EVENT_RESULTS.json').read_text());hold=json.loads((P/'HOLDOUT_RESULTS.json').read_text())
cohorts={'natural_ambiguous':[{'event_id':r['GT_event_id'],'take':r['take'],'BP_ids':r['candidate_ids'].split(';')} for r in old if r['match_classification']=='MULTIPLE_BP_CANDIDATES'],'masked_holdout':[{'event_id':r['GT_ID'],'take':r['take'],'BP_ids':[r['BP_id']]} for r in hold if r['BP_id']]};assert len(cohorts['natural_ambiguous'])==13 and len(cohorts['masked_holdout'])==35
save(W/'EVALUATION_POPULATIONS.json',cohorts)
protocol={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'question':'BP identity-ambiguous but temporally guided recovery; Fishman observable onset, NOT physical string release.','population':'Run all760 native hypotheses across12takes; no target GT IDs, matched BP IDs, string/dynamic/pitch correctness or GT sent to inference. Project13natural and35previouslyresolved holdout cases only after freeze. Natural13 comprise8development-take cases and5holdout cases, not13independent holdout.','group_rule':'For every native hypothesis form activity-support interval [frozen search_start, max(native offset,frozen search_end)]. Connected components of overlapping/touching intervals within each take; chronological sweep. No pitch restriction. Actual interrogation region is union of the original ±150ms onset windows only, not the entire activity-support envelope; gaps remain gaps.','candidate_rule':'Reuse byte-verified already-frozen local candidates/features for all native hypotheses. No new acoustic detection, feature computation or timestamp changes. Keep every candidate-context feature vector, including multiple representations of same coordinate.','selection_rule':'Call the exact frozen decide() on concatenated original candidate-context records in each union group. Same model/scaler/threshold0.5/exact-score-tie abstention. Highest score wins; tied score abstains even if duplicate contexts have same timestamp. No GT tie breaking, new thresholds, collapsing or timestamp averaging.','cohort_projection':'After freeze map previous correspondence BP IDs to operational components. All relevant IDs in one component: report that frozen component decision. Multiple components: ABSTAIN_AMBIGUOUS, no post-GT choice among components and no new merged region. Preserve all component predictions in audit.','catastrophic_rule':'Absolute selected timing error >100ms (same prior association tolerance), scoring only. Also report all >20/>30ms errors and correct yields, not just selected timing.','mode2':'NOT EXECUTABLE: no compatible independently frozen acoustic region authority, and BP signed-distance, absolute-distance and relative-activity features are undefined without BP. No replacement features or new region detector authorized.','raw60_audit':'Preserve all prior60non-resolved-query selections. Map to human references only after freeze; distinguish membership in requested cohorts from temporal compatibility. Within100ms is temporal compatibility, not proof of identity/correctness. No reference within100ms: UNVERIFIED_RAW_SELECTION, not necessarily false event.','limitations':'Prior investigator exposure to GT and prior outcomes; process-isolated inference, not investigator blind. Activity-union grouping is a prospectively declared input construction, not a retrained model or established acoustic episode authority.'}
save(W/'PROTOCOL.json',protocol)
records=[]
for phase in ['development','holdout']:
 d=P/phase;fp=d/'output/BLIND_CANDIDATES.json';fh=json.loads((d/'output/CANDIDATE_HASH.json').read_text());assert sha(fp)==fh['sha256'];records+=json.loads(fp.read_text())
assert len(records)==760
save(I/'input/CANDIDATES.json',records)
for f in ['selector.py','morphology.py']:shutil.copyfile(P/'development'/f,I/f)
for f in ['MODEL.joblib','SELECTOR_RULE.json']:shutil.copyfile(P/'development/output'/f,I/'input'/f)
# Original audio is not reprocessed; verified candidate/features are sufficient frozen inputs.
for phase in ['development','holdout']:
 d=P/phase
 for m in json.loads((d/'input/MANIFEST.json').read_text()):assert sha(d/'input'/m['audio'])==m['sha256']
save(W/'INPUT_AUDIT.json',{'authority_hashes':checks,'native_BP_verified':True,'all_source_audio_hashes_verified':12,'candidate_population':760,'model_sha256':sha(I/'input/MODEL.joblib'),'feature_and_generator_code_sha256':sha(I/'morphology.py'),'selector_code_sha256':sha(I/'selector.py'),'reuse':'All frozen native candidate coordinates/features, no BP rerun or acoustic re-extraction. Native BP pitch fields remain untrusted hypotheses; no GT/secure label fields.'})
save(W/'INPUT_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{str(p.relative_to(W)):sha(p) for p in [W/'EVALUATION_POPULATIONS.json',W/'PROTOCOL.json',W/'INPUT_AUDIT.json',I/'input/CANDIDATES.json',I/'input/MODEL.joblib',I/'input/SELECTOR_RULE.json',I/'selector.py',I/'morphology.py']}})
s='(version 1)\n(allow default)\n(deny network*)\n(deny file-read* (subpath "/Users") (subpath "/Volumes") (subpath "/private/tmp"))\n'
for p in [str(I),str(Path('.venv').resolve())]:s+=f'(allow file-read* (subpath "{p}"))\n'
s+='(allow file-read-metadata)\n';(W/'isolation.sb').write_text(s)
print('Authorities verified. Protocol/cohort/input hashes saved.760 BP query contexts; no GT in inference.')
