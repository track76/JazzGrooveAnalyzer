#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import soundfile as sf

HERE=Path(__file__).resolve().parent; P=json.loads((HERE/'protocol.json').read_text())
SR=44100; FRAME=2048; HOP=256; NFFT=4096; SCOPE=7422225
FREQ_ALL=np.fft.rfftfreq(NFFT,1/SR); KEEP=FREQ_ALL<=8000; FREQ=FREQ_ALL[KEEP].astype('<f8')
WIN=np.hanning(FRAME+1)[:-1].astype(np.float64)

def cb(x): return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()
def main():
 a=argparse.ArgumentParser(); a.add_argument('--mix',type=Path,required=True); a.add_argument('--representation',type=Path,required=True); a.add_argument('--nodes',type=Path,required=True); a.add_argument('--authority',type=Path,required=True); args=a.parse_args()
 assert sha(args.mix)==P['input_authorities']['controlled_mix']['sha256']
 audio,rate=sf.read(args.mix,dtype='float64',always_2d=True); assert rate==SR and len(audio)==SCOPE and audio.shape[1]==2
 mono=audio.mean(axis=1,dtype=np.float64); starts=np.arange(0,SCOPE-FRAME+1,HOP,dtype='<i8')
 power=np.empty((len(starts),int(KEEP.sum())),dtype='<f8')
 for first in range(0,len(starts),512):
  ss=starts[first:first+512]; frames=np.stack([mono[s:s+FRAME] for s in ss]); spec=np.fft.rfft(frames*WIN,n=NFFT,axis=1)
  power[first:first+len(ss)]=spec.real[:,KEEP]**2+spec.imag[:,KEEP]**2
 positive=power[power>0]; eps=max(np.finfo(np.float64).tiny,float(np.median(positive))*1e-12)
 use=(FREQ>=20)&(FREQ<=8000); scoped=power[:,use]; freq=FREQ[use]; total=scoped.sum(axis=1)
 centroid=np.divide((scoped*freq).sum(axis=1),total,out=np.full(len(starts),np.nan),where=total>0)
 bandwidth=np.sqrt(np.divide((scoped*(freq[None,:]-centroid[:,None])**2).sum(axis=1),total,out=np.full(len(starts),np.nan),where=total>0))
 flatness=np.exp(np.log(scoped+eps).mean(axis=1))/(scoped.mean(axis=1)+eps)
 low=power[:,(FREQ>=20)&(FREQ<250)].sum(axis=1); high=power[:,(FREQ>=2000)&(FREQ<=8000)].sum(axis=1)
 balance=10*np.log10((high+eps)/(low+eps)); future=13; count=len(starts)-future+1
 nodes=[]
 for i in range(count):
  sl=slice(i,i+future)
  values=[float(np.median(x[sl])) for x in (centroid,bandwidth,flatness,balance)]; available=bool(np.all(np.isfinite(values)))
  nodes.append({'frame_index':i,'anchor_start_sample':int(starts[i]),'attack_spectral_centroid':values[0] if available else None,'attack_spectral_bandwidth':values[1] if available else None,'attack_spectral_flatness':values[2] if available else None,'attack_high_low_spectral_balance_db':values[3] if available else None,'available':available,'unavailable_reason':None if available else 'NONFINITE_SPECTRAL_MOMENT_IN_SILENT_OR_ZERO_POWER_TRAJECTORY'})
 args.representation.parent.mkdir(parents=True,exist_ok=True); np.savez(args.representation,frame_starts=starts,frequency_hz=FREQ,power=power)
 h=hashlib.sha256(); h.update(cb({'schema':'H-CEDVAL010-EVENT-BLIND-ATTACK-TIMBRE-STFT-v1','frame':FRAME,'hop':HOP,'nfft':NFFT,'scope':SCOPE}));
 for name,array in [('frame_starts',starts),('frequency_hz',FREQ),('power',power)]: h.update(name.encode()+b'\0'+str(array.shape).encode()+b'\0'+array.tobytes())
 repfp=h.hexdigest(); node_doc={'protocol_id':P['protocol_id'],'protocol_fingerprint':P['protocol_fingerprint'],'epsilon':eps,'node_count':len(nodes),'dimensions':list(P['continuous_representation']['dimensions']),'nodes':nodes}
 node_doc['evidence_fingerprint']=hashlib.sha256(cb(node_doc)).hexdigest(); args.nodes.write_bytes(cb(node_doc))
 authority={'protocol_id':P['protocol_id'],'protocol_fingerprint':P['protocol_fingerprint'],'ground_truth_accessed':False,'input_mix_sha256':sha(args.mix),'representation':{'filename':args.representation.name,'byte_size':args.representation.stat().st_size,'sha256':sha(args.representation),'scientific_fingerprint':repfp,'schema':'H-CEDVAL010-EVENT-BLIND-ATTACK-TIMBRE-STFT-v1','external_relative_path':str(args.representation).split('/JGA/',1)[1]},'nodes':{'filename':args.nodes.name,'byte_size':args.nodes.stat().st_size,'sha256':sha(args.nodes),'evidence_fingerprint':node_doc['evidence_fingerprint'],'count':len(nodes)},'thresholds':None,'selection':None,'composite':None}
 args.authority.write_bytes(cb(authority))
if __name__=='__main__': main()
