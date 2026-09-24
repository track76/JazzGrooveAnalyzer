from pathlib import Path
import json,hashlib,csv,datetime,collections
import numpy as np,soundfile as sf
from scipy.signal import stft
from morphology import extract,means,NAMES
W=Path(__file__).resolve().parent;O=W/'output';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
checks=[]
for p in [W.parent.parent/'JGA_V1_OPERATIONAL_PLP_QUARTER_NEAREST_001_20260922/PLP_REFERENCE.csv',W.parent.parent/'JGA_BASS_V1_HISTORICAL_TRANSFER_20260924/RESULTS.json',W.parent.parent/'JGA_BASS_V1_HISTORICAL_TRANSFER_20260924/JGA_BASS_V1_EXACTLY_LIKE_YOU_ATTACKS.csv']:
 try:p.read_bytes();raise RuntimeError('PLP/reference access allowed')
 except PermissionError:checks.append({'path':str(p),'read_denied':True})
save(O/'ISOLATION_CHECKS.json',checks)
x,sr=sf.read(W/'input/FULLMIX.wav');x=x.mean(axis=1) if x.ndim>1 else x;b,srb=sf.read(W/'input/BASS.wav');b=b.mean(axis=1) if b.ndim>1 else b;assert sr==srb==44100 and len(x)==len(b)
records=json.loads((W/'input/BLIND_CANDIDATES.json').read_text());queries=json.loads((W/'input/QUERY_DECISIONS.json').read_text());eps=json.loads((W/'input/EPISODE_DECISIONS.json').read_text());data={};stemrel=[];fmrecords=[];curve={}
for r in records:
 bid=r['BP']['native_note_id'];bp=r['BP']['onset_local_s'];lo=r['search_start_s'];hi=r['search_end_s'];start=max(0,int((lo-.15)*sr)//44*44);end=min(len(x),int((hi+.15)*sr));z=extract(x[start:end],sr);t=z['t']+start/sr;ct=z['candidate_times']+start/sr;ii=np.flatnonzero((ct>=lo)&(ct<=hi));prom=np.array([10**z['X'][k,1] for k in ii]);median=float(np.median(prom)) if len(prom) else 0;mad=float(np.median(abs(prom-median))) if len(prom) else 0;threshold=median+3*mad;fm=[]
 for k in ii:
  feat=z['X'][k];p=float(10**feat[1]);salient=bool(p>threshold and feat[13]>0 and feat[11]>0);fr={'front_id':f'{bid}_FM_F{round(ct[k]*sr)}','timestamp_s':float(ct[k]),'sample':round(ct[k]*sr),'flux':float(z['flux'][z['candidate_frames'][k]]),'prominence':p,'prominence_median_plus3MAD':threshold,'salient_cue':salient,'RMS_post_pre_log10':float(feat[11]),'low_energy_post_pre_log10':float(feat[13]),'fullmix_minus_BP_ms':float((ct[k]-bp)*1000),'features':dict(zip(NAMES,feat.tolist()))};fm.append(fr);fmrecords.append({'BP_id':bid,**fr})
 salient=[f for f in fm if f['salient_cue']];pidx={round(c['timestamp_s']*sr):c for c in fm}
 # Stem curve only: no find_peaks/candidate generation on stem. Verify preserved flux samples.
 freq,tt,zz=stft(b[start:end],fs=sr,window='hann',nperseg=1024,noverlap=980,nfft=1024,boundary=None,padded=False);mag=abs(zz);band=(freq>=30)&(freq<250);sv=np.maximum(0,np.diff(mag[band],axis=1,prepend=mag[band,:1])).sum(axis=0);assert np.allclose(tt+start/sr,t,rtol=0,atol=1e-12)
 curve[bid+'_time']=t;curve[bid+'_fm_flux']=z['flux'];curve[bid+'_stem_flux']=sv;curve[bid+'_fm_low_energy']=z['low_energy'];curve[bid+'_fm_rms']=z['rms']
 rel=[]
 for j,c in enumerate(r['candidates']):
  ti=c['time_s'];frame=int(round((ti-start/sr)*sr/44-512/44));assert abs(t[frame]-ti)<1e-10;assert np.isclose(sv[frame],c['flux'],rtol=1e-7,atol=1e-12)
  local=[f for f in salient if abs(f['timestamp_s']-ti)<=512/sr];classification='FULLMIX_MULTIPLE_PLAUSIBLE_FRONTS' if len(local)>1 else ('FULLMIX_CORRESPONDING_FRONT' if abs(local[0]['timestamp_s']-ti)<=44/sr else 'FULLMIX_NEARBY_DISTINCT_FRONT') if local else 'NO_CLEAR_FULLMIX_FRONT';nearest=[]
  if fm:
   dist=min(abs(f['timestamp_s']-ti) for f in fm);nearest=[f for f in fm if abs(abs(f['timestamp_s']-ti)-dist)<1e-12]
  pre=float(means(z['low_energy'],np.array([frame]),-48,-12)[0]);post=float(means(z['low_energy'],np.array([frame]),12,48)[0]);rp=float(means(z['rms'],np.array([frame]),-48,-12)[0]);rq=float(means(z['rms'],np.array([frame]),12,48)[0]);ev={'flux_at_exact_stem_frame':float(z['flux'][frame]),'low_energy_pre':pre,'low_energy_post':post,'low_energy_log10_ratio':float(np.log10(max(post,1e-20)/max(pre,1e-20))),'RMS_pre':rp,'RMS_post':rq,'RMS_log10_ratio':float(np.log10(max(rq,1e-20)/max(rp,1e-20))),'flux_rise_one_frame':float(z['flux'][frame]-z['flux'][max(0,frame-1)])}
  a={'BP_id':bid,'pitch':r['BP']['midi_pitch'],'BP_onset':bp,'stem_status':queries[bid]['status'],'stem_candidate_id':c['candidate_id'],'stem_candidate_s':ti,'stem_minus_BP_ms':(ti-bp)*1000,'frozen_stem_score':queries[bid]['probabilities'][j],'fullmix_evidence':ev,'nearest_raw_fullmix_fronts_s':[f['timestamp_s'] for f in nearest],'nearest_raw_front_is_salient':[f['salient_cue'] for f in nearest],'nearby_salient_fullmix_fronts_s':[f['timestamp_s'] for f in local],'delta_FM_STEM_ms':[(f['timestamp_s']-ti)*1000 for f in local],'classification':classification};rel.append(a);stemrel.append(a)
 data[bid]={'search_start_s':lo,'search_end_s':hi,'BP_onset_s':bp,'fullmix_fronts':fm,'salient_fronts':salient,'stem_relations':rel}
 print('WINDOW',bid,'raw FM',len(fm),'salient cues',len(salient),flush=True)
np.savez_compressed(O/'SYNCHRONIZED_CURVES.npz',**curve);save(O/'QUERY_EVIDENCE.json',data);save(O/'ALL_FULLMIX_FRONTS.json',fmrecords)
out=[];late=[]
for e in eps:
 fs={f['sample']:f for bid in e['hypothesis_ids'] for f in data[bid]['salient_fronts']};fronts=sorted(fs.values(),key=lambda f:f['timestamp_s']);count=len(fronts);cohort='CLEAR_LOCAL_FRONT_CUE' if count==1 else 'MULTIPLE_LOCAL_FRONT_CUES' if count>1 else 'NO_CLEAR_LOCAL_FRONT_CUE';selectedclass=None
 if e['selected_s'] is not None:
  selectedclass='FULLMIX_AMBIGUOUS' if count>1 else 'FULLMIX_NO_SUPPORT' if not count else 'FULLMIX_SUPPORTS_STEM_SELECTION' if abs(fronts[0]['timestamp_s']-e['selected_s'])<=44/sr else 'FULLMIX_SUPPORTS_DIFFERENT_EARLIER_FRONT' if fronts[0]['timestamp_s']<e['selected_s'] else 'FULLMIX_SUPPORTS_DIFFERENT_LATER_FRONT'
 out.append({'episode_id':e['episode_id'],'route':e['route'],'historical_status':e['status'],'historical_selected_s':e['selected_s'],'hypothesis_ids':e['hypothesis_ids'],'salient_front_count':count,'salient_fronts_s':[f['timestamp_s'] for f in fronts],'diagnostic_class':cohort,'selected_crosscheck_class':selectedclass,'reason':'Prospective descriptive salience/energy flags across exact independent query windows; no source identity or selected full-mix attack is asserted.'})
 if e['selected_s'] is not None:
  offsets={bid:(e['selected_s']-data[bid]['BP_onset_s'])*1000 for bid in e['selected_BP_ids']};islate=any(v>1024/sr*1000 for v in offsets.values())
  if islate or e['episode_id'] in ['HF044','HF047']:
   late.append({'episode_id':e['episode_id'],'selected_stem_s':e['selected_s'],'stem_minus_successful_BP_ms':offsets,'late_beyond_Hann_support':islate,'earlier_salient_FM_fronts_s':[f['timestamp_s'] for f in fronts if f['timestamp_s']<e['selected_s']-44/sr],'all_salient_fronts_s':[f['timestamp_s'] for f in fronts],'selected_crosscheck_class':selectedclass,'qualification':'Earlier cue not automatically the beginning of this Bass event; mix may contain other sources.'})
save(O/'EPISODE_DIAGNOSTICS.json',out);save(O/'LATE_SELECTION_AUDIT.json',late)
with (O/'STEM_FULLMIX_ATTACK_INTERROGATION.csv').open('w',newline='') as f:
 fields=['episode_id','route','historical_episode_status']+list(stemrel[0])+['notes'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for e in eps:
  for bid in e['hypothesis_ids']:
   for r in data[bid]['stem_relations']:w.writerow({'episode_id':e['episode_id'],'route':e['route'],'historical_episode_status':e['status'],**{k:json.dumps(v) if isinstance(v,(dict,list)) else v for k,v in r.items()},'notes':'Raw nearest peak is descriptive only; qualified flags are unvalidated salience cues. No new full-mix Bass timestamp selected.'})
# Domain diagnosis from preserved stem values/scores only. Never score FM with logistic model.
rule=json.loads((W/'input/SELECTOR_RULE.json').read_text());names=rule['features'];mean=np.array(rule['scaler_mean']);scale=np.array(rule['scaler_scale']);coef=np.array(rule['coefficients'][0]);recordmap={r['BP']['native_note_id']:r for r in records};rep=[]
for e in eps:
 options=[(queries[bid]['probabilities'][k],c,bid) for bid in e['hypothesis_ids'] for k,c in enumerate(recordmap[bid]['candidates'])]
 if not options:continue
 prob,c,bid=max(options,key=lambda a:a[0]);v=np.array(c['features']);rep.append({'episode_id':e['episode_id'],'route':e['route'],'historical_status':e['status'],'cohort':'SELECTED' if e['selected_s'] is not None else 'ABSTAINED','representative':'Highest preserved stem score for domain description only; no new selection','BP_id':bid,'candidate_id':c['candidate_id'],'score':prob,'features':dict(zip(names,v.tolist())),'standardized_contributions':dict(zip(names,(((v-mean)/scale)*coef).tolist()))})
save(O/'STEM_DOMAIN_REPRESENTATIVES.json',rep)
summary={'episodes':63,'previous_selected':17,'previous_abstained':46,'abstention_classes':dict(collections.Counter(e['diagnostic_class'] for e in out if e['historical_selected_s'] is None)),'secure_abstention_classes':dict(collections.Counter(e['diagnostic_class'] for e in out if e['historical_selected_s'] is None and e['route']=='SECURE_ROUTE')),'selected_crosscheck':dict(collections.Counter(e['selected_crosscheck_class'] for e in out if e['historical_selected_s'] is not None)),'raw_fullmix_query_fronts':len(fmrecords),'stem_query_candidates':len(stemrel),'salient_fullmix_query_fronts':sum(f['salient_cue'] for f in fmrecords),'late_selections_audited':len(late),'domain_summary':{cohort:{'N':sum(r['cohort']==cohort for r in rep),'features':{n:{'median':float(np.median([r['features'][n] for r in rep if r['cohort']==cohort])),'median_contribution':float(np.median([r['standardized_contributions'][n] for r in rep if r['cohort']==cohort]))} for n in names}} for cohort in ['SELECTED','ABSTAINED']}}
save(O/'SUMMARY.json',summary)
save(O/'DIAGNOSTIC_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PLP_access':False,'fullmix_logistic_execution':False,'fullmix_attack_timestamps_selected':False,'files':{str(p.relative_to(W)):sha(p) for p in list(O.iterdir()) if p.is_file()},'implementation_sha256':sha(W/'run.py')});print('FROZEN',json.dumps({k:v for k,v in summary.items() if k!='domain_summary'}),flush=True)
