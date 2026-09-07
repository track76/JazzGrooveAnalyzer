"""Finalize preservation only after deterministic scientific and visual gates."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent


def canonical(d):return json.dumps(d,sort_keys=True,separators=(',',':'),allow_nan=False).encode()+b'\n'


def main():
    replay=Path('/private/tmp/jga-demucs-visualization-replay-20260907')
    figures=HERE/'figures'
    verification=json.loads((figures/'visualization_verification.json').read_text())
    for path in figures.iterdir():
        assert path.read_bytes()==(replay/path.name).read_bytes(), path.name
    report=json.loads((HERE/'canonical_operational_report.json').read_text())
    rows=json.loads((figures/'plot_data.json').read_text())
    for row in rows:
        event=report['elementary_metric_events'][int(row['canonical_record'].rsplit('/',1)[1])]
        assert row['eme_id']==event['eme_id']
        assert row['source_identity']==event['sound_source_id']
        assert row['asset_sha256']==event['source_asset_sha256']
        assert row['time_seconds']==event['timestamp_seconds']
    assert len(rows)==1789 and verification['figures']['drum_relative_timing']['point_count']==915
    result=json.loads((HERE/'result.json').read_text())
    assert result['classification']=='CONDITIONALLY_VALIDATED_GEOMETRIC_OPERATIONAL_PATH'
    result['visualization_acceptance']='PASS'
    result['visualization_replay']='PNG_SVG_PLOT_DATA_BYTE_IDENTICAL_IN_TWO_FRESH_PROCESSES'
    result['plot_data_sha256']=verification['plot_data_sha256']
    result['population_comparison_scope']='Matched relation preservation is Bass-only with Drum reference mapping; aggregate operational AD038/AD040 includes Piano, absent from the independent two-source reference. Do not interpret aggregate population differences as Piano preservation.'
    result['tests']={'focused_handoff_and_reporting':15,'broader_scientifically_relevant':633,'final_strengthened_handoff':3,'failures':0,'warnings':'Two existing audioread deprecations; renderer used temporary font caches without changing artifacts.'}
    (HERE/'result.json').write_bytes(canonical(result))
    immutable=HERE.parents[1]/'VAL-001/ad041_direct_input_acceptance_20260907/canonical_report_run_1.json'
    assert sha256(immutable.read_bytes()).hexdigest()=='eeb189217a722679d5f40bef4d809e2b38ab381e9dea81057023dfd3d80e05c7'
    assert json.loads(immutable.read_text())['scientific_fingerprint']=='e3d73705306ccc0e96ec78020a54f34aa4e8f267337afa6b7bd56b74fc4fdc4d'
    changed=subprocess.check_output(['git','diff','--name-only','--diff-filter=MD','8e6a626ef00c4e51f2769a051180a080704e24f8','--','validation'],text=True).splitlines()
    assert not changed, 'Historical tracked validation evidence changed'
    print(json.dumps({'classification':result['classification'],'canonical_sha256':result['canonical_sha256'],'scientific_fingerprint':result['scientific_fingerprint'],'visual_replay':result['visualization_replay']}))


if __name__=='__main__':main()
