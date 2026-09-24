from pathlib import Path
import json,hashlib,datetime,csv
import numpy as np,soundfile as sf
from morphology import extract,NAMES
FEATURES=NAMES+['BP_signed_distance_ms','BP_absolute_distance_ms','BP_relative_activity_position']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def check_isolation(W):
 paths=[W.parent/'EVALUATION_MAP.json',W.parent.parent/'JGA_GALLEGATI_CONTINUOUS_FISHMAN_GT_120_20260924/GROUND_TRUTH/GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1.json',W.parent.parent/'JGA_NATIVE_BP_GT_120_20260924/EVENT_RESULTS.json']
 checks=[]
 for p in paths:
  try:p.read_bytes();raise RuntimeError('Isolation failed '+str(p))
  except PermissionError:checks.append({'path':str(p),'read_denied':True})
 save(W/'output/ISOLATION_CHECKS.json',checks)
def generate(W):
 records=[]
 for m in json.loads((W/'input/MANIFEST.json').read_text()):
  p=W/'input'/m['audio'];assert sha(p)==m['sha256'];x,sr=sf.read(p);x=x.mean(axis=1) if x.ndim>1 else x;assert sr==44100
  notes=json.loads((W/'input'/m['notes']).read_text())
  for n in notes:
   bp=n['onset_local_s'];lo=max(0,bp-.15);hi=min(len(x)/sr,bp+.15);start=max(0,int((lo-.15)*sr)//44*44);end=min(len(x),int((hi+.15)*sr));z=extract(x[start:end],sr);times=z['candidate_times']+start/sr;eligible=np.flatnonzero((times>=lo)&(times<=hi));cand=[]
   for k in eligible:
    t=float(times[k]);dist=(t-bp)*1000;feat=z['X'][k].tolist()+[dist,abs(dist),(t-bp)/max(n['duration_s'],1e-9)]
    cand.append({'candidate_id':f"{n['native_note_id']}_F{round(t*sr)}",'time_s':t,'flux':float(z['flux'][z['candidate_frames'][k]]),'features':feat})
   records.append({'clip_id':m['clip_id'],'BP':n,'search_start_s':lo,'search_end_s':hi,'candidates':cand})
  print('LOCAL WINDOWS',m['clip_id'],len(notes),flush=True)
 save(W/'output/BLIND_CANDIDATES.json',records);save(W/'output/CANDIDATE_HASH.json',{'sha256':sha(W/'output/BLIND_CANDIDATES.json'),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});return records

def associate(records,gt,durations):
 out=[]
 for clip in sorted({g['clip_id'] for g in gt}):
  gs=sorted([g for g in gt if g['clip_id']==clip],key=lambda g:float(g['final_center_s']));rs=[r for r in records if r['clip_id']==clip]
  for i,g in enumerate(gs):
   t=float(g['final_center_s']);lo=(float(gs[i-1]['final_center_s'])+t)/2 if i else 0;hi=(float(gs[i+1]['final_center_s'])+t)/2 if i+1<len(gs) else durations[clip];pitch=g['midi_pitch'];cand=[r for r in rs if lo<=r['BP']['onset_local_s']<hi and r['BP']['offset_local_s']>=float(g['final_earliest_s'])];exact=[r for r in cand if r['BP']['midi_pitch']==pitch];octave=[r for r in cand if r['BP']['midi_pitch']!=pitch and (r['BP']['midi_pitch']-pitch)%12==0];tier=exact or octave or cand
   status='MISSED' if not tier else 'MULTIPLE_BP_CANDIDATES' if len(tier)>1 else 'CORRECT_PITCH_MATCH' if exact else 'OCTAVE_EQUIVALENT' if octave else 'WRONG_PITCH'
   out.append({'GT':g,'association':status,'record':tier[0] if len(tier)==1 and status!='WRONG_PITCH' else None,'associated_BP_ids':[r['BP']['native_note_id'] for r in tier]})
 return out

def decide(record,model,threshold):
 c=record['candidates']
 if not c:return {'status':'NO_CANDIDATE','selected_s':None,'probabilities':[]}
 p=model.predict_proba(np.array([a['features'] for a in c]))[:,1];order=np.argsort(-p,kind='stable');top=order[0];tie=len(order)>1 and abs(p[top]-p[order[1]])<=1e-12
 status='ABSTAIN_AMBIGUOUS' if p[top]<threshold or tie else 'ATTACK_SELECTED'
 return {'status':status,'selected_s':c[top]['time_s'] if status=='ATTACK_SELECTED' else None,'selected_id':c[top]['candidate_id'] if status=='ATTACK_SELECTED' else None,'probabilities':p.tolist()}

def metrics(err,total):
 a=np.asarray(err);ab=abs(a);n=len(a)
 if not n:return {'N':0,'total':total,'coverage_pct':0,'useful_yield_10_pct':0}
 return {'N':n,'total':total,'coverage_pct':100*n/total,'median_signed_ms':float(np.median(a)),'mean_signed_ms':float(np.mean(a)),'median_absolute_ms':float(np.median(ab)),'IQR_signed_ms':float(np.percentile(a,75)-np.percentile(a,25)),'P95_absolute_ms':float(np.percentile(ab,95)),'maximum_absolute_ms':float(max(ab)),**{f'within_{k}_pct':float(100*np.mean(ab<=k)) for k in [5,10,20,30]},'useful_yield_10_pct':float(100*np.sum(ab<=10)/total)}
