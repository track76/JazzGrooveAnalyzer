#!/usr/bin/env python3
import argparse, hashlib, json, wave
from pathlib import Path
import numpy as np

ROOT=Path('/Volumes/SSD Track/JGA/datasets/CED-VAL-005-REAL-JAZZ-MULTITRACK/raw/MaurizioPagnuttiSextet_AllTheGinIsGone_Full')
AUTH=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer/validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/input_authority_manifest.json')
N=10068072; SR=44100; CHUNK=65536; MAX=8388607
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def decode24(b,ch):
 q=np.frombuffer(b,dtype=np.uint8).reshape(-1,3); v=q[:,0].astype(np.int32)|(q[:,1].astype(np.int32)<<8)|(q[:,2].astype(np.int32)<<16); v=np.where(v&0x800000,v-0x1000000,v).astype(np.int64); return v.reshape(-1,ch)
def encode24(v):
 q=np.where(v<0,v+(1<<24),v).astype(np.uint32).ravel(); out=np.empty((len(q),3),np.uint8); out[:,0]=q; out[:,1]=q>>8; out[:,2]=q>>16; return out.tobytes()
def sources():
 a=json.loads(AUTH.read_text()); out=[]
 for x in sorted(a['assets'],key=lambda x:x['filename'].encode('utf-8')):
  p=ROOT/x['filename']; assert sha(p)==x['sha256']; w=wave.open(str(p),'rb'); assert (w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes(),w.getcomptype())==(x['channels'],3,SR,N,'NONE'); out.append((x,p,w))
 return out
def summed(src,n):
 total=np.zeros((n,2),np.int64)
 for x,p,w in src:
  a=decode24(w.readframes(n),x['channels']); total += np.repeat(a,2,axis=1) if x['channels']==1 else a
 return total
def round_ratio(v,num,den):
 sign=np.where(v<0,-1,1); a=np.abs(v); return sign*((a*num+den//2)//den)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--plan',type=Path,required=True); ap.add_argument('--output',type=Path); z=ap.parse_args(); src=sources(); peak=0
 for start in range(0,N,CHUNK): peak=max(peak,int(np.max(np.abs(summed(src,min(CHUNK,N-start))))))
 for _,_,w in src:w.close()
 plan={'authority_id':'PR-CEDVAL005-CONTROLLED-MIXDOWN-001','source_manifest_sha256':sha(AUTH),'source_count':16,'unscaled_absolute_peak':peak,'global_gain_numerator':MAX,'global_gain_denominator':peak,'global_gain_rational':f'{MAX}/{peak}','output':{'channels':2,'sample_rate_hz':SR,'frame_count':N,'bit_depth':24},'method':'exact int64 sum; mono duplicate; stereo preserve; global exact rational; nearest half away from zero'}
 if z.plan.exists(): assert json.loads(z.plan.read_text())==plan
 else: z.plan.write_text(json.dumps(plan,sort_keys=True,separators=(',',':'))+'\n')
 if z.output:
  src=sources(); z.output.parent.mkdir(parents=True,exist_ok=True)
  with wave.open(str(z.output),'wb') as w:
   w.setnchannels(2);w.setsampwidth(3);w.setframerate(SR)
   for start in range(0,N,CHUNK): w.writeframesraw(encode24(round_ratio(summed(src,min(CHUNK,N-start)),MAX,peak)))
  for _,_,w in src:w.close()
  with wave.open(str(z.output),'rb') as w: assert (w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes())==(2,3,SR,N)
 print(json.dumps({'plan':plan,'output':str(z.output) if z.output else None,'output_sha256':sha(z.output) if z.output else None},sort_keys=True))
if __name__=='__main__':main()
