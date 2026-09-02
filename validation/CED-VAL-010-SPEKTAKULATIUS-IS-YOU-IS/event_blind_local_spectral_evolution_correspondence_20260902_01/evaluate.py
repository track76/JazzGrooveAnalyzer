#!/usr/bin/env python3
import argparse, hashlib, json
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path
import numpy as np
from scipy.stats import mannwhitneyu

HERE=Path(__file__).resolve().parent; P=json.loads((HERE/'protocol.json').read_text())
OBS=['signed_local_spectral_evolution_correspondence','spectral_state_correspondence','positive_rearticulation_correspondence','negative_decay_correspondence']
POPS=['PRESERVED','MISSED','NEGATIVE']; COMPS=[('MISSED','NEGATIVE'),('MISSED','PRESERVED'),('PRESERVED','NEGATIVE')]
def cb(x): return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()
def cosine(x,y):
 d=np.linalg.norm(x)*np.linalg.norm(y)
 return None if not np.isfinite(d) or d==0 else float(np.dot(x,y)/d)
def delta(a,b): return float(2*mannwhitneyu(a,b,alternative='two-sided',method='asymptotic').statistic/(len(a)*len(b))-1)
def load_rep(path,authority):
 assert sha(path)==authority['sha256']
 with np.load(path,allow_pickle=False) as z: return z['frame_starts'],z['frequency_hz'],z['power']
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--mix',type=Path,required=True); ap.add_argument('--bassdi',type=Path,required=True); ap.add_argument('--outcomes',type=Path,required=True); ap.add_argument('--rows',type=Path,required=True); ap.add_argument('--result',type=Path,required=True); a=ap.parse_args()
 mixs,freq,mixp=load_rep(a.mix,P['authorities']['mix_stft']); basss,bfreq,bassp=load_rep(a.bassdi,P['authorities']['bassdi_stft']); assert sha(a.outcomes)==P['authorities']['outcome_authority']['sha256']
 compatibility={'sample_rate_hz':44100,'frame_samples':2048,'hop_samples':256,'fft_size':4096,'frequency_arrays_exact':bool(np.array_equal(freq,bfreq)),'mix_starts_equal_bassdi_prefix':bool(np.array_equal(mixs,basss[:len(mixs)])),'mix_power_shape':list(mixp.shape),'bassdi_shared_power_shape':list(bassp[:len(mixp)].shape),'power_dtype_exact':str(mixp.dtype)==str(bassp.dtype)=='float64','shared_scope_samples':[0,7422225]}; assert all((compatibility['frequency_arrays_exact'],compatibility['mix_starts_equal_bassdi_prefix'],compatibility['power_dtype_exact'])) and mixp.shape==(28986,744) and bassp[:len(mixp)].shape==mixp.shape
 bassp=bassp[:len(mixp)]; mt=mixp.sum(axis=1); bt=bassp.sum(axis=1); ms=np.full_like(mixp,np.nan); bs=np.full_like(bassp,np.nan); ma=np.isfinite(mt)&(mt>0); ba=np.isfinite(bt)&(bt>0); ms[ma]=mixp[ma]/mt[ma,None]; bs[ba]=bassp[ba]/bt[ba,None]
 md=ms[1:]-ms[:-1]; bd=bs[1:]-bs[:-1]; mr=np.maximum(md,0); br=np.maximum(bd,0); mn=np.maximum(-md,0); bn=np.maximum(-bd,0)
 outcomes=json.loads(a.outcomes.read_text(),parse_float=Decimal); rows=[]
 for source in outcomes['rows']:
  ts=source['timestamp']; i=int((ts*Decimal(44100)/Decimal(256)).to_integral_value(rounding=ROUND_FLOOR)); row={'id':source['id'],'population':source['population'],'timestamp_decimal':str(ts),'relation_index':i,'relation_start_sample':i*256 if 0<=i<len(md) else None}
  reason=None
  if i<0 or i>=len(md): reason='PROJECTED_RELATION_OUTSIDE_SHARED_SCOPE'
  elif not (ma[i] and ma[i+1] and ba[i] and ba[i+1]): reason='ZERO_OR_NONFINITE_SPECTRAL_STATE'
  if reason:
   for o in OBS: row[o]=None; row[o+'_unavailable_reason']=reason
  else:
   values={OBS[0]:cosine(md[i],bd[i]),OBS[1]:float(np.sqrt(ms[i]*bs[i]).sum()),OBS[2]:cosine(mr[i],br[i]),OBS[3]:cosine(mn[i],bn[i])}
   for o,v in values.items(): row[o]=v; row[o+'_unavailable_reason']=None if v is not None else 'ZERO_OR_NONFINITE_VECTOR_NORM'
  rows.append(row)
 rowdoc={'protocol_id':P['protocol_id'],'protocol_fingerprint':P['protocol_fingerprint'],'pre_gt_fingerprint':'f5f8fbb5456735d086659ada34edfdc60f0aa0db044451c3056baf4d4a1568d9','outcome_authority_sha256':sha(a.outcomes),'compatibility':compatibility,'rows':rows}; rowdoc['rows_fingerprint']=hashlib.sha256(cb(rowdoc)).hexdigest(); a.rows.parent.mkdir(parents=True,exist_ok=True); a.rows.write_bytes(cb(rowdoc))
 counts={p:sum(r['population']==p for r in rows) for p in POPS}; summaries={}
 for oi,o in enumerate(OBS):
  vals={p:np.array([r[o] for r in rows if r['population']==p and r[o] is not None],float) for p in POPS}; distributions={}
  for p,v in vals.items():
   q=np.quantile(v,[0,.25,.5,.75,1],method='linear') if len(v) else [None]*5; distributions[p]={'total':counts[p],'available':len(v),'unavailable':counts[p]-len(v),'minimum':q[0],'q1_linear':q[1],'median':q[2],'q3_linear':q[3],'maximum':q[4]}
  comparisons={}
  for ci,(first,second) in enumerate(COMPS):
   x,y=vals[first],vals[second]; d=delta(x,y); rng=np.random.Generator(np.random.PCG64(20260902+oi*3+ci)); boot=np.array([delta(x[rng.integers(0,len(x),len(x))],y[rng.integers(0,len(y),len(y))]) for _ in range(2000)]); test=mannwhitneyu(x,y,alternative='two-sided',method='asymptotic')
   comparisons[first+'_minus_'+second]={'cliffs_delta':d,'rank_auc':(d+1)/2,'cliffs_delta_bootstrap_95_ci':[float(np.quantile(boot,.025)),float(np.quantile(boot,.975))],'mann_whitney_u':float(test.statistic),'mann_whitney_two_sided_p':float(test.pvalue) if np.isfinite(test.pvalue) else None}
  summaries[o]={'decision_bearing':o==OBS[0],'distributions':distributions,'comparisons':comparisons}
 signed=summaries[OBS[0]]; availability_ok=all(signed['distributions'][p]['available']>=.8*counts[p] for p in POPS); mnci=signed['comparisons']['MISSED_minus_NEGATIVE']['cliffs_delta_bootstrap_95_ci']; mpci=signed['comparisons']['MISSED_minus_PRESERVED']['cliffs_delta_bootstrap_95_ci']
 if not availability_ok: classification='INDETERMINATE'
 elif mnci[0]>0 and mpci[0]<=0<=mpci[1]: classification='EVENT_BLIND_LOCAL_SPECTRAL_EVOLUTION_CORRESPONDENCE_SUPPORTED'
 elif mnci[0]>0 and mpci[1]<0: classification='EVENT_BLIND_LOCAL_SPECTRAL_EVOLUTION_CORRESPONDENCE_PARTIAL'
 elif mnci[0]<=0<=mnci[1]: classification='LOCAL_SPECTRAL_EVOLUTION_ATTRIBUTION_INDETERMINATE'
 elif mnci[1]<0: classification='EVENT_BLIND_LOCAL_SPECTRAL_EVOLUTION_CORRESPONDENCE_NOT_SUPPORTED'
 else: classification='INDETERMINATE'
 result={'protocol_id':P['protocol_id'],'protocol_fingerprint':P['protocol_fingerprint'],'pre_gt_commit':'e07e83fe9a568aa600dfa5ef4aa72eb5e4640f30','pre_gt_fingerprint':'f5f8fbb5456735d086659ada34edfdc60f0aa0db044451c3056baf4d4a1568d9','authorities':{'mix_sha256':sha(a.mix),'bassdi_sha256':sha(a.bassdi),'outcome_sha256':sha(a.outcomes)},'compatibility':compatibility,'population_counts':counts,'observables':summaries,'availability_invariant_pass':availability_ok,'classification':classification,'decision_authority':OBS[0],'descriptive_observables_cannot_alter_classification':True,'thresholding':False,'composite_score':False,'classifier':False}
 result['evaluation_fingerprint']=hashlib.sha256(cb(result)).hexdigest(); a.result.write_bytes(cb(result))
if __name__=='__main__': main()
