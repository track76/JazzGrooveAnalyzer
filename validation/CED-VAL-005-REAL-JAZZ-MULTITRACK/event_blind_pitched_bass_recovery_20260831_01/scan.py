#!/usr/bin/env python3
import argparse,hashlib
from pathlib import Path
from pitch_core import *
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--mix',type=Path,required=True);ap.add_argument('--expected-sha',required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert sha(a.mix)==a.expected_sha
 audio=load_resampled(a.mix); frames=[]
 for pos in range(0,len(audio)-FRAME+1,HOP):frames.append(frame_analysis(audio,pos,True))
 eligible=[f for f in frames if f['eligible']]; clusters=[]; cur=[]
 for f in eligible:
  if cur and (f['frame_index']-cur[-1]['frame_index']>3 or abs(1200*math.log2(f['best_f0_hz']/cur[-1]['best_f0_hz']))>70):clusters.append(cur);cur=[]
  cur.append(f)
 if cur:clusters.append(cur)
 raw=[]
 for z in clusters:
  stable_at=None
  for i in range(len(z)-2):
   q=z[i:i+3]
   if q[2]['frame_index']-q[0]['frame_index']==2 and 1200*math.log2(max(x['best_f0_hz'] for x in q)/min(x['best_f0_hz'] for x in q))<=35:stable_at=i;break
  if stable_at is None:continue
  cs=candidate_set(z); first=z[stable_at]; last=z[-1]; raw.append({'pitched_evidence_status':'PITCHED_EVIDENCE_PRESENT','timestamp_seconds':first['start_seconds'],'timestamp_sample_coordinate':first['frame_index']*HOP,'duration_seconds':last['start_seconds']+FRAME/SR-first['start_seconds'],'eligible_frame_count':len(z),'span_frame_count':last['frame_index']-first['frame_index']+1,'mean_harmonic_energy_ratio':float(np.mean([x['harmonic_energy_ratio'] for x in z])),'median_supported_partials':float(np.median([x['supported_partials'] for x in z])),'aggregate_best_score':cs[0]['aggregate_score'],'f0_candidates':cs})
 raw.sort(key=lambda x:x['timestamp_seconds']); kept=[]
 for x in raw:
  if kept and x['timestamp_seconds']-kept[-1]['timestamp_seconds']<.12:
   rank=lambda q:(q['eligible_frame_count'],q['aggregate_best_score'],-q['timestamp_seconds'])
   if rank(x)>rank(kept[-1]):kept[-1]=x
  else:kept.append(x)
 for i,x in enumerate(kept):x['candidate_id']=f'C{i:06d}'
 status={s:sum((f['eligible'] if s=='ELIGIBLE' else not f['eligible']) for f in frames) for s in ('ELIGIBLE','INELIGIBLE')}
 for f in frames:f.pop('_scores',None)
 out={'protocol_id':'H-CEDVAL005-EVENT-BLIND-CONTINUOUS-PITCHED-BASS-RECOVERY-01','stage':'EVENT_BLIND_MIX_ONLY','ground_truth_accessed':False,'input_sha256':a.expected_sha,'analysis_sample_rate_hz':SR,'scan_frame_count':len(frames),'scan_status_counts':status,'candidate_count':len(kept),'candidates':kept};out['candidate_fingerprint']=hashlib.sha256(canonical(out)).hexdigest();a.output.write_bytes(canonical(out)+b'\n');print(out['candidate_fingerprint'],len(kept))
if __name__=='__main__':main()
