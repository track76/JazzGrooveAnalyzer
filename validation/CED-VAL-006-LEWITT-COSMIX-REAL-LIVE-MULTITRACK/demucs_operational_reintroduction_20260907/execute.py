"""Prospective production acceptance runner. No reference data accessed here."""
from hashlib import sha256
import json
import os
from pathlib import Path
import sys

from jga.reporting.demucs_timing_report_service import DemucsTimingReportService
from jga.reporting.rhythm_section_timing_report import AuthorizedSourceInput
from jga.separation.authorized_demucs import AuthorizedDemucsRunner, file_sha256

HERE = Path(__file__).resolve().parent


def main():
    run = sys.argv[1]
    if run not in ['run_1','run_2']:
        raise ValueError(run)
    parent = json.loads((HERE/'parent_source_authority.json').read_text())
    auth = json.loads((HERE/'separator_authority.json').read_text())
    protocol_sha = file_sha256(HERE/'PROTOCOL.json')
    root = Path(os.environ['JGA_EXTERNAL_ROOT'])
    mix = json.loads((HERE.parent/'controlled_mixdown_authority/controlled_mixdown_authority.json').read_text())
    source = AuthorizedSourceInput(Path(mix['output_asset']['absolute_operational_path']),
        'Controlled mixture','TEMPORAL_REFERENCE',expected_sha256=parent['asset_sha256'],
        source_authority_id=parent['identity_inputs']['source_authority_id'],
        source_instance_key=parent['identity_inputs']['source_instance_key'])
    runner = AuthorizedDemucsRunner(HERE/'separator_authority.json',
        file_sha256(HERE/'separator_authority.json'),
        '/Users/StarTrack/Development/JGA-Demucs-env/bin/python',
        Path.home()/'.cache/huggingface/hub/models--adefossez--HTDemucs-6s/snapshots'/auth['model']['registry_revision'],
        resume_checksums=(json.loads((HERE/'run_1_resume_authority.json').read_text())['output_sha256']
            if run=='run_1' else None))
    report, stems, contexts = DemucsTimingReportService().build(source, runner,
        root/'experiments/CEDVAL006-AD041-HTDEMUCS6S-OPERATIONAL-20260907'/run,
        roles=auth['operational_role_authority'],execution_id='EXEC-CEDVAL006-AD041-HTDEMUCS6S-001',
        provenance_id='PROV-CEDVAL006-AD041-HTDEMUCS6S-001',
        role_authority_id='PI-CEDVAL006-HTDEMUCS6S-OPERATIONAL-ROLES-001',
        role_authority_fingerprint=protocol_sha,calibration_applicability='UNESTABLISHED',
        calibration_authority_id='PR-CEDVAL006-AD041-HTDEMUCS6S-OPERATIONAL-001',
        calibration_authority_fingerprint=protocol_sha,jga_revision='8e6a626ef00c4e51f2769a051180a080704e24f8+prospective-AD041-handoff')
    report.write(HERE/('canonical_'+run+'.json'))
    evidence={'protocol_sha256_before_execution':protocol_sha,
        'canonical_sha256':sha256(report.canonical_json.encode()).hexdigest(),
        'outputs':[{'source_identity':str(s.id),'key':s.name,'sha256':s.asset_sha256,
                    'path':s.asset_path,'lineage':s.transformation_provenance} for s in stems]}
    (HERE/('execution_'+run+'.json')).write_text(json.dumps(evidence,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'run':run,'scientific_fingerprint':report.scientific_fingerprint,
         'counts':{k:len(v.elementary_metric_events) for k,v in contexts.items()}}),flush=True)


if __name__ == '__main__':
    main()
