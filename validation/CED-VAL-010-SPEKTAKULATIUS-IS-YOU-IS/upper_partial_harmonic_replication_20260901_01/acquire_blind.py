#!/usr/bin/env python3
import hashlib,json,resource,sys,time
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy.signal import get_window

HERE=Path(__file__).parent; P=json.loads((HERE/'protocol.json').read_text())
IN=HERE/'separation_run_1'/'htdemucs_ft'/'CED-VAL-010-CONTROLLED-MIXDOWN-v0.1'/'bass.wav'
FRAME=4096;HOP=1024;FFT=16384;CHUNK_FRAMES=512
NODE_DTYPE=np.dtype([('frame','<i4'),('sample','<i8'),('f0_index','<i2'),('f0_hz','<f8'),('harmonic_score','<f8'),('missing_fundamental_balance','<f8'),('upper_partial_evidence','<f8'),('partial_prominence_dispersion','<f8')])

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canonical(value):return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()
def f0_grid():
 lo,hi=P['pre_gt_continuous_evidence']['f0_hz']; count=int(np.floor(1200*np.log2(hi/lo)/5))+1
 return lo*2**(np.arange(count)*5/1200)
def interpolate(power,frequencies,targets):
 upper=np.clip(np.searchsorted(frequencies,targets),1,len(frequencies)-1);lower=upper-1
 weight=(targets-frequencies[lower])/(frequencies[upper]-frequencies[lower])
 return power[:,lower]*(1-weight)+power[:,upper]*weight
def measure(audio,sample_rate,first,final):
 scope=audio[first*HOP:(final-1)*HOP+FRAME]
 frames=np.lib.stride_tricks.sliding_window_view(scope,FRAME)[::HOP].copy();frames-=frames.mean(axis=1,keepdims=True)
 power=np.abs(np.fft.rfft(frames*get_window('hann',FRAME,fftbins=True),FFT,axis=1))**2
 frequencies=np.fft.rfftfreq(FFT,1/sample_rate);f0=f0_grid();positive=np.where(power>0,power,np.nan)
 epsilon=np.maximum(np.finfo(np.float64).tiny,np.nanmedian(positive,axis=1)*1e-12)
 offsets=(-200,-175,-150,-125,-100,100,125,150,175,200);prominences=[]
 for harmonic in range(1,9):
  predicted=f0*harmonic;energy=interpolate(power,frequencies,predicted)
  background=np.median(np.stack([interpolate(power,frequencies,predicted*2**(offset/1200)) for offset in offsets]),axis=0)
  prominences.append(np.log1p(energy/(background+epsilon[:,None])))
 prominences=np.moveaxis(np.stack(prominences),0,-1);score=prominences.mean(axis=-1)
 maxima=(score[:,1:-1]>=score[:,:-2])&(score[:,1:-1]>=score[:,2:])&((score[:,1:-1]>score[:,:-2])|(score[:,1:-1]>score[:,2:]))
 indices=np.argwhere(maxima);indices[:,0]+=first;indices[:,1]+=1
 local=indices[:,0]-first;grid=indices[:,1];fundamental=prominences[local,grid,0];upper=prominences[local,grid,1:].mean(axis=1)
 values=np.empty(len(indices),dtype=NODE_DTYPE);values['frame']=indices[:,0];values['sample']=indices[:,0]*HOP;values['f0_index']=grid;values['f0_hz']=f0[grid]
 values['harmonic_score']=score[local,grid];values['missing_fundamental_balance']=upper-fundamental;values['upper_partial_evidence']=upper;values['partial_prominence_dispersion']=np.std(prominences[local,grid],axis=1)
 return score,values
def boundary_integrity(audio,sample_rate):
 total=1+(len(audio)-FRAME)//HOP;start=((total//4)//CHUNK_FRAMES)*CHUNK_FRAMES;count=min(900,total-start)
 whole=measure(audio,sample_rate,start,start+count);parts=[measure(audio,sample_rate,first,min(first+CHUNK_FRAMES,start+count)) for first in range(start,start+count,CHUNK_FRAMES)]
 combined_score=np.concatenate([part[0] for part in parts]);combined_nodes=np.concatenate([part[1] for part in parts])
 return {'start_global_frame':start,'frames_tested':count,'artificial_boundary_global_frame':start+CHUNK_FRAMES,'score_lattice_exact':np.array_equal(whole[0],combined_score),'node_table_exact':np.array_equal(whole[1],combined_nodes),'pass':np.array_equal(whole[0],combined_score) and np.array_equal(whole[1],combined_nodes)}
def acquire(tag):
 started=time.perf_counter();output=Path(tag);output.mkdir();expected=(HERE/'separated_bass_authority.sha256').read_text().split()[0];assert sha(IN)==expected
 sample_rate,decoded=wavfile.read(IN);assert sample_rate==44100 and decoded.ndim==2 and decoded.shape[1]==2;audio=decoded.astype(np.float64).mean(axis=1)
 integrity=boundary_integrity(audio,sample_rate);assert integrity['pass'];frame_count=1+(len(audio)-FRAME)//HOP;counts=np.zeros(frame_count,dtype=np.int64);chunks=[]
 for first in range(0,frame_count,CHUNK_FRAMES):
  final=min(first+CHUNK_FRAMES,frame_count);_,nodes=measure(audio,sample_rate,first,final);chunks.append(nodes);counts[first:final]=np.bincount(nodes['frame']-first,minlength=final-first)
 nodes=np.concatenate(chunks);offsets=np.r_[0,np.cumsum(counts)].astype('<i8');np.save(output/'nodes.npy',nodes,allow_pickle=False);np.save(output/'frame_offsets.npy',offsets,allow_pickle=False)
 roles=('nodes.npy','frame_offsets.npy');authority={'protocol_id':P['protocol_id'],'protocol_fingerprint':P['protocol_fingerprint'],'input_sha256':sha(IN),'ground_truth_accessed':False,'sample_rate':sample_rate,'recording_samples':len(audio),'frame_count':frame_count,'node_count':len(nodes),'chunk_boundary_integrity':integrity,'dimensions':['harmonic_score','missing_fundamental_balance','upper_partial_evidence','partial_prominence_dispersion'],'artifacts':{role:{'bytes':(output/role).stat().st_size,'sha256':sha(output/role)} for role in roles}}
 authority['evidence_fingerprint']=hashlib.sha256(canonical(authority)).hexdigest();(output/'evidence_authority.json').write_bytes(canonical(authority));(output/'execution_noncanonical.json').write_bytes(canonical({'runtime_seconds':time.perf_counter()-started,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
 print(json.dumps({'fingerprint':authority['evidence_fingerprint'],'frames':frame_count,'nodes':len(nodes)}))
if __name__=='__main__':acquire(sys.argv[1])
