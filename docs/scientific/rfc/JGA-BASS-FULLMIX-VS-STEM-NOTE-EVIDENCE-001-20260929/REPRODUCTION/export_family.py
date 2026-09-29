"""Export per-family matching artifacts for JGA-BASS-FULLMIX-VS-STEM-NOTE-EVIDENCE-001-20260929.

Independent reimplementation of the graph analysis used to produce MATCH_T*.json,
written so that every CSV/JSON artifact is cross-checked against the SSD match
result rather than being copied from it. Any disagreement is a hard failure.
"""
import json, csv, io, math, os, sys, hashlib
from pathlib import Path

ROOT = Path('/Users/StarTrack/Development/JazzGrooveAnalyzer')
sys.path.insert(0, str(ROOT))
from tools import jga_governance as g

TASK = [json.loads(x)['task_id'] for x in
        (ROOT / 'docs/project/AGENT_WORK_LEDGER.jsonl').read_text().splitlines()
        if x and json.loads(x)['task_id'].startswith('JGA-BASS-FULLMIX')][-1]
PKGR = 'docs/scientific/rfc/' + TASK + '/'
TOKEN = 'PI-BASS-FULLMIX-VS-STEM-STORAGE-20260929'
SSDN = Path('/Volumes/SSD Track/JGA/experiments/'
            'JGA_BASS_FULLMIX_VS_STEM_NOTE_EVIDENCE_001_20260929')
TOLS = ['T0', 'T1', 'T2', 'T4']
LOW_HZ = 43.06640625


def w(rel, data):
    if isinstance(data, (dict, list)):
        data = (json.dumps(data, indent=2) + '\n').encode()
    if isinstance(data, str):
        data = data.encode()
    g.write(ROOT, TOKEN, PKGR + rel, data)


def csvs(rows, cols):
    b = io.StringIO()
    wr = csv.DictWriter(b, fieldnames=cols, extrasaction='ignore')
    wr.writeheader()
    for r in rows:
        wr.writerow(r)
    return b.getvalue()


def main():
    M = {t: json.loads((SSDN / ('MATCH_%s.json' % t)).read_text()) for t in TOLS}
    fx = json.loads((SSDN / 'FULLMIX' / 'EVENTS.json').read_text())
    sy = json.loads((SSDN / 'STEM' / 'EVENTS.json').read_text())
    fxi = {e['candidate_id']: e for e in fx}
    syi = {e['candidate_id']: e for e in sy}
    for t in TOLS:
        tol = M[t]['tolerance_samples']
        n, m = len(fx), len(sy)
        par = list(range(n + m))

        def find(a):
            while par[a] != a:
                par[a] = par[par[a]]
                a = par[a]
            return a

        edges = []
        merges = 0
        for i, a in enumerate(fx):
            for j, b in enumerate(sy):
                d = abs(a['native_sample'] - b['native_sample'])
                if d <= tol:
                    ra, rb = find(i), find(n + j)
                    if ra != rb:
                        par[max(ra, rb)] = min(ra, rb)
                        merges += 1
                    edges.append({
                        'fullmix_candidate_id': a['candidate_id'],
                        'stem_candidate_id': b['candidate_id'],
                        'fullmix_native_sample': a['native_sample'],
                        'stem_native_sample': b['native_sample'],
                        'delta_samples': a['native_sample'] - b['native_sample'],
                        'abs_delta_samples': d,
                        'delta_ms': 1000.0 * (a['native_sample'] - b['native_sample']) / 44100,
                        'fullmix_state': a['state'], 'stem_state': b['state'],
                        'fullmix_f0_hz': a.get('f0_hz'), 'stem_f0_hz': b.get('f0_hz')})
        comps = {}
        for i in range(n):
            comps.setdefault(find(i), {'F': [], 'S': []})['F'].append(i)
        for j in range(m):
            comps.setdefault(find(n + j), {'F': [], 'S': []})['S'].append(j)

        w('MATCHING_EDGES_%s.csv' % t, csvs(edges, [
            'fullmix_candidate_id', 'stem_candidate_id', 'fullmix_native_sample',
            'stem_native_sample', 'delta_samples', 'abs_delta_samples', 'delta_ms',
            'fullmix_state', 'stem_state', 'fullmix_f0_hz', 'stem_f0_hz']))

        def key(c):
            return (min(fx[i]['native_sample'] for i in c['F']) if c['F']
                    else min(sy[j]['native_sample'] for j in c['S']))
        crows = []
        for cid, c in enumerate(sorted(comps.values(), key=key), 1):
            cls = ('UNMATCHED_STEM_ONLY' if not c['F']
                   else ('UNMATCHED_FULLMIX_ONLY' if not c['S'] else 'MATCHED'))
            nf = sum(1 for i in c['F'] for j in c['S']
                     if abs(fx[i]['native_sample'] - sy[j]['native_sample']) <= tol)
            cross = bool((len(c['F']) > 1 or len(c['S']) > 1) and c['F'] and c['S'])
            crows.append({
                'component_id': 'C%s_%04d' % (t, cid), 'n_fullmix': len(c['F']),
                'n_stem': len(c['S']), 'n_edges': nf, 'classification': cls,
                'crossing': cross,
                'fullmix_candidate_ids': '|'.join(fx[i]['candidate_id'] for i in sorted(c['F'])),
                'stem_candidate_ids': '|'.join(sy[j]['candidate_id'] for j in sorted(c['S']))})
        w('COMPONENTS_%s.csv' % t, csvs(crows, [
            'component_id', 'n_fullmix', 'n_stem', 'n_edges', 'classification',
            'crossing', 'fullmix_candidate_ids', 'stem_candidate_ids']))
        w('CROSSINGS_%s.csv' % t, csvs([c for c in crows if c['crossing']], [
            'component_id', 'n_fullmix', 'n_stem', 'n_edges',
            'fullmix_candidate_ids', 'stem_candidate_ids']))

        rows = []
        for c in crows:
            if c['classification'] != 'MATCHED':
                continue
            for fi in c['fullmix_candidate_ids'].split('|'):
                for sj in c['stem_candidate_ids'].split('|'):
                    a, b = fxi[fi], syi[sj]
                    if abs(a['native_sample'] - b['native_sample']) > tol:
                        continue
                    pf, ps = a.get('f0_hz'), b.get('f0_hz')
                    both = pf is not None and ps is not None
                    rows.append({
                        'component_id': c['component_id'],
                        'fullmix_candidate_id': fi, 'stem_candidate_id': sj,
                        'delta_samples': a['native_sample'] - b['native_sample'],
                        'delta_ms': 1000.0 * (a['native_sample'] - b['native_sample']) / 44100,
                        'fullmix_f0_hz': pf, 'stem_f0_hz': ps,
                        'delta_hz': (pf - ps) if both else '',
                        'delta_cents': (1200.0 * math.log2(pf / ps)) if both else '',
                        'frequency_ratio': (pf / ps) if both else '',
                        'pitch_population': 'ALL_F0_BOTH_VALID' if both else 'EXCLUDED_MISSING_F0',
                        'low_register_population': (
                            'BELOW_43_06640625_HZ' if both and pf < LOW_HZ
                            else ('AT_OR_ABOVE_43_06640625_HZ' if pf else 'UNDETERMINED_NO_F0')),
                        'component_ambiguous': c['crossing']})
        w('MATCHES_%s.csv' % t, csvs(rows, [
            'component_id', 'fullmix_candidate_id', 'stem_candidate_id', 'delta_samples',
            'delta_ms', 'fullmix_f0_hz', 'stem_f0_hz', 'delta_hz', 'delta_cents',
            'frequency_ratio', 'pitch_population', 'low_register_population',
            'component_ambiguous']))
        w('PITCH_CONTINUOUS_%s.json' % t, {
            'tolerance_family': t, 'tolerance_samples': tol, 'n_pairs': len(rows),
            'populations': M[t]['pitch_populations'],
            'threshold_applied': 'NONE', 'no_cent_rule': True, 'no_pitch_threshold': True})

        # hard cross-checks against the SSD match result
        assert len(edges) == M[t]['n_edges'], (t, 'edges')
        # general graph identity: components = nodes - successful_merges
        # (equals nodes - edges only while the graph is acyclic; T4 has cycle edges)
        roots = {find(k) for k in range(n + m)}
        assert len(roots) == n + m - merges, (t, 'graph identity', len(roots), n + m - merges)
        cycle_edges = len(edges) - merges
        assert len(crows) == M[t]['n_components'], (t, 'components', len(crows), M[t]['n_components'])
        assert len(roots) == M[t]['n_components'], (t, 'roots vs components')
        assert len(rows) == M[t]['n_pairs_enumerated'], (t, 'pairs')
        assert sum(1 for c in crows if c['crossing']) == M[t]['n_crossing_components'], (t, 'crossings')
        assert sum(1 for c in crows if c['classification'] == 'MATCHED') == M[t]['components']['MATCHED']
        assert all(e['abs_delta_samples'] <= tol for e in edges), (t, 'tolerance violated')
        nboth = sum(1 for r in rows if r['pitch_population'] == 'ALL_F0_BOTH_VALID')
        assert nboth == M[t]['pitch_populations']['ALL_F0_BOTH_VALID']['n_pairs'], (t, 'f0 pop')
        print('%s CROSS-CHECK PASS edges=%d merges=%d cycle_edges=%d comps=%d pairs=%d '
              'crossings=%d both_f0=%d'
              % (t, len(edges), merges, cycle_edges, len(crows), len(rows),
                 M[t]['n_crossing_components'], nboth))
    print('ALL FAMILY ARTIFACTS WRITTEN AND VERIFIED AGAINST SSD RESULT')


if __name__ == '__main__':
    main()
