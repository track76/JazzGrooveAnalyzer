import hashlib,json,math
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly

SR=44100; FRAME=4096; HOP=1024; NFFT=16384
FMIN=41.20344461410875; FMAX=195.99771799087463
F0S=FMIN*2**(np.arange(int(math.floor(1200*math.log2(FMAX/FMIN)/5))+1)*5/1200)
HARM=np.arange(1,9,dtype=float); WIN=np.hanning(FRAME+1)[:-1]; FFTFREQ=np.fft.rfftfreq(NFFT,1/SR)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def load_resampled(path):
 rate,data=wavfile.read(path); assert rate==48000
 data=data.astype(np.float64); data=data.mean(axis=1) if data.ndim==2 else data
 scale=float(np.max(np.abs(data))) or 1.; return resample_poly(data/scale,147,160,padtype='constant')
def interp(power,freq):
 x=freq*NFFT/SR; lo=np.floor(x).astype(int); frac=x-lo; ok=(lo>=0)&(lo+1<len(power)); out=np.zeros_like(x,float); out[ok]=power[lo[ok]]*(1-frac[ok])+power[lo[ok]+1]*frac[ok]; return out
def note(f):
 m=69+12*math.log2(f/440); lo=math.floor(m); n=lo if m-lo<=.5 else lo+1; names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']; return {'midi':n,'note':f'{names[n%12]}{n//12-1}','deviation_cents':100*(m-n)}
def frame_analysis(audio,pos,keep_scores=False):
 y=audio[pos:pos+FRAME]
 if len(y)!=FRAME:return None
 y=(y-y.mean())*WIN; power=np.abs(np.fft.rfft(y,NFFT))**2+1e-30; hf=F0S[:,None]*HARM[None,:]; hp=interp(power,hf)
 noise=[interp(power,hf*2**(o/1200)) for o in (-200,-175,-150,-125,-100,100,125,150,175,200)]; nl=np.median(np.stack(noise),axis=0)+1e-30
 prom=10*np.log10(hp/nl); supported=prom>=6; vals=np.log1p(hp/nl); scores=np.mean(np.sort(vals,axis=1)[:,-4:],axis=1); best=int(np.argmax(scores)); f=float(F0S[best]); bands=np.zeros_like(FFTFREQ,bool)
 for h in HARM:
  c=f*h
  if c<=1600:bands|=(FFTFREQ>=c*2**(-35/1200))&(FFTFREQ<=c*2**(35/1200))
 domain=(FFTFREQ>=40)&(FFTFREQ<=1600); ratio=float(power[bands&domain].sum()/power[domain].sum()); sup=int(supported[best].sum())
 out={'frame_index':pos//HOP,'start_seconds':pos/SR,'best_f0_hz':f,'best_score':float(scores[best]),'supported_partials':sup,'harmonic_energy_ratio':ratio,'eligible':bool(sup>=3 and ratio>=.12)}
 if keep_scores:out['_scores']=scores
 return out
def candidate_set(frames):
 agg=np.median(np.stack([f['_scores'] for f in frames if f['eligible']]),axis=0); order=np.argsort(agg)[::-1]; best=float(agg[order[0]]); out=[]
 for idx in order:
  f=float(F0S[idx])
  if float(agg[idx])<.95*best:break
  if all(abs(1200*math.log2(f/x['f0_hz']))>=35 for x in out):out.append({'f0_hz':f,'aggregate_score':float(agg[idx]),**note(f)})
  if len(out)==3:break
 return out
def reference_event(audio,t):
 frames=[frame_analysis(audio,p,True) for p in range(round((t+.04)*SR),round((t+.30)*SR)-FRAME+1,HOP)]; frames=[f for f in frames if f]
 stable=any(all(q['eligible'] for q in frames[i:i+3]) and 1200*math.log2(max(q['best_f0_hz'] for q in frames[i:i+3])/min(q['best_f0_hz'] for q in frames[i:i+3]))<=35 for i in range(max(0,len(frames)-2)))
 status='PITCHED_EVIDENCE_PRESENT' if stable and sum(f['eligible'] for f in frames)/len(frames)>=.5 else ('PITCHED_EVIDENCE_ABSENT' if not any(f['eligible'] for f in frames) else 'INDETERMINATE')
 cs=candidate_set(frames) if status=='PITCHED_EVIDENCE_PRESENT' else []
 for f in frames:f.pop('_scores',None)
 return {'status':status,'candidates':cs,'frames':frames}
