"""Independent saved-artifact verification; no audio extraction or parameter fitting."""
from pathlib import Path
import json,hashlib,sys,collections
import numpy as np
from scipy.signal import find_peaks
ROOT=Path(__file__).resolve().parents[5] if False else Path('/Users/StarTrack/Development/JazzGrooveAnalyzer')
BASE=ROOT/'docs/scientific/rfc/JGA_FULLMIX_BASS_CYMBAL_EVENT_PILOT_002_20260928'
def load(p):return json.loads(Path(p).read_text(),parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonstandard JSON '+x)))
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def equal(a,b):return bool(np.allclose(a,b,rtol=1e-9,atol=1e-9,equal_nan=True))
checks=[]
import csv
def check(name,result):
 checks.append({'check':name,'pass':bool(result)})
 if not result:raise AssertionError(name)
C=load(BASE/'CONFIGURATION/CONFIGURATION.json');S=load(BASE/'SUMMARY.json');I=load(BASE/'INPUT_MANIFEST/INPUT_MANIFEST.json');DSP=load(BASE/'DSP_METADATA.json');E=load(BASE/'EXTERNAL_ARRAYS.json');execution=load(BASE/'EXECUTION_PROVENANCE.json');eng=load(BASE/'ENGINEERING_INVARIANTS.json')
for p in BASE.rglob('*.json'):load(p)
check('all JSON standard finite/null',True)
check('source SHA',sha(ROOT/C['input'])==C['input_sha256']==S['source_sha256'])
check('executed configuration SHA',sha(BASE/'CONFIGURATION/CONFIGURATION.json')==execution['configuration_sha256'])
check('executed producer SHA',sha(BASE/'REPRODUCTION/producer.py')==execution['producer_sha256'])
for f in E['files']:check('external source and mirror '+Path(f['path']).name,sha(f['path'])==sha(f['backup_path'])==f['sha256'])
archive=np.load(E['files'][0]['path'],allow_pickle=False);A={k:archive[k] for k in archive.files};archive.close();sr=C['sample_rate'];hop=C['stft']['hop_length'];half=C['stft']['n_fft']//2;begin=E['processing_start_sample'];end=E['processing_end_sample_exclusive'];lo,hi=[round(t*sr) for t in C['region_s']]
metric_path=ROOT/'docs/historical_reports/JGA_HISTORICAL_REPORT_001/FINAL_SCORE_V1/METRIC_REFERENCE.csv'
with metric_path.open() as f:metric={r['quarter_label']:r for r in csv.DictReader(f)}
check('canonical region metadata only',round(float(metric['Q131']['reference_time'])*sr)==lo and round(float(metric['Q227']['reference_time'])*sr)==hi and metric['Q131']['measure_id']=='M33' and metric['Q226']['measure_id']=='M56')
check('native bounds', [lo,hi]==S['region_native_samples']==[2107392,3643392])
check('frame coordinates',np.array_equal(A['native_sample'],begin+np.arange(len(A['time_s']))*hop) and equal(A['time_s'],A['native_sample']/sr))
check('STFT synthetic invariants',eng['status']=='PASS' and all(x['pass'] and x['error_samples']==0 for x in eng['checks']) and not eng['half_window_subtraction'])
byid={};recomputed={}
def stat(values):
 v=np.asarray(values,float)
 return {'n':len(v),'min':float(np.min(v)),'q1':float(np.percentile(v,25)),'median':float(np.median(v)),'q3':float(np.percentile(v,75)),'max':float(np.max(v))} if len(v) else {'n':0,'status':'NOT_AVAILABLE'}
for arm in ['bass','cymbal']:
 raw=load(BASE/arm.upper()/'ALL_LOCAL_MAXIMA.json');peaks=load(BASE/arm.upper()/'PEAK_QUALIFIED_CANDIDATES.json');dedup=load(BASE/arm.upper()/'DEDUPLICATED_CANDIDATES.json');clusters=load(BASE/arm.upper()/'DEDUP_CLUSTERS.json');byid.update({r['candidate_id']:r for r in raw});ac=C[arm];flux=A[arm+'_flux'];freq=A['frequencies_hz'];bins=np.flatnonzero((freq>=ac['band_hz'][0])&(freq<=ac['band_hz'][1]));band=A[arm+'_magnitude'][bins].astype(float)
 reconstructed_flux=np.sqrt((np.maximum(np.diff(band,axis=1,prepend=band[:,:1]),0)**2).sum(axis=0));check(arm+' saved complete flux vs saved spectrum',equal(flux,reconstructed_flux))
 eps=C['features']['flatness_epsilon'];total=band.sum(axis=0);den=np.maximum(total,eps);f=freq[bins];centroid=(f[:,None]*band).sum(axis=0)/den;flatness=np.exp(np.log(np.maximum(band,eps)).mean(axis=0))/np.maximum(band.mean(axis=0),eps);sub=np.array([(band[idx]**2).sum(axis=0) for idx in np.array_split(np.arange(len(f)),C['features']['subband_energy_cv_bands'])]);cv=sub.std(axis=0)/np.maximum(sub.mean(axis=0),eps)
 check(arm+' feature traces from saved spectrum',equal(centroid,A[arm+'_centroid_hz']) and equal(flatness,A[arm+'_flatness']) and equal(cv,A[arm+'_subband_energy_cv']))
 local,props=find_peaks(flux,prominence=(None,None));check(arm+' all context local maxima',np.array_equal(local,A[arm+'_context_local_maxima_frames']))
 expected=[int(fr) for fr in local if lo<=begin+fr*hop<hi];check(arm+' every admitted maximum preserved',[r['frame_index'] for r in raw]==expected and len(set(r['candidate_id'] for r in raw))==len(raw))
 q25,q75=np.percentile(flux,[25,75]);threshold=(q75-q25)*C['peak']['prominence_iqr_factor'];threshold=threshold if threshold>0 else np.std(flux)*C['peak']['fallback_std_factor'];check(arm+' configured prominence applied',equal(threshold,DSP[arm]['thresholds']['prominence']))
 qual=find_peaks(flux,distance=ac['distance_frames'],prominence=threshold)[0];qualset=set(int(fr) for fr in qual if lo<=begin+fr*hop<hi);check(arm+' qualified membership',set(r['frame_index'] for r in peaks)==qualset);check(arm+' raw/qualified payload identity',all(r==byid[r['candidate_id']] for r in peaks))
 distance=set(find_peaks(flux,distance=ac['distance_frames'])[0]);promdict=dict(zip(local,props['prominences']));cr=C['cymbal_rule'];p50=np.percentile(flux,cr['compatible_flux_percentile']);p30=np.percentile(flux,cr['other_flux_percentile'])
 for r in raw:
  fr=r['frame_index'];sample=begin+fr*hop;check(r['candidate_id']+' coordinates and support',r['native_sample']==sample and r['landmark_timestamp_s']==sample/sr and lo<=sample<hi and r['analysis_support_native_samples']==[sample-hop-half,sample+half] and r['classification_algorithm_support_native_samples']==[begin,end] and r['decision_time_s']==end/sr and r['evidence_available_until_s']==end/sr)
  rejected=[]
  if fr not in distance:rejected.append('DISTANCE_SUPPRESSION')
  if promdict[fr]<threshold:rejected.append('BELOW_PROMINENCE')
  check(r['candidate_id']+' rejection trace',r['rejection_reasons']==rejected and r['peak_qualified']==(fr in qualset) and equal(r['prominence'],promdict[fr]))
  check(r['candidate_id']+' feature values',equal(r['flux'],flux[fr]) and equal(r['centroid_hz'],centroid[fr]) and equal(r['flatness_magnitude'],flatness[fr]) and equal(r['six_subband_energy_cv'],cv[fr]))
  expectedstate='AMBIGUOUS'
  if arm=='bass':
   f0=A['bass_f0_hz'][fr]
   if np.isfinite(f0):
    harmonics=[int(np.argmin(abs(freq-k*f0))) for k in range(1,C['harmonics']['max_harmonics']+1) if k*f0<=sr/2];hs=sum(float(A['fullmix_magnitude'][b,fr]) for b in harmonics);check(r['candidate_id']+' harmonic evidence',equal(hs,r['harmonic_magnitude_sum']) and len(harmonics)==len(r['harmonic_components']))
   else:check(r['candidate_id']+' missing evidence not zero',r['f0_hz'] is None and r['harmonic_magnitude_sum'] is None)
   if r['voiced'] and r['f0_hz'] is not None and C['pyin']['fmin']<=r['f0_hz']<=C['pyin']['fmax']:expectedstate='BASS_COMPATIBLE' if r['harmonic_magnitude_sum']>C['bass_rule']['harmonic_sum_to_flux_factor']*r['flux'] else 'BASS_POSSIBLE'
  else:
   if r['centroid_hz']>cr['compatible_centroid_hz'] and r['flux']>p50 and r['flatness_magnitude']<cr['compatible_flatness_max'] and r['six_subband_energy_cv']>cr['compatible_cv_min']:expectedstate='CYMBAL_COMPATIBLE'
   elif r['centroid_hz']>cr['other_centroid_hz'] and r['flux']>p30:expectedstate='OTHER_PERCUSSIVE_COMPATIBLE'
  check(r['candidate_id']+' preregistered class',r['state']==expectedstate)
 flat_members=[m for cluster in clusters for m in cluster['members']];check(arm+' every qualified member retained exactly',flat_members==peaks)
 for cluster,rep in zip(clusters,dedup):
  members=cluster['members'];chosen=min(members,key=lambda r:(r['native_sample'],r['candidate_id']));check(cluster['cluster_id']+' representative invariant',cluster['representative_id']==chosen['candidate_id']==rep['candidate_id'] and {k:v for k,v in rep.items() if k!='cluster_id'}==chosen)
  check(cluster['cluster_id']+' chain and span',all(b['landmark_timestamp_s']-a['landmark_timestamp_s']<=C['dedup']['tolerance_s'] for a,b in zip(members,members[1:])) and equal(cluster['span_s'],members[-1]['landmark_timestamp_s']-members[0]['landmark_timestamp_s']) and cluster['span_exceeds_pairwise_tolerance']==(cluster['span_s']>C['dedup']['tolerance_s']))
 counts=collections.Counter(r['state'] for r in dedup);check(arm+' state counts',all(S['arms'][arm]['states'][k]==v for k,v in counts.items()) and sum(S['arms'][arm]['states'].values())==len(dedup))
 calc={'all_local_maxima':len(raw),'peak_qualified':len(peaks),'deduplicated':len(dedup),'rejected':len(raw)-len(peaks),'merged_members':len(peaks)-len(dedup),'clusters':len(clusters),'multi_member_clusters':sum(len(c['members'])>1 for c in clusters),'cluster_size_distribution':dict(collections.Counter(str(len(c['members'])) for c in clusters)),'cluster_span_ms':stat([1000*c['span_s'] for c in clusters]),'clusters_span_exceeds_tolerance':sum(c['span_exceeds_pairwise_tolerance'] for c in clusters),'dedup_spacing_ms':stat(np.diff([r['landmark_timestamp_s'] for r in dedup])*1000),'evaluation_boundary_crossed':sum(r['evaluation_boundary_crossed'] for r in dedup),'source_support_truncated':sum(r['source_support_truncated'] for r in dedup),'flux':stat([r['flux'] for r in dedup]),'prominence':stat([r['prominence'] for r in dedup])}
 for k,v in calc.items():check(arm+' summary '+k,v==S['arms'][arm][k])
 recomputed[arm]=calc
plots=load(BASE/'PLOT_DATA.json');check('renderer SHA',plots['renderer_sha256']==sha(BASE/'REPRODUCTION/render.py'))
for name,points in plots['plots'].items():
 check(name+' plotted IDs/timestamps/state',all(p['candidate_id'] in byid and p['timestamp_s']==byid[p['candidate_id']]['landmark_timestamp_s'] and p['state']==byid[p['candidate_id']]['state'] for p in points));check(name+' PNG present',(BASE/'FIGURES'/(name+'.png')).is_file())
if (BASE/'RESULT.md').exists():
 report=(BASE/'RESULT.md').read_text()
 for key in ['all_local_maxima','peak_qualified','deduplicated','rejected','merged_members','clusters','multi_member_clusters','clusters_span_exceeds_tolerance','evaluation_boundary_crossed','source_support_truncated']:
  check('report '+key,('| '+key+' | '+str(recomputed['bass'][key])+' | '+str(recomputed['cymbal'][key])+' |') in report)
 for key in ['cluster_span_ms','dedup_spacing_ms','flux','prominence']:
  check('report median '+key,('| '+key+' median | '+format(recomputed['bass'][key]['median'],'.6f')+' | '+format(recomputed['cymbal'][key]['median'],'.6f')+' |') in report)
 for arm in ['bass','cymbal']:
  for state,count in S['arms'][arm]['states'].items():check('report state '+state,('| '+arm+' | '+state+' | '+str(count)+' |') in report)
if (BASE/'MANIFEST.json').exists():
 m=load(BASE/'MANIFEST.json');actual={str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file() and not p.name.startswith('._') and not p.name.endswith('.tmp') and '__pycache__' not in p.parts};listed={r['path'] for r in m['artifacts']};check('manifest complete artifact inventory',actual==listed|{'MANIFEST.json'} and m['actual_package_file_count']==len(actual))
 for r in m['artifacts']:check('manifest hash '+r['path'],sha(BASE/r['path'])==r['sha256'] and (BASE/r['path']).stat().st_size==r['size'])
print(json.dumps({'status':'PASS','check_count':len(checks),'failed_checks':[],'scope':'Independent saved-artifact arithmetic, provenance, frame, selection, rejection, dedup, plot and optional manifest checks; no source-identity validation','arms_recomputed':recomputed,'checks_by_category':['native coordinates','raw completeness','rejection reasons','configured selection and classification','harmonic components','cluster membership','unchanged landmark','statistics','plot references','input/config/script/array hashes']},indent=2,allow_nan=False))
