"""Exact, explicitly bounded non-identity comparison; no tolerance or tuning."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from snapshot import canonical
HERE = Path(__file__).resolve().parent

# Only identity fields and prospective serialization metadata are excluded.
IDENTITY = {'source_identity', 'sound_source_id', 'target_source_identity',
            'contributor_id', 'assignment_id', 'profile_id', 'scientific_fingerprint',
            'stem_ids', 'source_authority_id', 'source_instance_key', 'source_identity_rule'}
PROJECTION_ADDITIONS = {'distance_from_preceding_ms', 'distance_from_following_ms',
                      'nearest_displacement_ms'}

def projection(snapshot):
    aliases = {}
    for asset, diagnostic in snapshot['diagnostics'].items():
        for candidate in diagnostic['candidates']:
            aliases[candidate['id']] = f"candidate:{asset}:{candidate['observation_index']}:{candidate['timestamp'].hex()}"
        for event in diagnostic['events']:
            aliases[event['id']] = f"event:{asset}:{event['timestamp'].hex()}"
    def normalize(value, key=None):
        if isinstance(value, dict):
            return {k: normalize(v, k) for k, v in value.items()
                    if k not in IDENTITY | PROJECTION_ADDITIONS and k != 'schema'}
        if isinstance(value, list):
            return sorted((normalize(x, key) for x in value), key=canonical)
        if isinstance(value, str):
            return aliases.get(value, value)
        return value
    return normalize(snapshot)

def verify(baseline, corrected):
    for snapshot in (baseline, corrected):
        report = snapshot['report']
        counts = {x['label']: x['eme_count'] for x in report['source_authorities']}
        assert counts == {'Drums': 63, 'Piano': 49, 'Double Bass': 27}, counts
        assert len(report['ad038_localizations']) == 76
        assert Counter(x['correspondence_status'] for x in report['ad038_localizations']) == {'GEOMETRIC_ONLY': 76}
        assert report['ad040_profile']['accompaniment_relationship_count'] == 76
    first, second = projection(baseline), projection(corrected)
    if first != second:
        def diff(a,b,path=''):
            if type(a) is not type(b): return (path, a, b)
            if isinstance(a,dict):
                if a.keys()!=b.keys(): return (path, list(a), list(b))
                for k in a:
                    if a[k]!=b[k]: return diff(a[k],b[k],path+'/'+k)
            elif isinstance(a,list):
                if len(a)!=len(b): return (path,len(a),len(b))
                for i,(x,y) in enumerate(zip(a,b)):
                    if x!=y:return diff(x,y,path+f'/{i}')
            return (path,a,b)
        raise AssertionError(diff(first,second))
    ids = [x['source_identity'] for x in corrected['report']['source_authorities']]
    assert len(set(ids)) == 3
    assert all(x['stem_names'] == ['Mix'] for x in corrected['diagnostics'].values())
    return {'provenance_invariance': 'PASS', 'population': counts,
            'relationships':76, 'scientific_status':'GEOMETRIC_ONLY',
            'non_identity_projection_sha256':sha256(canonical(first).encode()).hexdigest(),
            'baseline_identity_rule':'uuid5(NAMESPACE_URL, stem.name)',
            'corrected_identity_rule':'jga-direct-input-source-identity/v1',
            'baseline_sha256':sha256(canonical(baseline).encode()).hexdigest(),
            'corrected_sha256':sha256(canonical(corrected).encode()).hexdigest()}

if __name__ == '__main__':
    result = verify(json.loads((HERE/'baseline.json').read_text()), json.loads((HERE/'corrected_identity.json').read_text()))
    with (HERE/'invariance_result.json').open('x') as stream: stream.write(canonical(result))
    print(canonical(result))
