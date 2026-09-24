"""Audio-only feature and independent candidate representation. No reference inputs."""
import numpy as np
from scipy.signal import stft,find_peaks
from scipy.ndimage import maximum_filter1d
NAMES=['log_flux_peak','log_prominence','log_width_ms','log_rise_ms','rise_slope_norm','decay_slope_norm','log_flux_integral','flux_post_pre_logratio','peak_local_mean_ratio','peak_local_max_ratio','rms_pre_log','rms_post_pre_logratio','low_energy_pre_log','low_energy_post_pre_logratio','broad_energy_post_pre_logratio','centroid_change','spectral_slope_change','late_low_energy_persistence','low_spectral_concentration_change']
def means(a,idx,lo,hi):
 c=np.r_[0.,np.cumsum(a,dtype=float)];l=np.clip(idx+lo,0,len(a));r=np.clip(idx+hi,0,len(a));return (c[r]-c[l])/np.maximum(r-l,1)
def extract(x,sr):
 assert sr==44100 and x.ndim==1
 f,t,z=stft(x,fs=sr,window='hann',nperseg=1024,noverlap=980,nfft=1024,boundary=None,padded=False);a=abs(z);low=(f>=30)&(f<250);v=np.maximum(0,np.diff(a[low],axis=1,prepend=a[low,:1])).sum(axis=0)
 idx,props=find_peaks(v,height=1e-12,prominence=(None,None),width=(None,None),wlen=95)
 power=a*a;lowe=power[low].sum(axis=0);broad=power.sum(axis=0);cent=(f[:,None]*power).sum(axis=0)/(broad+1e-20)
 band=(f>=30)&(f<=5000);lf=np.log(f[band]);lf-=lf.mean();slope=(lf[:,None]*np.log(a[band]+1e-12)).sum(axis=0)/(lf@lf)
 sample=np.clip(np.round(t*sr).astype(int),0,len(x));sq=np.r_[0.,np.cumsum(x*x)];l=np.clip(sample-512,0,len(x));r=np.clip(sample+512,0,len(x));rms=np.sqrt((sq[r]-sq[l])/np.maximum(1,r-l))
 peak=v[idx];pre=means(v,idx,-48,-12);post=means(v,idx,12,48);local=means(v,idx,-24,25);localmax=maximum_filter1d(v,size=97,mode='nearest')[idx]
 def log(x):return np.log10(np.maximum(x,1e-20))
 def ratio(a,b):return log(a)-log(b)
 rise=np.maximum(idx-props['left_bases'],1);dec=np.maximum(props['right_bases']-idx,1)
 lp=means(lowe,idx,-48,-12);lq=means(lowe,idx,12,48);bp=means(broad,idx,-48,-12);bq=means(broad,idx,12,48)
 X=np.column_stack([log(peak),log(props['prominences']),np.log1p(props['widths']*44/44.1),np.log1p(rise*44/44.1),(peak-v[props['left_bases']])/(peak*rise+1e-20),(peak-v[props['right_bases']])/(peak*dec+1e-20),log(local*49*44/44100),ratio(post,pre),peak/(local+1e-20),peak/(localmax+1e-20),log(means(rms,idx,-48,-12)),ratio(means(rms,idx,12,48),means(rms,idx,-48,-12)),log(lp),ratio(lq,lp),ratio(bq,bp),(means(cent,idx,12,48)-means(cent,idx,-48,-12))/1000,means(slope,idx,12,48)-means(slope,idx,-48,-12),ratio(means(lowe,idx,48,96),lq),ratio(lq/(bq+1e-20),lp/(bp+1e-20))]);assert np.isfinite(X).all()
 return {'t':t,'flux':v,'candidate_frames':idx,'candidate_times':t[idx],'X':X,'low_energy':lowe,'rms':rms}
