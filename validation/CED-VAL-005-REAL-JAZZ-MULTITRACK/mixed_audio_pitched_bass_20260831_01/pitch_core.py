import hashlib,json,math,wave
from pathlib import Path
import numpy as np
from scipy.io import wavfile

FMIN=41.20344461410875; FMAX=195.99771799087463; SR=44100
NFFT=16384; FRAME=4096; HOP=1024
F0S=FMIN*2**(np.arange(int(math.floor(1200*math.log2(FMAX/FMIN)/5))+1)*5/1200)
HARM=np.arange(1,9,dtype=float)

def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()
def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1048576),b''): h.update(block)
    return h.hexdigest()
def load_pcm(path):
    rate,data=wavfile.read(path)
    if rate!=SR: raise RuntimeError(f'unexpected sample rate {rate}')
    if data.ndim==2: data=data.astype(np.float64).mean(axis=1)
    else: data=data.astype(np.float64)
    scale=float(np.max(np.abs(data))) or 1.0
    return data/scale
def interp_power(power,freq):
    x=freq*NFFT/SR; lo=np.floor(x).astype(int); frac=x-lo
    ok=(lo>=0)&(lo+1<len(power)); out=np.zeros_like(x,dtype=float)
    out[ok]=power[lo[ok]]*(1-frac[ok])+power[lo[ok]+1]*frac[ok]
    return out
def note(f):
    m=69+12*math.log2(f/440); lower=math.floor(m); nearest=lower if m-lower<=.5 else lower+1
    names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    return {'midi':nearest,'note':f'{names[nearest%12]}{nearest//12-1}','deviation_cents':100*(m-nearest)}
def analyze_event(audio,t):
    start=round((t+.04)*SR); stop=round((t+.30)*SR); starts=list(range(start,stop-FRAME+1,HOP)); frames=[]; scores=[]
    win=np.hanning(FRAME+1)[:-1]; fftfreq=np.fft.rfftfreq(NFFT,1/SR)
    for pos in starts:
        y=audio[pos:pos+FRAME]
        if len(y)!=FRAME: continue
        y=(y-y.mean())*win; power=np.abs(np.fft.rfft(y,NFFT))**2+1e-30
        hf=F0S[:,None]*HARM[None,:]; hp=interp_power(power,hf)
        noise=[]
        for off in (-200,-175,-150,-125,-100,100,125,150,175,200): noise.append(interp_power(power,hf*2**(off/1200)))
        nl=np.median(np.stack(noise),axis=0)+1e-30; prom=10*np.log10(hp/nl); supported=prom>=6
        vals=np.log1p(hp/nl); sc=np.mean(np.sort(vals,axis=1)[:,-4:],axis=1)
        best=int(np.argmax(sc)); f=float(F0S[best]); bands=np.zeros_like(fftfreq,dtype=bool)
        for h in HARM:
            c=f*h
            if c>1600: continue
            bands|=(fftfreq>=c*2**(-35/1200))&(fftfreq<=c*2**(35/1200))
        domain=(fftfreq>=40)&(fftfreq<=1600); ratio=float(power[bands&domain].sum()/power[domain].sum())
        eligible=bool(supported[best].sum()>=3 and ratio>=.12)
        frames.append({'offset_seconds':(pos/SR)-t,'best_f0_hz':f,'supported_partials':int(supported[best].sum()),'harmonic_energy_ratio':ratio,'eligible':eligible})
        scores.append(sc)
    stable=False
    for i in range(max(0,len(frames)-2)):
        z=frames[i:i+3]
        if all(q['eligible'] for q in z) and 1200*math.log2(max(q['best_f0_hz'] for q in z)/min(q['best_f0_hz'] for q in z))<=35: stable=True
    eligible_count=sum(q['eligible'] for q in frames)
    if stable and frames and eligible_count/len(frames)>=.5: status='PITCHED_EVIDENCE_PRESENT'
    elif eligible_count==0: status='PITCHED_EVIDENCE_ABSENT'
    else: status='INDETERMINATE'
    candidates=[]
    if status=='PITCHED_EVIDENCE_PRESENT':
        agg=np.median(np.stack([s for s,q in zip(scores,frames) if q['eligible']]),axis=0); order=np.argsort(agg)[::-1]; best=float(agg[order[0]])
        for idx in order:
            f=float(F0S[idx])
            if float(agg[idx])<.95*best: break
            if all(abs(1200*math.log2(f/c['f0_hz']))>=35 for c in candidates): candidates.append({'f0_hz':f,'aggregate_score':float(agg[idx]),**note(f)})
            if len(candidates)==3: break
    return {'status':status,'frame_count':len(frames),'eligible_frame_count':eligible_count,'stable_run':stable,'candidates':candidates,'frames':frames}
