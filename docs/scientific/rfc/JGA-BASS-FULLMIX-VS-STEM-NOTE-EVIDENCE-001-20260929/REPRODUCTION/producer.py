"""Pilot002: preregistered fullmix evidence extraction; no pulse/source truth claims."""
import os,sys,json,hashlib,platform,datetime,io,warnings
from pathlib import Path
import numpy as np, scipy, scipy.signal as sig, soundfile as sf, librosa
R=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer');sys.path.insert(0,str(R));sys.dont_write_bytecode=True
from tools import jga_governance as g
O='docs/scientific/rfc/JGA_FULLMIX_BASS_CYMBAL_EVENT_PILOT_002_20260928/';TOKEN='codex-pilot002-20260928'
def clean(x):
 if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 if isinstance(x,np.ndarray):return clean(x.tolist())
 if isinstance(x,np.generic):return clean(x.item())
 if isinstance(x,float) and not np.isfinite(x):return None
 return x
def put(n,v):
 payload=v.encode() if isinstance(v,str) else (json.dumps(clean(v),indent=2,allow_nan=False)+'\n').encode()
 print(g.write(R,TOKEN,O+n,payload),flush=True)
def digest(p):
 with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def external_bytes(path,data):
 g.lease(R,TOKEN);path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 assert not path.exists(),f'Existing output requires inspection: {path}'
 tmp=path.with_suffix(path.suffix+'.tmp')
 with tmp.open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 os.replace(tmp,path)
 dst=Path(C['backup_root'])/path.name;dst.parent.mkdir(parents=True,exist_ok=True);t=dst.with_suffix(dst.suffix+'.tmp')
 with t.open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 expected=digest(path);assert digest(t)==expected;os.replace(t,dst);assert digest(dst)==expected
 print('EXTERNAL_BACKUP_PASS',path,flush=True)
 return {'path':str(path),'sha256':expected,'size':path.stat().st_size,'backup_path':str(dst),'backup_sha256':digest(dst),'status':'PASS','verified_at':g.now()}
def stats(x):
 a=np.asarray(x,float);return {'n':len(a),'min':float(a.min()),'q1':float(np.percentile(a,25)),'median':float(np.median(a)),'q3':float(np.percentile(a,75)),'max':float(a.max())} if len(a) else {'n':0,'status':'NOT_AVAILABLE'}
C=json.loads((R/O/'CONFIGURATION/CONFIGURATION.json').read_text());g.lease(R,TOKEN);started=g.now();source=R/C['input'];assert digest(source)==C['input_sha256'];info=sf.info(source);assert info.samplerate==C['sample_rate'] and info.channels==2 and info.subtype=='FLOAT';sr=info.samplerate
lo,hi=[round(t*sr) for t in C['region_s']];guard=round(C['context_s']*sr);begin=max(0,lo-guard);end=min(info.frames,hi+guard)
x,_=sf.read(source,start=begin,stop=end,dtype='float64',always_2d=True);y=x.mean(axis=1);del x
st=C['stft'].copy();st['dtype']=np.complex64;N=st['n_fft'];H=st['hop_length'];half=N//2
freq=librosa.fft_frequencies(sr=sr,n_fft=N);native=lambda f:begin+int(f)*H
D=librosa.stft(y,**st);mag_raw=np.abs(D).astype(float);frames=np.arange(D.shape[1]);times=(begin+frames*H)/sr
# Engineering checks do not choose parameters.
checks=[]
for at in [1024,2048,4096]:
 impulse=np.zeros(8192);impulse[at]=1.;z=librosa.stft(impulse,**st);peak=int(np.argmax(np.sum(abs(z)**2,axis=0)));checks.append({'impulse_sample':at,'peak_frame':peak,'frame_center_sample':peak*H,'error_samples':peak*H-at,'pass':peak*H==at})
assert all(c['pass'] for c in checks)
inv={'status':'PASS','checks':checks,'center':True,'formula':'processing_start_sample + frame_index * hop_length','half_window_subtraction':False,'hop_ms':1000*H/sr,'window_ms':1000*N/sr,'scope':'STFT frame coordinate invariant, not physical attack accuracy','filter_checks':[]}
put('INPUT_MANIFEST/INPUT_MANIFEST.json',{'task_id':C['task_id'],'source':{'path':C['input'],'sha256':digest(source),'sample_rate':sr,'channels':info.channels,'frames':info.frames,'duration_s':info.duration,'format':info.format,'subtype':info.subtype},'region':{'measure':'M33-M56','quarter_labels':'Q131-Q226','chorus_identity':'NOT_ESTABLISHED','requested_interval_s':C['region_s'],'native_start_inclusive':lo,'native_end_exclusive':hi,'native_interval_s':[lo/sr,hi/sr],'rounding':C['rounding'],'sample_count':hi-lo},'processing_support':{'start_sample':begin,'end_sample_exclusive':end,'source_padding_at_evaluation_boundary':False},'independence':{'original_fullmix_only':True,'stem_access':False,'human_access':False,'global_selection':False,'quarter_mapping':'PI-authorized interval only; no quarter array loaded'}})
arrays={'native_sample':begin+frames*H,'time_s':times,'fullmix_waveform':y,'fullmix_magnitude':mag_raw.astype('float32'),'frequencies_hz':freq};summary={};dsp={};inventories={};all_warnings=[]
for arm in ['bass','cymbal']:
 print('EXTRACTING',arm,flush=True);ac=C[arm];mask=(freq>=ac['band_hz'][0])&(freq<=ac['band_hz'][1]);f=freq[mask];fc=C['filter'];sos=sig.butter(fc['order'],ac['band_hz'],btype=fc['btype'],fs=sr,output='sos')
 filtered=sig.sosfiltfilt(sos,y,padtype=fc['padtype'],padlen=fc['padlen']);M=np.abs(librosa.stft(filtered,**st)).astype(float);band=M[mask];flux=np.sqrt(np.sum(np.maximum(np.diff(band,axis=1,prepend=band[:,:1]),0)**2,axis=0))
 q25,q75=np.percentile(flux,[25,75]);prom=C['peak']['prominence_iqr_factor']*(q75-q25)
 if prom<=0:prom=C['peak']['fallback_std_factor']*np.std(flux)
 maxima,props=sig.find_peaks(flux,prominence=(None,None));distance_kept=set(sig.find_peaks(flux,distance=ac['distance_frames'])[0].tolist());qualified=set(sig.find_peaks(flux,distance=ac['distance_frames'],prominence=prom)[0].tolist())
 total=np.sum(band,axis=0);eps=C['features']['flatness_epsilon'];den=np.maximum(total,eps);centroid=np.sum(f[:,None]*band,axis=0)/den;bw=np.sqrt(np.sum((f[:,None]-centroid)**2*band,axis=0)/den);cs=np.cumsum(band,axis=0);roll=f[np.argmax(cs>=C['features']['rolloff_magnitude_fraction']*total,axis=0)];flat=np.exp(np.mean(np.log(np.maximum(band,eps)),axis=0))/np.maximum(np.mean(band,axis=0),eps)
 sub=np.array([np.sum(band[idx]**2,axis=0) for idx in np.array_split(np.arange(len(f)),C['features']['subband_energy_cv_bands'])]);cv=np.std(sub,axis=0)/np.maximum(np.mean(sub,axis=0),eps)
 zcr=librosa.feature.zero_crossing_rate(filtered,frame_length=N,hop_length=H,center=True)[0];power=np.sum(band**2,axis=0);postframes=int(np.ceil(C['features']['post_energy_s']*sr/H));post=np.array([np.sum(power[i+1:min(len(power),i+postframes+1)]) for i in range(len(power))]);postcomplete=frames+postframes<len(power)
 f0=np.full(len(frames),np.nan);voiced=np.zeros(len(frames),dtype=bool);vp=np.full(len(frames),np.nan);harm=np.full(len(frames),np.nan);continuity=np.full(len(frames),np.nan);harmonics={}
 if arm=='bass':
  py=C['pyin'].copy();py['beta_parameters']=tuple(py['beta_parameters']);py['fill_na']=np.nan
  with warnings.catch_warnings(record=True) as ws:
   warnings.simplefilter('always');f0,voiced,vp=librosa.pyin(filtered,sr=sr,**py)
  all_warnings += [str(w.message) for w in ws];last=None
  for i in frames:
   if np.isfinite(f0[i]):
    if last is not None and i-last<=C['continuity']['max_gap_frames']:continuity[i]=abs(f0[i]-f0[last])
    last=i;hh=[]
    for k in range(1,C['harmonics']['max_harmonics']+1):
     hz=k*f0[i]
     if hz>sr/2:break
     b=int(np.argmin(abs(freq-hz)));hh.append({'harmonic_number':k,'requested_frequency_hz':hz,'bin':b,'bin_center_hz':freq[b],'magnitude':mag_raw[b,i]})
    harm[i]=sum(v['magnitude'] for v in hh);harmonics[int(i)]=hh
 thresholds={'prominence':prom,'iqr':q75-q25,'std':np.std(flux),'statistics_support_samples':[begin,end]}
 cr=C['cymbal_rule'];p50=np.percentile(flux,cr['compatible_flux_percentile']);p30=np.percentile(flux,cr['other_flux_percentile']);thresholds.update(flux_compatible_percentile_value=p50,flux_other_percentile_value=p30)
 rows=[]
 for j,fr in enumerate(maxima):
  sample=native(fr)
  if not lo<=sample<hi:continue
  reasons=[]
  if int(fr) not in distance_kept:reasons.append('DISTANCE_SUPPRESSION')
  if props['prominences'][j]<prom:reasons.append('BELOW_PROMINENCE')
  qual=int(fr) in qualified;assert qual==(len(reasons)==0)
  state='AMBIGUOUS';subtype=None
  if arm=='bass':
   if voiced[fr] and np.isfinite(f0[fr]) and C['pyin']['fmin']<=f0[fr]<=C['pyin']['fmax']:
    state='BASS_COMPATIBLE' if harm[fr]>C['bass_rule']['harmonic_sum_to_flux_factor']*flux[fr] else 'BASS_POSSIBLE'
  else:
   if centroid[fr]>cr['compatible_centroid_hz'] and flux[fr]>p50 and flat[fr]<cr['compatible_flatness_max'] and cv[fr]>cr['compatible_cv_min']:state='CYMBAL_COMPATIBLE'
   elif centroid[fr]>cr['other_centroid_hz'] and flux[fr]>p30:state='OTHER_PERCUSSIVE_COMPATIBLE'
   if state=='CYMBAL_COMPATIBLE':
    if centroid[fr]>cr['hihat_centroid_min'] and flat[fr]<cr['hihat_flatness_max']:subtype='TENTATIVE_HIHAT'
    elif cr['ride_centroid_min']<centroid[fr]<cr['ride_centroid_max'] and cv[fr]>cr['ride_cv_min']:subtype='TENTATIVE_RIDE'
  local_analysis=[sample-H-half,sample+half];local_class=[sample-half,sample+postframes*H+half] if arm=='cymbal' else [sample-half,sample+half]
  crossing=local_analysis[0]<lo or local_analysis[1]>hi or local_class[0]<lo or local_class[1]>hi
  row={'candidate_id':f'{arm.upper()}_F{int(fr):06d}','instrument_evidence':arm.upper(),'frame_index':int(fr),'native_sample':sample,'landmark_timestamp_s':sample/sr,'coordinate_convention':'processing_start_native_sample + frame_index*hop; centered STFT; no offset; frame-derived landmark not physical attack','analysis_support_native_samples':local_analysis,'classification_local_support_native_samples':local_class,'classification_algorithm_support_native_samples':[begin,end],'evidence_available_until_s':end/sr,'decision_time_s':end/sr,'decision_time_semantics':'earliest source-time availability for offline whole-context operation; not wall-clock completion','evaluation_boundary_crossed':crossing,'source_support_truncated':local_analysis[0]<begin or local_class[1]>end,'peak_qualified':qual,'rejection_reasons':reasons,'flux':flux[fr],'prominence':props['prominences'][j],'prominence_left_base_frame':int(props['left_bases'][j]),'prominence_right_base_frame':int(props['right_bases'][j]),'centroid_hz':centroid[fr],'rolloff_magnitude85_hz':roll[fr],'bandwidth_hz':bw[fr],'zcr_filtered':zcr[fr],'flatness_magnitude':flat[fr],'six_subband_energy_cv':cv[fr],'post_event_energy':post[fr] if postcomplete[fr] else None,'post_event_energy_status':'COMPUTED' if postcomplete[fr] else 'TRUNCATED','state':state,'tentative_subtype_hypothesis':subtype,'source_identity':'UNVALIDATED_COMPATIBILITY','confuser_status':'UNRESOLVED_NO_CONFIRMED_CONFUSER_LABEL'}
  if arm=='bass':row.update(f0_hz=f0[fr],voiced=bool(voiced[fr]),voiced_probability=vp[fr],harmonic_magnitude_sum=harm[fr],harmonic_status='COMPUTED' if np.isfinite(harm[fr]) else 'NOT_COMPUTED_NO_F0',harmonic_components=harmonics.get(int(fr),[]),distinct_harmonic_bins=len(set(h['bin'] for h in harmonics.get(int(fr),[]))),previous_voiced_f0_difference_hz=continuity[fr],continuity_status='COMPUTED' if np.isfinite(continuity[fr]) else 'NOT_COMPUTED_NO_NEAR_PRIOR_VOICED_FRAME',continuity_within_heuristic=bool(continuity[fr]<=C['continuity']['max_difference_hz']) if np.isfinite(continuity[fr]) else None)
  rows.append(clean(row))
 peaks=[r for r in rows if r['peak_qualified']];groups=[]
 for row in peaks:
  if not groups or row['landmark_timestamp_s']-groups[-1][-1]['landmark_timestamp_s']>C['dedup']['tolerance_s']:groups.append([row])
  else:groups[-1].append(row)
 clusters=[];dedup=[]
 for k,group in enumerate(groups):
  rep=min(group,key=lambda r:(r['native_sample'],r['candidate_id']));span=group[-1]['landmark_timestamp_s']-group[0]['landmark_timestamp_s'];cid=f'{arm.upper()}_CL{k+1:05d}'
  clusters.append({'cluster_id':cid,'member_ids':[r['candidate_id'] for r in group],'members':group,'representative_id':rep['candidate_id'],'representative_selection_rule':C['dedup']['representative'],'span_s':span,'span_exceeds_pairwise_tolerance':span>C['dedup']['tolerance_s'],'reason':'adjacent-gap heuristic; no physical same-attack claim'})
  dedup.append(dict(rep,cluster_id=cid))
 for name,data in [('ALL_LOCAL_MAXIMA',rows),('PEAK_QUALIFIED_CANDIDATES',peaks),('DEDUPLICATED_CANDIDATES',dedup),('DEDUP_CLUSTERS',clusters)]:put(arm.upper()+'/'+name+'.json',data)
 states={s:sum(r['state']==s for r in dedup) for s in (['BASS_COMPATIBLE','BASS_POSSIBLE','AMBIGUOUS','UNRESOLVED'] if arm=='bass' else ['CYMBAL_COMPATIBLE','OTHER_PERCUSSIVE_COMPATIBLE','AMBIGUOUS','UNRESOLVED'])};sizes={str(n):sum(len(q)==n for q in groups) for n in sorted(set(map(len,groups)))}
 summary[arm]={'all_local_maxima':len(rows),'peak_qualified':len(peaks),'deduplicated':len(dedup),'rejected':len(rows)-len(peaks),'merged_members':len(peaks)-len(dedup),'states':states,'clusters':len(clusters),'multi_member_clusters':sum(len(q)>1 for q in groups),'cluster_size_distribution':sizes,'cluster_span_ms':stats([1000*q['span_s'] for q in clusters]),'clusters_span_exceeds_tolerance':sum(q['span_exceeds_pairwise_tolerance'] for q in clusters),'dedup_spacing_ms':stats(np.diff([r['landmark_timestamp_s'] for r in dedup])*1000),'evaluation_boundary_crossed':sum(r['evaluation_boundary_crossed'] for r in dedup),'source_support_truncated':sum(r['source_support_truncated'] for r in dedup),'flux':stats([r['flux'] for r in dedup]),'prominence':stats([r['prominence'] for r in dedup])}
 arrays.update({arm+'_filtered_waveform':filtered,arm+'_magnitude':M.astype('float32'),arm+'_flux':flux,arm+'_context_local_maxima_frames':maxima,arm+'_context_prominences':props['prominences'],arm+'_context_distance_kept_frames':np.array(sorted(distance_kept)),arm+'_context_peak_qualified_frames':np.array(sorted(qualified)),arm+'_centroid_hz':centroid,arm+'_rolloff_hz':roll,arm+'_bandwidth_hz':bw,arm+'_flatness':flat,arm+'_subband_energy_cv':cv,arm+'_zcr':zcr,arm+'_post_event_energy':post})
 if arm=='bass':arrays.update(bass_f0_hz=f0,bass_voiced=voiced,bass_voiced_probability=vp,bass_harmonic_magnitude_sum=harm,bass_prior_voiced_difference_hz=continuity)
 w,response=sig.sosfreqz(sos,worN=1024,fs=sr);imp=np.zeros(sr*2+1);imp[sr]=1.;fi=sig.sosfiltfilt(sos,imp,padtype=fc['padtype'],padlen=fc['padlen']);sym=float(np.max(abs(fi-fi[::-1])));tail=float(np.max(abs(fi[np.abs(np.arange(len(fi))-sr)>round(.5*sr)])))
 inv['filter_checks'].append({'arm':arm,'impulse_sample':sr,'filtered_abs_peak_sample':int(np.argmax(abs(fi))),'symmetry_max_abs_difference':sym,'max_abs_tail_beyond_guard_0_5s':tail,'interpretation':'engineering descriptor only; zero-phase does not prove unchanged transient maxima'})
 dsp[arm]={'sos':sos,'response_frequency_hz':w,'single_pass_response_magnitude':abs(response),'forward_backward_magnitude':abs(response)**2,'phase':'offline forward/backward zero phase in ideal interior; noncausal waveform deformation and edge effects remain','padding':fc,'band_bin_indices':np.where(mask)[0],'band_bin_centers_hz':f,'thresholds':thresholds,'stft':C['stft'],'zcr_center_padding':'librosa edge-value padding; distinct from STFT reflect','support':[begin,end]}
 print('ARM_COMPLETE',arm,summary[arm],flush=True)
put('ENGINEERING_INVARIANTS.json',inv);put('DSP_METADATA.json',dsp)
stream=io.BytesIO();np.savez_compressed(stream,**arrays);meta=external_bytes(Path(C['external_root'])/'EVIDENCE_ARRAYS.npz',stream.getvalue());put('EXTERNAL_ARRAYS.json',{'files':[meta],'processing_start_sample':begin,'processing_end_sample_exclusive':end,'arrays':{k:{'shape':list(v.shape),'dtype':str(v.dtype)} for k,v in arrays.items()},'nan_semantics':'NaN in numeric NPZ pitch/harmonic arrays means missing measurement, never zero; JSON uses null/status'})
put('SUMMARY.json',{'task_id':C['task_id'],'classification':'EXPERIMENTAL_DIAGNOSTIC_NOT_PROMOTED','region_native_samples':[lo,hi],'region_s':[lo/sr,hi/sr],'source_sha256':C['input_sha256'],'arms':summary,'independence':C['constraints'],'raw_inventory_preserved':True,'all_rejections_preserved':True,'all_merged_members_preserved':True,'no_physical_identity_validation':True})
put('EXECUTION_PROVENANCE.json',{'started_at':started,'finished_at':g.now(),'python':sys.version,'platform':platform.platform(),'versions':{'numpy':np.__version__,'scipy':scipy.__version__,'librosa':librosa.__version__,'soundfile':sf.__version__},'input_sha256':digest(source),'configuration_sha256':digest(R/O/'CONFIGURATION/CONFIGURATION.json'),'producer_sha256':digest(Path(__file__)),'head':g.git(R,'rev-parse','HEAD').decode().strip(),'task_authority':'PI-PILOT002-CODEX-TAKEOVER-20260928','warnings':all_warnings,'execution_status':'EXTRACTION_COMPLETED_PENDING_INDEPENDENT_VALIDATION','command':'PYTHONDONTWRITEBYTECODE=1 .venv/bin/python '+O+'REPRODUCTION/producer.py','rerun_requires':'new authorized isolated output namespace; refuses to overwrite external evidence'})
