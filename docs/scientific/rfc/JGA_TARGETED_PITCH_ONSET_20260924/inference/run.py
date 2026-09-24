from pathlib import Path
import json,csv,hashlib,datetime
import numpy as np,soundfile as sf
from scipy.signal import fftconvolve
W=Path(__file__).resolve().parent;I=W/'input';O=W/'output';sr=44100;hop=44
load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
checks=[]
for p in ['/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/scientific/rfc/JGA_V1_OPERATIONAL_PLP_QUARTER_NEAREST_001_20260922/PLP_REFERENCE.csv','/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/scientific/rfc/JGA_BASS_V1_HISTORICAL_TRANSFER_20260924/inference/output/EPISODE_DECISIONS.json']:
 try:open(p).read(1);raise RuntimeError('prohibited input readable')
 except PermissionError:checks.append({'path':p,'read_denied':True})
save(O/'ISOLATION_CHECKS.json',checks)
E=load(I/'EPISODES.json');M={r['note_id']:json.loads(r['native_hypothesis']) for r in csv.DictReader(open(I/'MEMBERSHIP.csv'))};x,s=sf.read(I/'FULLMIX.wav');assert s==sr;x=x.mean(axis=1)
def observe(y,t,f0,wide):
 baseline=float(np.percentile(y,10));peak=float(y.max());low=baseline+.2*(peak-baseline);high=baseline+.6*(peak-baseline);relative=float(np.median(y)/(4*np.median(wide)+1e-20));dynamic=peak/(baseline+1e-20)
 candidates=[];incomplete=False
 if peak<1e-8 or relative<.01:status='TARGET_NOT_OBSERVABLE'
 elif dynamic<4:status='TARGET_ACTIVITY_CONTINUOUS'
 else:
  armed=False;pending=None;count=0;latched=False;hold=int(np.ceil(sr/(f0*hop)))
  for j,v in enumerate(y):
   if v<=low:armed=True;pending=None;count=0;latched=False;continue
   if not armed:continue
   if pending is None:pending=j
   if latched:continue
   count=count+1 if v>=high else 0
   if count>=hold:candidates.append(float(t[pending]));latched=True;armed=False;pending=None
  incomplete=pending is not None
  if len(candidates)>1:status='TARGET_ONSET_MULTIPLE'
  elif incomplete:status='TARGET_ONSET_UNRESOLVED'
  elif len(candidates)==1:status='TARGET_ONSET_CLEAR'
  elif y[0]>low:status='TARGET_ACTIVITY_CONTINUOUS'
  else:status='TARGET_ONSET_UNRESOLVED'
 return {'status':status,'candidate_s':candidates,'baseline':baseline,'peak':peak,'low':low,'high':high,'relative_power_proxy':relative,'dynamic_ratio':float(dynamic),'incomplete_rise':incomplete}
def trace(on,f0):
 a=on-.15;b=on+.15;N=2*round(2*sr/f0)+1;w=np.hanning(N);w=w/w.sum();margin=N+44;start=max(0,int(a*sr)-margin);end=min(len(x),int(b*sr)+margin+1);seg=x[start:end];local=np.arange(len(seg))/sr
 frames=np.arange(int(np.ceil(a*sr/hop))*hop,int(np.floor(b*sr/hop))*hop+1,hop);inds=frames-start;t=frames/sr
 channels=[]
 for cents in [-35,0,35]:
  freq=f0*2**(cents/1200);c=fftconvolve(seg*np.exp(-2j*np.pi*freq*local),w,mode='same');channels.append(4*abs(c[inds])**2)
 energy=np.max(channels,axis=0);wide=fftconvolve(seg**2,w,mode='same')[inds];info=observe(energy,t,f0,wide)
 info.update({'f0':f0,'kernel_samples':N,'support_ms':N/sr*1000,'ENBW_hz':float(sr*(w*w).sum()),'tuning_low_hz':f0*2**(-35/1200),'tuning_high_hz':f0*2**(35/1200),'approx_first_null_halfwidth_hz':2*sr/(N-1)})
 return t,energy,wide,info
# Implementation controls only; no parameter fitting or historical outcome optimization.
test_t=np.arange(300)*hop/sr
assert observe(np.zeros(300),test_t,100,np.ones(300))['status']=='TARGET_NOT_OBSERVABLE'
assert observe(np.ones(300),test_t,100,np.ones(300))['status']=='TARGET_ACTIVITY_CONTINUOUS'
a=np.zeros(300);a[100:]=1;assert observe(a,test_t,100,np.ones(300))['candidate_s']==[float(test_t[100])]
save(O/'IMPLEMENTATION_CHECKS.json',{'zero_energy_not_observable':True,'constant_energy_continuous':True,'known_energy_step_preserves_grid_crossing':True,'scope':'state logic checks only, not physical onset validation'})
rows=[];traces={};targets=[]
for e in E:
 targets.append({'episode_id':e['episode_id'],'frozen_fundamental_midi':e['fundamental_midi'],'ambiguity':e['ambiguity'],'exact_members':[M[k] for k in e['member_ids']]})
 for bid in e['member_ids']:
  native=M[bid];on=float(native['onset_s']);pitches=sorted(set([int(native['midi_pitch']),int(e['fundamental_midi'])]))
  for pitch in pitches:
   key=f'{e["episode_id"]}_{bid}_{pitch}';f0=440*2**((pitch-69)/12);t,y,wide,obs=trace(on,f0);traces[key+'_t']=t;traces[key+'_fundamental']=y;traces[key+'_wide']=wide
   supporting=[]
   for harmonic in [2,3]:
    ht,hy,hw,hinfo=trace(on,f0*harmonic);assert np.array_equal(ht,t);traces[key+f'_harmonic{harmonic}']=hy
    hinfo['harmonic_number']=harmonic;hinfo['supports_primary_candidates']=[c for c in obs['candidate_s'] if hinfo['status']!='TARGET_NOT_OBSERVABLE' and any(abs(c-hc)<=obs['support_ms']/2000 for hc in hinfo['candidate_s'])];supporting.append(hinfo)
   row={'episode_id':e['episode_id'],'BP_member_id':bid,'query_id':key,'pitch_name':['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][pitch%12]+str(pitch//12-1),'midi_pitch':pitch,'f0_hz':f0,'BP_onset_s':on,'BP_offset_s':float(native['offset_s']),'window_start_s':on-.15,'window_end_s':on+.15,'target_frequency_bandwidth_ENBW_hz':obs['ENBW_hz'],'supporting_harmonics_observed':sum(h['status']!='TARGET_NOT_OBSERVABLE' for h in supporting),'supporting_harmonics_with_same_rise':sum(bool(h['supports_primary_candidates']) for h in supporting),'target_onset_status':obs['status'],'target_onset_candidates_s':obs['candidate_s'],'selected_clear_onset_s':obs['candidate_s'][0] if obs['status']=='TARGET_ONSET_CLEAR' else None,'selected_minus_BP_ms':1000*(obs['candidate_s'][0]-on) if obs['status']=='TARGET_ONSET_CLEAR' else None,'target_observation':obs,'harmonic_observations':supporting,'ambiguity_notes':'Conditional pitched-component observation; finite-band leakage and centered smoothing; original family ambiguity retained.'}
   rows.append(row)
results=[]
for e in E:
 rr=[r for r in rows if r['episode_id']==e['episode_id']];clear=[r for r in rr if r['target_onset_status']=='TARGET_ONSET_CLEAR'];cs=[r['selected_clear_onset_s'] for r in clear];states=[r['target_onset_status'] for r in rr];shared=False
 if 'TARGET_ONSET_MULTIPLE' in states:status='TARGET_ONSET_MULTIPLE'
 elif cs:
  if 'TARGET_ONSET_UNRESOLVED' in states:status='TARGET_ONSET_UNRESOLVED'
  elif max(cs)-min(cs)<=hop/sr+1e-12:status='TARGET_ONSET_CLEAR';shared=len(clear)>1
  elif len(set(r['midi_pitch'] for r in clear))>1:status='TARGET_ONSET_UNRESOLVED'
  else:status='TARGET_ONSET_MULTIPLE'
 elif all(s=='TARGET_NOT_OBSERVABLE' for s in states):status='TARGET_NOT_OBSERVABLE'
 elif all(s in ['TARGET_ACTIVITY_CONTINUOUS','TARGET_NOT_OBSERVABLE'] for s in states):status='TARGET_ACTIVITY_CONTINUOUS'
 else:status='TARGET_ONSET_UNRESOLVED'
 results.append({'episode_id':e['episode_id'],'status':status,'shared_target_onset':shared,'clear_query_coordinates_s':cs,'query_ids':[r['query_id'] for r in rr],'identity_ambiguity':e['ambiguity'],'note':'No coordinate averaging; all query outcomes retained. Shared means within one hop only, not physical identity proof.'})
save(O/'TARGET_DEFINITIONS.json',targets);save(O/'TARGET_OBSERVATIONS.json',rows);save(O/'EPISODE_OBSERVATIONS.json',results);np.savez_compressed(O/'TARGET_TRACES.npz',**traces)
with open(O/'TARGETED_PITCH_ONSET_FULLMIX.csv','w') as out:
 fields=list(rows[0])+['episode_status'];w=csv.DictWriter(out,fieldnames=fields);w.writeheader();statuses={e['episode_id']:e['status'] for e in results}
 for r in rows:w.writerow({k:json.dumps(v) if isinstance(v,(dict,list)) else v for k,v in (r|{'episode_status':statuses[r['episode_id']]}).items()})
save(O/'OBSERVATION_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'implementation_sha256':sha(Path(__file__)),'method_sha256':sha(I/'METHOD.json'),'files':{p.name:sha(p) for p in sorted(O.iterdir()) if p.is_file()}})
print('Observation freeze saved; aggregate interpretation not performed in inference.')
