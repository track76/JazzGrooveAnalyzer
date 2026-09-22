"""Independent read-only checks; no tracker or estimator execution."""
from pathlib import Path
import bisect, csv, hashlib, json, statistics
import numpy as np

P = Path(__file__).resolve().parent
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def data(p):
    return json.loads(Path(p).read_text())
def rows(p):
    return list(csv.DictReader(Path(p).open()))

for name in ['INPUT_CONFIGURATION_FREEZE.json', 'NUMERICAL_OUTPUT_FREEZE.json']:
    for path, digest in data(P/name)['files'].items():
        assert sha(P/path) == digest, path
for path, digest in data(P/'PARENT_HASHES.json').items():
    assert sha(path) == digest, path
for r in rows(P/'INPUT_LINEAGE.csv'):
    assert sha(P/r['snapshot']) == r['sha256'] == sha(r['original_path'])
inventory = data(P.parent/'JGA_TEMPO_AUTHORITY_PHASE_CLOSURE_20260922/PRESERVATION_INVENTORY.json')
for path, record in inventory.items():
    assert sha(path) == (record if isinstance(record,str) else record['sha256']), path
beats = np.load(P/'INPUT_SNAPSHOTS/PLP_TIMESTAMPS.npy').tolist()
native = {r['event_id']: r for r in rows(P/'INPUT_SNAPSHOTS/NATIVE_EVENTS.csv')}
states = {r['JGA_EVENT_ID']: r for r in rows(P/'INPUT_SNAPSHOTS/SOURCE_STATES.csv')}
events = rows(P/'EVENT_READOUT.csv')
assert len(events) == len(native) == 1627
active=[]
for r in events:
    t = float(r['native_s'])
    assert t == float(native[r['event_id']]['timestamp_s'])
    assert r['source_state'] == states[r['event_id']]['source_state']
    assert (r['IN_SCOPE']=='True') == (0 <= t < 330)
    if r['IN_SCOPE']=='True': active.append(r)
    if r['reference_available']=='True':
        k=bisect.bisect_left(beats,t)
        candidates=[i for i in (k-1,k) if 0<=i<len(beats)]
        i=min(candidates,key=lambda j:(abs(beats[j]-t),j))
        assert i == int(r['PLP_peak_index'])
        assert abs(float(r['marker_offset_ms'])-1000*(t-beats[i])) < 1e-9
assert len(active)==1606
original=[]
for name in ['DRUM_DERIVATION_RESULTS.json','DRUM_VALIDATION_RAW.json']:
    original.extend(data(P/'INPUT_SNAPSHOTS'/name))
original={r['event']['event_id']:r for r in original}
attacks=rows(P/'QUALIFIED_DRUM_READOUT.csv')
assert len(attacks)==10
for r in attacks:
    parent=original[r['event_id']]
    expected=parent['result']['estimate_s']
    assert (float(r['estimate_s']) if r['estimate_s'] else None)==expected
    if expected is not None:
        assert float(r['review_lo_s']) == parent['event']['review_lo_s']
        assert float(r['review_hi_s']) == parent['event']['review_hi_s']
        assert abs(float(r['attack_offset_ms'])-1000*(expected-float(r['PLP_s']))) < 1e-9
for category, predicate in [('BASS_INCLUSIVE',lambda r:'BASS' in r['source_state']),('DRUM_INCLUSIVE',lambda r:'DRUM' in r['source_state'])]:
    values=[float(r['marker_offset_ms']) for r in active if predicate(r)]
    s=next(r for r in rows(P/'TIMING_STATISTICS.csv') if r['section']=='WHOLE' and r['category']==category)
    assert len(values)==int(s['N'])
    assert abs(statistics.median(values)-float(s['median_ms']))<1e-9
    assert abs(statistics.mean(values)-float(s['mean_ms']))<1e-9
    assert abs(statistics.stdev(values)-float(s['SD_ms']))<1e-9
for p in (P/'FAILED_SERIALIZATION_RUN').glob('*.csv'):
    assert sha(p)==sha(P/p.name),p.name
print(json.dumps({'status':'PASS','native_rows':1627,'included':1606,'preserved_attack_records':10,'historical_inventory_files':len(inventory),'nearest_peak_independently_checked':True,'source_states_and_timestamps_unchanged':True,'serialization_adapter_tables_identical':True}))
