#!/usr/bin/env python3
import hashlib,importlib.util,json,sys
from fractions import Fraction
from pathlib import Path
import numpy as np
from numba import njit,prange
from scipy.stats import mannwhitneyu

HERE=Path(__file__).parent;P=json.loads((HERE/'protocol.json').read_text());N=7422225;SR=44100;HOP_SECONDS=1024/SR
SCORER=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer/validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/separation_robustness_20260825_01/score.py')
DIMENSIONS=('maximum_harmonic_score','missing_fundamental_balance','upper_partial_evidence','partial_prominence_dispersion')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canonical(value):return (json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def events(payload):
 output=[]
 for index,event in enumerate(payload['elementary_metric_events']):output.append({'eme_id':event['eme_id'],'native_index':event.get('producer_frame',index),'time':Fraction(event['producer_sample_coordinate'],SR)})
 return sorted(output,key=lambda item:(item['time'],item['native_index'],item['eme_id']))
def correspondence(original,separated):
 spec=importlib.util.spec_from_file_location('frozen_scorer',SCORER);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.SCOPE_END=Fraction(N,SR)
 return module.assign(events(original),events(separated))
def summary(values,unavailable):
 values=np.asarray(values,float);q=np.quantile(values,(.25,.5,.75));return {'n_available':len(values),'n_unavailable':unavailable,'minimum':float(values.min()),'q1':float(q[0]),'median':float(q[1]),'q3':float(q[2]),'maximum':float(values.max())}
@njit(parallel=True)
def bootstrap_auc(x,y,ix,iy):
 output=np.empty(ix.shape[0],np.float64)
 for b in prange(ix.shape[0]):
  left=np.sort(x[ix[b]]);right=np.sort(y[iy[b]]);wins=0.0
  for value in left:
   lo=np.searchsorted(right,value,side='left');hi=np.searchsorted(right,value,side='right');wins+=lo+.5*(hi-lo)
  output[b]=wins/(len(left)*len(right))
 return output
def compare(left,right,seed):
 left=np.asarray(left,float);right=np.asarray(right,float);u,pvalue=mannwhitneyu(left,right,alternative='two-sided');auc=float(u/(len(left)*len(right)))
 rng=np.random.Generator(np.random.PCG64(seed));ix=rng.integers(0,len(left),size=(10000,len(left)),dtype=np.int32);iy=rng.integers(0,len(right),size=(10000,len(right)),dtype=np.int32);deltas=2*bootstrap_auc(left,right,ix,iy)-1;ci=np.quantile(deltas,(.025,.975))
 return {'cliff_delta':2*auc-1,'rank_auc':auc,'mann_whitney_p':float(pvalue),'cliff_delta_bootstrap_ci95':[float(ci[0]),float(ci[1])]}
def measure(nodes,offsets,timestamp):
 first=max(0,int(np.ceil((timestamp-.050)/HOP_SECONDS)));final=min(len(offsets)-1,int(np.floor((timestamp+.050)/HOP_SECONDS))+1)
 if first>=len(offsets)-1 or final<=first:return {dimension:None for dimension in DIMENSIONS}|{'unavailable_reason':'no complete LONG frame in fixed window'}
 local=nodes[offsets[first]:offsets[final]]
 if len(local)==0:return {dimension:None for dimension in DIMENSIONS}|{'unavailable_reason':'no mathematical local F0 maximum in fixed window'}
 order=np.lexsort((local['f0_index'],local['frame'],-local['harmonic_score']));best=local[order[0]]
 return {'maximum_harmonic_score':float(local['harmonic_score'].max()),'missing_fundamental_balance':float(local['missing_fundamental_balance'].max()),'upper_partial_evidence':float(local['upper_partial_evidence'].max()),'partial_prominence_dispersion':float(best['partial_prominence_dispersion']),'unavailable_reason':None}
def main(destination):
 authority=json.loads((HERE/'evidence_1/evidence_authority.json').read_text());assert authority['evidence_fingerprint']=='39625b741d438816eb64b412ea6da4c351766e8496df540ef88fc4427f931c36'
 original=json.loads((HERE/'original_bass_observations.json').read_text());separated=json.loads((HERE/'separated_bass_observations_1.json').read_text());assignment=correspondence(original,separated);preserved_ids={item['original_eme_id'] for item in assignment['matches']}
 originals=original['elementary_metric_events'];timestamps=np.array([event['producer_sample_coordinate']/SR for event in originals]);identifiers=[event['eme_id'] for event in originals];labels=np.array(['PRESERVED' if identifier in preserved_ids else 'MISSED' for identifier in identifiers]);assert sum(labels=='PRESERVED')==assignment['matched_count']
 duration=N/SR;edges=np.linspace(0,duration,21);negatives=[]
 for index in range(20):
  upper=edges[index+1]+(1e-12 if index==19 else 0);required=int(((timestamps>=edges[index])&(timestamps<upper)).sum());lattice=edges[index]+(np.arange(10000)+.5)/10000*(edges[index+1]-edges[index]);eligible=np.min(np.abs(lattice[:,None]-timestamps[None,:]),axis=1)>.050;negatives.extend(lattice[eligible][:required])
 negatives=np.asarray(negatives);assert len(negatives)==len(originals);negative_authority={'rule':P['negative_population'],'coordinates':[float(value) for value in negatives]};negative_fingerprint=hashlib.sha256(canonical(negative_authority)).hexdigest()
 nodes=np.load(HERE/'evidence_1/nodes.npy',mmap_mode='r');offsets=np.load(HERE/'evidence_1/frame_offsets.npy',mmap_mode='r');combined_times=np.r_[timestamps,negatives];combined_labels=np.r_[labels,np.repeat('NEGATIVE',len(negatives))];rows=[]
 for sequence,(timestamp,population) in enumerate(zip(combined_times,combined_labels)):
  measured=measure(nodes,offsets,timestamp);rows.append({'id':identifiers[sequence] if sequence<len(identifiers) else f'NEG-{sequence-len(identifiers):04d}','timestamp':float(timestamp),'population':str(population),**measured})
 populations={population:int(sum(combined_labels==population)) for population in ('PRESERVED','MISSED','NEGATIVE')};results={}
 for ordinal,dimension in enumerate(DIMENSIONS):
  values={population:[row[dimension] for row in rows if row['population']==population and row[dimension] is not None] for population in populations}
  results[dimension]={'summaries':{population:summary(values[population],populations[population]-len(values[population])) for population in populations},'PRESERVED_vs_MISSED':compare(values['PRESERVED'],values['MISSED'],20260901+ordinal),'PRESERVED_vs_NEGATIVE':compare(values['PRESERVED'],values['NEGATIVE'],20261901+ordinal),'MISSED_vs_NEGATIVE':compare(values['MISSED'],values['NEGATIVE'],20262901+ordinal)}
 availability_ok=all(results[dimension]['summaries'][population]['n_available']/populations[population]>=.80 for dimension in DIMENSIONS for population in ('PRESERVED','MISSED'))
 deltas=[results[dimension]['PRESERVED_vs_MISSED']['cliff_delta'] for dimension in DIMENSIONS]
 if not availability_ok:classification='INDETERMINATE'
 elif all(value>=.147 for value in deltas):classification='INDEPENDENT_HARMONIC_STRUCTURE_REPLICATION_SUPPORTED'
 elif sum(value>0 for value in deltas)>=3 and sum(value>=.147 for value in deltas)>=2:classification='INDEPENDENT_HARMONIC_STRUCTURE_REPLICATION_PARTIAL'
 else:classification='INDEPENDENT_HARMONIC_STRUCTURE_REPLICATION_NOT_SUPPORTED'
 result={'protocol_id':P['protocol_id'],'protocol_fingerprint':P['protocol_fingerprint'],'evidence_authority':authority,'ground_truth_authority':{'BassDI_sha256':'990f69207ca891e4691a37277f6675a5fcafb86d0777ce9e2ed77685c350a1f0','original_observations_sha256':sha(HERE/'original_bass_observations.json'),'separated_observations_sha256':sha(HERE/'separated_bass_observations_1.json'),'correspondence_method_sha256':sha(SCORER)},'correspondence':assignment,'negative_fingerprint':negative_fingerprint,'populations':populations,'dimensions':results,'decision_deltas':dict(zip(DIMENSIONS,deltas)),'availability_gate':availability_ok,'classification':classification,'threshold_fitted':False,'composite_score':False,'jga_modified':False,'rows':rows}
 result['evaluation_fingerprint']=hashlib.sha256(canonical(result)).hexdigest();Path(destination).write_bytes(canonical(result));print(json.dumps({'classification':classification,'deltas':result['decision_deltas'],'fingerprint':result['evaluation_fingerprint']}))
if __name__=='__main__':main(sys.argv[1])
