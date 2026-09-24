from pathlib import Path
import json,hashlib,datetime,subprocess,importlib.metadata,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];R=P.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
B=R/'JGA_LEARNED_LOCAL_ATTACK_SELECTOR_20260924';F=R/'JGA_CONTAINED_BP_FALLBACK_20260924';G=R/'JGA_GALLEGATI_CONTINUOUS_FISHMAN_GT_120_20260924';N=R/'JGA_NATIVE_BP_GT_120_20260924'
verified=[]
for path,base in [(B/'development/output/SELECTOR_FREEZE.json',B/'development'),(B/'holdout/output/PREDICTIONS_FREEZE.json',B/'holdout'),(B/'EVALUATION_FREEZE.json',B),(F/'INPUT_FREEZE.json',F),(F/'inference/output/PREDICTION_FREEZE.json',F/'inference'),(F/'EVALUATION_FREEZE.json',F),(G/'GROUND_TRUTH/GT_FREEZE.json',G/'GROUND_TRUTH'),(N/'RAW_RESULTS_FREEZE.json',N)]:
 for k,h in json.load(open(path))['files'].items():
  assert sha(base/k)==h,(path,k)
 verified.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path)})
assert sha(G/'GROUND_TRUTH/GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1.json')=='a4047bf252f28fa3289279bdcaa5e90226dcf0af994a51e0dd5df05174484631'
assert sha(G/'GROUND_TRUTH/GT_FREEZE.json')=='535e3d3d930db323320a5959da3999bc605ba278234671d0540d04b281b3ebd7'
split=json.load(open(B/'TAKE_SPLIT.json'));assert sha(B/'TAKE_SPLIT.json')==json.load(open(B/'SPLIT_FREEZE.json'))['sha256']
for t,m in split['takes'].items():assert sha(Path(m['source_wav']))==m['source_sha256'],t
metrics=json.load(open(B/'EVALUATION.json'))['pooled'];j=metrics['methods']['JGA'];assert j['N']==35 and j['total']==40 and round(j['median_absolute_ms'],3)==5.213 and round(j['P95_absolute_ms'],3)==5.621 and j['within_10_pct']==100
save(P/'UPSTREAM_VERIFICATION.json',{'status':'PASS','prior_freezes':verified,'source_audio_hashes_verified':12,'GT_hash_verified':True,'split_hash_verified':True,'performance_verified':j,'no_scientific_reexecution':True})
save(P/'ENVIRONMENT.json',{'python':sys.version,'executable':sys.executable,'packages':sorted([{'name':d.metadata.get('Name',''),'version':d.version} for d in importlib.metadata.distributions()],key=lambda d:d['name'].lower()),'recovery':'Recreate environments from project configurations and preserved package records; system Python/Homebrew executables are not portable project assets.'})
core='''# PI authority: best validated JGA Bass attack baseline

PI milestone decision recorded 2026-09-25; experiment authority JGA_LEARNED_LOCAL_ATTACK_SELECTOR_20260924. CURRENT BEST VALIDATED BASS ATTACK BASELINE. This is a controlled-domain comparison authority, not completion of historical Bass-v1.

## Architecture and scope

Audio → official Spotify Basic Pitch 0.4.0 (bundled ICASSP 2022 model) → native BP note identity + approximate onset → fixed local ±150 ms window → local acoustic candidates → frozen JGA Learned Local Attack Selector → selected existing acoustic attack coordinate / abstention.

The controlled September-14 Gallegati Fishman corpus has120 human-reference events in12 continuous takes. Target reference is channel-specific observable onset in Fishman Full Circle, NOT physical string release. The validated question is recognized note + approximate neighborhood → local attack selection. It does not validate autonomous note identity, raw-query event completeness, arbitrary audio domains or historical Ray Brown timing. Same-rater GT and1ms annotation steps do not establish sub-millisecond human accuracy.

## Exact implementation authority

All paths below are relative to docs/scientific/rfc. JGA_LEARNED_LOCAL_ATTACK_SELECTOR_20260924/development/selector.py defines candidate windows, features and decisions; development/morphology.py defines acoustic features. development/output/SELECTOR_RULE.json is the exact parameter authority; MODEL.joblib is the serialized scaler/model. SHA-256s:

- selector.py: c20687006752d2ec07c0de6be12d1f7055669e387d6f8c746c76c245686c3433
- morphology.py: ac003cdaf4799e696204d95c527ee8cb747d262d4a9e17ca80aa3669b1570b70
- SELECTOR_RULE.json: db998eaed9485edf913fd78d0698ad2fc9896a13d896dbffd5504e922dbc0a42
- MODEL.joblib: 6523e71a1788b05b8c112570b1dc5a20736bea33942f68ad00ffd70359fb2474

Local window is BP onset±0.15s, clipped only to source limits. Feature context extends0.15s on either side; candidate eligibility remains within the local window. Original44sample frame grid is preserved. Positive magnitude spectral flux30≤f<250Hz, Hann1024, hop44,44100Hz; all eligible local maxima from the exact frozen generator remain candidates. No refractory suppression or timing correction.

The frozen22feature order is listed in SELECTOR_RULE.json, alongside exact scaler means/scales, coefficients and intercept. It includes flux magnitude/prominence/width/rise/decay/integral, local flux ratios, RMS and low/broadband energy changes, centroid/slope, persistence/concentration and three BP-relative location features. Source code specifies exact transforms and frame ranges; it takes precedence over prose. In particular BP_relative_activity_position=(candidate−BP_onset)/max(BP_duration,1e-9), unchanged even where domain shift makes its distribution problematic.

Normalization is the fitted StandardScaler; logistic regression C=0.1, not the older C=1/threshold0.99 morphology classifier. Frozen decision threshold0.5: choose the highest predicted probability only if ≥0.5 and no top-score tie within1e-12. Otherwise ABSTAIN_AMBIGUOUS; empty candidates NO_CANDIDATE. Stable score ordering is implementation-defined in the frozen file. Exactly one existing coordinate is emitted for a selected query. No averaging, snapping or bias correction.

## Development/holdout and provenance

TAKE_SPLIT.json and SPLIT_FREEZE.json define8 complete development takes /4holdout takes, with no take overlap. Split SHA-256:151f1433d48ff99b1eafc48023ffd5424ba1bfd4349b2da9177dd3cf6fb84047. Development:0028,0029,0030,0033,0034,0036,0039,0040. Holdout:0031,0035,0037,0038 (all20260914).

PROSPECTIVE_PROTOCOL.json, development/train.py, CV_RESULTS.json and DEVELOPMENT_CANDIDATES.csv preserve candidate labels, take-level cross-validation and model selection. Development had72 uniquely recognized GT correspondences; positive training evidence included90 near-interval proxies, not90 independent notes. The exact original label distinctions and weights remain authoritative. Holdout predictions were saved before evaluation-GT reveal; prediction/selector/evaluation freezes and isolation checks remain unchanged. Investigator exposure predates this study; process isolation is not a pristine investigator-blind claim.

GT authority JGA_GALLEGATI_CONTINUOUS_FISHMAN_GT_120_20260924/GROUND_TRUTH/GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1.json SHA-256 a4047bf252f28fa3289279bdcaa5e90226dcf0af994a51e0dd5df05174484631; GT_FREEZE.json SHA-256535e3d3d930db323320a5959da3999bc605ba278234671d0540d04b281b3ebd7. Native BP provenance, settings, source hashes and all hypotheses are in JGA_NATIVE_BP_GT_120_20260924. TAKE_SPLIT.json records all12original WAV hashes and paths; MANIFEST references these without duplicating audio.

## Exact controlled holdout result

35/40 selected =87.5%; median absolute error5.213ms; P95 absolute error5.621ms;100% of selected within±10ms. Five GT events had unresolved BP correspondence: this is recognized-note-conditional performance, not guaranteed autonomous recognition. All35selected precede their plausible GT intervals; no offset correction was applied. Additional raw BP-query selections outside the matched cohort are not automatically verified attacks.

On the same35matched events the learned selector improves over native BP (MAE14.629/P9551.478ms), nearest-to-BP candidate (19.217/53.096ms), earliest candidate (148.039/179.044ms), and largest-flux candidate (5.227/36.775ms). EVALUATION.json retains unrounded values and all stratification; HOLDOUT_ATTACK_SELECTIONS.csv/HOLDOUT_RESULTS.json retain event-level evidence. The advantage over the largest-flux baseline is principally outlier control, not a large median change.

## Secondary contained fallback

JGA_CONTAINED_BP_FALLBACK_20260924 remains a separate secondary validated component using the unchanged selector. Each ambiguous BP hypothesis keeps its own ordinary window; never bridge them. One selected hypothesis yields its coordinate; multiple hypotheses at one exact acoustic sample yield shared identity-unresolved attack; distinct selected coordinates cause abstention; none selected causes abstention. Natural ambiguous cohort8/13, MAE4.822/P955.480ms; maskedholdout18/35, MAE5.240/P955.598ms; allselectedwithin10ms. Three prior catastrophic union-window cases became abstentions. These statistics MUST NOT be pooled with primary35/40validation. BP-blind/autonomous recovery is not established.

## Historical and diagnostic evidence — not replacement authorities

JGA_BASS_V1_HISTORICAL_TRANSFER_20260924 used fixed28UNFLAGGED/SECURE_ROUTE and35FLAGGED/AMBIGUOUS_ROUTE. These are operational identity routes, not independent identityGT. It selected17uniqueattacks/63episodes and abstained46 (secure3/28, ambiguous14/35). The walking structure was insufficiently recovered. The result remains a partial diagnostic map; historical Bass-v1 milestone NOT complete.

JGA_STEM_FULLMIX_DOMAIN_SHIFT_20260924 documents important Fishman→historical/Demucs feature-distribution shift; this is not a causal Demucs latency measurement. Generic full-mix cues remain ambiguous. JGA_NOTE_CONDITIONED_FULLMIX_20260924 resolved0/63 under its overly restrictive ≥3observable-harmonic/nonoverlap sufficiency convention; this does not disprove note-conditioned observation. JGA_TARGETED_PITCH_ONSET_20260924 yielded37/63CLEAR (58.73%) conditional full-mix target-energy observations. Its centered filtering/bandwidth and timing accuracy remain unvalidated against historicalGT. None supersedes the controlled baseline. No Ray Brown physical timing authority is finalized.

## Mandatory future comparison directive

Do not restart Bass development from scratch. Preserve this Learned Local Attack Selector as the comparison baseline. Every proposed improvement/extension must report: whether the baseline changed; controlled-domain coverage; median absolute error; P95 absolute error;±10ms performance; abstention behavior; historical/cross-domain coverage; and whether coverage gains sacrifice validated timing precision. A visually plausible historical result cannot supersede this baseline without independent validation.

RAW PLP remains the quarter-reference authority, never an acoustic-selection guide. Freeze historical attack timestamps before PLP evaluation. Original full mix remains original audio authority; stems provide complementary source/identity evidence. Next scientific goal: improve cross-domain/historical coverage while preserving this controlled baseline. No new science is executed by this milestone.

## Package and hash convention

This immutable core contains the PI authority without a self-referential digest. BASELINE_FREEZE.json binds this core and every referenced scientific payload by SHA-256, role and size; its byte SHA-256 is the baseline freeze hash. The public authority document quotes that hash. MANIFEST.json additionally hashes the public authority, freeze and operational package files; SHA256SUMS.txt verifies all manifest entries. Manifest/sums and outer citation-bearing documents are not recursively hashed into their own digest. Root bootstrap and commit/backup receipts are operational references, not mutable scientific payload. Audio is referenced with full hashes/paths and preserved in the external complete project backup. Git excludes large audio/raw arrays, but the complete backup preserves them.
'''
(P/'AUTHORITY_CORE.md').write_text(core)
# Bind complete scientific experiment payloads, including audio references, without duplicating them.
names=['JGA_LEARNED_LOCAL_ATTACK_SELECTOR_20260924','JGA_CONTAINED_BP_FALLBACK_20260924','JGA_NATIVE_BP_GT_120_20260924','JGA_GALLEGATI_CONTINUOUS_FISHMAN_GT_120_20260924','JGA_BASS_V1_HISTORICAL_TRANSFER_20260924','JGA_BP_AMBIGUITY_ATTACK_RECOVERY_20260924','JGA_BASIC_PITCH_HARMONIC_FAMILY_20260924','JGA_BP_FRAGMENT_REARTICULATION_20260924','JGA_STEM_FULLMIX_DOMAIN_SHIFT_20260924','JGA_NOTE_CONDITIONED_FULLMIX_20260924','JGA_TARGETED_PITCH_ONSET_20260924']
entries=[];stage=[]
for name in names:
 base=R/name;status='PRIMARY_BASELINE' if name==names[0] else 'SECONDARY_VALIDATED' if name==names[1] else 'INPUT_AUTHORITY' if name in names[2:4] else 'RESEARCH_EVIDENCE_NOT_REPLACEMENT'
 for p in sorted(base.rglob('*')):
  if not p.is_file() or '__pycache__' in p.parts or p.name.startswith('._') or p.name=='.DS_Store' or p.suffix in ['.pyc','.log']:continue
  rel=str(p.relative_to(ROOT));large=p.suffix.lower() in ['.wav','.flac','.mp3','.m4a','.npz','.npy'] or p.stat().st_size>=90_000_000
  entries.append({'root':'REPOSITORY','relative_path':rel,'role':'source_audio_or_array_reference' if large else 'scientific_evidence','size':p.stat().st_size,'sha256':sha(p),'authority_status':status,'dependency':name,'git_payload':not large})
  if not large:stage.append(rel)
for take,m in split['takes'].items():
 p=Path(m['source_wav']);entries.append({'root':'SSD_TRACK_JGA','relative_path':str(p.relative_to('/Volumes/SSD Track/JGA')),'role':'original_Fishman_continuous_take','size':p.stat().st_size,'sha256':sha(p),'authority_status':'SOURCE_AUDIO','dependency':take,'git_payload':False})
for p in [P/'AUTHORITY_CORE.md',P/'UPSTREAM_VERIFICATION.json',P/'ENVIRONMENT.json']:
 entries.append({'root':'REPOSITORY','relative_path':str(p.relative_to(ROOT)),'role':'baseline_authority_core','size':p.stat().st_size,'sha256':sha(p),'authority_status':'PI_SELECTED_BASELINE','dependency':'PI milestone decision','git_payload':True})
entries.sort(key=lambda r:(r['root'],r['relative_path']))
save(P/'BASELINE_FREEZE.json',{'schema':'JGA_BASELINE_FREEZE_V1','roots':{'REPOSITORY':str(ROOT),'SSD_TRACK_JGA':'/Volumes/SSD Track/JGA'},'entries':entries,'hash_convention':'SHA256 of these exact bytes binds immutable scientific payload. Citation wrapper and operational manifests are outer nonrecursive verification layers.'})
freezehash=sha(P/'BASELINE_FREEZE.json')
public=R/'JGA_BASS_BEST_VALIDATED_BASELINE_20260924.md';public.write_text(core+'\nBaseline freeze SHA-256: `'+freezehash+'`\n\n[Manifest](JGA_BASS_BEST_VALIDATED_BASELINE_20260924/MANIFEST.json) · [Freeze](JGA_BASS_BEST_VALIDATED_BASELINE_20260924/BASELINE_FREEZE.json)\n')
# Update the canonical generator source, preserving all old checkpoint bytes below it.
state=ROOT/'docs/JGA_PROJECT_STATE.md';old=state.read_text();(P/'PREVIOUS_PROJECT_STATE.md').write_text(old)
section=f'''# Current authoritative checkpoint — best validated Bass baseline · 2026-09-25

**CURRENT BEST VALIDATED BASS ATTACK BASELINE** — PI-selected [authority](scientific/rfc/JGA_BASS_BEST_VALIDATED_BASELINE_20260924.md). Audio → Basic Pitch → fixed ±150 ms local window → acoustic candidates → frozen JGA Learned Local Attack Selector → selected attack / abstain.

Controlled Gallegati/Fishman holdout: **35/40 selected =87.5%; median absolute error5.213ms; P95 absolute error5.621ms;100% of selected within±10ms.** Recognized-note-conditional timing validation, not autonomous Bass identity or universal transfer. Contained fallback is a separate secondary validation, never pooled with35/40.

Baseline freeze SHA-256: `{freezehash}`. [Manifest](scientific/rfc/JGA_BASS_BEST_VALIDATED_BASELINE_20260924/MANIFEST.json).

**Historical Bass-v1 NOT complete.** Direct Exactly Like You/Demucs transfer recovered17/63episodes,46abstentions; only a partial diagnostic map. Targeted-pitch full-mix branch has37/63CLEAR(58.73%) but no independent timing validation. Historical Bass microtiming authority is NOT finalized. Prior Report001 remains unchanged in its operational scope; it does not validate this newer Bass architecture.

**Do not restart Bass development from scratch.** Preserve the frozen Learned Local Attack Selector as mandatory comparison baseline. Future methods are extensions/improvements and must report controlled coverage, median/P95 absolute error,±10ms, abstention, cross-domain coverage and any precision cost. Visually plausible historical observations cannot supersede controlled validation. Next scientific goal: improve cross-domain/historical coverage while preserving controlled baseline performance; new science requires PI authorization.

RAW PLP remains temporal authority for quarter reference and must not guide acoustic attack selection. Freeze historical attack timestamps before PLP evaluation. Full mix remains original audio authority; stems are complementary source/identity evidence. This milestone records authority/preservation only; no algorithm change or new scientific execution.

---

## Preserved prior authoritative checkpoints — historical scopes unchanged

'''
state.write_text(section+old)
save(P/'INTENDED_STAGE.json',sorted(stage+[str(public.relative_to(ROOT)),'docs/JGA_PROJECT_STATE.md','JGA_BOOTSTRAP.md']))
print('Baseline freeze',freezehash,'entries',len(entries),'Git evidence files',len(stage))
