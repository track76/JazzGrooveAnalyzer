#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

import numpy as np
from numba import njit, prange
from scipy.stats import mannwhitneyu

HERE = Path(__file__).parent
P = json.loads((HERE / 'protocol.json').read_text())
HOP_SECONDS = 1024 / 44100
FEATURES = list(P['measurements'])
DATASETS = {
    'CED-VAL-005': {
        'root': Path('/private/tmp/cedval005_max_recoverable_bass_20260901/complete_1/LONG_AUTHORITY'),
        'evaluation': Path('/private/tmp/cedval005_max_recoverable_bass_20260901/evaluation_1.json'), 'time_key': 'time'},
    'CED-VAL-006': {
        'root': Path('/private/tmp/cedval006_long_emergence_clean_restart_20260901/evidence_1'),
        'evaluation': Path('/private/tmp/cedval006_long_emergence_clean_restart_20260901/evaluation_1.json'), 'time_key': 'timestamp'},
    'CED-VAL-009': {
        'root': Path('/private/tmp/cedval009_long_emergence_blinded_replication_20260901/evidence_1'),
        'evaluation': Path('/private/tmp/cedval009_long_emergence_blinded_replication_20260901/evaluation_1.json'), 'time_key': 'timestamp'},
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n').encode()


def summary(values, unavailable):
    values = np.asarray(values, dtype=float)
    q = np.quantile(values, (0.25, 0.5, 0.75))
    return {'n_available':len(values), 'n_unavailable':unavailable, 'minimum':float(values.min()), 'q1':float(q[0]), 'median':float(q[1]), 'q3':float(q[2]), 'maximum':float(values.max())}


@njit(parallel=True)
def bootstrap_auc(x, y, ix, iy):
    output = np.empty(ix.shape[0], dtype=np.float64)
    for b in prange(ix.shape[0]):
        left = np.sort(x[ix[b]])
        right = np.sort(y[iy[b]])
        wins = 0.0
        for value in left:
            lo = np.searchsorted(right, value, side='left')
            hi = np.searchsorted(right, value, side='right')
            wins += lo + 0.5 * (hi - lo)
        output[b] = wins / (len(left) * len(right))
    return output


def compare(preserved, missed, seed):
    preserved = np.asarray(preserved, dtype=np.float64)
    missed = np.asarray(missed, dtype=np.float64)
    u, pvalue = mannwhitneyu(preserved, missed, alternative='two-sided')
    auc = float(u / (len(preserved) * len(missed)))
    rng = np.random.Generator(np.random.PCG64(seed))
    ix = rng.integers(0, len(preserved), size=(10000, len(preserved)), dtype=np.int32)
    iy = rng.integers(0, len(missed), size=(10000, len(missed)), dtype=np.int32)
    boot_delta = 2 * bootstrap_auc(preserved, missed, ix, iy) - 1
    ci = np.quantile(boot_delta, (0.025, 0.975))
    return {'cliff_delta':2*auc-1, 'rank_auc':auc, 'mann_whitney_p':float(pvalue), 'cliff_delta_bootstrap_ci95':[float(ci[0]),float(ci[1])]}


def extract(root, timestamp):
    nodes = np.load(root / 'nodes.npy', mmap_mode='r')
    offsets = np.load(root / 'frame_offsets.npy', mmap_mode='r')
    scores = np.load(root / 'score_lattice.npy', mmap_mode='r')
    spectrum = np.load(root / 'spectrum_0_2000hz.npy', mmap_mode='r')
    first = max(0, int(np.ceil((timestamp - 0.050) / HOP_SECONDS)))
    final = min(len(offsets)-1, int(np.floor((timestamp + 0.050) / HOP_SECONDS)) + 1)
    result = {feature:None for feature in FEATURES}
    if first < final:
        frame_power = np.asarray(spectrum[first:final], dtype=np.float64)
        total = frame_power.sum(axis=1)
        levels = np.log10(total + np.finfo(np.float64).tiny)
        result['local_log_spectral_level_max'] = float(levels.max())
        result['local_log_spectral_level_median'] = float(np.median(levels))
        result['local_time_frequency_contrast'] = float(levels.max()-np.median(levels))
        full_flux, low_flux = [], []
        low_end = int(np.floor(250 / (44100 / 16384))) + 1
        for frame in range(first, final):
            if frame == 0:
                full_flux.append(0.0); low_flux.append(0.0); continue
            current = np.asarray(spectrum[frame], dtype=np.float64)
            previous = np.asarray(spectrum[frame-1], dtype=np.float64)
            full_flux.append(float(np.maximum(current-previous,0).sum()/(previous.sum()+np.finfo(np.float64).tiny)))
            low_flux.append(float(np.maximum(current[:low_end]-previous[:low_end],0).sum()/(previous[:low_end].sum()+np.finfo(np.float64).tiny)))
        result['maximum_fullband_positive_spectral_flux'] = max(full_flux)
        result['maximum_lowband_positive_spectral_flux'] = max(low_flux)
    if first >= len(offsets)-1 or first >= final:
        return result
    local = nodes[offsets[first]:offsets[final]]
    if len(local) == 0:
        return result
    result['maximum_harmonic_score'] = float(local['score'].max())
    result['maximum_harmonic_energy_relation'] = float(local['harmonic_energy_relation'].max())
    result['maximum_fundamental_prominence'] = float(local['fundamental_prominence'].max())
    result['maximum_upper_partial_evidence'] = float(local['upper_partial_evidence'].max())
    result['maximum_missing_fundamental_balance'] = float((local['upper_partial_evidence']-local['fundamental_prominence']).max())
    result['maximum_emergence_change'] = float(local['score_change'].max())
    result['competing_node_count'] = int(len(local))
    unique_f0 = len(np.unique(local['f0_index']))
    result['f0_hypothesis_count'] = int(unique_f0)
    result['node_per_f0_crowding'] = float(len(local)/unique_f0) if unique_f0 else None
    maximum_score_order = np.lexsort((local['f0_index'], local['frame'], -local['score']))
    best_score = local[maximum_score_order[0]]
    partial = np.asarray(best_score['partial_prominence'], dtype=np.float64)
    result['partial_prominence_dispersion_at_max_score'] = float(np.std(partial))
    normalized = partial/partial.sum() if partial.sum() else np.zeros(8)
    result['partial_prominence_entropy_at_max_score'] = float(-(normalized[normalized>0]*np.log(normalized[normalized>0])).sum())
    emergence_order = np.lexsort((local['f0_index'], local['frame'], -local['score_change']))
    best_emergence = local[emergence_order[0]]
    frame, grid = int(best_emergence['frame']), int(best_emergence['f0_index'])
    result['fixed_f0_persistence_mean'] = float(np.mean(scores[max(0,frame-4):min(len(scores),frame+5),grid]))
    return result


def main(destination):
    all_results = {}
    for dataset_index, (dataset, authority) in enumerate(DATASETS.items()):
        evaluation = json.loads(authority['evaluation'].read_text())
        rows = [row for row in evaluation['rows'] if row['population'] in ('PRESERVED','MISSED')]
        extracted = [{**{'population':row['population'],'id':row['id'],'timestamp':row[authority['time_key']]}, **extract(authority['root'], row[authority['time_key']])} for row in rows]
        dataset_result = {'authority':{'evaluation_sha256':sha(authority['evaluation']),'evidence_authority_sha256':sha(authority['root'].parent/'evidence_authority.json') if dataset=='CED-VAL-005' else sha(authority['root']/'evidence_authority.json')}, 'populations':{p:sum(row['population']==p for row in extracted) for p in ('PRESERVED','MISSED')}, 'features':{}}
        for feature_index, feature in enumerate(FEATURES):
            values = {}
            for population in ('PRESERVED','MISSED'):
                population_rows = [row for row in extracted if row['population']==population]
                values[population] = [row[feature] for row in population_rows if row[feature] is not None]
            availability = {population:len(values[population])/dataset_result['populations'][population] for population in values}
            dataset_result['features'][feature] = {
                'PRESERVED':summary(values['PRESERVED'],dataset_result['populations']['PRESERVED']-len(values['PRESERVED'])),
                'MISSED':summary(values['MISSED'],dataset_result['populations']['MISSED']-len(values['MISSED'])),
                'comparison':compare(values['PRESERVED'],values['MISSED'],20260901+dataset_index*1000+feature_index),
                'availability':availability,
            }
        all_results[dataset] = dataset_result
    cross = {}
    for feature in FEATURES:
        deltas = {dataset:all_results[dataset]['features'][feature]['comparison']['cliff_delta'] for dataset in DATASETS}
        availability_ok = all(all_results[dataset]['features'][feature]['availability'][population]>=0.80 for dataset in DATASETS for population in ('PRESERVED','MISSED'))
        material = [value for value in deltas.values() if abs(value)>=0.147]
        if not availability_ok:
            classification='INDETERMINATE'
        elif len(material)==3 and (all(value>0 for value in material) or all(value<0 for value in material)):
            classification='CONSISTENT'
        elif material:
            classification='MATERIAL_DEPENDENT'
        else:
            classification='WEAK'
        cross[feature]={'deltas':deltas,'directions':{dataset:('PRESERVED_HIGHER' if value>0 else 'MISSED_HIGHER' if value<0 else 'EQUAL') for dataset,value in deltas.items()},'classification':classification}
    result={'protocol_id':P['protocol_id'],'protocol_fingerprint':P['protocol_fingerprint'],'datasets':all_results,'cross_dataset':cross,'no_classifier_fitted':True,'no_threshold_fitted':True,'jga_modified':False}
    result['result_fingerprint']=hashlib.sha256(canonical(result)).hexdigest()
    Path(destination).write_bytes(canonical(result))
    print(json.dumps({'fingerprint':result['result_fingerprint'],'classifications':{feature:value['classification'] for feature,value in cross.items()}},sort_keys=True))


if __name__ == '__main__':
    main(sys.argv[1])
