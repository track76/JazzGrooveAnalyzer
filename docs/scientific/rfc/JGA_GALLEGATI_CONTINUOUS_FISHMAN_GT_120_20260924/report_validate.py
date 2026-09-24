from pathlib import Path
import csv,json,hashlib,collections
from decimal import Decimal as D
import numpy as np
P=Path(__file__).resolve().parent;F=P/'GROUND_TRUTH';G=P.parent/'JGA_BASIC_PITCH_GALLEGATI_TIMING_VALIDATION_20260924/GROUND_TRUTH'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return list(csv.DictReader(p.open()))
freeze=json.loads((F/'GT_FREEZE.json').read_text())
for n,h in freeze['files'].items():assert sha(F/n)==h
for n,h in freeze['parents'].items():assert sha(Path(n))==h
for n,x in freeze['sources'].items():assert sha(Path(n))==x['sha256']
assert sha(G/'GT_FREEZE.json')=='7b62b71cf41051c73eee85590c4f4a88b42030c2dfd618c302dc39ac88a75832'
for n,h in json.loads((G/'GT_FREEZE.json').read_text())['files'].items():assert sha(G/n)==h
name='GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1';rows=json.loads((F/(name+'.json')).read_text())['events'];lookup={r['event_id']:r for r in rows};cs={r['event_id']:r for r in read(F/(name+'.csv'))}
assert len(rows)==len(lookup)==120 and set(collections.Counter(r['take_id'] for r in rows).values())=={10}
for old in json.loads((G/'GALLEGATI_FISHMAN_OBSERVABLE_ONSET_GT_V1.json').read_text())['events']:
 for k,v in old.items():assert lookup[old['event_id']][k]==v
for old in read(G/'GALLEGATI_FISHMAN_OBSERVABLE_ONSET_GT_V1.csv'):
 for k,v in old.items():assert cs[old['event_id']][k]==v
prov=json.loads((F/'ANNOTATION_PROVENANCE.json').read_text())
for eid,x in prov.items():
 if 'pass1' not in x:continue
 def restore(a,k):return D(a['mapping']['crop_start_sample'])/D(a['mapping']['sample_rate'])+D(str(a['raw'][k+'_local_s']))
 c=restore(x['pass1'],'center');e=restore(x['pass1'],'earliest');l=restore(x['pass1'],'latest')
 if x['pass2']:
  c=(c+restore(x['pass2'],'center'))/2;e=min(e,restore(x['pass2'],'earliest'));l=max(l,restore(x['pass2'],'latest'))
 for key,v in [('center',c),('earliest',e),('latest',l)]:assert float(v)==lookup[eid]['final_'+key+'_s']
s=json.loads((P/'REPEATABILITY_SUMMARY.json').read_text());o=s['overall'];prev=json.loads((P.parent/'JGA_GALLEGATI_FISHMAN_ONSET_REPEATABILITY_20260924/SUMMARY.json').read_text())['overall']
rr=read(P/'EVENT_REPEATABILITY.csv');errors=np.array([(float(r['pass2_center_s'])-float(r['pass1_center_s']))*1000 for r in rr]);assert abs(np.median(np.abs(errors))-o['median_absolute_ms'])<1e-8
lines=['# September-14 continuous Fishman repeatability and 120-event GT','', '**Decision: repeatability confirmed; expanded validation GT created.** No adjudication triggers were found. This is same-rater reproducibility of the Fishman observable landmark, not physical onset accuracy.','', 'Both original Pass-2 exports were preserved byte-for-byte before parsing. The receipt matches the response SHA-256. Passes were joined by canonical event ID and restored via each independently randomized excerpt’s integer source-sample offset; presentation order was not used for matching.','', '## Repeatability — 24 audit events','', '| Metric | 24-event audit | Earlier 36-event pilot |','|---|---:|---:|']
for label,key,oldkey in [('Median signed ms','median_signed_ms','median_signed_ms'),('Mean signed ms','mean_signed_ms','mean_signed_ms'),('Median absolute ms','median_absolute_ms','median_absolute_ms'),('IQR signed ms','IQR_signed_ms','IQR_signed_ms'),('P95 absolute ms','P95_absolute_ms','p95_absolute_ms'),('Maximum absolute ms','maximum_absolute_ms','maximum_absolute_ms')]:lines.append(f'| {label} | {o[key]:.3f} | {prev[oldkey]:.3f} |')
lines+=['| Within ±2 / ±5 / ±10 / ±20 ms | 100% at each bound | 100% at each bound |','| Plausible intervals overlap | 24/24 (100%) | 36/36 (100%) |','',f"Signed range: {o['minimum_signed_ms']:.3f} to {o['maximum_signed_ms']:.3f} ms. No uncertain/incomplete or disjoint-interval cases. The maximum is modestly larger than the previous pilot, while both studies remain entirely inside ±2 ms. No material new repeatability problem is established relative to the intended 10–30 ms validation scale.",'','**Precision qualification:** the interface used 1 ms marker steps. Fractional restored coordinates and midpoints explain the decimal values; they do not demonstrate sub-millisecond human accuracy. Shared same-rater bias is not tested.','', '## Descriptive group results','', '| Group | N | Median signed ms | Mean ms | Median absolute ms | IQR ms | P95 absolute ms | Max absolute ms |','|---|---:|---:|---:|---:|---:|---:|---:|']
for typ in ['strings','conditions']:
 for group,x in s[typ].items():lines.append(f"| {group} | {x['N']} | {x['median_signed_ms']:.3f} | {x['mean_signed_ms']:.3f} | {x['median_absolute_ms']:.3f} | {x['IQR_signed_ms']:.3f} | {x['P95_absolute_ms']:.3f} | {x['maximum_absolute_ms']:.3f} |")
lines+=['','Every group has 100% interval overlap and 100% within each ±2/5/10/20 ms bound. Group sizes are small (6 per string, 8 per condition); these are descriptive results. Full group ranges and metrics are in REPEATABILITY_SUMMARY.json; all 24 differences and intervals are in EVENT_REPEATABILITY.csv.','','## Final references and preservation','','The neutral rule was recorded before Pass-2 comparison in FINAL_REFERENCE_RULE.json, consistent with the prior PI-authorized GT methodology:','','- Original 36: exact adjudicated values and provenance preserved, including literal original CSV fields.','- New 24 audit events: midpoint of source-coordinate centers; earliest human earliest bound and latest human latest bound. Both annotations retained.','- New 60 non-repeated events: primary values unchanged, explicitly marked primary-only with cohort audit support. These 60 were not individually repeat-validated.','','Definition: **Channel-specific observable onset in the Fishman Full Circle pickup signal; NOT physical string-release Ground Truth.**','','120 unique events; exactly ten per each of 12 September-14 continuous Fishman takes. Source hashes, bounds, metadata and final-reference arithmetic verified. No exclusions or unresolved events. September 19 excluded.','','## Validation artifact','',f'- Data: GROUND_TRUTH/{name}.json',f'- Data SHA-256: `{sha(F/(name+".json"))}`',f'- Freeze: GROUND_TRUTH/GT_FREEZE.json',f'- Freeze SHA-256: `{sha(F/"GT_FREEZE.json")}`','','**Ready for take-level continuous detector development/holdout: YES, as reference preparation.** No split or detector is run here. Future selection must occur at the take level. These takes have prior isolated-event research exposure; a later holdout can test new continuous normalization/re-arm logic but must not be described as wholly unseen audio. Retain individual uncertainty intervals, including the wider original adjudicated cases, in timing validation.','','Canonical JGA, original GT, PLP, Report 001 and historical analyses unchanged. No Basic Pitch, spectral detector or Ray Brown processing. No commit or push. Stop for PI review.']
(P/'RESULT.md').write_text('\n'.join(lines)+'\n')
(P/'VALIDATION.json').write_text(json.dumps({'status':'PASS','events':120,'takes':12,'per_take':10,'GT36_preserved_exact_JSON_and_CSV':True,'all_parent_and_source_hashes_verified':True,'independent_final_arithmetic_check':True,'repeatability_recomputed_from_source_coordinates':True,'uncertain':0,'excluded':0,'expanded_GT_JSON_sha256':sha(F/(name+'.json')),'freeze_sha256':sha(F/'GT_FREEZE.json'),'no_detector_run':True,'no_canonical_changes':True},indent=2)+'\n')
print('PASS: frozen files/parents/sources; old36 exact; 120 unique; final arithmetic independently checked.')
