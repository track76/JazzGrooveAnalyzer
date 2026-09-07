"""Prospective verification and frozen reference scoring; no DSP or tuning."""
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def canonical(d):
    return json.dumps(d, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()+b'\n'


def read(name):
    return json.loads((HERE/name).read_text())


def normalize(report):
    result = deepcopy(report)
    result.pop('scientific_fingerprint')
    for source in result['source_authorities']:
        source.pop('path_used')
    fingerprint = sha256(canonical(result)[:-1]).hexdigest()
    return {**result, 'scientific_fingerprint':fingerprint}


def score(report):
    path = HERE.parent/'separation_robustness_20260825_01/score.py'
    spec = importlib.util.spec_from_file_location('frozen_scorer',path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    reference = json.loads(module.REFERENCE.read_text())
    mappings = {label: module.assign(module.events(reference,label),module.events(report,label))
                for label in ['Drums','Double Bass']}
    return {'reference_sha256':sha256(module.REFERENCE.read_bytes()).hexdigest(),
            'matcher_sha256':sha256(path.read_bytes()).hexdigest(),
            'sources':mappings, 'ad038_ad040':module.level3(reference,report,mappings)}


def main():
    reports=[read('canonical_run_1.json'),read('canonical_run_2.json')]
    a,b=map(normalize,reports)
    assert canonical(a)==canonical(b), 'Scientific replay changed'
    ex=[read('execution_run_1.json'),read('execution_run_2.json')]
    assert [x['sha256'] for x in ex[0]['outputs']]==[x['sha256'] for x in ex[1]['outputs']]
    assert len(set(x['source_identity'] for x in ex[0]['outputs']))==6
    old=json.loads((HERE.parent/'bass_preservation_phase2_20260825_01/canonical_report_M2_run_1.json').read_text())
    assert read('preparation_replay.json')['status']=='PASS'
    # Historical reports omit strength/confidence; frozen-code same-asset replay
    # above proves those fields without inventing historical serialized values.
    fields=['producer_frame','producer_sample_coordinate','timestamp_seconds','observation_index']
    for label in ['Drums','Double Bass']:
        previous=next(s for s in old['source_authorities'] if s['label']==label)
        current=next(s for s in a['source_authorities'] if s['label']==label)
        assert previous['sha256']==current['sha256'], 'Frozen output bytes changed'
        def observations(doc):
            return sorted(tuple(row[k] for k in fields) for row in doc['observations'][label])
        assert observations(old)==observations(a), 'Non-identity observation changed'
    events={e['eme_id']:e for e in a['elementary_metric_events']}
    assert len(events)==len(a['elementary_metric_events'])
    by_source={s['source_identity']:s for s in a['source_authorities']}
    assert len(by_source)==3 and {s['label'] for s in by_source.values()}=={'Drums','Piano','Double Bass'}
    targets={e['eme_id'] for e in events.values() if by_source[e['sound_source_id']]['role']=='ACCOMPANIMENT'}
    assert {l['target_eme_id'] for l in a['ad038_localizations']}==targets
    assert len(a['ad038_localizations'])==len(targets)
    for e in events.values():assert e['source_asset_sha256']==by_source[e['sound_source_id']]['sha256']
    for s in by_source.values():
        prep=s['separation_provenance']['detector_preparation']
        assert prep['source_identity']==s['source_identity'] and prep['input_separated_wav_sha256']==s['sha256']
        assert prep['input_frame_count']==prep['output_frame_count']
    for loc in a['ad038_localizations']:
        assert loc['target_timestamp_ms']==events[loc['target_eme_id']]['timestamp_seconds']*1000
        for key in ['preceding_reference','following_reference','nearest_reference']:
            ref=loc[key]
            if ref is not None:
                assert ref['timestamp_seconds']==events[ref['eme_id']]['timestamp_seconds']
                assert ref['timestamp_ms']==ref['timestamp_seconds']*1000
        for key in ['distance_from_preceding','distance_from_following']:
            assert loc[key+'_ms']==(None if loc[key+'_seconds'] is None else loc[key+'_seconds']*1000)
        for key in ['nearest_displacement','nearest_absolute_displacement']:
            assert loc[key+'_ms']==loc[key+'_seconds']*1000
    assert all(r['correspondence_status']=='GEOMETRIC_ONLY' for r in a['ad040_profile']['relationships'])
    scored=score(a)
    assert canonical(scored)==canonical(score(b))
    for name,value in [('canonical_operational_report.json',a),('preservation.json',scored)]:
        (HERE/name).write_bytes(canonical(value))
    summary={label:{k:v for k,v in row.items() if k not in ['matches','original_only','separated_only']}
             for label,row in scored['sources'].items()}
    summary['Piano']={'operational_source':'AVAILABLE','operational_population':next(s['eme_count'] for s in a['source_authorities'] if s['label']=='Piano'),'preservation_percentage':'NOT_ESTABLISHED','timing_preservation_error':'NOT_ESTABLISHED'}
    result={'classification':'CONDITIONALLY_VALIDATED_GEOMETRIC_OPERATIONAL_PATH',
        'scope':'Observable evidence only; Piano preservation unestablished; no physical-onset or complete-performance claim',
        'source_results':summary,'populations':{s['label']:s['eme_count'] for s in a['source_authorities']},
        'ad040':{k:a['ad040_profile'][k] for k in ['represented_eme_count','temporal_reference_eme_count','accompaniment_relationship_count']},
        'canonical_sha256':sha256(canonical(a)).hexdigest(),'scientific_fingerprint':a['scientific_fingerprint'],
        'six_output_assets_byte_identical_replay':True,'canonical_replay':'BYTE_IDENTICAL_WITH_PATH_LOCATORS_EXTERNALIZED_PER_PROTOCOL',
        'historical_same_asset_drums_bass_nonidentity_invariance':True,
        'preservation_scoring_replay':'BYTE_IDENTICAL','selective_missingness':'Complete unmatched time populations preserved; uniformity and cause not inferred',
        'resolution_seconds':{'reference':512/48000,'separated':512/44100},
        'visualization_acceptance':'PENDING','bpm_recommendation':'Do not begin BPM automatically; conditional observed-subset path requires separate PI scope approval.'}
    (HERE/'result.json').write_bytes(canonical(result))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
