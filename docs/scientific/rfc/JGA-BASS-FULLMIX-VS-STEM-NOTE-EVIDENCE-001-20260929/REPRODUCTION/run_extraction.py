"""Symmetric dual-arm Bass event extraction for JGA-BASS-FULLMIX-VS-STEM-NOTE-EVIDENCE-001-20260929.

Preregistration 0.2. Identical extractor code path for both arms. The only
difference between the two runs is the input audio file. No arm is special-cased,
no parameter is selected from data, and no candidate is deleted.
"""
import os, sys, json, math, hashlib, platform, warnings
from pathlib import Path
import numpy as np
import scipy, scipy.signal as sig, soundfile as sf, librosa

ROOT = Path('/Users/StarTrack/Development/JazzGrooveAnalyzer')
TASK = 'JGA-BASS-FULLMIX-VS-STEM-NOTE-EVIDENCE-001-20260929'
PKG = ROOT / 'docs/scientific/rfc' / TASK
CFG = json.loads((PKG / 'EXTRACTOR_CONFIG_FULLMIX.json').read_text())
SR_EXPECTED = 44100
LOW_REGISTER_HZ = 43.06640625


def durable_write(path, data):
    """Atomic + fsync + read-back verify. Plain write_text lost data when the
    ExFAT SSD volume was remounted, so every external payload is now synced and
    verified before the run is allowed to continue."""
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
    back = path.read_bytes()
    assert back == data, ('read-back mismatch', str(path), len(back), len(data))
    return hashlib.sha256(data).hexdigest()


def clean(x):
    if isinstance(x, dict):
        return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    if isinstance(x, np.ndarray):
        return clean(x.tolist())
    if isinstance(x, np.generic):
        return clean(x.item())
    if isinstance(x, float) and not math.isfinite(x):
        return None
    return x


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def stats(x):
    a = np.asarray([v for v in x if v is not None and np.isfinite(v)], float)
    if not len(a):
        return {'n': 0, 'status': 'NOT_AVAILABLE'}
    return {'n': int(len(a)), 'min': float(a.min()), 'q1': float(np.percentile(a, 25)),
            'median': float(np.median(a)), 'q3': float(np.percentile(a, 75)),
            'max': float(a.max()), 'mean': float(a.mean())}


def extract(arm, input_path, expected_sha, out_dir):
    """Run the frozen preregistered extractor on one arm. Same code for both arms."""
    C = CFG
    assert C['sample_rate'] == SR_EXPECTED
    assert C['channel_handling'] == 'arithmetic_mean_stereo'
    assert C['rounding'] == 'nearest_integer_half_even'
    assert C['interval'] == 'start_inclusive_end_exclusive'

    got = sha256_file(input_path)
    assert got == expected_sha, (arm, got, expected_sha)

    info = sf.info(input_path)
    assert info.samplerate == C['sample_rate'], (arm, info.samplerate)
    assert info.channels == 2, (arm, info.channels)
    assert info.subtype == 'FLOAT', (arm, info.subtype)

    lo, hi = [round(t * info.samplerate) for t in C['region_s']]
    guard = round(C['context_s'] * info.samplerate)
    begin = max(0, lo - guard)
    end = min(info.frames, hi + guard)

    x, _ = sf.read(input_path, start=begin, stop=end, dtype='float64', always_2d=True)
    y = x.mean(axis=1)
    del x

    st = dict(C['stft'])
    st['dtype'] = np.complex64
    N, H = st['n_fft'], st['hop_length']
    half = N // 2

    freq = librosa.fft_frequencies(sr=info.samplerate, n_fft=N)
    native = lambda f: begin + int(f) * H
    D = librosa.stft(y, **st)
    mag_raw = np.abs(D).astype(float)
    frames = np.arange(D.shape[1])

    ac = C['bass']
    mask = (freq >= ac['band_hz'][0]) & (freq <= ac['band_hz'][1])
    f = freq[mask]
    fc = C['filter']
    sos = sig.butter(fc['order'], ac['band_hz'], btype=fc['btype'],
                     fs=info.samplerate, output='sos')
    filtered = sig.sosfiltfilt(sos, y, padtype=fc['padtype'], padlen=fc['padlen'])

    M = np.abs(librosa.stft(filtered, **st)).astype(float)
    band = M[mask]
    flux = np.sqrt(np.sum(np.maximum(np.diff(band, axis=1, prepend=band[:, :1]), 0) ** 2, axis=0))

    q25, q75 = np.percentile(flux, [25, 75])
    prom = C['peak']['prominence_iqr_factor'] * (q75 - q25)
    prom_fallback = None
    if prom <= 0:
        prom_fallback = C['peak']['fallback_std_factor'] * np.std(flux)
        prom = prom_fallback
    assert prom > 0, (arm, 'non-positive prominence threshold')

    maxima, props = sig.find_peaks(flux, prominence=(None, None))
    distance_kept = set(sig.find_peaks(flux, distance=ac['distance_frames'])[0].tolist())
    qualified = set(sig.find_peaks(flux, distance=ac['distance_frames'], prominence=prom)[0].tolist())

    total = np.sum(band, axis=0)
    eps = C['features']['flatness_epsilon']
    den = np.maximum(total, eps)
    centroid = np.sum(f[:, None] * band, axis=0) / den
    flat = np.exp(np.mean(np.log(np.maximum(band, eps)), axis=0)) / np.maximum(np.mean(band, axis=0), eps)
    power = np.sum(band ** 2, axis=0)
    postframes = int(np.ceil(C['features']['post_energy_s'] * info.samplerate / H))
    post = np.array([np.sum(power[i + 1:min(len(power), i + postframes + 1)])
                     for i in range(len(power))])
    postcomplete = frames + postframes < len(power)

    py = dict(C['pyin'])
    py['beta_parameters'] = tuple(py['beta_parameters'])
    py['fill_na'] = np.nan
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter('always')
        f0, voiced, vp = librosa.pyin(filtered, sr=info.samplerate, **py)
    all_warnings = [str(w.message) for w in ws]

    nfr = len(frames)
    f0 = np.asarray(f0, float)
    if len(f0) < nfr:
        f0 = np.concatenate([f0, np.full(nfr - len(f0), np.nan)])
    f0 = f0[:nfr]
    voiced = np.asarray(voiced, bool)[:nfr]
    vp = np.asarray(vp, float)[:nfr]
    if len(vp) < nfr:
        vp = np.concatenate([vp, np.full(nfr - len(vp), np.nan)])

    harm = np.full(nfr, np.nan)
    continuity = np.full(nfr, np.nan)
    harmonics = {}
    last = None
    for i in frames:
        if not np.isfinite(f0[i]):
            continue
        if last is not None and i - last <= C['continuity']['max_gap_frames']:
            continuity[i] = abs(f0[i] - f0[last])
        last = i
        hh = []
        for k in range(1, C['harmonics']['max_harmonics'] + 1):
            hz = k * f0[i]
            if hz > info.samplerate / 2:
                break
            b = int(np.argmin(abs(freq - hz)))
            hh.append({'harmonic_number': k, 'requested_frequency_hz': float(hz),
                       'bin': b, 'bin_center_hz': float(freq[b]),
                       'magnitude': float(mag_raw[b, i])})
        harm[i] = float(sum(v['magnitude'] for v in hh))
        harmonics[int(i)] = hh

    rows = []
    for j, fr in enumerate(maxima):
        sample = native(fr)
        if not (lo <= sample < hi):
            continue
        reasons = []
        if int(fr) not in distance_kept:
            reasons.append('DISTANCE_SUPPRESSION')
        if props['prominences'][j] < prom:
            reasons.append('BELOW_PROMINENCE')
        qual = int(fr) in qualified
        assert qual == (len(reasons) == 0), (arm, fr, reasons)
        state = 'AMBIGUOUS'
        if voiced[fr] and np.isfinite(f0[fr]) and C['pyin']['fmin'] <= f0[fr] <= C['pyin']['fmax']:
            state = ('BASS_COMPATIBLE' if harm[fr] > C['bass_rule']['harmonic_sum_to_flux_factor'] * flux[fr]
                     else 'BASS_POSSIBLE')
        local_analysis = [sample - H - half, sample + half]
        local_class = [sample - H - half, sample + H + half]
        crossing = (local_analysis[0] < lo or local_analysis[1] > hi
                    or local_class[0] < lo or local_class[1] > hi)
        row = {
            'candidate_id': 'BASS_F%06d' % int(fr),
            'arm': arm, 'instrument_evidence': 'BASS',
            'frame_index': int(fr), 'native_sample': sample,
            'landmark_timestamp_s': sample / info.samplerate,
            'coordinate_convention': 'processing_start_native_sample + frame_index*hop; centered STFT; no offset; frame-derived landmark not physical attack',
            'analysis_support_native_samples': local_analysis,
            'classification_local_support_native_samples': local_class,
            'classification_algorithm_support_native_samples': [begin, end],
            'evidence_available_until_s': end / info.samplerate,
            'evaluation_boundary_crossed': bool(crossing),
            'source_support_truncated': bool(local_analysis[0] < begin or local_class[1] > end),
            'peak_qualified': qual, 'rejection_reasons': reasons,
            'flux': float(flux[fr]), 'prominence': float(props['prominences'][j]),
            'prominence_left_base_frame': int(props['left_bases'][j]),
            'prominence_right_base_frame': int(props['right_bases'][j]),
            'centroid_hz': float(centroid[fr]), 'flatness_magnitude': float(flat[fr]),
            'post_event_energy': float(post[fr]) if postcomplete[fr] else None,
            'post_event_energy_status': 'COMPUTED' if postcomplete[fr] else 'TRUNCATED',
            'state': state, 'tentative_subtype_hypothesis': None,
            'source_identity': 'UNVALIDATED_COMPATIBILITY',
            'confuser_status': 'UNRESOLVED_NO_CONFIRMED_CONFUSER_LABEL',
            'f0_hz': float(f0[fr]) if np.isfinite(f0[fr]) else None,
            'voiced': bool(voiced[fr]),
            'voiced_probability': float(vp[fr]) if np.isfinite(vp[fr]) else None,
            'harmonic_magnitude_sum': float(harm[fr]) if np.isfinite(harm[fr]) else None,
            'harmonic_status': 'COMPUTED' if np.isfinite(harm[fr]) else 'NOT_COMPUTED_NO_F0',
            'harmonic_components': harmonics.get(int(fr), []),
            'previous_voiced_f0_difference_hz': float(continuity[fr]) if np.isfinite(continuity[fr]) else None,
            'continuity_status': ('COMPUTED' if np.isfinite(continuity[fr])
                                  else 'NOT_COMPUTED_NO_NEAR_PRIOR_VOICED_FRAME'),
            'low_register_flag': (bool(np.isfinite(f0[fr]) and f0[fr] < LOW_REGISTER_HZ)
                                  if np.isfinite(f0[fr]) else None),
            'low_register_boundary_hz': LOW_REGISTER_HZ,
            'low_register_boundary_basis': 'geometry-derived boundary fixed at preregistration; reporting descriptor only, not a filter, threshold or match rule',
        }
        rows.append(clean(row))

    peaks = [r for r in rows if r['peak_qualified']]
    groups = []
    for row in peaks:
        if not groups or row['landmark_timestamp_s'] - groups[-1][-1]['landmark_timestamp_s'] > C['dedup']['tolerance_s']:
            groups.append([row])
        else:
            groups[-1].append(row)
    clusters, dedup = [], []
    for k, group in enumerate(groups):
        rep = min(group, key=lambda r: (r['native_sample'], r['candidate_id']))
        span = group[-1]['landmark_timestamp_s'] - group[0]['landmark_timestamp_s']
        cid = 'BASS_CL%05d' % (k + 1)
        clusters.append({'cluster_id': cid, 'member_ids': [r['candidate_id'] for r in group],
                         'members': group, 'representative_id': rep['candidate_id'],
                         'representative_selection_rule': C['dedup']['representative'],
                         'span_s': span, 'span_exceeds_pairwise_tolerance': bool(span > C['dedup']['tolerance_s']),
                         'reason': 'adjacent-gap heuristic; no physical same-attack claim'})
        d = dict(rep); d['cluster_id'] = cid
        dedup.append(d)

    # STFT coordinate invariant, identical for both arms
    inv = []
    for at in (1024, 2048, 4096):
        imp = np.zeros(8192); imp[at] = 1.0
        z = librosa.stft(imp, **st)
        peak = int(np.argmax(np.sum(abs(z) ** 2, axis=0)))
        inv.append({'impulse_sample': at, 'peak_frame': peak,
                    'error_samples': peak * H - at, 'pass': peak * H == at})
    assert all(c['pass'] for c in inv), (arm, inv)

    out = {
        'arm': arm, 'input_path': input_path, 'input_sha256': got,
        'region_native_samples': [lo, hi], 'region_s': [lo / info.samplerate, hi / info.samplerate],
        'processing_support': [begin, end],
        'thresholds': {'prominence': float(prom), 'iqr': float(q75 - q25),
                       'std': float(np.std(flux)),
                       'prominence_fallback_used': prom_fallback is not None,
                       'statistics_support': 'entire_processing_context'},
        'bands': {'bass_hz': ac['band_hz'], 'n_bins': int(mask.sum())},
        'filter': {'design': fc['design'], 'order': fc['order'], 'btype': fc['btype'],
                   'application': fc['application'], 'padtype': fc['padtype'], 'padlen': fc['padlen']},
        'stft': {**st, 'dtype': 'complex64'},
        'pyin': {k: (list(v) if isinstance(v, tuple) else v) for k, v in C['pyin'].items()},
        'dedup': C['dedup'], 'continuity': C['continuity'], 'harmonics': C['harmonics'],
        'bass_rule': C['bass_rule'],
        'low_register_boundary_hz': LOW_REGISTER_HZ,
        'counts': {'all_local_maxima': len(rows), 'peak_qualified': len(peaks),
                   'deduplicated': len(dedup), 'rejected': len(rows) - len(peaks),
                   'merged_members': len(peaks) - len(dedup), 'clusters': len(clusters),
                   'multi_member_clusters': int(sum(len(q) > 1 for q in groups))},
        'states': {s: int(sum(r['state'] == s for r in dedup))
                   for s in ('BASS_COMPATIBLE', 'BASS_POSSIBLE', 'AMBIGUOUS', 'UNRESOLVED')},
        'cluster_size_distribution': {str(n): int(sum(len(q) == n for q in groups))
                                      for n in sorted({len(q) for q in groups})},
        'cluster_span_ms': stats([1000 * c['span_s'] for c in clusters]),
        'dedup_spacing_ms': stats(np.diff([r['landmark_timestamp_s'] for r in dedup]) * 1000),
        'evaluation_boundary_crossed': int(sum(r['evaluation_boundary_crossed'] for r in dedup)),
        'source_support_truncated': int(sum(r['source_support_truncated'] for r in dedup)),
        'flux': stats([r['flux'] for r in dedup]),
        'prominence': stats([r['prominence'] for r in dedup]),
        'engineering_invariants': {'stft_coordinate': inv, 'formula': 'native_sample = begin + frame_index*hop',
                                   'hop_ms': 1000 * H / info.samplerate,
                                   'window_ms': 1000 * N / info.samplerate},
        'warnings': all_warnings,
        'density_events_per_s': len(dedup) / ((hi - lo) / info.samplerate),
        'extraction_status': 'COMPLETED',
    }
    out['events'] = dedup
    out['clusters'] = clusters
    out['all_local_maxima'] = rows
    out['peak_qualified'] = peaks
    import io as _io
    _b = _io.BytesIO()
    np.savez_compressed(_b,
                        native_sample=begin + frames * H,
                        time_s=(begin + frames * H) / info.samplerate,
                        waveform=y, magnitude=mag_raw.astype('float32'),
                        band_magnitude=M.astype('float32'), flux=flux,
                        f0_hz=f0, voiced=voiced, voiced_probability=vp,
                        harmonic_magnitude_sum=harm,
                        previous_voiced_difference_hz=continuity,
                        centroid_hz=centroid, flatness=flat, post_event_energy=post,
                        frequencies_hz=freq,
                        context_local_maxima_frames=np.asarray(maxima),
                        context_prominences=props['prominences'])
    out['arrays_sha256'] = durable_write(out_dir / 'EXTRACTION_ARRAYS.npz', _b.getvalue())
    return clean(out)


def main():
    import datetime
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    manifest = json.loads((PKG / 'INPUT_MANIFEST.json').read_text())
    results = {}
    for arm in ('FULLMIX', 'STEM'):
        d = manifest['arms'][arm]
        out_dir = Path(d['external_root'])
        out_dir.mkdir(parents=True, exist_ok=True)
        print('EXTRACTING', arm, flush=True)
        r = extract(arm, d['path'], d['sha256'], out_dir)
        results[arm] = r
        durable_write(out_dir / 'EVENTS.json', json.dumps(clean(r['events']), indent=2) + '\n')
        durable_write(out_dir / 'CLUSTERS.json', json.dumps(clean(r['clusters']), indent=2) + '\n')
        durable_write(out_dir / 'ALL_LOCAL_MAXIMA.json', json.dumps(clean(r['all_local_maxima']), indent=2) + '\n')
        durable_write(out_dir / 'PEAK_QUALIFIED.json', json.dumps(clean(r['peak_qualified']), indent=2) + '\n')
        meta = {k: v for k, v in r.items() if k not in ('events', 'clusters', 'all_local_maxima', 'peak_qualified')}
        durable_write(out_dir / 'EXTRACTION_SUMMARY.json', json.dumps(clean(meta), indent=2) + '\n')
        print('ARM_COMPLETE', arm, r['counts'], r['states'], flush=True)
    (PKG / 'REPRODUCTION' / '_extraction_done').write_text(json.dumps({
        'started': started, 'arms': {a: results[a]['counts'] for a in results}}, indent=2) + '\n')
    print('EXTRACTION_BOTH_ARMS_COMPLETE', flush=True)


if __name__ == '__main__':
    main()
