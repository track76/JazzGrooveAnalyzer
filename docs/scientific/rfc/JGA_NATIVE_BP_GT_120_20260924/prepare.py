from pathlib import Path
import json,hashlib,shutil,datetime
W=Path(__file__).resolve().parent; R=W.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x): p.write_text(json.dumps(x,indent=2)+'\n')
G=R/'JGA_GALLEGATI_CONTINUOUS_FISHMAN_GT_120_20260924/GROUND_TRUTH'
assert sha(G/'GT_FREEZE.json')=='535e3d3d930db323320a5959da3999bc605ba278234671d0540d04b281b3ebd7'
assert sha(G/'GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1.json')=='a4047bf252f28fa3289279bdcaa5e90226dcf0af994a51e0dd5df05174484631'
sources=json.loads((G/'GT_FREEZE.json').read_text())['sources']; mapping=[]; inputs=[]
for i,(s,v) in enumerate(sorted(sources.items()),1):
 p=Path(s); assert sha(p)==v['sha256']; name=f'T{i:02}'; dest=W/'inference/input'/f'{name}.wav';shutil.copyfile(p,dest)
 inputs.append({'clip_id':name,'audio_path':str(dest),'audio_sha256':sha(dest)})
 mapping.append({'clip_id':name,'source_wav':s,**v})
save(W/'SOURCE_MAP.json',mapping);save(W/'inference/INPUT_AUDIO.json',inputs)
save(W/'PHASE0_AUDIT.json',{'GT_hash_verified':True,'freeze_hash_verified':True,'complete_take_outputs_found':False,'prior_output':'JGA_BASIC_PITCH_GALLEGATI_TIMING_VALIDATION_20260924/NATIVE_BASIC_PITCH','prior_scope':'36 isolated excerpts; not reusable for complete-take inference','sources_verified':mapping,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
save(W/'MATCHING_PROTOCOL.json',{'rule':'Partition each take into chronological GT territories at midpoints between consecutive human centers, with take endpoints outer bounds. Native hypotheses whose onset lies in a territory and whose offset reaches its GT earliest plausible bound are associated candidates. Use expected pitch first, octave-equivalent second, other pitch last. Exactly one hypothesis in the highest available pitch tier permits matching; multiple remain MULTIPLE_BP_CANDIDATES with no timestamp choice. All native hypotheses retained including pre-target-ending fragments and unmatched extras. This is conservative reference-assisted correspondence, not an deployable onset selector. No nearest-GT ranking, amplitude ranking, or duration ranking.','reason':'Known controlled pitch plus chronological correspondence and persistence; no hypothesis selected for small timing error. Native timestamps never changed.','additional_definition':'Native hypotheses not in any event association set; ambiguous-associated hypotheses reported separately, not asserted false notes.','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
old=(R/'JGA_BASIC_PITCH_GALLEGATI_TIMING_VALIDATION_20260924/run_inference.py').read_text()
old=old.replace("if '/JazzGrooveAnalyzer/' in p or p.startswith('/Volumes/'):","if ('/JazzGrooveAnalyzer/' in p and not p.startswith(str(W)+os.sep)) or p.startswith('/Volumes/'):")
old=old.replace('assert len(inputs)==36','assert len(inputs)==12').replace("'clips':36","'clips':12")
(W/'inference/run.py').write_text(old)
print('Verified both GT authority hashes and 12 source hashes; copied complete WAVs. No GT centers read.')
