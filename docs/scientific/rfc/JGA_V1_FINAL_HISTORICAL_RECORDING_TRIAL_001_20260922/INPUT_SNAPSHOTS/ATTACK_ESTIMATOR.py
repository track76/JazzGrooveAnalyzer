import numpy as np
def estimate(pcm,anchor,fs=44100):
 # Absolute PCM-aligned 44-sample bins (~0.998ms); no source filtering.
 width=44;low=int(np.floor((anchor-.08)*fs/width));high=int(np.ceil((anchor+.04)*fs/width));idx=np.arange(low,high);energy=np.array([np.mean(pcm[i*width:(i+1)*width].astype(float)**2,axis=0) for i in idx]);times=idx*width/fs
 baseline=(times>=anchor-.06)&(times<anchor-.04);search=(times>=anchor-.04)&(times<=anchor+.02)
 found=[];detail=[]
 for ch in range(2):
  b=float(np.median(energy[baseline,ch]));p=float(np.quantile(energy[search,ch],.95));th=max(4*b,b+.01*(p-b));detail.append({'baseline':b,'p95':p,'threshold':th})
  if b<=0 or p<16*b:return {'status':'ABSTAIN','reason':'insufficient sharp rise relative to baseline','estimate_s':None,'details':detail}
  valid=energy[:,ch]>=th;hits=[i for i in range(len(idx)-2) if search[i] and all(valid[i:i+3]) and i>0 and not valid[i-1]]
  if not hits:return {'status':'ABSTAIN','reason':'no sustained threshold crossing','estimate_s':None,'details':detail}
  found.append(float(times[hits[0]]))
 if abs(found[0]-found[1])>.003:return {'status':'ABSTAIN','reason':'stereo crossings disagree by >3ms','estimate_s':None,'crossings':found,'details':detail}
 return {'status':'ESTIMATED','reason':'first sustained sharp energy emergence in both channels','estimate_s':max(found),'crossings':found,'details':detail}
