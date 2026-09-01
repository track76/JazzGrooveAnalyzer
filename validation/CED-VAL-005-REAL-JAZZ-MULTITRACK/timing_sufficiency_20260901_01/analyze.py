import hashlib,json,math,platform,sys
from pathlib import Path
import numpy as np
from scipy.stats import wasserstein_distance,ks_2samp

ROOT=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer')
BASE=ROOT/'validation/CED-VAL-005-REAL-JAZZ-MULTITRACK'
HERE=Path(__file__).parent
P=json.loads((HERE/'protocol.json').read_text())
FILES={
 'original_eme':BASE/'run_20260824_112305/elementary_metric_events.json',
 'original_localizations':BASE/'run_20260824_112305/drum_relative_localizations.json',
 'original_profile':BASE/'run_20260824_112305/rhythm_section_timing_profile.json',
 'separated_jga':BASE/'htdemucsft_replication_20260831_01/jga_run_1.json',
 'correspondence':BASE/'htdemucsft_replication_20260831_01/scoring_1.json'}
EXPECTED={k:P['authorities'][k+'_sha256'] for k in FILES}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=lambda v:v.item() if isinstance(v,np.generic) else TypeError(type(v).__name__)).encode()+b'\n'
def desc(a):
 a=np.asarray(a,float); q=np.quantile(a,[.25,.5,.75]); med=q[1]
 return {'n':len(a),'minimum':float(a.min()),'q1':float(q[0]),'median':float(med),'q3':float(q[2]),'maximum':float(a.max()),'iqr':float(q[2]-q[0]),'mad':float(np.median(np.abs(a-med))),'mean':float(a.mean())}
def direction(a):
 a=np.asarray(a); n=len(a); return {'negative':int((a<0).sum()),'zero':int((a==0).sum()),'positive':int((a>0).sum()),'negative_fraction':float((a<0).sum()/n),'zero_fraction':float((a==0).sum()/n),'positive_fraction':float((a>0).sum()/n)}
def comp(ref,test):
 r=np.asarray(ref); t=np.asarray(test); dr=desc(r);dt=desc(t)
 return {'reference':dr,'test':dt,'absolute_reference':desc(abs(r)),'absolute_test':desc(abs(t)),
 'median_shift_abs':abs(dt['median']-dr['median']),'q1_shift_abs':abs(dt['q1']-dr['q1']),'q3_shift_abs':abs(dt['q3']-dr['q3']),
 'iqr_relative_change_abs':abs(dt['iqr']-dr['iqr'])/dr['iqr'] if dr['iqr'] else None,
 'wasserstein_1_seconds':float(wasserstein_distance(r,t)),'ks_statistic':float(ks_2samp(r,t).statistic),
 'direction_reference':direction(r),'direction_test':direction(t),'directional_balance_difference':abs(direction(t)['positive_fraction']-direction(r)['positive_fraction'])}
def main(out):
 observed={k:sha(v) for k,v in FILES.items()}; assert observed==EXPECTED
 orig_l=json.loads(FILES['original_localizations'].read_text()); sep=json.loads(FILES['separated_jga'].read_text()); score=json.loads(FILES['correspondence'].read_text())
 sep_l=sep['drum_relative_localizations']; matches=score['runs']['run_1']['Double Bass']['level_2']['matches']
 om={x['target_eme_id']:x for x in orig_l}; preserved_ids={x['original_eme_id'] for x in matches}; missed_ids=set(om)-preserved_ids
 assert (len(orig_l),len(sep_l),len(preserved_ids),len(missed_ids))==(1138,825,782,356)
 def vals(xs): return np.array([x['nearest_signed_displacement_seconds'] for x in xs],float)
 def times(xs): return np.array([x['target_timestamp_seconds'] for x in xs],float)
 ov,sv=vals(orig_l),vals(sep_l); pres=[om[k] for k in sorted(preserved_ids)]; miss=[om[k] for k in sorted(missed_ids)]
 duration=228.30095238095238; edges=np.linspace(0,duration,11)
 def bix(t): return np.minimum(np.searchsorted(edges,t,side='right')-1,9)
 oi,si=bix(times(orig_l)),bix(times(sep_l)); pi=bix(times(pres))
 coverage=[]; local=[]
 for i in range(10):
  on=int((oi==i).sum()); sn=int((si==i).sum()); pn=int((pi==i).sum()); ret=pn/on
  coverage.append({'bin':i+1,'start_s':float(edges[i]),'end_s':float(edges[i+1]),'original':on,'separated':sn,'preserved_original':pn,'separated_density_ratio':sn/on,'preserved_retention':ret})
  local.append({'bin':i+1,**comp(ov[oi==i],sv[si==i])})
 global_c=comp(ov,sv); missing_c=comp(vals(pres),vals(miss))
 g=P['global_gate']; global_pass=(global_c['median_shift_abs']<=g['median_shift_max_s'] and global_c['q1_shift_abs']<=g['q1_q3_shift_max_s'] and global_c['q3_shift_abs']<=g['q1_q3_shift_max_s'] and global_c['wasserstein_1_seconds']<=g['wasserstein_max_s'] and global_c['iqr_relative_change_abs']<=g['iqr_relative_change_max'] and global_c['directional_balance_difference']<=g['directional_balance_difference_max'])
 local_pass=[x['median_shift_abs']<=.023219954648526078 and x['wasserstein_1_seconds']<=.023219954648526078 and x['directional_balance_difference']<=.15 for x in local]
 severe=[x['median_shift_abs']>.046439909297052155 or x['wasserstein_1_seconds']>.046439909297052155 for x in local]
 rets=np.array([x['preserved_retention'] for x in coverage]); density_ok=sum(.4<=x['separated_density_ratio']<=1.25 for x in coverage)
 coverage_pass=(sum(x['separated']==0 for x in coverage)==0 and rets.min()>=.4 and density_ok>=9 and rets.std()/rets.mean()<=.2)
 missing_material=(missing_c['wasserstein_1_seconds']>.023219954648526078 or missing_c['median_shift_abs']>.023219954648526078 or missing_c['directional_balance_difference']>.15 or missing_c['ks_statistic']>.20)
 rng=np.random.Generator(np.random.PCG64(20260901)); metrics=[]
 for _ in range(1000):
  s=ov[rng.choice(len(ov),782,replace=False)]; c=comp(ov,s); metrics.append([c['wasserstein_1_seconds'],c['median_shift_abs'],c['iqr_relative_change_abs'],c['directional_balance_difference']])
 arr=np.array(metrics); qs={str(q):[float(x) for x in np.quantile(arr,q,axis=0)] for q in (.5,.95,.99)}
 def vector(c):return [c['wasserstein_1_seconds'],c['median_shift_abs'],c['iqr_relative_change_abs'],c['directional_balance_difference']]
 pc=comp(ov,vals(pres)); actual={'preserved_original':vector(pc),'end_to_end_separated':vector(global_c)}
 exceed95={k:[v[i]>qs['0.95'][i] for i in range(4)] for k,v in actual.items()}; exceed99={k:[v[i]>qs['0.99'][i] for i in range(4)] for k,v in actual.items()}
 sufficient=global_pass and coverage_pass and sum(local_pass)>=8 and not any(severe) and not missing_material and not any(any(v) for v in exceed95.values())
 partial=global_pass and not any(x['separated']==0 for x in coverage) and rets.min()>=.25 and sum(local_pass)>=6 and sum(severe)<=2 and all(sum(v)<=1 for v in exceed99.values())
 classification='SUFFICIENT' if sufficient else ('PARTIALLY_SUFFICIENT' if partial else 'INSUFFICIENT')
 result={'protocol_id':P['protocol_id'],'protocol_fingerprint':P['protocol_fingerprint'],'authority_sha256_verified':observed,'populations':{'original_bass':1138,'original_drums':907,'separated_bass':825,'preserved_original_bass':782,'missed_original_bass':356,'separated_drums':len(sep['elementary_metric_events']['Drums'])},'global_profile':global_c,'temporal_coverage':{'duration_s':duration,'bins':coverage,'empty_separated_bins':sum(x['separated']==0 for x in coverage),'minimum_preserved_retention':float(rets.min()),'retention_cv':float(rets.std()/rets.mean()),'density_ratio_in_range_bins':density_ok},'local_profile':{'bins':local,'passing_bins':sum(local_pass),'severe_bins':sum(severe)},'missingness_bias':{'comparison':missing_c,'material':missing_material},'subsampling':{'seed':20260901,'iterations':1000,'subset_size':782,'metric_order':['wasserstein_1_seconds','median_shift_abs','iqr_relative_change_abs','directional_balance_difference'],'quantiles':qs,'actual':actual,'exceeds_p95':exceed95,'exceeds_p99':exceed99},'gates':{'global':global_pass,'coverage':coverage_pass,'local_pass_count':sum(local_pass),'local_severe_count':sum(severe),'missingness_not_material':not missing_material,'sufficient':sufficient,'partially_sufficient':partial},'classification':classification,'environment':{'python':sys.version.split()[0],'numpy':np.__version__,'platform':platform.platform()},'limitations':P['firewall']}
 fp=hashlib.sha256(canon(result)).hexdigest(); result['result_fingerprint']=fp; Path(out).write_bytes(canon(result)); print(json.dumps({'classification':classification,'fingerprint':fp,'sha256':sha(Path(out))}))
if __name__=='__main__': main(sys.argv[1])
