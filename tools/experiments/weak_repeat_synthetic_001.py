"""Minimal reproducible synthetic innovation contrast. No audio/third-party data.
Only observation arrays enter the detector. Latent truth is used by scorer only.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import hashlib,json,math,platform,sys
from pathlib import Path
import numpy as np
FS=2000;N=3600;T=np.arange(N)/FS;PRE=T<.65
FREQS=[55.,73.,98.];DECAYS=[.7,1.4]
BASIS=np.column_stack([np.exp(-d*T)*fn(2*np.pi*f*h*T) for f in FREQS for d in DECAYS for h in [1,2] for fn in [np.sin,np.cos]]+[np.sin(2*np.pi*f*T) for f in [231.,347.]]+[np.cos(2*np.pi*f*T) for f in [231.,347.]])
# Fixed family and prehistory only; no fitted state ever sees target/future samples.
PINV=np.linalg.pinv(BASIS[PRE],rcond=1e-5)
WIN=40;STRIDE=10;ENDS=np.arange(1400,N+1,STRIDE);STARTS=ENDS-WIN

def signal(seed,kind,amp=0.):
 rng=np.random.default_rng(seed);f=float(rng.choice(FREQS));d=float(rng.choice(DECAYS));phi=float(rng.uniform(-np.pi,np.pi));baseamp=float(rng.uniform(.7,1.3));tau=float(rng.uniform(.85,1.15));at=int(round(tau*FS));tau=at/FS
 bass=baseamp*np.exp(-d*T)*(np.sin(2*np.pi*f*T+phi)+.25*np.sin(4*np.pi*f*T+.3))
 background=.20*np.sin(2*np.pi*231*T+rng.uniform(-np.pi,np.pi))+.15*np.cos(2*np.pi*347*T+rng.uniform(-np.pi,np.pi));noise=rng.normal(0,.012,N);x=bass+background+noise;u=np.maximum(T-tau,0);ramp=np.minimum(u/.01,1)
 added=np.zeros(N)
 if kind in ['attack','strong']:added=amp*ramp*np.exp(-d*u)*np.sin(2*np.pi*f*u+rng.uniform(-np.pi,np.pi));added[T<tau]=0
 elif kind=='gain_without_event':added=.10*ramp*bass
 elif kind=='mask_without_bass_event':added=.18*np.exp(-((T-tau)/.015)**2)*np.sin(2*np.pi*311*T)
 elif kind=='pitch_drift_without_event':
  phasewarp=2*np.pi*1.3*(u-.01*(1-np.exp(-u/.01)));warped=baseamp*np.exp(-d*T)*(np.sin(2*np.pi*f*T+phi+phasewarp)+.25*np.sin(4*np.pi*f*T+.3+2*phasewarp));added=warped-bass
 elif kind=='stable':pass
 else:raise ValueError(kind)
 return x+added,{'seed':seed,'kind':kind,'amp':amp,'reference_s':tau,'reference_sample':at,'f':f,'decay':d,'digital_uncertainty_s':.5/FS}

def detector(x,threshold):
 coef=PINV@x[PRE];pred=BASIS@coef;res=x-pred
 power=np.r_[0,np.cumsum(res*res)];score=np.sqrt((power[ENDS]-power[STARTS])/WIN)/.012
 active=score>threshold;times=[];was=False
 for end,on in zip(ENDS,active):
  if on and not was:times.append(float(end/FS))
  was=bool(on)
 return times,score,pred

def interval(k,n):
 if not n:return None
 z=1.959963984540054;p=k/n;den=1+z*z/n;center=(p+z*z/(2*n))/den;half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
 return [max(0,center-half),min(1,center+half)]

def main():
 out=Path(os.environ['JGA_OUTPUT_ROOT']);root=Path(__file__).resolve().parents[2];plan=json.loads((Path(__file__).with_name('PLAN.json')).read_bytes())
 # Calibrate threshold on stable H0 ONLY, disjoint fixed seeds; never tune on test.
 calibration=[]
 for seed in range(1000,1064):
  x,_=signal(seed,'stable');_,score,_=detector(x,float('inf'));calibration.append(float(score.max()))
 threshold=float(np.quantile(calibration,.99,method='higher'));records=[];raw=[];timing=[]
 arms=[('stable',0.),('gain_without_event',0.),('mask_without_bass_event',0.),('pitch_drift_without_event',0.),('attack',.03),('attack',.08),('attack',.16),('strong',.4)]
 # Matched scenes across arms; uncertainty resampling unit is scene, not event.
 for kind,amp in arms:
  for i in range(64):
   seed=2000+i;x,truth=signal(seed,kind,amp);times,score,pred=detector(x,threshold)
   positive=kind in ['attack','strong'];errors=[t-truth['reference_s'] for t in times];valid=[j for j,e in enumerate(errors) if abs(e)<=.05];matched=min(valid,key=lambda j:abs(errors[j])) if positive and valid else None
   r=dict(truth,candidates_s=times,positive=positive,matched=matched is not None,missed=int(positive and matched is None),extra=len(times)-int(matched is not None),UNKNOWN_P=True,UNKNOWN_I=True,censored=0,error_s=errors[matched] if matched is not None else None,observed_novelty=bool(times),N_semantics='thresholded causal residual, not physical gesture',forecast_precondition_number=float(np.linalg.cond(BASIS[PRE])))
   records.append(r)
   if r['error_s'] is not None:timing.append(r['error_s'])
   # Paired source/background/prehistory audit. Reference never passed to detector.
   if i==0:raw.append((kind+str(amp),x,score,pred))
 summary={}
 for kind,amp in arms:
  a=[r for r in records if r['kind']==kind and r['amp']==amp];k=sum(r['matched'] if r['positive'] else r['observed_novelty'] for r in a);e=[r['error_s'] for r in a if r['error_s'] is not None]
  summary[kind+'_'+str(amp)]={'n':len(a),'matched_or_false_positive_scenes':k,'fraction':k/len(a),'Wilson95_conditional_generator_scenes':interval(k,len(a)),'missed':sum(r['missed'] for r in a),'extra_events':sum(r['extra'] for r in a),'unknown_P':len(a),'unknown_I':len(a),'censored':0,'timing_matched_only':{'n':len(e),'median_s':float(np.median(e)) if e else None,'p95_absolute_s':float(np.quantile(np.abs(e),.95)) if e else None},'physical_accuracy':None}
 # Leakage checks: alter future and confirm fitted coefficients remain identical.
 x,tr=signal(2077,'attack',.08);coef=PINV@x[PRE];modified=x.copy();modified[~PRE]+=17*np.sin(np.arange((~PRE).sum()));assert np.array_equal(coef,PINV@modified[PRE]);x0,_=signal(2077,'stable');assert np.array_equal(x[PRE],x0[PRE]);assert not set(range(1000,1064))&set(range(2000,2064))
 # Exact observational collision: same-pitch phase-aligned additive excitation vs
 # multiplicative gain change of existing oscillation. These are MODEL labels,
 # not physically recorded gestures. One array, two latent construction accounts.
 collisions=[]
 for i in range(32):
  x,tr=signal(3000+i,'stable');rng=np.random.default_rng(3000+i);tau=tr['reference_s'];g=.08*np.minimum(np.maximum(T-tau,0)/.01,1);component=np.exp(-.7*T)*np.sin(2*np.pi*73*T+.2)
  h0=x+(1+g)*component;h1=x+np.add(np.ones(N),g)*component;observation=h0;assert np.array_equal(h0,h1)
  decisions0=detector(h0,threshold)[0];decisions1=detector(h1,threshold)[0];assert decisions0==decisions1
  collisions.append({'scene':i,'bit_identical':True,'same_detector_decision':True,'oracle_latent_labels_distinct':True,'H0':'gain change without stipulated new event','H1':'phase-aligned additive software excitation','P':'UNIDENTIFIABLE_IN_THIS_SURROGATE','array_sha256':hashlib.sha256(observation.tobytes()).hexdigest()})
 # Post-only refit diagnostic: score the same local sinusoid after a step of a
 # same-frequency component. This intentionally uses future data, never deployed.
 tt=np.arange(600)/FS;f=73.;b=np.column_stack([np.sin(2*np.pi*f*tt),np.cos(2*np.pi*f*tt)]);baseline=b@np.array([.7,.2]);addition=b@np.array([.05,-.02]);y=baseline+addition;postfit=b@np.linalg.lstsq(b,y,rcond=None)[0];post_error=float(np.sqrt(np.mean((y-postfit)**2)));past_forecast_error=float(np.sqrt(np.mean(addition**2)))
 # Paired bootstrap on scenario-level matched advantage over weak .03; conditional
 # engineering uncertainty only, never clinical/physical/general-jazz inference.
 rng=np.random.default_rng(909);lo=np.array([r['matched'] for r in records if r['kind']=='attack' and r['amp']==.03],float);hi=np.array([r['matched'] for r in records if r['kind']=='attack' and r['amp']==.16],float);delta=hi-lo;boot=np.array([delta[rng.integers(0,64,64)].mean() for _ in range(1000)])
 result={'status':'COMPLETED_SYNTHETIC_DEVELOPMENT_ONLY','physical_reference':'BLOCKED_REFERENCE','Phase_B':'NOT_STARTED','plan_sha256':hashlib.sha256(Path(__file__).with_name('PLAN.json').read_bytes()).hexdigest(),'threshold_calibration_H0_only':threshold,'calibration_scenes':64,'test_scenes':64,'test_observations':len(records),'summary':summary,'identifiability_collision_pairs':len(collisions),'identical_pairs':sum(r['bit_identical'] for r in collisions),'max_possible_balanced_accuracy_on_balanced_identical_pairs':.5,'postfit_diagnostic':{'post_only_RMSE':post_error,'past_constrained_RMSE':past_forecast_error,'future_fit_is_not_a_valid_detector':True},'paired_detection_advantage_amp016_minus003':{'estimate':float(delta.mean()),'bootstrap95_conditional_scene':[float(v) for v in np.quantile(boot,[.025,.975])]},'leakage_checks':{'past_coefficients_future_invariant':True,'H0_H1_prehistory_bit_identical':True,'calibration_test_seed_disjoint':True,'truth_not_detector_argument':True,'no_per_case_normalization_by_future':True,'threshold_frozen_before_test':True},'limitations':['Matched model family is optimistic; drift/gain/background negatives are explicit out-of-model stresses','Conditional synthetic intervals are not physical uncertainty or population jazz accuracy','No attribution of N to Bass I or physical P','Fixed synthetic clock zero offset to software index only; no physical synchronization evidence'],'environment':{'python':sys.version,'numpy':np.__version__,'platform':platform.platform()}}
 for name,value in [('RESULTS.json',result),('EVENT_RECORDS.json',records),('IDENTIFIABILITY_COLLISIONS.json',collisions)]:
  (out/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
 np.savez_compressed(out/'EXAMPLE_ARRAYS.npz',**{name+'_'+k:arr for name,x,s,p in raw for k,arr in [('mix',x),('score',s),('past_prediction',p)]})
 (out/'MANIFEST.json').write_text(json.dumps({p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':p.stat().st_size} for p in out.iterdir() if p.is_file() and p.name not in ['stdout.txt','stderr.txt','MANIFEST.json']},sort_keys=True,indent=2)+'\n')
 print(json.dumps({'status':result['status'],'summary':summary,'threshold':threshold,'collisions':len(collisions),'postfit':result['postfit_diagnostic']}),flush=True)
if __name__=='__main__':main()
