#!/usr/bin/env python3
import argparse,hashlib,json,math
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.stats import fisher_exact,norm
HERE=Path(__file__).parent
P5=Path('/private/tmp/cedval005-htdemucsft-replication-20260831-01/scoring_1.json')
P6=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer/validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/bass_preservation_phase2_20260825_01/scoring_execution_1.json')
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()
def wilson(k,n,z=1.959963984540054):
 p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return [c-h,c+h]
def summary(k,n):return {'recovered':k,'missed':n-k,'total':n,'preservation_probability':k/n,'wilson_95':wilson(k,n)}
def effect(a,b,c,d):
 # rows with/without; columns recovered/missed
 p1=a/(a+b);p0=c/(c+d);w1=wilson(a,a+b);w0=wilson(c,c+d);rd=p1-p0
 rdci=[rd-math.sqrt((p1-w1[0])**2+(w0[1]-p0)**2),rd+math.sqrt((w1[1]-p1)**2+(p0-w0[0])**2)]
 rr=p1/p0;se_rr=math.sqrt(1/a-1/(a+b)+1/c-1/(c+d));orx=a*d/(b*c);se_or=math.sqrt(1/a+1/b+1/c+1/d)
 odds,p=fisher_exact([[a,b],[c,d]],alternative='two-sided');phi=(a*d-b*c)/math.sqrt((a+b)*(c+d)*(a+c)*(b+d))
 return {'absolute_risk_difference':rd,'newcombe_95':rdci,'relative_risk':rr,'relative_preservation_difference_percent':(rr-1)*100,'relative_risk_log_wald_95':[math.exp(math.log(rr)-1.959963984540054*se_rr),math.exp(math.log(rr)+1.959963984540054*se_rr)],'odds_ratio':orx,'odds_ratio_log_wald_95':[math.exp(math.log(orx)-1.959963984540054*se_or),math.exp(math.log(orx)+1.959963984540054*se_or)],'phi':phi,'fisher_exact_two_sided_p':p,'fisher_odds_ratio':odds}
def mh(tables):
 num=den=0
 for a,b,c,d in tables:
  n=a+b+c+d
  if n:num+=a*d/n;den+=b*c/n
 return num/den if den else None
def logistic(rows):
 X=np.array([[1,r['with_kick'],r['time_norm'],r['local_bass_count'],r['local_kick_count']] for r in rows],float);y=np.array([r['recovered'] for r in rows],float);beta=np.zeros(X.shape[1]);conv=False
 for i in range(100):
  eta=np.clip(X@beta,-30,30);p=1/(1+np.exp(-eta));w=np.maximum(p*(1-p),1e-9);h=X.T@(w[:,None]*X);g=X.T@(y-p);new=beta+np.linalg.pinv(h)@g
  if np.max(np.abs(new-beta))<1e-10:beta=new;conv=True;break
  beta=new
 cov=np.linalg.pinv(h);se=math.sqrt(cov[1,1]);return {'converged':conv,'iterations':i+1,'kick_log_odds_coefficient':beta[1],'adjusted_kick_odds_ratio':math.exp(beta[1]),'wald_95':[math.exp(beta[1]-1.959963984540054*se),math.exp(beta[1]+1.959963984540054*se)],'predictors':['intercept','Kick<=30ms','normalized_time','local_Bass_count_+/-0.5s','local_Kick_count_+/-0.5s']}
def dataset(name,score,kick_path,sr,scope):
 k=json.loads(kick_path.read_text());kt=sorted(Fraction(x['producer_sample_coordinate'],sr) for x in k['events']);lvl=score
 original=[]
 for x in lvl['matches']:original.append((x['original_eme_id'],Fraction(x['original_time']['numerator'],x['original_time']['denominator']),1))
 for x in lvl['original_only']:original.append((x['original_eme_id'],Fraction(x['original_time']['numerator'],x['original_time']['denominator']),0))
 original.sort(key=lambda x:(x[1],x[0]));times=[x[1] for x in original];rows=[]
 for ident,t,rec in original:
  dist=min(abs(t-q) for q in kt);db=sum(abs(t-q)<=Fraction(1,2) for q in times)-1;dk=sum(abs(t-q)<=Fraction(1,2) for q in kt)
  rows.append({'id':ident,'time_seconds':float(t),'nearest_kick_distance_seconds':float(dist),'with_kick':int(dist<=Fraction(3,100)),'recovered':rec,'local_bass_count':db,'local_kick_count':dk,'time_norm':float(t/scope)})
 bands=[('0_10ms',lambda d:d<=.010),('10_30ms',lambda d:.010<d<=.030),('30_60ms',lambda d:.030<d<=.060),('over_60ms',lambda d:d>.060)]
 bandout={n:summary(sum(r['recovered'] for r in z),len(z)) for n,f in bands for z in [[r for r in rows if f(r['nearest_kick_distance_seconds'])]]}
 w=[r for r in rows if r['with_kick']];wo=[r for r in rows if not r['with_kick']];a=sum(r['recovered'] for r in w);c=sum(r['recovered'] for r in wo);eff=effect(a,len(w)-a,c,len(wo)-c)
 temporal=[]
 for q in range(4):
  z=[r for r in rows if min(3,int(r['time_norm']*4))==q];ww=[r for r in z if r['with_kick']];nn=[r for r in z if not r['with_kick']];temporal.append({'quarter':q+1,'with_kick':summary(sum(x['recovered'] for x in ww),len(ww)) if ww else None,'without_kick':summary(sum(x['recovered'] for x in nn),len(nn)) if nn else None,'table':[sum(x['recovered'] for x in ww),sum(not x['recovered'] for x in ww),sum(x['recovered'] for x in nn),sum(not x['recovered'] for x in nn)]})
 edges={key:[float(x) for x in np.quantile([r[key] for r in rows],[.25,.5,.75])] for key in ('local_bass_count','local_kick_count')}
 density=[];tables=[]
 for key in edges:
  for q in range(4):
   z=[r for r in rows if np.searchsorted(edges[key],r[key],side='right')==q];ww=[r for r in z if r['with_kick']];nn=[r for r in z if not r['with_kick']];tab=[sum(x['recovered'] for x in ww),sum(not x['recovered'] for x in ww),sum(x['recovered'] for x in nn),sum(not x['recovered'] for x in nn)];density.append({'density':key,'quartile':q+1,'n':len(z),'table':tab});
   if all(x>0 for x in tab):tables.append(tab)
 return {'dataset':name,'kick_eme_count':len(kt),'bass_count':len(rows),'with_kick':summary(a,len(w)),'without_kick':summary(c,len(wo)),'effect':eff,'proximity_bands':bandout,'temporal_quarters':temporal,'temporal_mantel_haenszel_odds_ratio':mh([x['table'] for x in temporal if all(v>0 for v in x['table'])]),'density_quartile_edges':edges,'density_strata':density,'density_mantel_haenszel_odds_ratio':mh(tables),'adjusted_logistic':logistic(rows)}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();p=json.loads((HERE/'protocol.json').read_text());q=dict(p);fp=q.pop('protocol_fingerprint');assert hashlib.sha256(canon(q)).hexdigest()==fp
 s5=json.loads(P5.read_text())['runs']['run_1']['Double Bass']['level_2'];s6=json.loads(P6.read_text())['runs']['M1_run_1']['level_2']['Double Bass'];d5=dataset('CED-VAL-005',s5,HERE/'ced005_kick_run_1.json',44100,Fraction(10068072,44100));d6=dataset('CED-VAL-006',s6,HERE/'ced006_kick_run_1.json',48000,Fraction(11912868,48000));e=d5['effect'];gate=e['absolute_risk_difference']<=-.10 and e['newcombe_95'][1]<0 and e['fisher_exact_two_sided_p']<.05
 r={'protocol_id':p['protocol_id'],'protocol_fingerprint':fp,'primary':d5,'secondary':d6,'substantial_negative_association_gate':gate,'interpretation':p['interpretation_firewall']};r['result_fingerprint']=hashlib.sha256(canon(r)).hexdigest();a.output.write_bytes(canon(r)+b'\n');print(r['result_fingerprint'],gate)
if __name__=='__main__':main()
