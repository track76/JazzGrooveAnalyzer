from pathlib import Path
import json,csv,hashlib,datetime
import numpy as np,soundfile as sf
from scipy.signal import stft
from scipy.stats import spearmanr
W=Path(__file__).resolve().parent;I=W/'input';O=W/'output'
load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
checks=[]
for p in ['/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/scientific/rfc/JGA_V1_OPERATIONAL_PLP_QUARTER_NEAREST_001_20260922/PLP_REFERENCE.csv','/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/scientific/rfc/JGA_BASS_V1_HISTORICAL_TRANSFER_20260924/JGA_BASS_V1_EXACTLY_LIKE_YOU_ATTACKS.csv']:
 try:open(p).read(1);raise RuntimeError('Forbidden read permitted')
 except PermissionError:checks.append({'path':p,'read_denied':True})
save(O/'ISOLATION_CHECKS.json',checks)
E=load(I/'EPISODES.json');Q=load(I/'QUERY_EVIDENCE.json');prev={e['episode_id']:e for e in load(I/'PREVIOUS_EPISODES.json')};rule=load(I/'RULE.json')
M={r['note_id']:json.loads(r['native_hypothesis']) for r in csv.DictReader(open(I/'MEMBERSHIP.csv'))}
assert len(E)==63 and len(M)==98
sr=44100;hop=44;n=1024;df=sr/n
lo=min(min(float(M[k]['onset_s']),Q[k]['search_start_s']) for k in Q)-2
hi=max(max(float(M[k]['offset_s']),Q[k]['search_end_s']) for k in Q)+1
start=int(lo*sr)//hop*hop;end=int(hi*sr)
P={};waves={}
for name in ['BASS','FULLMIX']:
 x,s=sf.read(I/(name+'.wav'),start=start,stop=end);assert s==sr;x=x.mean(axis=1);waves[name]=x
 freq,tt,z=stft(x,fs=sr,window='hann',nperseg=n,noverlap=n-hop,nfft=n,boundary=None,padded=False)
 t=tt+start/sr;mask=(freq>=30)&(freq<=2000);P[name]=abs(z[mask])**2
freq=freq[mask];B=P['BASS'];F=P['FULLMIX'];eps=1e-20
cos=lambda a,b:float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)+eps))
rows=[];templates={};curves={};identity=[]
for e in E:
 eid=e['episode_id'];identity.append({'episode_id':eid,'frozen_root_midi':e['fundamental_midi'],'ambiguity':e['ambiguity'],'exact_member_ids':e['member_ids'],'members':[M[k] for k in e['member_ids']]})
 for bid in e['member_ids']:
  q=Q[bid];native=M[bid];on=float(native['onset_s']);off=float(native['offset_s'])
  pitches=sorted(set([int(e['fundamental_midi']),int(native['midi_pitch'])]))
  for pitch in pitches:
   key=f'{eid}_{bid}_{pitch}';f0=440*2**((pitch-69)/12);harm=np.arange(1,int(2000//f0)+1)*f0
   bands=np.array([abs(freq-h)<=df for h in harm]);counts=bands.sum(axis=1);valid=counts>0;bands=bands[valid];harm=harm[valid];counts=counts[valid];union=bands.any(axis=0)
   a=max(on,e['start_s']);b=min(off,e['end_s']);active=(t>=a)&(t<=b);background=(t>=a-(b-a))&(t<a)
   mean=B[:,active].mean(axis=1) if active.any() else np.zeros(len(freq));base=B[:,background].mean(axis=1) if background.any() else np.zeros(len(freq))
   sig=bands@mean;sig=sig/(sig.sum()+eps);enrich=(bands@mean)/(counts/len(freq)*mean.sum()+eps);observable=enrich>1
   resolved=f0>2*df and sum(observable)>=3 and active.any() and mean.sum()>eps
   template={'f0':f0,'pitch':pitch,'harmonics_hz':harm.tolist(),'halfwidth_hz':df,'band_bin_counts':counts.tolist(),'observable':observable.tolist(),'signature':sig.tolist(),'background_harmonic_energy':(bands@base).tolist(),'background_enrichment':((bands@mean+eps)/(bands@base+eps)).tolist(),'resolution_sufficient':bool(resolved),'activity_start':a,'activity_end':b}
   templates[key]=template
   HB=bands@B;HF=bands@F
   win=(t>=q['search_start_s'])&(t<=q['search_end_s']);curves[key+'_t']=t[win];curves[key+'_mix']=HF[:,win];curves[key+'_stem']=HB[:,win]
   for c in q['fullmix_fronts']:
    ct=c['timestamp_s'];j=int(np.argmin(abs(t-ct)));assert abs(t[j]-ct)<1e-8
    fm_pre=F[:,j-12:j].mean(axis=1);fm_post=F[:,j+1:j+13].mean(axis=1);bs_pre=B[:,j-12:j].mean(axis=1);bs_post=B[:,j+1:j+13].mean(axis=1)
    delta=np.maximum(fm_post-fm_pre,0);hm=np.maximum(bands@(fm_post-fm_pre),0);hb=np.maximum(bands@(bs_post-bs_pre),0)
    enrichment=float(delta[union].sum()/(delta.sum()+eps)/(union.mean()+eps))
    sim=cos(hm,sig);cross=cos(hm,hb)
    dd=np.maximum(np.diff(HF[:,j-12:j+13],axis=1),0);peakidx=np.argmax(dd,axis=1)-11
    coherent=observable&(hm>eps)&(abs(peakidx)<=6)
    coherence=float(coherent.sum()/max(observable.sum(),1));temporal=cos(np.maximum(np.diff(HB[:,j-12:j+13],axis=1),0).ravel(),dd.ravel())
    rank=float(spearmanr(hm,sig).statistic) if np.ptp(hm)>0 and np.ptp(sig)>0 else 0
    if not np.isfinite(rank):rank=0
    if not resolved or hm.sum()<=eps:percussion='INSUFFICIENT';cls='UNRESOLVED'
    else:
     percussion='PITCH_COHERENT' if coherence>=.5 and enrichment>=1.5 else ('BROADBAND_DOMINATED' if enrichment<=1 and coherence<.5 else 'MIXED')
     if percussion=='PITCH_COHERENT' and sim>=.8 and cross>=.8:cls='BASS_COMPATIBLE'
     elif percussion=='PITCH_COHERENT' or (percussion=='MIXED' and sim>=.8):cls='MIXED_SOURCE'
     elif percussion=='BROADBAND_DOMINATED' and sim<.8:cls='NON_BASS_COMPATIBLE'
     else:cls='UNRESOLVED'
    rows.append({'episode_id':eid,'BP_member_id':bid,'target_pitch':pitch,'template_id':key,'f0':f0,'candidate_s':ct,'sample':c['sample'],'BP_onset_s':on,'candidate_minus_BP_ms':1000*(ct-on),'harmonic_coherence':coherence,'target_enrichment':enrichment,'stem_signature_similarity':sim,'synchronous_stem_mix_similarity':cross,'temporal_rise_similarity':temporal,'harmonic_rank_similarity':rank,'target_band_energy_rise':float(hm.sum()),'f0_energy_change':float((bands@(fm_post-fm_pre))[0]),'target_pre':(bands@fm_pre).tolist(),'target_post':(bands@fm_post).tolist(),'target_positive_change':hm.tolist(),'non_target_change_fraction':float(delta[~union].sum()/(delta.sum()+eps)),'percussion_class':percussion,'source_classification':cls,'previous_stem_status':prev[eid]['historical_status'],'previous_selected_s':prev[eid]['historical_selected_s'],'prior_salient_cue':c['salient_cue'],'notes':'Compatibility is diagnostic, not independent Bass attribution or onset validation.'})
# Freeze complete detailed evidence and classifications BEFORE aggregate outcome inspection.
save(O/'TARGET_IDENTITIES.json',identity);save(O/'TEMPLATES_SIGNATURES.json',templates);save(O/'CANDIDATE_ATTRIBUTIONS.json',rows)
np.savez_compressed(O/'HARMONIC_CURVES.npz',**curves)
save(O/'PRE_RESULT_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'implementation_sha256':sha(Path(__file__)),'rule_sha256':sha(I/'RULE.json'),'candidate_population_sha256':sha(I/'QUERY_EVIDENCE.json'),'files':{p.name:sha(p) for p in sorted(O.iterdir()) if p.is_file()}})
results=[]
for e in E:
 eid=e['episode_id'];rr=[r for r in rows if r['episode_id']==eid];compatible=sorted(set(r['candidate_s'] for r in rr if r['source_classification']=='BASS_COMPATIBLE'));mixed=set(r['candidate_s'] for r in rr if r['source_classification']=='MIXED_SOURCE')-set(compatible)
 status='MULTIPLE_BASS_COMPATIBLE_FRONTS' if len(compatible)>1 else ('UNRESOLVED_ATTRIBUTION' if len(compatible)==1 and mixed else ('UNIQUE_BASS_COMPATIBLE_FRONT' if compatible else ('UNRESOLVED_ATTRIBUTION' if any(r['source_classification'] in ['UNRESOLVED','MIXED_SOURCE'] for r in rr) else 'NO_BASS_COMPATIBLE_FRONT')))
 old=prev[eid];s=old['historical_selected_s'];results.append({'episode_id':eid,'status':status,'compatible_fronts_s':compatible,'mixed_fronts_s':sorted(mixed),'pitch_coherent_coordinates':len(set(r['candidate_s'] for r in rr if r['percussion_class']=='PITCH_COHERENT')),'previous_multiple_cue_abstention':old['historical_selected_s'] is None and old['diagnostic_class']=='MULTIPLE_LOCAL_FRONT_CUES','previous_selected_s':s,'counterpart':s is not None and any(abs(c-s)<=hop/sr for c in compatible),'earlier_compatible':[] if s is None else [c for c in compatible if c<s-hop/sr],'later_compatible':[] if s is None else [c for c in compatible if c>s+hop/sr]})
save(O/'EPISODE_RESULTS.json',results)
statusmap={e['episode_id']:e['status'] for e in results}
with open(O/'NOTE_CONDITIONED_FULLMIX_ATTRIBUTION.csv','w') as out:
 fields=list(rows[0])+['harmonic_template','empirical_signature','episode_status'];w=csv.DictWriter(out,fieldnames=fields);w.writeheader()
 for r in rows:
  r=dict(r);tmp=templates[r['template_id']];r.update(harmonic_template=tmp['harmonics_hz'],empirical_signature=tmp['signature'],episode_status=statusmap[r['episode_id']]);w.writerow({k:json.dumps(v) if isinstance(v,list) else v for k,v in r.items()})
from collections import Counter
summary={'episodes':63,'primary_N':sum(r['previous_multiple_cue_abstention'] for r in results),'primary_status':dict(Counter(r['status'] for r in results if r['previous_multiple_cue_abstention'])),'all_status':dict(Counter(r['status'] for r in results)),'previous17_counterpart':sum(r['counterpart'] for r in results),'previous17_earlier':sum(bool(r['earlier_compatible']) for r in results),'previous17_later':sum(bool(r['later_compatible']) for r in results),'template_evaluations':len(templates),'resolved_templates':sum(x['resolution_sufficient'] for x in templates.values()),'candidate_note_evaluations':len(rows),'class_counts':dict(Counter(r['source_classification'] for r in rows)),'special':[r for r in results if r['episode_id'] in ['HF044','HF047']]}
save(O/'SUMMARY.json',summary);save(O/'RESULT_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{p.name:sha(p) for p in sorted(O.iterdir()) if p.is_file()}})
print(json.dumps(summary,indent=2))
