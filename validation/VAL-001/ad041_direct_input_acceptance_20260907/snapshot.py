"""Capture scientific observations using the selected checkout on PYTHONPATH."""
from dataclasses import asdict
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
import sys
from uuid import UUID
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.reporting.rhythm_section_timing_report import AuthorizedSourceInput
from jga.reporting.rhythm_section_timing_report_service import RhythmSectionTimingReportService

ROOT = Path.cwd()
AUTHORITY = ROOT / 'validation/VAL-001/authorities/AD-041_DIRECT_INPUT_SOURCE_INSTANCE_AUTHORITY_V1.json'
EXPECTED_AUTHORITY_SHA = 'b3a76361f30a0dbbc0b79cd15b4a7485ec66b95c42d2cd2c076cb783ee9da347'
LABELS = ('Drums', 'Piano', 'Double Bass')
FILES = ('drums.wav', 'piano.wav', 'double_bass.wav')
KWARGS = dict(execution_id='VAL001-AD041-PROSPECTIVE-01', provenance_id='VAL-001-CONTROLLED-STEMS', role_authority_id='AD-040-CONTROLLED-ROLE-AUTHORITY', role_authority_fingerprint='b8983e8', calibration_applicability='UNESTABLISHED', calibration_authority_id='VAL-001-CALIBRATION-CONTEXT', calibration_authority_fingerprint='UNAPPLIED-CONTROLLED-CONTEXT', jga_revision='AD041-DIRECT-INPUT-ACCEPTANCE-01')

def encode(value):
    if isinstance(value, UUID): return str(value)
    if isinstance(value, datetime): return 'OPERATIONAL_WALL_CLOCK_EXCLUDED'
    raise TypeError(type(value))

def canonical(value):
    return json.dumps(value, default=encode, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False) + '\n'

def capture(corrected):
    assert sha256(AUTHORITY.read_bytes()).hexdigest() == EXPECTED_AUTHORITY_SHA
    authority = json.loads(AUTHORITY.read_bytes())
    inputs = []
    for label, filename, binding in zip(LABELS, FILES, authority['bindings']):
        kw = dict(source_authority_id=authority['source_authority_id'], source_instance_key=binding['source_instance_key']) if corrected else {}
        inputs.append(AuthorizedSourceInput(ROOT / 'recordings/validation/stems' / filename, label, 'TEMPORAL_REFERENCE' if label == 'Drums' else 'ACCOMPANIMENT', binding['asset_sha256'], **kw))
    contexts = []
    class RecordingPipeline(AnalysisPipeline):
        def analyze(self, *args, **kwargs):
            result = super().analyze(*args, **kwargs)
            contexts.append(result)
            return result
    report = RhythmSectionTimingReportService(pipeline_factory=RecordingPipeline).build(tuple(inputs), **KWARGS)
    document = json.loads(report.canonical_json)
    diagnostics = {}
    for context in contexts:
        digest = sha256(context.audio.path.read_bytes()).hexdigest()
        diagnostics[digest] = {
            'candidates': [asdict(x) for x in context.domain_pulse_candidates],
            'events': [asdict(x) for x in context.elementary_metric_events],
            'stem_names': [x.name for x in context.audio_stems],
            'stem_ids': [str(x.id) for x in context.audio_stems],
            'observed_classifications': [asdict(x.classification) for x in context.observed_sources],
        }
    return {'report': document, 'diagnostics': diagnostics}

if __name__ == '__main__':
    destination = Path(sys.argv[2])
    with destination.open('x') as stream:
        stream.write(canonical(capture(sys.argv[1] == 'corrected')))
