#!/usr/bin/env python3
import argparse, hashlib, json, wave
from pathlib import Path
import numpy as np

HERE=Path(__file__).parent
P=json.loads((HERE/'protocol.json').read_text())
ROOT=Path(P['dataset']['root']); N=7422225; SR=44100; CHUNK=65536; MAX=8388607

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest()

def decode24(data,channels):
 raw=np.frombuffer(data,dtype=np.uint8).reshape(-1,3)
 value=raw[:,0].astype(np.int32)|(raw[:,1].astype(np.int32)<<8)|(raw[:,2].astype(np.int32)<<16)
 value=np.where(value&0x800000,value-0x1000000,value).astype(np.int64)
 return value.reshape(-1,channels)

def encode24(value):
 packed=np.where(value<0,value+(1<<24),value).astype(np.uint32).ravel()
 output=np.empty((len(packed),3),np.uint8); output[:,0]=packed; output[:,1]=packed>>8; output[:,2]=packed>>16
 return output.tobytes()

def sources():
 opened=[]
 for item in sorted(P['input_authorities'],key=lambda value:value['file'].encode('utf-8')):
  path=ROOT/item['file']; assert sha(path)==item['sha256']
  reader=wave.open(str(path),'rb')
  assert (reader.getnchannels(),reader.getsampwidth(),reader.getframerate(),reader.getnframes(),reader.getcomptype())==(item['channels'],3,SR,item['frames'],'NONE')
  opened.append((item,reader))
 return opened

def summed(opened,count):
 total=np.zeros((count,2),np.int64)
 for item,reader in opened:
  decoded=decode24(reader.readframes(count),item['channels'])
  total+=np.repeat(decoded,2,axis=1) if item['channels']==1 else decoded
 return total

def round_ratio(value,numerator,denominator):
 sign=np.where(value<0,-1,1); absolute=np.abs(value)
 return sign*((absolute*numerator+denominator//2)//denominator)

def main():
 parser=argparse.ArgumentParser(); parser.add_argument('--plan',type=Path,required=True); parser.add_argument('--output',type=Path,required=True); args=parser.parse_args()
 opened=sources(); peak=0
 for start in range(0,N,CHUNK):peak=max(peak,int(np.max(np.abs(summed(opened,min(CHUNK,N-start))))))
 for _,reader in opened:reader.close()
 plan={'authority_id':'PR-CEDVAL010-CONTROLLED-MIXDOWN-001','source_count':10,'common_intersection_frames':N,'unscaled_absolute_peak':peak,'global_gain_numerator':MAX,'global_gain_denominator':peak,'global_gain_rational':f'{MAX}/{peak}','output':{'channels':2,'sample_rate_hz':SR,'frame_count':N,'bit_depth':24},'method':'exact int64 sum; mono duplicate; stereo preserve; common intersection; global exact rational; nearest half away from zero'}
 if args.plan.exists():assert json.loads(args.plan.read_text())==plan
 else:args.plan.write_text(json.dumps(plan,sort_keys=True,separators=(',',':'))+'\n')
 opened=sources(); args.output.parent.mkdir(parents=True,exist_ok=True)
 with wave.open(str(args.output),'wb') as writer:
  writer.setnchannels(2);writer.setsampwidth(3);writer.setframerate(SR)
  for start in range(0,N,CHUNK):writer.writeframesraw(encode24(round_ratio(summed(opened,min(CHUNK,N-start)),MAX,peak)))
 for _,reader in opened:reader.close()
 with wave.open(str(args.output),'rb') as reader:assert (reader.getnchannels(),reader.getsampwidth(),reader.getframerate(),reader.getnframes())==(2,3,SR,N)
 print(json.dumps({'plan':plan,'output_sha256':sha(args.output)},sort_keys=True))

if __name__=='__main__':main()
