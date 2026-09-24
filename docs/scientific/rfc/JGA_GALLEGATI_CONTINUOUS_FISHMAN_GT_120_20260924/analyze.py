from pathlib import Path
import json,csv,hashlib
from decimal import Decimal as D
import numpy as np
P=Path(__file__).resolve().parent;A=P.parent/'JGA_GALLEGATI_CONTINUOUS_FISHMAN_GT_COMPLETION_20260924';B=P.parent/'JGA_GALLEGATI_CONTINUOUS_FISHMAN_GT_PASS1_INGESTION_20260924'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return list(csv.DictReader(p.open()))
def out(p,rows):
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def loadpass(base,manifest,passno):
 rp=base/f'ORIGINAL_EXPORTS/PI_FISHMAN_CONTINUOUS_GT_PASS{passno}_RESPONSES.json';rc=base/f'ORIGINAL_EXPORTS/PI_FISHMAN_CONTINUOUS_GT_PASS{passno}_RECEIPT.json';r=json.loads(rp.read_text());c=json.loads(rc.read_text());assert c['response_sha256']==sha(rp) and r['pass']==passno==c['completed_pass']
 m={x['item_id']:x for x in read(manifest)};assert len(r['items'])==len(m)==c['items_complete'];assert len({x['item_id'] for x in r['items']})==len(m) and {x['item_id'] for x in r['items']}==set(m)
 result={}
 for x in r['items']:
  z=m[x['item_id']];origin=D(z['crop_start_sample'])/D(z['sample_rate']);v={}
  for name in ['center','earliest','latest']:
   a=x[name+'_local_s'];v[name]=origin+D(str(a)) if a is not None else None
   if a is not None:assert 0<=a<=4
  result[z['event_id']]={'values':v,'raw':x,'mapping':z}
 return result
p1=loadpass(B,A/'TECHNICAL/PRIVATE_EXCERPT_MANIFEST.csv',1);p2=loadpass(P,B/'TECHNICAL/PASS2_PRIVATE_MANIFEST.csv',2)
selected={x['event_id'] for x in read(B/'TECHNICAL/PASS2_SELECTION.csv')};assert set(p2)==selected and len(selected)==24 and set(p2)<=set(p1)
meta={x['event_id']:x for x in read(B/'TECHNICAL/PRIMARY_SOURCE_COORDINATES.csv')};rows=[]
for eid in sorted(p2):
 a=p1[eid];b=p2[eid];assert a['mapping']['source_wav']==b['mapping']['source_wav'] and a['mapping']['source_sha256']==b['mapping']['source_sha256'];flags=[]
 for label,z in [('pass1',a),('pass2',b)]:
  v=z['values'];raw=z['raw']
  if raw['uncertain'] or raw.get('annotation_difficulty') or raw.get('notes','').strip():flags.append(label+'_UNCERTAIN_DIFFICULTY_NOTE')
  if any(x is None for x in v.values()):flags.append(label+'_MISSING')
  elif not v['earliest']<=v['center']<=v['latest']:flags.append(label+'_ORDER')
  elif v['latest']-v['earliest']>=D('.005'):flags.append(label+'_WIDE')
 av=a['values'];bv=b['values'];delta=float((bv['center']-av['center'])*1000) if av['center'] is not None and bv['center'] is not None else None
 overlap=all(v[k] is not None for v in [av,bv] for k in ['earliest','latest']) and max(av['earliest'],bv['earliest'])<=min(av['latest'],bv['latest'])
 if not overlap:flags.append('NO_INTERVAL_OVERLAP')
 if delta is not None and abs(delta)>2:flags.append('EXCEEDS_PREVIOUS_2MS_ENVELOPE')
 rows.append({'event_id':eid,'string':meta[eid]['string'],'dynamic':meta[eid]['dynamic'],'take':meta[eid]['take'],'pass1_center_s':str(av['center']),'pass2_center_s':str(bv['center']),'pass1_earliest_s':str(av['earliest']),'pass1_latest_s':str(av['latest']),'pass2_earliest_s':str(bv['earliest']),'pass2_latest_s':str(bv['latest']),'delta_ms':delta,'absolute_delta_ms':abs(delta) if delta is not None else None,'interval_overlap':bool(overlap),'review_flags':'|'.join(flags)})
def stats(rs):
 x=np.array([r['delta_ms'] for r in rs if r['delta_ms'] is not None]);a=np.abs(x)
 return {'N':len(x),'median_signed_ms':float(np.median(x)),'mean_signed_ms':float(np.mean(x)),'median_absolute_ms':float(np.median(a)),'IQR_signed_ms':float(np.percentile(x,75)-np.percentile(x,25)),'P95_absolute_ms':float(np.percentile(a,95)),'maximum_absolute_ms':float(a.max()),'minimum_signed_ms':float(x.min()),'maximum_signed_ms':float(x.max()),**{f'within_{k}ms_percent':float(np.mean(a<=k)*100) for k in [2,5,10,20]},'overlap_N':sum(r['interval_overlap'] for r in rs),'overlap_percent':100*sum(r['interval_overlap'] for r in rs)/len(rs)}
s={'overall':stats(rows),'strings':{g:stats([r for r in rows if r['string']==g]) for g in sorted({r['string'] for r in rows})},'conditions':{g:stats([r for r in rows if r['dynamic']==g]) for g in sorted({r['dynamic'] for r in rows})},'flagged_events':[r['event_id'] for r in rows if r['review_flags']],'GT_construction_allowed':not any(r['review_flags'] for r in rows),'precision_qualification':'UI 1ms steps; fractional source restoration does not imply sub-ms human accuracy.'}
out(P/'EVENT_REPEATABILITY.csv',rows);(P/'REPEATABILITY_SUMMARY.json').write_text(json.dumps(s,indent=2)+'\n')
if __name__=='__main__':print(json.dumps(s,indent=2))
