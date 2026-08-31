#!/usr/bin/env python3
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
from pitch_core import canonical,sha,load_resampled,reference_event
HERE=Path(__file__).parent
def wilson(k,n,z=1.959963984540054):
 if not n:return None
 p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return [c-h,c+h]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--candidates',type=Path,required=True);ap.add_argument('--candidate-sha',required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert sha(a.candidates)==a.candidate_sha
 p=json.load(open(HERE/'protocol.json'));q=dict(p);fp=q.pop('protocol_fingerprint');assert hashlib.sha256(canonical(q)).hexdigest()==fp;auth=p['authorities_locked_until_candidate_commit'];assert sha(auth['correspondence']['path'])==auth['correspondence']['sha256'];assert sha(auth['original_bass_audio']['path'])==auth['original_bass_audio']['sha256']
 cand=json.load(open(a.candidates));score=json.load(open(auth['correspondence']['path']))['runs']['run_1']['Double Bass']['level_2']; originals=[]
 for recovered,key in ((True,'matches'),(False,'original_only')):
  for x in score[key]:
   t=x['original_time'];originals.append({'original_id':x['original_eme_id'],'timestamp_seconds':t['numerator']/t['denominator'],'baseline_status':'RECOVERED_BASS' if recovered else 'MISSED_BASS'})
 originals.sort(key=lambda x:(x['timestamp_seconds'],x['original_id']));edges=[]
 for ci,c in enumerate(cand['candidates']):
  for oi,o in enumerate(originals):
   d=abs(c['timestamp_seconds']-o['timestamp_seconds'])
   if d<=.05:edges.append((d,c['timestamp_seconds'],o['timestamp_seconds'],c['candidate_id'],o['original_id'],ci,oi))
 usedc=set();usedo=set();matches=[]
 for d,ct,ot,cid,oid,ci,oi in sorted(edges):
  if ci in usedc or oi in usedo:continue
  usedc.add(ci);usedo.add(oi);matches.append({'candidate_index':ci,'original_index':oi,'absolute_displacement_seconds':d,'signed_displacement_seconds':ct-ot})
 bass=load_resampled(auth['original_bass_audio']['path']);pitch_errors=[];miss_pitch=[]
 for m in matches:
  c=cand['candidates'][m['candidate_index']];o=originals[m['original_index']];ref=reference_event(bass,o['timestamp_seconds']);errs=[]
  if ref['status']=='PITCHED_EVIDENCE_PRESENT':
   for x in c['f0_candidates']:
    for y in ref['candidates']:errs.append(abs(1200*math.log2(x['f0_hz']/y['f0_hz'])))
  err=min(errs) if errs else None;m.update({'candidate_id':c['candidate_id'],'original_id':o['original_id'],'baseline_status':o['baseline_status'],'candidate_timestamp_seconds':c['timestamp_seconds'],'original_timestamp_seconds':o['timestamp_seconds'],'pitch_reference':ref,'pitch_error_cents':err,'pitch_compatible':bool(err is not None and err<=50)});pitch_errors.append(err)
  if o['baseline_status']=='MISSED_BASS':miss_pitch.append(m)
 ncan=len(cand['candidates']);nmatch=len(matches);new=sum(m['baseline_status']=='MISSED_BASS' for m in matches);old=nmatch-new;unmatched=ncan-nmatch;precision=nmatch/ncan if ncan else 0;missrec=new/356;incr=new/1138;combined=(782+new)/1138;allrec=nmatch/1138;f1=2*precision*allrec/(precision+allrec) if precision+allrec else 0;disp=[m['absolute_displacement_seconds'] for m in matches]
 pe=[m for m in miss_pitch if m['pitch_error_cents'] is not None];pc=sum(m['pitch_compatible'] for m in pe);peprop=len(pe)/new if new else None;pcprop=pc/len(pe) if pe else None;ratio=unmatched/new if new else None
 invariants=True
 if new and peprop<.5:cls='INDETERMINATE'
 else:
  useful=new/356>=.15 and precision>=.30 and ratio<=2 and np.median(disp)<=.025 and pcprop>=.50
  partial=new/356>=.05 and precision>=.15 and ratio<=5 and np.median(disp)<=.040 and pcprop>=.25
  cls='USEFUL' if useful else ('PARTIAL' if partial else 'INSUFFICIENT')
 summary={'original_bass':1138,'baseline_recovered':782,'baseline_missed':356,'scanner_candidates':ncan,'matched_any':nmatch,'matched_baseline_recovered':old,'newly_recovered_missed_bass':new,'unmatched_candidates':unmatched,'candidate_precision':precision,'candidate_precision_wilson_95':wilson(nmatch,ncan),'missed_population_recall':missrec,'missed_recall_wilson_95':wilson(new,356),'incremental_all_original_recall':incr,'retrospective_combined_recall':combined,'scanner_all_original_recall':allrec,'scanner_f1_any_original':f1,'unmatched_per_newly_recovered':ratio,'timing':{'median_abs_seconds':float(np.median(disp)) if disp else None,'q1_abs_seconds':float(np.quantile(disp,.25)) if disp else None,'q3_abs_seconds':float(np.quantile(disp,.75)) if disp else None,'rmse_seconds':math.sqrt(sum(x*x for x in disp)/len(disp)) if disp else None,'maximum_abs_seconds':max(disp) if disp else None},'missed_match_pitch':{'temporally_matched':new,'evaluable':len(pe),'evaluable_proportion':peprop,'compatible':pc,'compatible_proportion':pcprop,'wilson_95':wilson(pc,len(pe))}}
 out={'protocol_id':p['protocol_id'],'protocol_fingerprint':fp,'candidate_stream_sha256':a.candidate_sha,'candidate_fingerprint':cand['candidate_fingerprint'],'matches':matches,'summary':summary,'classification':'EVENT_BLIND_PITCHED_BASS_RECOVERY: '+cls,'interpretation_firewall':p['scientific_firewall']};out['result_fingerprint']=hashlib.sha256(canonical(out)).hexdigest();a.output.write_bytes(canonical(out)+b'\n');print(out['result_fingerprint'],out['classification'])
if __name__=='__main__':main()
