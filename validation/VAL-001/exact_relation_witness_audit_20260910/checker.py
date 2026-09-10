"""Independent all-pairs checker. Never imports the generator or its helpers.

Integer cross-products/gcd implement all time arithmetic here. The shared
transport module supplies JSON, SHA-256 and byte I/O only.
"""
import math
import re
import struct
from functools import total_ordering
from pathlib import Path

from transport import canonical, content_id, files_index, read, rows, write


class Disagreement(ValueError):
    pass


def check(condition, detail):
    if not condition:
        raise Disagreement(detail)


@total_ordering
class Number:
    def __init__(self, n, d=1):
        if d == 0:
            raise Disagreement('zero denominator')
        if d < 0:
            n, d = -n, -d
        divisor = math.gcd(n, d)
        self.n, self.d = n // divisor, d // divisor

    def __eq__(self, other):
        return isinstance(other, Number) and self.n == other.n and self.d == other.d

    def __lt__(self, other):
        return self.n * other.d < other.n * self.d

    def __hash__(self):
        return hash((self.n, self.d))

    def __add__(self, other):
        return Number(self.n * other.d + other.n * self.d, self.d * other.d)

    def __sub__(self, other):
        return Number(self.n * other.d - other.n * self.d, self.d * other.d)

    def __mul__(self, other):
        return Number(self.n * other.n, self.d * other.d)

    def __truediv__(self, other):
        return Number(self.n * other.d, self.d * other.n)

    def __abs__(self):
        return Number(abs(self.n), self.d)

    def json(self):
        return [str(self.n), str(self.d)]


def supplied_ratio(value):
    check(isinstance(value, list) and len(value) == 2, 'rational shape')
    check(all(isinstance(v, str) and re.fullmatch(r'0|-?[1-9][0-9]*', v) for v in value),
          'integer syntax')
    n, d = (int(v) for v in value)
    check(d > 0, 'denominator sign')
    number = Number(n, d)
    check(number.json() == value, 'unreduced rational')
    return number


def producer(record):
    payload = record['producer_bits']
    check(isinstance(payload, str) and re.fullmatch('[0-9a-f]{16}', payload), 'binary64 spelling')
    word = int(payload, 16)
    exponent = (word >> 52) & 2047
    significand = word & ((1 << 52) - 1)
    check(exponent != 2047, 'nonfinite time')
    power = -1074
    if exponent:
        significand += 1 << 52
        power = exponent - 1075
    if word >> 63:
        significand = -significand
    exact = (Number(significand << power) if power >= 0 else
             Number(significand, 1 << (-power)))
    check(supplied_ratio(record['ratio']) == exact, 'bits/ratio mismatch')
    value = struct.unpack('!d', word.to_bytes(8, 'big'))[0]
    check(value.hex() == record['hex'], 'bits/hex mismatch')
    token = record['original_json_numeric_token']
    check(isinstance(token, str) and re.fullmatch(
        r'-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?', token), 'token syntax')
    check(struct.pack('!d', float(token)).hex() == payload, 'token roundtrip mismatch')
    check(bool(record['field_lineage']), 'field provenance absent')
    return exact


def verify(bundle, directory):
    """Rebuild truth from producer events, then check catalogues and every output."""
    b, frozen = bundle['binding'], bundle['input']
    if bundle.get('synthetic_fixture') is True:
        check(len(frozen['events']) <= 16 and b['source_uuid'] !=
              'c46d6cb9-b99c-5bd6-8d81-656dc1ad48ec', 'scientific population in synthetic path')
    else:
        check(bundle.get('admission_receipt', {}).get('authorized_input_sha256') == b['input_freeze_sha256'],
              'unauthorized input')
    zero, two = Number(0), Number(2)
    check(frozen['source_identity'] == b['source_uuid'] and
          frozen['source_authority_id'] == b['source_authority_id'] and
          frozen['source_instance_key'] == b['source_instance_key'] and
          frozen['asset_sha256'] == b['asset_sha256'], 'input lineage')
    event, clock, parents = {}, {}, set()
    for e in frozen['events']:
        check(set(e) == {'eme_id', 'pulse_candidate_id', 'source_identity', 'asset_sha256',
              'timestamp', 'observation_timestamp', 'strength', 'producer_frame',
              'producer_sample_coordinate', 'frame_coordinate_rule'}, 'non-observation event fields')
        eid, parent = e['eme_id'], e['pulse_candidate_id']
        check(isinstance(eid, str) and bool(eid) and eid not in event, 'event identity')
        check(isinstance(parent, str) and bool(parent) and parent not in parents, 'parent identity')
        check(e['source_identity'] == b['source_uuid'] and e['asset_sha256'] == b['asset_sha256'],
              'event/source lineage')
        t = producer(e['timestamp'])
        check(producer(e['observation_timestamp']) == t and
              e['observation_timestamp']['producer_bits'] == e['timestamp']['producer_bits'],
              'EME/observation disagreement')
        producer(e['strength'])
        check(all(k in e for k in ('producer_frame', 'producer_sample_coordinate',
                                   'frame_coordinate_rule')), 'missing frame provenance')
        event[eid], clock[eid] = e, t
        parents.add(parent)
    check(len(event) == int(b['counts']['events']) and
          len(set(clock.values())) == int(b['counts']['distinct_centers']), 'event count')
    origin, low, high = [producer(frozen['scope'][k]) for k in ('origin', 'start', 'end')]
    check(origin == low == zero and low <= high and
          all(low <= v <= high for v in clock.values()), 'scope')
    check(len(bundle['inputs']) == 1, 'input catalogue cardinality')
    input_record = bundle['inputs'][0]
    check(input_record['id'] == content_id(input_record['body']), 'input content hash')
    check(canonical(input_record['body']) == canonical({
        'population': b['population'], 'source': b['source_uuid'], 'asset': b['asset_sha256'],
        'source_authority_id': b['source_authority_id'], 'source_instance_key': b['source_instance_key'],
        'input_manifest_sha256': b['input_freeze_sha256'],
        'canonical_report_sha256': frozen['canonical_report_sha256'],
        'events': frozen['events'], 'scope': frozen['scope'],
        'measurement_authority': 'PRESERVED_ACCEPTED_JGA_OBSERVATIONS_NO_NEW_CALIBRATION',
        'numerical_authority': 'EXACT_ACCEPTED_BINARY64_RECONSTRUCTION'}), 'input catalogue conflict')

    def identity(a, c):
        if c < a:
            a, c = c, a
        return ['EXACT_PAIR_V1', b['input_freeze_sha256'], b['source_uuid'], a, c]
    def relation(t):
        return ['EXACT_RELATION_V1', b['input_freeze_sha256'], b['source_uuid'], t.json()]
    def ends(pair):
        a, c = (clock[i] for i in pair)
        return (a, c) if a <= c else (c, a)
    groups, pair_times, coincident = {}, {}, []
    # Independent nested traversal: no generator catalogue or grouping input.
    ids = sorted(event)
    for right in range(len(ids)):
        for left in range(right):
            pair = ids[left], ids[right]
            a, c = clock[pair[0]], clock[pair[1]]
            t = Number(abs(c.n*a.d - a.n*c.d), c.d*a.d)
            if t == zero:
                coincident.append(pair)
            else:
                groups.setdefault(t, []).append(pair)
                pair_times[pair] = t
    coincident.sort()
    for group in groups.values():
        group.sort()
    check(len(pair_times) + len(coincident) == int(b['counts']['unordered_pairs']) and
          len(groups) == int(b['counts']['positive_period_coordinates']), 'complete pair count')
    refs, observed_pairs, reversed_count = {}, set(), 0
    for entry in bundle['periods']:
        p = entry['body']
        check(entry['id'] == content_id(p), 'period content hash')
        check(p['population'] == b['population'], 'period source population')
        t = supplied_ratio(p['T'])
        check(t in groups and t not in refs and supplied_ratio(p['f']) * t == Number(1),
              'period identity')
        members = []
        for witness in p['pairs']:
            check(len(witness['ids']) == 2, 'witness arity')
            a, c = witness['ids']
            pair = tuple(sorted((a, c)))
            check(pair in pair_times and pair not in observed_pairs, 'duplicate/invalid pair')
            check(pair_times[pair] == t, 'catalogue temporal relation')
            check(witness['times'] == [clock[i].json() for i in (a, c)] and
                  witness['parents'] == [event[i]['pulse_candidate_id'] for i in (a, c)],
                  'catalogue event lineage')
            reversed_count += a > c
            members.append(pair)
            observed_pairs.add(pair)
        check(sorted(members) == groups[t], 'catalogue relation incompleteness')
        zeros = []
        for witness in p['coincident_pairs']:
            check(len(witness['ids']) == 2, 'zero witness arity')
            pair = tuple(sorted(witness['ids']))
            check(pair in coincident and witness['times'] == [clock[i].json() for i in witness['ids']]
                  and witness['parents'] == [event[i]['pulse_candidate_id'] for i in witness['ids']],
                  'coincident lineage')
            zeros.append(pair)
        check(sorted(zeros) == coincident, 'coincident coverage')
        refs[t] = entry['id']
    check(set(refs) == set(groups) and observed_pairs == set(pair_times), 'complete catalogue coverage')
    directory = Path(directory)
    authority = {key: b[key] for key in ('input_freeze_sha256', 'preregistration_sha256',
        'input_authority_sha256', 'implementation_sha256', 'environment_sha256', 'source_uuid',
        'source_authority_id', 'source_instance_key', 'asset_sha256')}
    authority.update(checker_authority='FROZEN_IMPLEMENTATION_BINDING',
                     replay_authority='PREREGISTRATION_SECTION_9')
    missing = {'numerical': [], 'physical_timing_uncertainty': 'NOT_ESTABLISHED',
               'physical_event_independence': 'NOT_ESTABLISHED'}
    schema = 'JGA-EXACT-RELATION-WITNESS-V1'
    totals = {}
    def equal_file(name, expected):
        actual = (directory / name).read_bytes()
        check(actual == canonical(expected) + b'\n', 'output disagreement: ' + name)
        totals[name] = '1'
    def equal_stream(name, expected):
        count = 0
        with (directory / name).open('rb') as handle:
            for wanted in expected:
                check(handle.readline() == canonical(wanted) + b'\n',
                      'output disagreement: ' + name + ':' + str(count))
                count += 1
            check(handle.read(1) == b'', 'extra output records: ' + name)
        totals[name] = str(count)
    def distribution(t):
        ordered = sorted(groups[t], key=lambda p: (*ends(p), p))
        endpoints = sorted(set(clock[i] for p in groups[t] for i in p))
        previous, gaps = None, []
        for p in ordered:
            start = ends(p)[0]
            if previous is not None:
                gaps.append((start-previous).json())
            previous = start
        return {'ordered_witness_ids': [identity(*p) for p in ordered],
                'intervals': [[v.json() for v in ends(p)] for p in ordered],
                'endpoint_times': [v.json() for v in endpoints],
                'extent': [endpoints[0].json(), endpoints[-1].json()], 'successive_start_gaps': gaps}
    equal_file('events.json', {'schema': schema, 'authority': authority, 'scope': frozen['scope'],
        'missingness': missing, 'events': [event[i] for i in sorted(ids, key=lambda i: (clock[i], i))]})
    def expected_relations():
        for t in sorted(groups):
            yield {'relation_id': relation(t), 'seconds': t.json(),
                'witness_ids': [identity(*p) for p in groups[t]], 'witness_count': str(len(groups[t])),
                'catalogue_ids': [refs[t]], 'status': 'SINGLETON' if len(groups[t]) == 1 else 'REPEATED',
                'authority': authority, 'missingness': missing, 'distribution': distribution(t)}
    equal_stream('relations.jsonl', expected_relations())
    def expected_witnesses():
        for t in sorted(groups):
            for pair in groups[t]:
                yield {'witness_id': identity(*pair), 'relation_id': relation(t), 'event_ids': list(pair),
                    'parent_ids': [event[i]['pulse_candidate_id'] for i in pair],
                    'endpoint_times': [clock[i].json() for i in pair], 'seconds': t.json(),
                    'chronological_event_ids': sorted(pair, key=lambda i: (clock[i], i)),
                    'support': [v.json() for v in ends(pair)], 'authority': authority,
                    'catalogue_ids': [refs[t]], 'events_reference': 'events.json',
                    'measurement_authority': 'PRESERVED_ACCEPTED_JGA_OBSERVATIONS_NO_NEW_CALIBRATION'}
    equal_stream('witnesses.jsonl', expected_witnesses())
    def expected_dependencies():
        for t in sorted(groups):
            local = groups[t]
            for a_index in range(len(local)):
                for c_index in range(a_index+1, len(local)):
                    a, c = local[a_index], local[c_index]
                    overlap = sorted(i for i in a if i in c)
                    a0, a1 = ends(a)
                    c0, c1 = ends(c)
                    temporal = ('DISJOINT' if a1 < c0 or c1 < a0 else
                                'TOUCH' if a1 == c0 or c1 == a0 else 'OVERLAP')
                    yield {'relation_id': relation(t), 'witness_ids': [identity(*a), identity(*c)],
                        'shared_event_ids': overlap, 'dependence': 'SHARED_ENDPOINT' if overlap else 'EVENT_DISJOINT',
                        'temporal_relation': temporal, 'statistical_independence': 'NOT_ESTABLISHED'}
    equal_stream('witness_relations.jsonl', expected_dependencies())

    expected_geometry = set()
    for center in clock.values():
        for boundary in clock.values():
            if center != boundary:
                expected_geometry.add((center, abs(boundary-center)*two))
    seen_geometry, contained_total, positive_total = set(), 0, 0
    def expected_windows():
        nonlocal contained_total, positive_total
        previous = None
        for entry in bundle['windows']:
            w = entry['body']
            check(entry['id'] == content_id(w) and w['population'] == b['population'], 'window authority')
            u, length = supplied_ratio(w['u']), supplied_ratio(w['L'])
            key = u, length
            check(key in expected_geometry and key not in seen_geometry and
                  (previous is None or previous < key), 'window population/order')
            previous = key
            seen_geometry.add(key)
            lower, upper = u-length/two, u+length/two
            clip_low, clip_high = max(low, lower), min(high, upper)
            centers, boundaries, contained, positive = [], [], [], []
            for i in ids:
                if clock[i] == u:
                    centers.append(i)
                if abs(clock[i]-u)*two == length:
                    boundaries.append(i)
                if clip_low <= clock[i] <= clip_high:
                    contained.append(i)
                if lower < clock[i] < upper:
                    positive.append(i)
            scales = [{'ids': [a, c], 'times': [clock[a].json(), clock[c].json()],
                       'parents': [event[a]['pulse_candidate_id'], event[c]['pulse_candidate_id']]}
                      for a in centers for c in boundaries]
            gaps = []
            if lower < clip_low:
                gaps.append({'ends': [lower.json(), clip_low.json()], 'closed': [True, False]})
            if clip_high < upper:
                gaps.append({'ends': [clip_high.json(), upper.json()], 'closed': [False, True]})
            expected_body = {'population': b['population'], 'u': u.json(), 'L': length.json(),
                'center_ids': centers, 'scale_pairs': scales,
                'membership': {'contained': contained, 'positive': positive, 'boundary': boundaries},
                'requested': [lower.json(), upper.json()],
                'asset_clipped': [clip_low.json(), clip_high.json()],
                'available': [clip_low.json(), clip_high.json()],
                'asset_unavailable': gaps, 'unavailable': gaps,
                'asset_truncated': lower != clip_low or upper != clip_high, 'scope_truncated': False}
            check(w == expected_body, 'independent window geometry/lineage')
            ci, pi = [], []
            for a, c in sorted(pair_times):
                if a in contained and c in contained:
                    ci.append(identity(a, c))
                if a in positive and c in positive:
                    pi.append(identity(a, c))
            contained_total += len(ci)
            positive_total += len(pi)
            yield {'window_id': entry['id'], 'body': expected_body,
                'both_contained': ci, 'both_positive': pi,
                'mask_rule': 'For each endpoint ID, membership in contained/positive/boundary; all pairs in witnesses.jsonl, including zero/one endpoint cases.',
                'witness_reference': 'witnesses.jsonl'}
        check(seen_geometry == expected_geometry and
              len(seen_geometry) == int(b['counts']['center_specific_windows']), 'window completeness')
    equal_stream('windows.jsonl', expected_windows())
    equal_file('reuse_audit.json', {'unique_positive_pairs': str(len(pair_times)),
        'catalogue_positive_pair_occurrences': str(len(pair_times)), 'duplicate_violations': [],
        'reversed_catalogue_occurrences': str(reversed_count),
        'coincident_distinct_events': [{'witness_id': identity(*p), 'event_ids': list(p),
            'times': [clock[i].json() for i in p], 'status': 'COINCIDENT_DISTINCT_EVENTS'} for p in coincident],
        'windows': str(len(seen_geometry)), 'both_contained_occurrences': str(contained_total),
        'both_positive_occurrences': str(positive_total), 'pair_conservation': True,
        'coordinate_repetition_counts_as_witness': False})
    repeated = sorted(t for t, witnesses in groups.items() if len(witnesses) > 1)
    def expected_ratios():
        for i, a in enumerate(repeated):
            for c in repeated[i+1:]:
                yield {'relation_ids': [relation(a), relation(c)], 'ratio_b_over_a': (c/a).json()}
    equal_stream('relation_ratios.jsonl', expected_ratios())
    equal_file('candidate_population.json', {'schema': schema,
        'object': 'ADMISSIBLE_RECURRENT_TEMPORAL_CANDIDATE_POPULATION',
        'acceptance': 'PENDING_INDEPENDENT_ACCEPTANCE',
        'status': 'EMPTY_NO_EXACT_RECURRENCE' if not repeated else 'PROPOSED_COMPLETE_MEMBERSHIP',
        'authority': authority, 'scope': frozen['scope'], 'missingness': missing,
        'members': [{'relation_id': relation(t), 'seconds': t.json(),
                     'witness_count': str(len(groups[t])), 'witness_ids': [identity(*p) for p in groups[t]],
                     'distribution': distribution(t)} for t in repeated],
        'references': {'events': 'events.json', 'witnesses': 'witnesses.jsonl',
            'dependencies': 'witness_relations.jsonl', 'windows': 'windows.jsonl',
            'ratios': 'relation_ratios.jsonl', 'relations': 'relations.jsonl'},
        'scientific_status': 'RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED',
        'beat_reference_authorized': False, 'bpm_authorized': False})
    data_names = ('events.json', 'relations.jsonl', 'witnesses.jsonl', 'witness_relations.jsonl',
                  'windows.jsonl', 'reuse_audit.json', 'relation_ratios.jsonl', 'candidate_population.json')
    outcome = ('NO_EXACT_RELATION_RECURRENCE_OBSERVED' if len(repeated) == 0 else
               'EXACT_RELATION_RECURRENCE_OBSERVED')
    population = {0: 'NO_REPEATED_EXACT_RELATIONS', 1: 'ONE_REPEATED_EXACT_RELATION'}.get(
        len(repeated), 'MULTIPLE_REPEATED_EXACT_RELATIONS')
    equal_file('result.json', {'schema': schema, 'authority': authority, 'proposed_outcome': outcome,
        'acceptance': 'PENDING_INDEPENDENT_ACCEPTANCE', 'population_classification': population,
        'contract_status': 'CONTRACT_VALID', 'missingness': missing, 'scope': frozen['scope'],
        'counts': {'events': str(len(event)), 'positive_witnesses': str(len(pair_times)),
                  'relations': str(len(groups)), 'repeated_relations': str(len(repeated)),
                  'windows': str(len(seen_geometry))}, 'data_files': files_index(directory, data_names),
        'scientific_status': 'RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED',
        'beat_reference_authorized': False, 'bpm_authorized': False})
    report = {'schema': schema, 'authority': authority, 'status': 'CONTRACT_VALID',
        'acceptance': 'PENDING_REPLAY', 'independent_proposed_outcome': outcome,
        'asserted_record_counts': totals, 'discrepancies': [],
        'generator_files': files_index(directory, (*data_names, 'result.json')),
        'derivation': 'PRODUCER_BITS_INTEGER_CROSS_PRODUCTS_ALL_UNORDERED_EVENT_PAIRS'}
    write(directory / 'checker.json', report)
    return report
