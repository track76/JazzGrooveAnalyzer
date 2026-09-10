"""Non-scientific fixture construction. Never reads repository/external inputs."""
import json
import struct
from fractions import Fraction
from itertools import combinations

from transport import content_id


def fixture(values, reverse=False):
    def rat(x):
        return [str(x.numerator), str(x.denominator)]
    def number(value, pointer):
        value = float(value)
        return {'producer_bits': struct.pack('>d', value).hex(), 'hex': value.hex(),
            'ratio': rat(Fraction(value)), 'original_json_numeric_token': json.dumps(value),
            'field_lineage': pointer, 'measurement_authority': 'SYNTHETIC_NOT_SCIENTIFIC',
            'numerical_authority': 'EXACT_ACCEPTED_BINARY64_RECONSTRUCTION'}
    source = 'SYNTHETIC_SOURCE_NOT_REAL'
    events = [{'eme_id': f'E{i:03}', 'pulse_candidate_id': f'P{i:03}',
        'source_identity': source, 'asset_sha256': 'a'*64, 'producer_frame': str(i),
        'producer_sample_coordinate': str(i), 'frame_coordinate_rule': 'SYNTHETIC_DIAGNOSTIC',
        'timestamp': number(v, f'/synthetic/events/{i}/timestamp'),
        'observation_timestamp': number(v, f'/synthetic/observations/{i}/timestamp'),
        'strength': number(1, f'/synthetic/events/{i}/strength')}
        for i, v in enumerate(values)]
    maximum = max(float(v) for v in values)
    scope = {'origin': number(0, '/synthetic/origin'), 'start': number(0, '/synthetic/start'),
             'end': number(maximum, '/synthetic/end')}
    inp = {'source_identity': source, 'source_authority_id': 'SYNTHETIC_AUTHORITY',
        'source_instance_key': 'SYNTHETIC_KEY', 'asset_sha256': 'a'*64,
        'canonical_report_sha256': 'b'*64, 'events': events, 'scope': scope}
    times = {e['eme_id']: Fraction(float(v)) for e, v in zip(events, values)}
    parents = {e['eme_id']: e['pulse_candidate_id'] for e in events}
    def pair(a, c):
        ids = [c, a] if reverse else [a, c]
        return {'ids': ids, 'times': [rat(times[i]) for i in ids], 'parents': [parents[i] for i in ids]}
    groups, zeros = {}, []
    for a, c in combinations(sorted(times), 2):
        distance = abs(times[a]-times[c])
        if distance:
            groups.setdefault(distance, []).append(pair(a, c))
        else:
            zeros.append(pair(a, c))
    periods = []
    for t in sorted(groups):
        body = {'population': 'SYNTHETIC_POPULATION', 'T': rat(t), 'f': rat(1/t),
                'pairs': groups[t], 'coincident_pairs': zeros}
        periods.append({'id': content_id(body), 'body': body})
    windows = []
    for u in sorted(set(times.values())):
        centers = sorted(i for i in times if times[i] == u)
        for length in sorted({2*abs(t-u) for t in times.values() if t != u}):
            lo, hi = u-length/2, u+length/2
            a, c = max(Fraction(0), lo), min(Fraction(maximum), hi)
            boundary = sorted(i for i in times if abs(times[i]-u) == length/2)
            gaps = []
            if lo < a:
                gaps.append({'ends': [rat(lo), rat(a)], 'closed': [True, False]})
            if c < hi:
                gaps.append({'ends': [rat(c), rat(hi)], 'closed': [False, True]})
            # Ordered center/boundary identities never reverse their roles.
            scales = [{'ids': [i, j], 'times': [rat(times[i]), rat(times[j])],
                       'parents': [parents[i], parents[j]]} for i in centers for j in boundary]
            body = {'population': 'SYNTHETIC_POPULATION', 'u': rat(u), 'L': rat(length),
                'center_ids': centers, 'scale_pairs': scales,
                'membership': {'contained': sorted(i for i in times if a <= times[i] <= c),
                    'positive': sorted(i for i in times if lo < times[i] < hi), 'boundary': boundary},
                'requested': [rat(lo), rat(hi)], 'asset_clipped': [rat(a), rat(c)],
                'available': [rat(a), rat(c)], 'asset_unavailable': gaps, 'unavailable': gaps,
                'asset_truncated': [a, c] != [lo, hi], 'scope_truncated': False}
            windows.append({'id': content_id(body), 'body': body})
    input_hash = content_id(inp)
    body = {'population': 'SYNTHETIC_POPULATION', 'source': source, 'asset': inp['asset_sha256'],
        'source_authority_id': inp['source_authority_id'], 'source_instance_key': inp['source_instance_key'],
        'input_manifest_sha256': input_hash, 'canonical_report_sha256': inp['canonical_report_sha256'],
        'events': events, 'scope': scope,
        'measurement_authority': 'PRESERVED_ACCEPTED_JGA_OBSERVATIONS_NO_NEW_CALIBRATION',
        'numerical_authority': 'EXACT_ACCEPTED_BINARY64_RECONSTRUCTION'}
    binding = {'input_freeze_sha256': input_hash, 'source_uuid': source,
        'source_authority_id': inp['source_authority_id'], 'source_instance_key': inp['source_instance_key'],
        'asset_sha256': inp['asset_sha256'], 'population': 'SYNTHETIC_POPULATION',
        'preregistration_sha256': 'c'*64, 'input_authority_sha256': 'd'*64,
        'implementation_sha256': 'e'*64, 'environment_sha256': 'f'*64,
        'counts': {'events': str(len(events)), 'distinct_centers': str(len(set(times.values()))),
            'unordered_pairs': str(len(events)*(len(events)-1)//2),
            'positive_period_coordinates': str(len(periods)), 'center_specific_windows': str(len(windows))}}
    return {'synthetic_fixture': True, 'binding': binding, 'input': inp,
            'inputs': [{'id': content_id(body), 'body': body}], 'periods': periods, 'windows': windows}
