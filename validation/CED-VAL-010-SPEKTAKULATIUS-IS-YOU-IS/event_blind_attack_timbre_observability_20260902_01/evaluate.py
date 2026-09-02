#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path
import numpy as np
from scipy.stats import mannwhitneyu

HERE=Path(__file__).resolve().parent; P=json.loads((HERE/'protocol.json').read_text())
DIMS=list(P['continuous_representation']['dimensions']); POPS=['PRESERVED','MISSED','NEGATIVE']
COMPS=[('MISSED','PRESERVED'),('MISSED','NEGATIVE'),('PRESERVED','NEGATIVE')]
def cb(x): return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def delta(a,b): return float(2*mannwhitneyu(a,b,alternative='two-sided',method='asymptotic').statistic/(len(a)*len(b))-1)
def main():
 a=argparse.ArgumentParser(); a.add_argument('--authority',type=Path,required=True); a.add_argument('--nodes',type=Path,required=True); a.add_argument('--rows',type=Path,required=True); a.add_argument('--result',type=Path,required=True); args=a.parse_args()
 assert sha(args.authority)==P['outcome_authority']['sha256']; outcome=json.loads(args.authority.read_text()); evidence=json.loads(args.nodes.read_text())
 starts=np.array([n['anchor_start_sample'] for n in evidence['nodes']],dtype=np.int64); rows=[]; radius=.050*44100
 for source in outcome['rows']:
  center=source['timestamp']*44100; ids=np.flatnonzero((starts>=center-radius)&(starts<=center+radius)); row={'id':source['id'],'population':source['population'],'timestamp':source['timestamp']}
  for dim in DIMS:
   valid=[i for i in ids if evidence['nodes'][i]['available'] and evidence['nodes'][i][dim] is not None]
   if valid:
    chosen=min(valid,key=lambda i:(evidence['nodes'][i][dim],starts[i])); row[dim]=evidence['nodes'][chosen][dim]; row[dim+'_anchor_start_sample']=int(starts[chosen]); row[dim+'_unavailable_reason']=None
   else: row[dim]=None; row[dim+'_anchor_start_sample']=None; row[dim+'_unavailable_reason']='NO_AVAILABLE_CONTINUOUS_NODE_IN_FROZEN_WINDOW'
  rows.append(row)
 rowdoc={'protocol_id':P['protocol_id'],'protocol_fingerprint':P['protocol_fingerprint'],'pre_gt_evidence_fingerprint':evidence['evidence_fingerprint'],'outcome_authority_sha256':sha(args.authority),'rows':rows}; rowdoc['rows_fingerprint']=hashlib.sha256(cb(rowdoc)).hexdigest(); args.rows.parent.mkdir(parents=True,exist_ok=True); args.rows.write_bytes(cb(rowdoc))
 summary={}
 for di,dim in enumerate(DIMS):
  values={p:np.array([r[dim] for r in rows if r['population']==p and r[dim] is not None],dtype=float) for p in POPS}; dist={}
  for p in POPS:
   v=values[p]; q=np.quantile(v,[.25,.5,.75],method='linear') if len(v) else [None]*3; dist[p]={'available':len(v),'unavailable':sum(r['population']==p for r in rows)-len(v),'q1_linear':q[0],'median':q[1],'q3_linear':q[2]}
  comparisons={}
  for ci,(first,second) in enumerate(COMPS):
   x,y=values[first],values[second]; d=delta(x,y); rng=np.random.Generator(np.random.PCG64(20260902+di*3+ci)); boot=np.array([delta(x[rng.integers(0,len(x),len(x))],y[rng.integers(0,len(y),len(y))]) for _ in range(2000)]); test=mannwhitneyu(x,y,alternative='two-sided',method='asymptotic')
   comparisons[first+'_minus_'+second]={'cliffs_delta':d,'rank_auc':(d+1)/2,'cliffs_delta_bootstrap_95_ci':[float(np.quantile(boot,.025)),float(np.quantile(boot,.975))],'mann_whitney_u':float(test.statistic),'mann_whitney_two_sided_p':float(test.pvalue)}
  summary[dim]={'distributions':dist,'comparisons':comparisons}
 counts={p:sum(r['population']==p for r in rows) for p in POPS}; invariant=any(summary[d]['distributions'][p]['available']<.8*counts[p] for d in DIMS for p in ('PRESERVED','MISSED'))
 qualifying=[]; weak=[]; positive=[]
 for dim in DIMS:
  x=summary[dim]['comparisons']['MISSED_minus_NEGATIVE']; lo,hi=x['cliffs_delta_bootstrap_95_ci'];
  if x['cliffs_delta']<=-.147 and hi<0: qualifying.append(dim)
  if abs(x['cliffs_delta'])<.147 or lo<=0<=hi: weak.append(dim)
  if x['cliffs_delta']>0: positive.append(dim)
 if invariant: classification='INDETERMINATE'
 elif len(qualifying)>=3 and not positive: classification='EVENT_BLIND_TIMBRAL_EVIDENCE_SUPPORTED'
 elif len(qualifying) in (1,2): classification='EVENT_BLIND_TIMBRAL_EVIDENCE_PARTIAL'
 elif not qualifying and len(weak)>=3: classification='SOURCE_ATTRIBUTION_INDETERMINATE'
 else: classification='EVENT_BLIND_TIMBRAL_EVIDENCE_NOT_SUPPORTED'
 result={'protocol_id':P['protocol_id'],'protocol_fingerprint':P['protocol_fingerprint'],'pre_gt_commit':'2089815f912d7b69c0eaa709df54bc8938bdce85','pre_gt_evidence_fingerprint':evidence['evidence_fingerprint'],'outcome_authority_sha256':sha(args.authority),'population_counts':counts,'dimensions':summary,'decision_diagnostics':{'qualifying_missed_vs_negative':qualifying,'weak_or_indistinct_missed_vs_negative':weak,'positive_missed_vs_negative':positive},'classification':classification,'threshold_fitted':False,'composite_score':False,'classifier':False}
 result['evaluation_fingerprint']=hashlib.sha256(cb(result)).hexdigest(); args.result.write_bytes(cb(result))
if __name__=='__main__': main()
