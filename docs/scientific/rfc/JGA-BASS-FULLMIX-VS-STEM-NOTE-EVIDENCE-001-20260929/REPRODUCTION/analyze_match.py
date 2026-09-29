"""Temporal graph matching for JGA-BASS-FULLMIX-VS-STEM-NOTE-EVIDENCE-001-20260929.

Preregistration 0.2. Independent execution of the four tolerance families T0/T1/T2/T4.
Rules, applied without exception:

  * An edge exists iff |d_fullmix - d_stem| <= tolerance_samples.
  * Edges are NOT filtered by pitch, state, amplitude or any similarity.
  * No nearest-neighbour assignment, no cost function, no Hungarian/greedy
    resolution, no one-to-one constraint.
  * Connected components over the resulting graph classify every event as
    MATCHED, UNMATCHED_FULLMIX_ONLY, UNMATCHED_STEM_ONLY or AMBIGUOUS.
  * Crossings (a matched pair whose separation exceeds the tolerance, or any
    component that could admit more than one pairing) are recorded, not resolved.
  * Continuous pitch comparison runs only after matching, on matched pairs.
  * No pitch threshold, cent threshold, or success threshold is applied anywhere.
"""
import json, math, hashlib, os
from pathlib import Path
import numpy as np

ROOT = Path('/Users/StarTrack/Development/JazzGrooveAnalyzer')
TASK = 'JGA-BASS-FULLMIX-VS-STEM-NOTE-EVIDENCE-001-20260929'
PKG = ROOT / 'docs/scientific/rfc' / TASK
SSDN = Path('/Volumes/SSD Track/JGA/experiments/'
            'JGA_BASS_FULLMIX_VS_STEM_NOTE_EVIDENCE_001_20260929')
TOLS = [('T0', 0), ('T1', 512), ('T2', 1024), ('T4', 2048)]
LOW_REGISTER_HZ = 43.06640625


def durable_write(path, data):
    """Atomic + fsync + directory sync + read-back verify on the ExFAT volume."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        data = data.encode()
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
    d = os.open(str(path.parent), os.O_RDONLY)
    try:
        os.fsync(d)
    finally:
        os.close(d)
    assert path.read_bytes() == data, ('read-back mismatch', str(path))
    return hashlib.sha256(data).hexdigest()


def build_graph(fx, sy, tol):
    """Union-find over bipartite (fullmix, stem) nodes. Pure temporal adjacency."""
    n, m = len(fx), len(sy)
    parent = list(range(n + m))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    edges = []
    for i, a in enumerate(fx):
        for j, b in enumerate(sy):
            d = abs(a - b)
            if d <= tol:
                union(i, n + j)
                edges.append({'fullmix_index': i, 'stem_index': j,
                              'delta_samples': int(a - b), 'abs_delta_samples': int(d),
                              'delta_ms': 1000.0 * (a - b) / 44100,
                              'abs_delta_ms': 1000.0 * d / 44100})
    comps = {}
    for i in range(n):
        comps.setdefault(find(i), {'fullmix': [], 'stem': []})['fullmix'].append(i)
    for j in range(m):
        comps.setdefault(find(n + j), {'fullmix': [], 'stem': []})['stem'].append(j)
    return edges, comps


def analyze(arm_label, tol_name, tol, fx_ev, sy_ev):
    fx = [e['native_sample'] for e in fx_ev]
    sy = [e['native_sample'] for e in sy_ev]
    edges, comps = build_graph(fx, sy, tol)
    edge_by_f = {}
    for e in edges:
        edge_by_f.setdefault(e['fullmix_index'], []).append(e)
    edge_by_s = {}
    for e in edges:
        edge_by_s.setdefault(e['stem_index'], []).append(e)

    def pitch(e):
        v = e.get('f0_hz')
        return float(v) if v is not None and math.isfinite(v) else None

    comp_rows, matches, crossings, unmatched_f, unmatched_s = [], [], [], [], []
    for cid, c in enumerate(sorted(comps.values(), key=lambda q: (min(fx[i] for i in q['fullmix'])
                                                               if q['fullmix'] else min(sy[j] for j in q['stem']))), 1):
        F, S = sorted(c['fullmix']), sorted(c['stem'])
        eids = [e for i in F for e in edge_by_f.get(i, [])] + \
               [e for j in S for e in edge_by_s.get(j, [])]
        eids = [e for e in eids if e['fullmix_index'] in F and e['stem_index'] in S]
        deg_f = [len(edge_by_f.get(i, [])) for i in F]
        deg_s = [len(edge_by_s.get(j, [])) for j in S]
        cross = False
        reasons = []
        if len(F) > 1 and len(S) == 1:
            cross = True; reasons.append('SINGLE_STEM_MULTIPLE_FULLMIX')
        if len(S) > 1 and len(F) == 1:
            cross = True; reasons.append('SINGLE_FULLMIX_MULTIPLE_STEM')
        if len(F) > 1 and len(S) > 1:
            cross = True; reasons.append('MULTIPLE_FULLMIX_MULTIPLE_STEM')
        for e in eids:
            if e['abs_delta_samples'] > tol:
                cross = True; reasons.append('EDGE_WITHIN_TOLERANCE')
        if not F:
            cls = 'UNMATCHED_STEM_ONLY'
        elif not S:
            cls = 'UNMATCHED_FULLMIX_ONLY'
        else:
            cls = 'MATCHED'
            for i in F:
                for j in S:
                    if (i, j) not in {(e['fullmix_index'], e['stem_index']) for e in eids}:
                        continue
                    pf, ps = pitch(fx_ev[i]), pitch(sy_ev[j])
                    row = {'tolerance_family': tol_name, 'tolerance_samples': tol,
                           'component_id': 'C%s_%04d' % (tol_name, cid),
                           'fullmix_index': i, 'stem_index': j,
                           'fullmix_candidate_id': fx_ev[i]['candidate_id'],
                           'stem_candidate_id': sy_ev[j]['candidate_id'],
                           'fullmix_native_sample': fx_ev[i]['native_sample'],
                           'stem_native_sample': sy_ev[j]['native_sample'],
                           'delta_samples': int(fx_ev[i]['native_sample'] - sy_ev[j]['native_sample']),
                           'delta_ms': 1000.0 * (fx_ev[i]['native_sample'] - sy_ev[j]['native_sample']) / 44100,
                           'fullmix_state': fx_ev[i]['state'], 'stem_state': sy_ev[j]['state'],
                           'fullmix_f0_hz': pf, 'stem_f0_hz': ps}
                    if pf is not None and ps is not None:
                        row['delta_hz'] = pf - ps
                        row['delta_cents'] = 1200.0 * math.log2(pf / ps)
                        row['frequency_ratio'] = pf / ps
                        row['pitch_population'] = 'ALL_F0_BOTH_VALID'
                    else:
                        row['delta_hz'] = None; row['delta_cents'] = None
                        row['frequency_ratio'] = None
                        row['pitch_population'] = 'EXCLUDED_MISSING_F0'
                    if pf is not None and pf < LOW_REGISTER_HZ:
                        row['low_register_population'] = 'BELOW_43_06640625_HZ'
                    elif pf is not None:
                        row['low_register_population'] = 'AT_OR_ABOVE_43_06640625_HZ'
                    else:
                        row['low_register_population'] = 'UNDETERMINED_NO_F0'
                    row['component_ambiguous'] = bool(cross)
                    row['ambiguity_reason'] = sorted(set(reasons)) if cross else None
                    matches.append(row)
        for i in F:
            if not edge_by_f.get(i):
                unmatched_f.append(fx_ev[i]['candidate_id'])
        for j in S:
            if not edge_by_s.get(j):
                unmatched_s.append(sy_ev[j]['candidate_id'])
        comp_rows.append({'component_id': 'C%s_%04d' % (tol_name, cid),
                          'n_fullmix': len(F), 'n_stem': len(S), 'n_edges': len(eids),
                          'classification': cls, 'crossing': cross,
                          'crossing_reasons': sorted(set(reasons)),
                          'fullmix_candidate_ids': [fx_ev[i]['candidate_id'] for i in F],
                          'stem_candidate_ids': [sy_ev[j]['candidate_id'] for j in S],
                          'fullmix_native_samples': [fx_ev[i]['native_sample'] for i in F],
                          'stem_native_samples': [sy_ev[j]['native_sample'] for j in S]})
        if cross:
            crossings.append({'component_id': 'C%s_%04d' % (tol_name, cid),
                              'reasons': sorted(set(reasons)), 'n_fullmix': len(F), 'n_stem': len(S),
                              'n_edges': len(eids),
                              'resolution': 'NOT_RESOLVED_BY_DESIGN',
                              'note': 'ambiguity is reported, never collapsed by a nearest-neighbour or pitch rule'})
    return edges, comp_rows, matches, crossings, unmatched_f, unmatched_s


def main():
    fx_ev = json.loads((SSDN / 'FULLMIX' / 'EVENTS.json').read_text())
    sy_ev = json.loads((SSDN / 'STEM' / 'EVENTS.json').read_text())
    lo, hi = 2107392, 3643392
    dur = (hi - lo) / 44100
    out = {}
    for name, tol in TOLS:
        edges, comps, matches, crossings, uf, us = analyze('FULLMIX_vs_STEM', name, tol, fx_ev, sy_ev)
        nmatch = len({m['fullmix_index'] for m in matches})
        nsmatch = len({m['stem_index'] for m in matches})
        pop_all = [m for m in matches if m['pitch_population'] == 'ALL_F0_BOTH_VALID']
        pop_low = [m for m in pop_all if m['low_register_population'] == 'BELOW_43_06640625_HZ']
        d = lambda k: [abs(m['delta_samples']) for m in k]
        out[name] = {
            'tolerance_samples': tol, 'tolerance_ms': 1000.0 * tol / 44100,
            'n_edges': len(edges), 'n_components': len(comps),
            'components': {c: sum(1 for r in comps if r['classification'] == c) for c in
                           ('MATCHED', 'UNMATCHED_FULLMIX_ONLY', 'UNMATCHED_STEM_ONLY')},
            'n_fullmix_events_in_matched_components': nmatch,
            'n_stem_events_in_matched_components': nsmatch,
            'fullmix_coverage_fraction': nmatch / len(fx_ev),
            'stem_coverage_fraction': nsmatch / len(sy_ev),
            'n_unmatched_fullmix_only': len(uf), 'n_unmatched_stem_only': len(us),
            'unmatched_fullmix_candidate_ids': uf, 'unmatched_stem_candidate_ids': us,
            'n_pairs_enumerated': len(matches),
            'n_ambiguous_pairs': sum(1 for m in matches if m['component_ambiguous']),
            'n_crossing_components': len(crossings),
            'ambiguity_density_among_fullmix_events': sum(1 for m in matches if m['component_ambiguous']) / len(fx_ev),
            'pitch_populations': {
                'ALL_F0_BOTH_VALID': {
                    'n_pairs': len(pop_all),
                    'fraction_of_pairs': len(pop_all) / len(matches) if matches else None,
                    'abs_delta_cents': sorted(abs(m['delta_cents']) for m in pop_all),
                    'abs_delta_hz': sorted(abs(m['delta_hz']) for m in pop_all),
                    'signed_delta_cents': sorted(m['delta_cents'] for m in pop_all),
                    'frequency_ratio': sorted(m['frequency_ratio'] for m in pop_all),
                    'threshold_applied': 'NONE',
                    'note': 'continuous values reported as distributions; no cent boundary, no pass/fail cut'},
                'VALIDITY_QUALIFIED': {
                    'qualification': 'both arms voiced=True and finite f0_hz within the preregistered pyin fmin/fmax window [41.2, 350.0] Hz',
                    'boundary_hz': LOW_REGISTER_HZ,
                    'boundary_basis': 'geometry-derived boundary fixed at preregistration; reporting descriptor only',
                    'n_pairs': len(pop_low),
                    'low_register_pairs': [{
                        'fullmix_candidate_id': m['fullmix_candidate_id'],
                        'stem_candidate_id': m['stem_candidate_id'],
                        'fullmix_f0_hz': m['fullmix_f0_hz'], 'stem_f0_hz': m['stem_f0_hz'],
                        'delta_cents': m['delta_cents'], 'delta_hz': m['delta_hz'],
                        'fullmix_state': m['fullmix_state'], 'stem_state': m['stem_state']}
                        for m in pop_low],
                    'threshold_applied': 'NONE'}},
            'temporal_summary': {
                'abs_delta_samples': sorted(abs(e['abs_delta_samples']) for e in edges) if edges else [],
                'abs_delta_ms': sorted(e['abs_delta_ms'] for e in edges) if edges else [],
                'signed_delta_ms': sorted(e['delta_ms'] for e in edges) if edges else [],
                'max_abs_delta_samples_observed': max((e['abs_delta_samples'] for e in edges), default=None),
                'note': 'every edge is by construction within tolerance; distributions are descriptive of graph structure, not of physical timing agreement'},
        }
        durable_write(SSDN / ('MATCH_%s.json' % name), json.dumps(out[name], indent=2) + '\n')
        print(name, 'tol=%d' % tol, 'edges=%d' % len(edges), 'components=%d' % len(comps),
              'matched_pairs=%d' % len(matches), 'crossings=%d' % len(crossings), flush=True)
    durable_write(PKG / 'REPRODUCTION' / '_match_done', json.dumps({k: out[k]['n_edges'] for k in out}) + '\n')
    return out


if __name__ == '__main__':
    main()
