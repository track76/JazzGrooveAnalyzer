from pathlib import Path
import json,csv,hashlib
from decimal import Decimal as D
from collections import defaultdict
O=Path(__file__).resolve().parent;R=O.parent
F=json.loads((O/'JGA_WHOLE_TRACK_GROOVE_PROCEDURE_FREEZE.json').read_text())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(n,v):(O/n).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
def write(n,rows):
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with (O/n).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
def read(n):return list(csv.DictReader(Path(n).open()))
native=[x for x in json.loads((R/'JGA_REALMUSIC_DB_REPLICATION_002_EXACTLY_LIKE_YOU_20260920/FULLMIX_EVENT_SEQUENCE.json').read_text()) if x['family']=='F_MIX'];native.sort(key=lambda e:e['timestamp_s'])
grid=json.loads(Path(F['grid']['path']).read_text());bass=json.loads((R/'JGA_OBSERVABLE_EVENT_INVENTORY_001_EXACTLY_LIKE_YOU_20260920/BASS_EVENT_INVENTORY.json').read_text());links=defaultdict(list)
for e in bass:
 if e['countable'] and e['evidence_grade'] in ['HIGH','MEDIUM']:links[e['fmix_nearest_s']].append(e['event_id'])
models={'ADTOF':'ADTOF_PYTORCH','MU_U':'MUSCRIPTOR_MEDIUM_UNCONSTRAINED','MU_C':'MUSCRIPTOR_MEDIUM_TRIO_CONDITIONED'}
existing={}
for c in F['evidence_contexts']:
 allrows=json.loads(Path(c['normalized']).read_text());existing[c['name']]=[e for e in allrows if c['name'] in e['provenance'] and e['SYSTEM'] in models.values()]
def owner(t):
 for c in sorted(F['evidence_contexts'],key=lambda c:(c['priority'],c['start'],c['name'])):
  if c['start']+.05<=t<=c['end']-.05:return c['name']
 return f'NEW_{int(t//15):03d}'
def adapter(n,es,available=None):
 t=n['timestamp_s'];r={'JGA_EVENT_ID':n['event_id'],'native_timestamp':str(t),'context':owner(t),'source_state_provisional':True,'adapter_sha256':F['adapter']['sha256']};available=set(models) if available is None else set(available)
 for a,m in models.items():
  r[a+'_available']=a in available
  for fam in (['DRUM'] if a=='ADTOF' else ['DRUM','BASS','PIANO','OTHER']):
   pool=[e for e in es if e['SYSTEM']==m and e['INSTRUMENT_FAMILY_NORMALIZED']==fam];near=min(pool,key=lambda e:(abs(e['EVENT_ONSET_SECONDS']-t),e['EVENT_ONSET_SECONDS'],e['EVENT_ID'])) if pool and a in available else None;d=abs(near['EVENT_ONSET_SECONDS']-t)*1000 if near else None;p=a+'_'+fam
   r[p+'_event_id']=near['EVENT_ID'] if near else None;r[p+'_timestamp_s']=near['EVENT_ONSET_SECONDS'] if near else None;r[p+'_distance_ms']=d;r[p+'_raw_label']=near['INSTRUMENT_LABEL_RAW'] if near else None
   for tol in [10,20,35,50]:r[p+f'_support_{tol}ms']=d is not None and d<=tol+1e-9
 b=r['MU_U_BASS_support_35ms'] and bool(links[t]);dr=r['ADTOF_DRUM_support_35ms'] or (r['MU_U_DRUM_support_35ms'] and r['MU_C_DRUM_support_35ms']);r['frozen_Bass_native_links']=';'.join(links[t]);r['source_state']='BASS_AND_DRUM_SUPPORTED' if b and dr else 'BASS_SUPPORTED' if b else 'DRUM_SUPPORTED' if dr else 'UNKNOWN';r['UNKNOWN_reason']=('MISSING_EVIDENCE' if len(available)<3 else 'INSUFFICIENT_SUPPORT_UNDER_FROZEN_RULE') if not b and not dr else '';r['CONFLICT_reason']='';r['missing_streams']=';'.join(sorted(set(models)-available));r['MU_Drum_condition_disagreement']=r['MU_U_DRUM_support_35ms']!=r['MU_C_DRUM_support_35ms'];r['MU_Bass_condition_disagreement']=r['MU_U_BASS_support_35ms']!=r['MU_C_BASS_support_35ms'];return r
def quarter(n):
 t=D(str(n['timestamp_s']));ds=[abs(t-D(str(q['time_seconds']))) for q in grid];i=min(range(len(grid)),key=lambda i:(ds[i],grid[i]['time_seconds']));q=grid[i];return {'JGA_EVENT_ID':n['event_id'],'native_timestamp':str(n['timestamp_s']),'quarter_id':q['beat_index'],'quarter_timestamp':str(q['time_seconds']),'stored_local_BPM':str(q['local_bpm']),'JGA_NATIVE_EVENT_TO_QUARTER_MS':str((t-D(str(q['time_seconds'])))*1000),'QUARTER_TIE':sum(d==ds[i] for d in ds)>1,'BOUNDARY_CONDITION':t<D(str(grid[0]['time_seconds'])) or t>D(str(grid[-1]['time_seconds']))}
