from pathlib import Path
import csv,json,hashlib,statistics
from decimal import Decimal as D
P=Path(__file__).resolve().parent; parent=P.parent
rows=lambda p:list(csv.DictReader(p.open()))
r=rows(parent/'data/global__PLP_REFERENCE.csv');m=rows(P/'METRIC_REFERENCE.csv');assert len(r)==len(m)==905
for i,(x,y) in enumerate(zip(r,m)):
 assert x['time_seconds']==y['reference_time'] and y['quarter_label']==f'Q{i+1}'
 if i>=2:assert int(y['metric_beat'])==(i-2)%4+1 and y['measure_id']==f'M{(i-2)//4+1}'
 else:assert not y['metric_beat'] and not y['measure_id']
for w in rows(P/'BPM_EVOLUTION.csv'):
 i=int(w['start_index']);j=int(w['end_index']);assert j-i==32
 assert abs(float(D(1920)/(D(r[j]['time_seconds'])-D(r[i]['time_seconds'])))-float(w['BPM']))<1e-10
assert round(D(r[2]['time_seconds']),9)==D('0.812698413')
a={x['quarter_id']:x for x in rows(parent/'data/source__SOURCE_CONDITIONED_ASSIGNMENTS.csv')}
pp=rows(P/'MICROTIMING_PAIRS.csv');old=rows(P/'ORIGINAL_PAIRS.csv');assert len(pp)==len(old)==21
for x,y in zip(pp,old):
 assert x['pair_id']==y['pair_id'] and x['bass_time']==y['bass_time'] and x['drum_time']==y['drum_time'] and x['drum_minus_bass_ms']==y['drum_minus_bass_ms']
 assert x['bass_event_id']!=x['drum_event_id'] and x['bass_time']!=x['drum_time']
 assert a[x['quarter_id']]['status']=='DISTINCT_PAIR'
obs=rows(P/'PRIMARY_OBSERVATIONS.csv');profile=json.loads((P/'PROFILE.json').read_text())
for k in ['BASS','DRUM']:
 v=[float(x['offset_ms']) for x in obs if x['source']==k];assert len(v)==profile['primary'][k]['N'];assert abs(statistics.median(v)-profile['primary'][k]['median_ms'])<1e-8
 for x in [x for x in obs if x['source']==k]:assert a[x['quarter_id']][k+'_timestamp']==x['timestamp'] and a[x['quarter_id']][k+'_state']==x['original_state']
page=json.loads((P/'PAGE_EVENTS.json').read_text());ids=[i for x in page for i in x['event_ids']];assert len(ids)==len(set(ids))==1606
rr=json.loads((P/'PAGE_LINEAGE.json').read_text());assert [i for x in rr for i in x['quarter_ids']]==list(range(905))
assert all(x['measure_end']-x['measure_start']<=3 for x in rr)
print('PASS: frozen coordinates, metric propagation, BPM windows, original pairs, primary medians, exhaustive page coverage')
