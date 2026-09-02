#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
P=json.loads((HERE/'protocol.json').read_text())
EXPECTED=P['authorities']['mix_stft']

def canonical(value): return (json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for block in iter(lambda:f.read(1048576),b''): h.update(block)
 return h.hexdigest()
def scientific_fingerprint(starts,freq,power):
 h=hashlib.sha256(); h.update(canonical({'schema':'H-CEDVAL010-EVENT-BLIND-ATTACK-TIMBRE-STFT-v1','frame':2048,'hop':256,'nfft':4096,'scope':7422225}))
 for name,array in [('frame_starts',starts.astype('<i8',copy=False)),('frequency_hz',freq.astype('<f8',copy=False)),('power',power.astype('<f8',copy=False))]: h.update(name.encode()+b'\0'+str(array.shape).encode()+b'\0'+array.tobytes(order='C'))
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--stft',type=Path,required=True); ap.add_argument('--relations',type=Path,required=True); ap.add_argument('--authority',type=Path,required=True); a=ap.parse_args()
 assert sha(a.stft)==EXPECTED['sha256']
 with np.load(a.stft,allow_pickle=False) as z:
  assert sorted(z.files)==['frame_starts','frequency_hz','power']; starts=z['frame_starts']; freq=z['frequency_hz']; power=z['power']
 assert starts.dtype==np.dtype('<i8') and freq.dtype==np.dtype('<f8') and power.dtype==np.dtype('<f8')
 assert power.shape==(28986,744) and np.array_equal(starts,np.arange(28986,dtype=np.int64)*256)
 assert len(freq)==744 and freq[0]==0 and freq[1]==10.7666015625 and freq[-1]==7999.5849609375
 sfp=scientific_fingerprint(starts,freq,power); assert sfp==EXPECTED['scientific_fingerprint']
 total=power.sum(axis=1); state_available=np.isfinite(total)&(total>0); state=np.full_like(power,np.nan); state[state_available]=power[state_available]/total[state_available,None]
 delta=state[1:]-state[:-1]; finite=np.all(np.isfinite(delta),axis=1); delta_norm=np.linalg.norm(delta,axis=1); signed_available=finite&(delta_norm>0)
 positive=np.maximum(delta,0); negative=np.maximum(-delta,0); positive_available=finite&(np.linalg.norm(positive,axis=1)>0); negative_available=finite&(np.linalg.norm(negative,axis=1)>0)
 hashes={}
 for name,array in [('spectral_state',state),('signed_evolution',delta),('positive_rearticulation',positive),('negative_decay',negative)]:
  h=hashlib.sha256(); h.update(canonical({'identity':name,'shape':list(array.shape),'dtype':'little-endian float64'})); h.update(array.astype('<f8',copy=False).tobytes(order='C')); hashes[name]=h.hexdigest()
 relations=[]
 for i in range(len(starts)-1):
  sa=bool(state_available[i] and state_available[i+1]); sva=bool(signed_available[i]); pa=bool(positive_available[i]); na=bool(negative_available[i])
  relations.append({'relation_index':i,'start_frame_sample':int(starts[i]),'end_frame_sample':int(starts[i+1]),'sample_displacement':256,'state_pair_available':sa,'signed_evolution_available':sva,'positive_rearticulation_available':pa,'negative_decay_available':na,'unavailable_reason':None if sa and sva and pa and na else 'ZERO_OR_NONFINITE_POWER_OR_EVOLUTION_NORM'})
 relation_doc={'protocol_id':P['protocol_id'],'protocol_fingerprint':P['protocol_fingerprint'],'stft_sha256':EXPECTED['sha256'],'stft_scientific_fingerprint':sfp,'frame_count':len(starts),'relation_count':len(relations),'relations':relations}; relation_doc['relation_chain_fingerprint']=hashlib.sha256(canonical(relation_doc)).hexdigest(); a.relations.parent.mkdir(parents=True,exist_ok=True); a.relations.write_bytes(canonical(relation_doc))
 counts={k:{'available':sum(r[k] for r in relations),'unavailable':sum(not r[k] for r in relations)} for k in ('state_pair_available','signed_evolution_available','positive_rearticulation_available','negative_decay_available')}
 authority={'protocol_id':P['protocol_id'],'protocol_fingerprint':P['protocol_fingerprint'],'ground_truth_accessed':False,'bassdi_representation_accessed':False,'outcome_populations_accessed':False,'authoritative_stft':{'external_relative_to_JGA_EXTERNAL_ROOT':EXPECTED['external_relative_to_JGA_EXTERNAL_ROOT'],'sha256':EXPECTED['sha256'],'scientific_fingerprint':sfp,'byte_size':EXPECTED['byte_size'],'reused_in_place':True,'recomputed':False,'duplicated':False},'compatibility':{'frame_samples':2048,'hop_samples':256,'fft_size':4096,'frequency_bin_count':744,'frequency_coordinates_verified':True,'frame_origin_sample':0,'native_displacement_samples':256},'frames':len(starts),'relations':len(relations),'availability':counts,'reconstructible_evidence_fingerprints':hashes,'relation_chain':{'filename':a.relations.name,'sha256':sha(a.relations),'fingerprint':relation_doc['relation_chain_fingerprint']},'candidate_selection':False,'thresholding':False,'pruning':False,'smoothing':False,'temporal_aggregation':False,'source_inference':False,'dense_arrays_duplicated':False}
 authority['pre_gt_authority_fingerprint']=hashlib.sha256(canonical(authority)).hexdigest(); a.authority.write_bytes(canonical(authority))
if __name__=='__main__': main()
