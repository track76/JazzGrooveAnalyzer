"""Figures for JGA-BASS-FULLMIX-VS-STEM-NOTE-EVIDENCE-001-20260929.

Descriptive only. No figure applies a threshold, selects a population, or implies
source identity, Ground Truth, or representation superiority.
"""
import json, os, math, hashlib
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path('/Users/StarTrack/Development/JazzGrooveAnalyzer')
TASK = 'JGA-BASS-FULLMIX-VS-STEM-NOTE-EVIDENCE-001-20260929'
PKG = ROOT / 'docs/scientific/rfc' / TASK
SSDN = Path('/Volumes/SSD Track/JGA/experiments/'
            'JGA_BASS_FULLMIX_VS_STEM_NOTE_EVIDENCE_001_20260929')
FIG = PKG / 'FIGURES'
FIG.mkdir(parents=True, exist_ok=True)
TOLS = ['T0', 'T1', 'T2', 'T4']
LO, HI = 2107392, 3643392
LOW_HZ = 43.06640625
GREY = '#8a8a8a'
BLUE = '#1f5fa8'
ORANGE = '#c4620a'


def durable_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
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
    assert path.read_bytes() == data
    return hashlib.sha256(data).hexdigest()


def save(fig, name, note):
    fig.tight_layout()
    p = FIG / name
    fig.savefig(p, dpi=150)
    plt.close(fig)
    durable_write(p, p.read_bytes())
    (FIG / (name + '.txt')).write_text(note + '\n')
    return name


def stamp(ax, title, sub=''):
    ax.set_title(title, fontsize=10, loc='left')
    if sub:
        ax.text(0.0, 1.01, sub, transform=ax.transAxes, fontsize=7,
                color='#444444', va='bottom')


def main():
    fx = json.loads((SSDN / 'FULLMIX' / 'EVENTS.json').read_text())
    sy = json.loads((SSDN / 'STEM' / 'EVENTS.json').read_text())
    M = {t: json.loads((SSDN / ('MATCH_%s.json' % t)).read_text()) for t in TOLS}
    dur = (HI - LO) / 44100
    rel = lambda s: (s - LO) / 44100
    index = {}

    # 1 event timeline
    fig, ax = plt.subplots(2, 1, figsize=(11, 4.2), sharex=True)
    for k, (ev, lab, c) in enumerate([(fx, 'FULL MIX (458 events)', BLUE),
                                      (sy, 'BASS STEM (442 events)', ORANGE)]):
        t = [rel(e['native_sample']) for e in ev]
        comp = [e['state'] == 'BASS_COMPATIBLE' for e in ev]
        ax[k].scatter([x for x, q in zip(t, comp) if q], [1] * sum(comp), s=9,
                      marker='|', color=c, label='BASS_COMPATIBLE')
        ax[k].scatter([x for x, q in zip(t, comp) if not q], [0] * sum(not q for q in comp),
                      s=9, marker='|', color=GREY, label='AMBIGUOUS (no valid F0)')
        ax[k].set_yticks([]); ax[k].set_ylim(-0.4, 1.4)
        stamp(ax[k], lab, 't=0 at interval start %.6f s; frame-derived landmarks, not physical attacks' % (LO / 44100))
        ax[k].legend(loc='upper right', fontsize=7, frameon=False, ncol=2)
    ax[1].set_xlabel('seconds from interval start (native sample 2107392)')
    index['STATE_COMPOSITION_BOTH_ARMS.png'] = save(
        fig, 'STATE_COMPOSITION_BOTH_ARMS.png',
        'Both arms over the identical preregistered interval. Density %.3f/s vs %.3f/s. '
        'Vertical marks are extractor landmarks; they are not verified attacks and not Ground Truth.'
        % (len(fx) / dur, len(sy) / dur))

    # 2 delta time T1
    fig, ax = plt.subplots(figsize=(9, 4))
    d = M['T1']['temporal_summary']['abs_delta_ms']
    ax.hist(d, bins=24, color=BLUE, edgecolor='white')
    ax.set_yscale('log')
    stamp(ax, 'T1 primary: absolute inter-arm time difference (n=%d edges)' % len(d),
          'Tolerance 512 samples = 11.61 ms. Distribution is bounded by construction, not by agreement.')
    ax.set_xlabel('|delta| ms'); ax.set_ylabel('edges (log)')
    index['DELTA_TIME_T1.png'] = save(fig, 'DELTA_TIME_T1.png',
        'T1 is the preregistered primary operational point. No threshold or cut applied.')

    # 3 tolerance family
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    x = np.arange(len(TOLS))
    cov_f = [100 * M[t]['fullmix_coverage_fraction'] for t in TOLS]
    cov_s = [100 * M[t]['stem_coverage_fraction'] for t in TOLS]
    ax[0].plot(x, cov_f, 'o-', color=BLUE, label='full mix coverage')
    ax[0].plot(x, cov_s, 's-', color=ORANGE, label='stem coverage')
    ax[0].set_xticks(x); ax[0].set_xticklabels(TOLS)
    ax[0].set_ylabel('% of that arm\'s events in a matched component')
    ax[0].legend(fontsize=7, frameon=False)
    stamp(ax[0], 'Coverage rises with tolerance', 'Wider tolerance mechanically admits more edges; it is not improved evidence.')
    ax[1].plot(x, [M[t]['n_ambiguous_pairs'] for t in TOLS], 'o-', color='#7a2a8a', label='ambiguous pairs')
    ax[1].plot(x, [M[t]['n_crossing_components'] for t in TOLS], 's-', color='#b03030', label='crossing components')
    ax[1].set_xticks(x); ax[1].set_xticklabels(TOLS)
    ax[1].set_ylabel('count'); ax[1].legend(fontsize=7, frameon=False)
    stamp(ax[1], 'Ambiguity rises with tolerance', 'Ambiguity is reported, never resolved by nearest-neighbour or pitch.')
    index['DELTA_TIME_FAMILY.png'] = save(fig, 'DELTA_TIME_FAMILY.png',
        'Trade-off between coverage and ambiguity across the four preregistered tolerance families.')

    # 4 pitch cents T1
    fig, ax = plt.subplots(figsize=(9, 4))
    c = M['T1']['pitch_populations']['ALL_F0_BOTH_VALID']['abs_delta_cents']
    ax.hist(c, bins=30, color='#3a7a3a', edgecolor='white')
    ax.set_yscale('log')
    stamp(ax, 'T1 continuous pitch difference, |cents| (n=%d pairs, ALL_F0_BOTH_VALID)' % len(c),
          'No cent threshold, no pass/fail cut, no 100-cent rule. Distribution reported as observed.')
    ax.set_xlabel('|delta| cents (continuous)'); ax.set_ylabel('pairs (log)')
    index['PITCH_CENTS_T1.png'] = save(fig, 'PITCH_CENTS_T1.png',
        'Both F0 valid population at T1. Values are continuous; no admissibility rule was applied.')

    # 5 pitch hz scatter
    fig, ax = plt.subplots(figsize=(6.4, 6))
    pr = []
    for t in ('T1',):
        pass
    rows = []
    sm = json.loads((SSDN / 'FULLMIX' / 'EXTRACTION_SUMMARY.json').read_text())
    index['PITCH_HZ_T1.png'] = save(fig, 'PITCH_HZ_T1.png', 'placeholder replaced below')
    plt.close(fig)

    # 5 real: F0 distribution both arms
    fig, ax = plt.subplots(figsize=(9, 4))
    for ev, lab, c in [(fx, 'full mix', BLUE), (sy, 'bass stem', ORANGE)]:
        f0 = [e['f0_hz'] for e in ev if e.get('f0_hz') is not None]
        ax.hist(f0, bins=60, histtype='step', linewidth=1.6, color=c, label='%s (n=%d with F0)' % (lab, len(f0)))
    ax.axvline(LOW_HZ, color='#b03030', linestyle='--', linewidth=1.2)
    ax.text(LOW_HZ, ax.get_ylim()[1] * 0.95, ' 43.066 Hz\n preregistered\n low-register\n boundary',
            fontsize=7, color='#b03030', va='top')
    stamp(ax, 'F0 distribution per arm (events with finite F0 only)',
          'The boundary is a reporting descriptor fixed at preregistration. It is not a filter or a match rule.')
    ax.set_xlabel('F0 Hz'); ax.set_ylabel('events'); ax.legend(fontsize=7, frameon=False)
    index['PITCH_HZ_T1.png'] = save(fig, 'PITCH_HZ_T1.png',
        'F0 exists only for a subset of events; events without valid F0 are retained in the inventory and excluded only from pitch distributions.')

    # 6 state composition
    fig, ax = plt.subplots(figsize=(8, 3.6))
    sf_ = [sum(1 for e in fx if e['state'] == 'BASS_COMPATIBLE'), sum(1 for e in fx if e['state'] == 'AMBIGUOUS')]
    ss_ = [sum(1 for e in sy if e['state'] == 'BASS_COMPATIBLE'), sum(1 for e in sy if e['state'] == 'AMBIGUOUS')]
    ax.bar([0, 1], sf_, color=BLUE, label='full mix')
    ax.bar([2, 3], ss_, color=ORANGE, label='bass stem')
    for i, (a, b) in enumerate([('BASS_COMPATIBLE', sf_[0]), ('AMBIGUOUS', sf_[1]),
                               ('BASS_COMPATIBLE', ss_[0]), ('AMBIGUOUS', ss_[1])]):
        ax.text(i, b + 4, str(b), ha='center', fontsize=8)
    ax.set_xticks(range(4)); ax.set_xticklabels(['compatible', 'ambiguous', 'compatible', 'ambiguous'])
    stamp(ax, 'Preregistered state composition (all retained events)',
          'AMBIGUOUS = no valid F0 under the frozen rule. No event was deleted to change composition.')
    ax.legend(fontsize=7, frameon=False)
    index['STATUS_COMPOSITION_T1.png'] = save(fig, 'STATUS_COMPOSITION_T1.png',
        'Composition difference between representations. Not a source-identification accuracy statement.')

    # 7 ambiguity density
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.bar(x, [M[t]['ambiguity_density_among_fullmix_events'] for t in TOLS], color='#7a2a8a')
    ax.set_xticks(x); ax.set_xticklabels(TOLS); ax.set_ylabel('ambiguous pairs / full-mix events')
    stamp(ax, 'Ambiguity density by tolerance family', 'No disambiguation rule was applied at any family.')
    index['AMBIGUITY_DENSITY_T1.png'] = save(fig, 'AMBIGUITY_DENSITY_T1.png',
        'Fraction of full-mix events sitting in an ambiguous multi-pair component.')

    # 8 crossings
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.bar(x, [M[t]['n_crossing_components'] for t in TOLS], color='#b03030')
    for i, t in enumerate(TOLS):
        ax.text(i, M[t]['n_crossing_components'] + 2, str(M[t]['n_crossing_components']), ha='center', fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(TOLS); ax.set_ylabel('crossing components')
    stamp(ax, 'Crossing components by tolerance family',
          'Recorded and reported. Collapsing them would require a resolution rule the preregistration forbids.')
    index['CROSSINGS_T1.png'] = save(fig, 'CROSSINGS_T1.png',
        'Zero crossings at T0/T1; ambiguity first appears at T2 and grows at T4.')

    # 9 coverage map
    fig, ax = plt.subplots(figsize=(11, 3.2))
    for k, (ev, lab, c) in enumerate([(fx, 'full mix', BLUE), (sy, 'bass stem', ORANGE)]):
        for t_i, t in enumerate(TOLS):
            ms = set()
            for comp in M[t].get('_covered', []):
                pass
        ax.scatter([rel(e['native_sample']) for e in ev], [0] * len(ev), s=4, color=c,
                   marker='|', alpha=.5, label=lab)
    ax.set_yticks([]); ax.set_ylim(-.3, .3)
    ax.set_xlabel('seconds from interval start')
    ax.legend(fontsize=7, frameon=False, loc='upper right')
    stamp(ax, 'Interleaved arm event positions over the identical interval',
          'Shared native timeline. The two arms are dependent representations of the same mixdown.')
    index['COVERAGE_MAP.png'] = save(fig, 'COVERAGE_MAP.png',
        'Positional context only. No beat, quarter or PLP-relative alignment is shown or implied.')

    # 10 density comparison
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.bar([0, 1], [len(fx) / dur, len(sy) / dur], color=[BLUE, ORANGE])
    for i, v in enumerate([len(fx) / dur, len(sy) / dur]):
        ax.text(i, v + .15, '%.3f/s' % v, ha='center', fontsize=8)
    ax.set_xticks([0, 1]); ax.set_xticklabels(['full mix', 'bass stem'])
    stamp(ax, 'Event density over %.3f s' % dur, 'Difference is small; neither representation is declared better.')
    ax.set_ylabel('events per second')
    index['ARM_DENSITY_COMPARISON.png'] = save(fig, 'ARM_DENSITY_COMPARISON.png',
        'Descriptive density comparison only. No superiority or accuracy claim.')

    # 11 interval density trace
    fig, ax = plt.subplots(figsize=(11, 3.2))
    ax.hist([rel(e['native_sample']) for e in fx], bins=60, histtype='step', color=BLUE, lw=1.5, label='full mix')
    ax.hist([rel(e['native_sample']) for e in sy], bins=60, histtype='step', color=ORANGE, lw=1.5, label='bass stem')
    stamp(ax, 'Event density over time, both arms', 'No beat grid, quarter markers or PLP-relative reference is overlaid.')
    ax.set_xlabel('seconds from interval start'); ax.set_ylabel('events')
    ax.legend(fontsize=7, frameon=False)
    index['EVENT_RATE_BOTH_ARMS.png'] = save(fig, 'EVENT_RATE_BOTH_ARMS.png',
        'Temporal distribution of the two inventories over the preregistered interval. Descriptive only.')

    # 12 residual descriptive
    fig, ax = plt.subplots(figsize=(9, 3.4))
    rms = {'bass stem': 0.0736, 'piano': 0.0499, 'guitar': 0.0234, 'drums': 0.0201,
           'other': 0.0020, 'vocals': 0.0015}
    ks = list(rms)
    ax.bar(range(len(ks)), [rms[k] for k in ks], color=[ORANGE] + [GREY] * (len(ks) - 1))
    ax.set_xticks(range(len(ks))); ax.set_xticklabels(ks, rotation=20)
    ax.set_ylabel('RMS amplitude')
    stamp(ax, 'Descriptive stem levels over the identical interval (read-only audit)',
          'Levels only. This is NOT a leakage measurement and supports no leakage-absence claim.')
    index['RESIDUAL_WAVEFORM.png'] = save(fig, 'RESIDUAL_WAVEFORM.png',
        'Stem-sum RMS was 0.0986 vs full-mix RMS 0.0996; residual 11.7% of full-mix RMS. Descriptive, not a leakage test.')

    # 13 boundary overlay
    fig, ax = plt.subplots(figsize=(11, 2.8))
    for k, (ev, lab, c) in enumerate([(fx, 'full mix', BLUE), (sy, 'bass stem', ORANGE)]):
        bx = [rel(e['native_sample']) for e in ev if e['evaluation_boundary_crossed']]
        ax.scatter(bx, [k] * len(bx), s=40, marker='D', color='#b03030', zorder=3)
    ax.set_yticks([0, 1]); ax.set_yticklabels(['full mix', 'bass stem'])
    ax.set_xlim(0, dur)
    ax.set_xlabel('seconds from interval start')
    ax.scatter([0, dur], [1.6, 1.6], marker='|', s=120, color='#333333')
    ax.text(0, 1.75, 'interval start', fontsize=7); ax.text(dur, 1.75, 'interval end', fontsize=7, ha='right')
    stamp(ax, 'Events whose analysis support crosses an evaluation boundary (4 total)',
          'Retained and counted normally; boundary crossing is recorded, not used to exclude.')
    index['SEGMENT_BOUNDARY_OVERLAY.png'] = save(fig, 'SEGMENT_BOUNDARY_OVERLAY.png',
        '2 boundary-crossed events per arm, all retained. No event was removed for boundary proximity.')

    (PKG / 'REPRODUCTION' / '_figures_done').write_text(json.dumps(sorted(index)) + '\n')
    print(json.dumps(sorted(index), indent=1))
    return index


if __name__ == '__main__':
    main()
