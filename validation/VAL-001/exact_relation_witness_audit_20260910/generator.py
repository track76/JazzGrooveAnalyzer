"""Catalogue traversal for the frozen exact-relation contract. No audio input.

Import has no input I/O. Calling generate requires an admitted in-memory bundle;
the operational runner supplies that bundle only after authorization and hashes.
"""
import math
import re
import struct
from fractions import Fraction
from itertools import combinations
from pathlib import Path

from transport import canonical, content_id, files_index, write, write_rows

SCHEMA = 'JGA-EXACT-RELATION-WITNESS-V1'
DATA = ('events.json', 'relations.jsonl', 'witnesses.jsonl',
        'witness_relations.jsonl', 'windows.jsonl', 'reuse_audit.json',
        'relation_ratios.jsonl', 'candidate_population.json')


class ContractError(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise ContractError(reason)


def rational(value):
    require(isinstance(value, list) and len(value) == 2, 'rational shape')
    require(all(isinstance(v, str) and re.fullmatch(r'0|-?[1-9][0-9]*', v)
                for v in value), 'rational integer spelling')
    n, d = map(int, value)
    require(d > 0 and math.gcd(n, d) == 1, 'noncanonical rational')
    return Fraction(n, d)


def ratio(value):
    return [str(value.numerator), str(value.denominator)]


def decode(record):
    bits = record['producer_bits']
    require(isinstance(bits, str) and re.fullmatch('[0-9a-f]{16}', bits), 'bits')
    value = struct.unpack('>d', bytes.fromhex(bits))[0]
    require(math.isfinite(value), 'nonfinite producer')
    exact = Fraction(*value.as_integer_ratio())
    require(rational(record['ratio']) == exact, 'producer/ratio conflict')
    require(record['hex'] == value.hex(), 'producer/hex conflict')
    # Token is used only for binary64 round-trip admission, never subtraction.
    token = record['original_json_numeric_token']
    require(isinstance(token, str) and re.fullmatch(
        r'-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?', token), 'token')
    require(struct.pack('>d', float(token)).hex() == bits, 'producer/token conflict')
    require(bool(record['field_lineage']), 'missing field lineage')
    return exact


def pair_id(binding, ids):
    return ['EXACT_PAIR_V1', binding['input_freeze_sha256'],
            binding['source_uuid'], *sorted(ids)]


def relation_id(binding, t):
    return ['EXACT_RELATION_V1', binding['input_freeze_sha256'],
            binding['source_uuid'], ratio(t)]


def admit(bundle):
    """Validate catalogue claims before creating output. No response evaluation."""
    b, inp = bundle['binding'], bundle['input']
    require(bundle.get('synthetic_fixture') is True or
            bundle.get('admission_receipt', {}).get('authorized_input_sha256') == b['input_freeze_sha256'],
            'missing operational admission')
    if bundle.get('synthetic_fixture') is True:
        require(len(inp['events']) <= 16 and b['source_uuid'] !=
                'c46d6cb9-b99c-5bd6-8d81-656dc1ad48ec', 'real population forbidden in fixtures')
    require(inp['source_identity'] == b['source_uuid'], 'input source')
    require(inp['source_authority_id'] == b['source_authority_id'], 'source authority')
    require(inp['source_instance_key'] == b['source_instance_key'], 'source key')
    require(inp['asset_sha256'] == b['asset_sha256'], 'asset')
    events = inp['events']
    require(len(events) == int(b['counts']['events']), 'event count')
    byid, times, parents = {}, {}, set()
    for event in events:
        require(set(event) == {'eme_id', 'pulse_candidate_id', 'source_identity', 'asset_sha256',
                'producer_frame', 'producer_sample_coordinate', 'frame_coordinate_rule',
                'timestamp', 'observation_timestamp', 'strength'}, 'event field allowlist')
        i, parent = event['eme_id'], event['pulse_candidate_id']
        require(isinstance(i, str) and bool(i) and i not in byid, 'event identity')
        require(isinstance(parent, str) and bool(parent) and parent not in parents,
                'unique parent')
        require(event['source_identity'] == b['source_uuid'] and
                event['asset_sha256'] == b['asset_sha256'], 'event lineage')
        time = decode(event['timestamp'])
        require(decode(event['observation_timestamp']) == time and
                event['timestamp']['producer_bits'] ==
                event['observation_timestamp']['producer_bits'], 'observation time')
        decode(event['strength'])
        require(all(k in event for k in ('producer_frame', 'producer_sample_coordinate',
                                         'frame_coordinate_rule')), 'diagnostics')
        byid[i], times[i] = event, time
        parents.add(parent)
    origin, start, end = (decode(inp['scope'][k]) for k in ('origin', 'start', 'end'))
    require(origin == start == 0 and start <= end, 'scope contract')
    require(all(start <= t <= end for t in times.values()), 'event outside scope')
    require(len(set(times.values())) == int(b['counts']['distinct_centers']), 'centers')
    inputs = bundle['inputs']
    require(len(inputs) == 1, 'input catalogue count')
    record = inputs[0]
    require(record['id'] == content_id(record['body']), 'input content ID')
    body = record['body']
    expected = {'population': b['population'], 'source': b['source_uuid'],
                'asset': b['asset_sha256'], 'source_authority_id': b['source_authority_id'],
                'source_instance_key': b['source_instance_key'],
                'input_manifest_sha256': b['input_freeze_sha256'],
                'canonical_report_sha256': inp['canonical_report_sha256'],
                'events': events, 'scope': inp['scope'],
                'measurement_authority': 'PRESERVED_ACCEPTED_JGA_OBSERVATIONS_NO_NEW_CALIBRATION',
                'numerical_authority': 'EXACT_ACCEPTED_BINARY64_RECONSTRUCTION'}
    require(canonical(body) == canonical(expected), 'divergent input catalogue')

    def checked_pair(p):
        ids = p['ids']
        require(len(ids) == 2 and ids[0] != ids[1] and all(i in byid for i in ids),
                'pair identity')
        require(p['times'] == [ratio(times[i]) for i in ids] and
                p['parents'] == [byid[i]['pulse_candidate_id'] for i in ids], 'pair lineage')
        return tuple(sorted(ids))

    groups, refs, seen, coincident, reversals = {}, {}, set(), None, 0
    for record in bundle['periods']:
        p = record['body']
        require(record['id'] == content_id(p), 'period content ID')
        require(p['population'] == b['population'], 'period population')
        t = rational(p['T'])
        require(t > 0 and rational(p['f']) == 1 / t and t not in groups, 'period coordinate')
        local = []
        for raw in p['pairs']:
            ids = checked_pair(raw)
            require(ids not in seen, 'duplicate authoritative pair')
            require(abs(times[ids[0]] - times[ids[1]]) == t, 'pair separation')
            seen.add(ids)
            local.append(ids)
            reversals += raw['ids'] != list(ids)
        require(bool(local), 'empty relation')
        groups[t], refs[t] = sorted(local), record['id']
        zero = [checked_pair(raw) for raw in p['coincident_pairs']]
        require(len(zero) == len(set(zero)) and
                all(times[i] == times[j] for i, j in zero), 'coincident pairs')
        if coincident is None:
            coincident = sorted(zero)
        require(coincident == sorted(zero), 'coincident catalogue disagreement')
    coincident = coincident or []
    # All-pair coverage check; the generator's grouping is still catalogue-derived.
    expected_pairs = set(combinations(sorted(byid), 2))
    require(seen.isdisjoint(coincident) and seen | set(coincident) == expected_pairs,
            'complete pair conservation')
    require(len(expected_pairs) == int(b['counts']['unordered_pairs']) and
            len(groups) == int(b['counts']['positive_period_coordinates']), 'frozen pair counts')
    return b, inp, byid, times, groups, refs, coincident, reversals, checked_pair


def generate(bundle, destination):
    b, inp, events, times, groups, refs, coincident, reversals, check_pair = admit(bundle)
    dest = Path(destination)
    dest.mkdir(parents=True, exist_ok=False)
    authority = {k: b[k] for k in ('input_freeze_sha256', 'preregistration_sha256',
        'input_authority_sha256', 'implementation_sha256', 'environment_sha256',
        'source_uuid', 'source_authority_id', 'source_instance_key', 'asset_sha256')}
    authority['checker_authority'] = 'FROZEN_IMPLEMENTATION_BINDING'
    authority['replay_authority'] = 'PREREGISTRATION_SECTION_9'
    missing = {'numerical': [], 'physical_timing_uncertainty': 'NOT_ESTABLISHED',
               'physical_event_independence': 'NOT_ESTABLISHED'}
    repeated = [t for t in sorted(groups) if len(groups[t]) >= 2]
    outcome = ('EXACT_RELATION_RECURRENCE_OBSERVED' if repeated else
               'NO_EXACT_RELATION_RECURRENCE_OBSERVED')
    population = ('NO_REPEATED_EXACT_RELATIONS' if not repeated else
                  'ONE_REPEATED_EXACT_RELATION' if len(repeated) == 1 else
                  'MULTIPLE_REPEATED_EXACT_RELATIONS')
    def support(ids):
        return sorted(times[i] for i in ids)
    def location(t):
        order = sorted(groups[t], key=lambda ids: (*support(ids), ids))
        starts = [support(ids)[0] for ids in order]
        endpoints = sorted({times[i] for ids in order for i in ids})
        return {'ordered_witness_ids': [pair_id(b, ids) for ids in order],
                'intervals': [[ratio(v) for v in support(ids)] for ids in order],
                'endpoint_times': [ratio(v) for v in endpoints],
                'extent': [ratio(endpoints[0]), ratio(endpoints[-1])],
                'successive_start_gaps': [ratio(y-x) for x, y in zip(starts, starts[1:])]}
    write(dest / 'events.json', {'schema': SCHEMA, 'authority': authority,
        'scope': inp['scope'], 'missingness': missing,
        'events': [events[i] for i in sorted(events, key=lambda i: (times[i], i))]})
    def relations():
        for t in sorted(groups):
            yield {'relation_id': relation_id(b, t), 'seconds': ratio(t),
                'witness_ids': [pair_id(b, ids) for ids in groups[t]],
                'witness_count': str(len(groups[t])), 'catalogue_ids': [refs[t]],
                'status': 'REPEATED' if len(groups[t]) >= 2 else 'SINGLETON',
                'authority': authority, 'missingness': missing, 'distribution': location(t)}
    write_rows(dest / 'relations.jsonl', relations())
    def witnesses():
        for t in sorted(groups):
            for ids in groups[t]:
                yield {'witness_id': pair_id(b, ids), 'relation_id': relation_id(b, t),
                    'event_ids': list(ids), 'parent_ids': [events[i]['pulse_candidate_id'] for i in ids],
                    'endpoint_times': [ratio(times[i]) for i in ids], 'seconds': ratio(t),
                    'chronological_event_ids': sorted(ids, key=lambda i: (times[i], i)),
                    'support': [ratio(v) for v in support(ids)], 'authority': authority,
                    'catalogue_ids': [refs[t]], 'events_reference': 'events.json',
                    'measurement_authority': 'PRESERVED_ACCEPTED_JGA_OBSERVATIONS_NO_NEW_CALIBRATION'}
    write_rows(dest / 'witnesses.jsonl', witnesses())
    def dependencies():
        for t in sorted(groups):
            for a, c in combinations(groups[t], 2):
                common = sorted(set(a) & set(c))
                left, right = max(support(a)[0], support(c)[0]), min(support(a)[1], support(c)[1])
                yield {'relation_id': relation_id(b, t), 'witness_ids': [pair_id(b, a), pair_id(b, c)],
                    'shared_event_ids': common, 'dependence': 'SHARED_ENDPOINT' if common else 'EVENT_DISJOINT',
                    'temporal_relation': 'DISJOINT' if left > right else 'TOUCH' if left == right else 'OVERLAP',
                    'statistical_independence': 'NOT_ESTABLISHED'}
    write_rows(dest / 'witness_relations.jsonl', dependencies())
    all_pairs = sorted(ids for local in groups.values() for ids in local)
    seen_windows, count_contained, count_positive = set(), 0, 0
    start, end = (decode(inp['scope'][k]) for k in ('start', 'end'))
    expected_windows = {(u, 2 * abs(t-u)) for u in set(times.values())
                        for t in times.values() if t != u}
    def windows():
        nonlocal count_contained, count_positive
        previous = None
        for record in bundle['windows']:
            w = record['body']
            require(record['id'] == content_id(w), 'window content ID')
            require(w['population'] == b['population'], 'window population')
            u, length = rational(w['u']), rational(w['L'])
            key = u, length
            require(key in expected_windows and key not in seen_windows, 'window population/duplicate')
            require(previous is None or previous < key, 'window order')
            previous = key
            seen_windows.add(key)
            centers = sorted(i for i in times if times[i] == u)
            boundary = sorted(i for i in times if abs(times[i]-u) == length/2)
            lo, hi = u-length/2, u+length/2
            clip = [max(start, lo), min(end, hi)]
            membership = {'contained': sorted(i for i in times if clip[0] <= times[i] <= clip[1]),
                          'positive': sorted(i for i in times if abs(times[i]-u) < length/2),
                          'boundary': boundary}
            gaps = []
            if lo < clip[0]:
                gaps.append({'ends': [ratio(lo), ratio(clip[0])], 'closed': [True, False]})
            if clip[1] < hi:
                gaps.append({'ends': [ratio(clip[1]), ratio(hi)], 'closed': [False, True]})
            require(w['center_ids'] == centers and w['membership'] == membership, 'window membership')
            require(w['requested'] == [ratio(lo), ratio(hi)] and
                    w['asset_clipped'] == [ratio(v) for v in clip] and
                    w['available'] == w['asset_clipped'] and
                    w['asset_unavailable'] == gaps and w['unavailable'] == gaps and
                    w['asset_truncated'] == (clip != [lo, hi]) and
                    w['scope_truncated'] is False, 'window coverage')
            scale_pairs = []
            for p in w['scale_pairs']:
                check_pair(p)
                scale_pairs.append(tuple(p['ids']))
            require(scale_pairs == [(i, j) for i in centers for j in boundary], 'scale lineage')
            inc = {name: [pair_id(b, ids) for ids in all_pairs
                          if all(i in membership[name] for i in ids)]
                   for name in ('contained', 'positive')}
            count_contained += len(inc['contained'])
            count_positive += len(inc['positive'])
            yield {'window_id': record['id'], 'body': w, 'both_contained': inc['contained'],
                   'both_positive': inc['positive'],
                   'mask_rule': 'For each endpoint ID, membership in contained/positive/boundary; all pairs in witnesses.jsonl, including zero/one endpoint cases.',
                   'witness_reference': 'witnesses.jsonl'}
        require(seen_windows == expected_windows and
                len(seen_windows) == int(b['counts']['center_specific_windows']), 'complete windows')
    write_rows(dest / 'windows.jsonl', windows())
    write(dest / 'reuse_audit.json', {'unique_positive_pairs': str(len(all_pairs)),
        'catalogue_positive_pair_occurrences': str(len(all_pairs)), 'duplicate_violations': [],
        'reversed_catalogue_occurrences': str(reversals),
        'coincident_distinct_events': [{'witness_id': pair_id(b, ids), 'event_ids': list(ids),
            'times': [ratio(times[i]) for i in ids], 'status': 'COINCIDENT_DISTINCT_EVENTS'} for ids in coincident],
        'windows': str(len(seen_windows)), 'both_contained_occurrences': str(count_contained),
        'both_positive_occurrences': str(count_positive), 'pair_conservation': True,
        'coordinate_repetition_counts_as_witness': False})
    write_rows(dest / 'relation_ratios.jsonl', (
        {'relation_ids': [relation_id(b, a), relation_id(b, c)], 'ratio_b_over_a': ratio(c/a)}
        for a, c in combinations(repeated, 2)))
    write(dest / 'candidate_population.json', {'schema': SCHEMA,
        'object': 'ADMISSIBLE_RECURRENT_TEMPORAL_CANDIDATE_POPULATION',
        'acceptance': 'PENDING_INDEPENDENT_ACCEPTANCE',
        'status': 'PROPOSED_COMPLETE_MEMBERSHIP' if repeated else 'EMPTY_NO_EXACT_RECURRENCE',
        'authority': authority, 'scope': inp['scope'], 'missingness': missing,
        'members': [{'relation_id': relation_id(b, t), 'seconds': ratio(t),
                     'witness_count': str(len(groups[t])),
                     'witness_ids': [pair_id(b, ids) for ids in groups[t]],
                     'distribution': location(t)} for t in repeated],
        'references': {'events': 'events.json', 'witnesses': 'witnesses.jsonl',
                       'dependencies': 'witness_relations.jsonl', 'windows': 'windows.jsonl',
                       'ratios': 'relation_ratios.jsonl', 'relations': 'relations.jsonl'},
        'scientific_status': 'RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED',
        'beat_reference_authorized': False, 'bpm_authorized': False})
    result = {'schema': SCHEMA, 'authority': authority, 'proposed_outcome': outcome,
        'acceptance': 'PENDING_INDEPENDENT_ACCEPTANCE', 'population_classification': population,
        'contract_status': 'CONTRACT_VALID', 'missingness': missing, 'scope': inp['scope'],
        'counts': {'events': str(len(events)), 'positive_witnesses': str(len(all_pairs)),
                   'relations': str(len(groups)), 'repeated_relations': str(len(repeated)),
                   'windows': str(len(seen_windows))}, 'data_files': files_index(dest, DATA),
        'scientific_status': 'RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED',
        'beat_reference_authorized': False, 'bpm_authorized': False}
    write(dest / 'result.json', result)
    return result
