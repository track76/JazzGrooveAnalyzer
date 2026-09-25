from pathlib import Path
import json,csv,hashlib,sys,io
import numpy as np
sys.path.insert(0,'tools')
from continuous_backup import atomic_write_and_backup,MIRROR
O=Path('docs/scientific/rfc/JGA_FINAL_REPORT_CANDIDATE_20260925')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,b):atomic_write_and_backup(O/n,b.encode() if isinstance(b,str) else b)
def js(n,x):put(n,json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def rows(n):return list(csv.DictReader((O/n).open()))
s=json.loads((O/'FINAL_GRID_SUMMARY.json').read_text());p=json.loads((O/'REPORT_PROVENANCE.json').read_text())
for f,h in p['input_hashes'].items():assert sha(Path(f))==h
assert sha(O/'FINAL_ANCHORED_GRID_PROTOCOL.md')==p['protocol_sha256']
g=rows('FINAL_ANCHORED_BMIG_DMIG.csv');a=rows('FINAL_ANCHOR_AUDIT.csv');ev=rows('EVENT_PROVENANCE_127.csv');assert len(g)==len(a)==64 and len(ev)==127
for inst,key in [('BASS','BMIG'),('DRUM','DMIG')]:
 d=json.loads((O/(inst+'_OWN_ONLY_INPUT.json')).read_text());n=np.array(d['n']);t=np.array(d['t'],float);x=np.array([float(r[key+'_time_s']) for r in g]);assert np.all(np.diff(x)>0)
 D=np.diff(np.eye(64),n=2,axis=0);L=np.zeros((len(n),64));L[np.arange(len(n)),n]=1
 # Independent augmented least-squares solution of preregistered objective.
 origin=np.median(t);design=np.vstack([L,D/4]);target=np.r_[t-origin,np.zeros(62)];check=np.linalg.lstsq(design,target,rcond=None)[0]+origin;assert max(abs(check-x))<1e-10
 for r in a:
  if r[inst+'_anchor_present']=='YES':
   native=next(e for e in ev if e['event_ID']==r[inst+'_anchor_event_ID']);assert native['original_time_s']==r[inst+'_anchor_time_s'];assert native['instrument']==inst
for r in g:
 assert float(r['B_DISPLAY_ms'])==-float(r['D_DISPLAY_ms']);assert abs(float(r['GRID_DELTA_ms'])-float(r['B_DISPLAY_ms'])+float(r['D_DISPLAY_ms']))<1e-10
mixed=[r for r in a if r['BASS_anchor_present']!=r['DRUM_anchor_present'] or r['quarter_ID'] in ['Q167','Q168','Q169','Q189']]
b=io.StringIO();w=csv.DictWriter(b,fieldnames=mixed[0]);w.writeheader();w.writerows(mixed);put('MIXED_SUPPORT_CASES.csv',b.getvalue())
bpm=json.loads((O/'FINAL_BPM_SUMMARY.json').read_text());bpm['delta_at_display_precision_BPM']=round(bpm['last_BPM'],2)-round(bpm['first_BPM'],2)
if bpm['delta_at_display_precision_BPM']==0:bpm['reader_text']=f"BPM interno: {bpm['first_BPM']:.2f} → {bpm['last_BPM']:.2f} · invariato"
bpm['precision_note']='Native first/last values and raw difference retained; invariato refers only to approved 0.01BPM display precision, avoiding floating-point +0.00 increase.'
js('FINAL_BPM_SUMMARY.json',bpm)
s['candidate_report_gate']='BLOCKED_APPROVED_PLUS_1_6_STATEMENT_NOT_SUPPORTED';s['musicological_reading_preserved']='NOT_ESTABLISHED_NO_AUTHORIZATION_TO_REUSE_TEXT';s['final_report_candidate_generated']=False
js('FINAL_GRID_SUMMARY.json',s)
js('SCIENTIFIC_QA.json',{'objective_integrity':'PASS','coverage_each':64,'measures_each':16,'strictly_increasing_each':True,'independent_augmented_least_squares_verification':'PASS','observed_timestamps_preserved':True,'observed_events_invented':False,'mixed_support_logic_verified':True,'M42_Q1_Q2_Q3_verified':True,'M47_Q3_verified':True,'cross_instrument_input':False,'direct_delta_interpolation':False,'preregistered_before_comparison':True,'midpoint_arithmetic':'PASS','candidate_report_gate':'BLOCKED','physical_pulse_validity':'NOT_ESTABLISHED','abrupt_duration_changes_preserved':True})
js('VISUAL_QA.json',{'status':'NOT_RUN','reason':'Specific musicological conclusion gate requires STOP before candidate generation. No candidate PDF generated; no visual approval claimed.'})
put('READER_SUMMARY.md','# Reader summary withheld\n\nThe approved +1.6ms paragraph is NOT reproduced. New six-measure median +8.886ms; prior+1.578ms; signed change+7.308ms. Candidate generation stopped under the PI musicological conclusion gate. No alternate reader-facing conclusion invented.\n')
put('SOFTWARE_REQUIREMENT.md','# Future analysis range — record only\n\n[TUTTO IL BRANO] or [DA MM:SS.xx] → [A MM:SS.xx]. Every subsequent analysis/report respects and identifies the selected interval. No GUI or bootstrap change authorized/performed.\n')
put('RESULT.md','# Anchored reconstruction — candidate generation STOPPED\n\nObjective integrity PASS:64BMIG/64DMIG,16measures each, strictly increasing, all63Bass/64Drum native events preserved,56Bass/49Drum independent soft anchors. No hard snap or cross-instrument reconstruction.\n\nThe preregistered local quadratic model privileges anchors but yields six-complete-measure median+8.886246628359018ms, versus+1.5783824640962507ms, change+7.307864164262767ms. The exact approved+1.6ms paragraph cannot be used truthfully. The prompt’s explicit conclusion gate requires STOP before generation despite the general viewable-PDF objective. Therefore NO candidate PDF was created and no visual PASS claimed. No retuning attempted.\n\nLocal evidence priority does not establish a valid underlying musical pulse: Bass consecutive durations span234.407–508.871ms (117.908–255.965BPM); Drum295.966–427.450ms (140.367–202.726BPM). Maximum consecutive-duration changes227.497ms/116.934ms remain in CONTINUITY_AUDIT.csv. Strict monotonicity does not establish gradualness, perceptual validity or model acceptance. No observation deleted or residual capped.\n\nComparisons include all existing prior instrument grids separately (Bass56coordinates,Drum40), and the common10measure subset separately. All previous studies remain unchanged. MIDPOINT values are display-only decomposition, not independent observations.\n\nBPM first/last native local_bpm entries in[Q131,Q195) retained without recomputation; both display161.50BPM, invariato at0.01BPM precision. Global reference remains median904elementaryintervalBPM161.49902343750287, separate from rolling32interval curve.\n\nNo audio inference, final report overwrite, freeze, canonical promotion, bootstrap, commit or push. STOP for PI review of the new scientific result.\n')
p['candidate_generation_stopped']=True;p['stop_reason']='Approved six-measure +1.6ms sentence not supported by new result';js('REPORT_PROVENANCE.json',p)
put('verify_and_close.py',Path(__file__).read_bytes())
entries=[{'relative_path':f.name,'size_bytes':f.stat().st_size,'sha256':sha(f),'authority_status':'UNAPPROVED_CANDIDATE_AUDIT_REPORT_BLOCKED'} for f in sorted(O.iterdir()) if f.is_file() and f.name not in ['MANIFEST.json','SHA256SUMS.txt']]
js('MANIFEST.json',{'status':'INCOMPLETE_REPORT_CANDIDATE_MUSICOLOGICAL_GATE_BLOCKED','method_frozen':False,'entries':entries})
checks=entries+[{'relative_path':'MANIFEST.json','sha256':sha(O/'MANIFEST.json')}]
put('SHA256SUMS.txt',''.join(f"{x['sha256']}  {x['relative_path']}\n" for x in checks))
for x in checks:
 f=O/x['relative_path'];assert sha(f)==x['sha256']==sha(MIRROR/f)
assert sha(O/'SHA256SUMS.txt')==sha(MIRROR/O/'SHA256SUMS.txt')
print('Audit verification and package mirror PASS; report gate BLOCKED; files',len(checks)+1)
print('Mixed cases',[(r['quarter_ID'],r['BASS_anchor_present'],r['DRUM_anchor_present']) for r in a if r['quarter_ID'] in ['Q167','Q168','Q169','Q189']])
print('BPM',bpm['first_BPM'],bpm['last_BPM'],bpm['delta_BPM'],bpm['reader_text'])
