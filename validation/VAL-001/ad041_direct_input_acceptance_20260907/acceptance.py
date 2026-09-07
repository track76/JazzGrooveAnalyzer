"""Controlled direct-input acceptance after the exact provenance gate passes."""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from uuid import NAMESPACE_URL, uuid5

from snapshot import AUTHORITY, EXPECTED_AUTHORITY_SHA, FILES, KWARGS, LABELS, ROOT, canonical, capture
from invariance import verify
HERE = Path(__file__).resolve().parent

def cli(destination):
    authority = json.loads(AUTHORITY.read_bytes())
    args = [sys.executable, str(ROOT/'tools/run_rhythm_section_timing_report.py')]
    for label, filename, binding in zip(LABELS, FILES, authority['bindings']):
        role = 'TEMPORAL_REFERENCE' if label == 'Drums' else 'ACCOMPANIMENT'
        args += ['--source', f'{role}={label}={ROOT / "recordings/validation/stems" / filename}',
                 '--expected-sha256', f'{label}={binding["asset_sha256"]}',
                 '--source-identity', f'{label}={authority["source_authority_id"]}={binding["source_instance_key"]}']
    for key,value in KWARGS.items(): args += ['--'+key.replace('_','-'), value]
    args += ['--output', str(destination)]
    subprocess.run(args, check=True)

def verify_final(report, captured):
    reference = json.loads((HERE/'corrected_identity.json').read_bytes())
    # Check every final field against the identity-gated execution. New projections
    # and explicit contract/provenance fields are verified below before removal.
    stripped = deepcopy(report)
    contract = stripped['scientific_status'].pop('analyzable_only_contract')
    assert contract == {
        'meaning':'Temporal geometry of ANALYZABLE observations relative to the authorized Drum reference.',
        'complete_performance_coverage_claimed':False, 'missing_events_reconstructed':False,
        'not_analyzable_timing_inferred':False, 'missing_evidence_is_musical_absence':False,
        'tactus_inferred':False, 'non_null_separator_ad041_status':'DEFERRED_SEPARATION_AUTHORITY_NOT_ESTABLISHED'}
    for label, records in stripped['observations'].items():
        authority = next(x for x in report['source_authorities'] if x['label']==label)
        diagnostic = captured['diagnostics'][authority['sha256']]
        candidates = {x['id']:x for x in diagnostic['candidates']}
        for item in records:
            candidate = candidates[item['pulse_candidate_id']]
            assert item.pop('strength') == candidate['strength']
            assert item.pop('confidence') == candidate['confidence']
    source_map = {x['source_identity']:x for x in report['source_authorities']}
    assert len(source_map)==3
    binding_authority = json.loads(AUTHORITY.read_bytes())
    for binding in binding_authority['bindings']:
        expected = str(uuid5(NAMESPACE_URL, json.dumps(dict(rule='jga-direct-input-source-identity/v1', source_authority_id=binding_authority['source_authority_id'], source_instance_key=binding['source_instance_key']), sort_keys=True, separators=(',',':'))))
        assert source_map[expected]['sha256']==binding['asset_sha256']
    counts=Counter()
    milliseconds=0
    for item in stripped['ad038_localizations']:
        source=source_map[item['target_source_identity']]
        counts[source['label']]+=1
        assert item.pop('target_asset_sha256')==source['sha256']
        for seconds,ms in [('target_timestamp_seconds','target_timestamp_ms'), ('nearest_absolute_displacement_seconds','nearest_absolute_displacement_ms')]:
            assert item.pop(ms)==(None if item[seconds] is None else item[seconds]*1000.0)
            milliseconds+=1
        for seconds,ms in [('distance_from_preceding_seconds','distance_from_preceding_ms'),('distance_from_following_seconds','distance_from_following_ms'),('nearest_displacement_seconds','nearest_displacement_ms')]:
            assert item[ms]==(None if item[seconds] is None else item[seconds]*1000.0)
            milliseconds+=1
        for key in ('preceding_reference','following_reference','nearest_reference'):
            ref=item[key]
            if ref is not None:
                assert ref.pop('timestamp_ms')==ref['timestamp_seconds']*1000.0
                assert source_map[ref['source_identity']]['label']=='Drums'
                milliseconds+=1
        assert item['correspondence_status']=='GEOMETRIC_ONLY'
    assert counts=={'Piano':49,'Double Bass':27}
    stripped.pop('scientific_fingerprint')
    expected=deepcopy(reference['report']); expected.pop('scientific_fingerprint')
    assert stripped==expected, 'Unexpected final scientific field change'
    assert captured['diagnostics']==reference['diagnostics']
    content=deepcopy(report); fingerprint=content.pop('scientific_fingerprint')
    assert sha256(canonical(content).rstrip('\n').encode()).hexdigest()==fingerprint
    return milliseconds

def main():
    baseline=json.loads((HERE/'baseline.json').read_bytes())
    corrected=json.loads((HERE/'corrected_identity.json').read_bytes())
    assert verify(baseline,corrected)['provenance_invariance']=='PASS'
    assert json.loads((HERE/'invariance_result.json').read_bytes())['provenance_invariance']=='PASS'
    assert sha256(AUTHORITY.read_bytes()).hexdigest()==EXPECTED_AUTHORITY_SHA
    output_directory = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE
    output_directory.mkdir(parents=True, exist_ok=True)
    outputs=[output_directory/f'canonical_report_run_{i}.json' for i in (1,2)]
    for path in outputs: cli(path)
    assert outputs[0].read_bytes()==outputs[1].read_bytes()
    report=json.loads(outputs[0].read_bytes())
    assert outputs[0].read_text()==canonical(report)
    captured=json.loads(canonical(capture(True)))
    assert captured['report']==report
    milliseconds=verify_final(report,captured)
    result=dict(classification='PASS_ANALYZABLE_TIMING_REPORT_ACCEPTED',
                direct_input_ad041='PASS', non_null_separator_ad041='DEFERRED_SEPARATION_AUTHORITY_NOT_ESTABLISHED',
                population={'Drums':63,'Piano':49,'Double Bass':27}, relationships=76,
                provenance_invariance='EXACT_PASS', scientific_status='GEOMETRIC_ONLY',
                replay='BYTE_IDENTICAL_CLI_AND_INDEPENDENT_CAPTURE',
                milliseconds_rule='authoritative_seconds * 1000.0', millisecond_values_verified=milliseconds,
                canonical_result_sha256=sha256(outputs[0].read_bytes()).hexdigest(),
                scientific_fingerprint=report['scientific_fingerprint'],
                source_authority_sha256=EXPECTED_AUTHORITY_SHA,
                source_identities={x['label']:x['source_identity'] for x in report['source_authorities']})
    with (output_directory/'result.json').open('x') as stream: stream.write(canonical(result))
    lines=['# Controlled ANALYZABLE timing acceptance','', 'GEOMETRIC_ONLY: temporal geometry of supported observations relative to the authorized Drum reference. No complete-performance or missing-event claim.','', '| SOURCE | ABSOLUTE TIME (ms) | PRECEDING DRUM (ms) | FOLLOWING DRUM (ms) | NEAREST DRUM (ms) | SIGNED DISPLACEMENT (ms) | ABSOLUTE DISPLACEMENT (ms) |','|---|---:|---:|---:|---:|---:|---:|']
    for label in ('Piano','Double Bass'):
        sid=result['source_identities'][label]
        rows=[x for x in report['ad038_localizations'] if x['target_source_identity']==sid]
        for row in (rows[0],rows[len(rows)//2],rows[-1]):
            def ref(key): return 'null' if row[key] is None else repr(row[key]['timestamp_ms'])
            lines.append('| '+' | '.join([label,repr(row['target_timestamp_ms']),ref('preceding_reference'),ref('following_reference'),ref('nearest_reference'),repr(row['nearest_displacement_ms']),repr(row['nearest_absolute_displacement_ms'])])+' |')
    lines+=['', 'Complete machine-readable result: [canonical_report_run_1.json](canonical_report_run_1.json).', '', 'Scientific fingerprint: `'+report['scientific_fingerprint']+'`.','', 'This result validates direct inputs only. AD-041 derived identity for non-null separators is deferred; separator authority is not yet established.']
    with (output_directory/'SUMMARY.md').open('x') as stream: stream.write('\n'.join(lines)+'\n')
    print(canonical(result))

if __name__=='__main__':main()
