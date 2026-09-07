"""Prospective AD-041 identity tests; no labels or checksums enter UUID names."""
from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path
import shutil
from uuid import NAMESPACE_URL, uuid5

import pytest
from jga.audio.file_audio_source import FileAudioSource
from jga.engines.audio_preprocessor import AudioPreprocessor
from jga.core.audio_stem import AudioStem
from jga.runtime.analysis_context import AnalysisContext
from jga.separation.null_separator import NullSeparator
from jga.separation.dummy_multi_stem_separator import DummyMultiStemSeparator
from jga.source_understanding.services.source_understanding_service import SourceUnderstandingService
from jga.translation.dummy_semantic_bridge import DummySemanticBridge
from jga.reporting.rhythm_section_timing_report import AuthorizedSourceInput, RhythmSectionTimingReportError
from jga.reporting.rhythm_section_timing_report_service import RhythmSectionTimingReportService

AUTH = json.loads(Path('validation/VAL-001/authorities/AD-041_DIRECT_INPUT_SOURCE_INSTANCE_AUTHORITY_V1.json').read_text())
PATHS = tuple(Path('recordings/validation/stems') / name for name in ('drums.wav','piano.wav','double_bass.wav'))

def binding(index):
    return dict(source_authority_id=AUTH['source_authority_id'], source_instance_key=AUTH['bindings'][index]['source_instance_key'], expected_sha256=AUTH['bindings'][index]['asset_sha256'])

def test_three_mix_identities_preserved_through_semantic_bridge_and_relocation(tmp_path):
    ids = []
    for index, path in enumerate(PATHS):
        audio = FileAudioSource().load(str(path), **binding(index))
        expected = uuid5(NAMESPACE_URL, json.dumps(dict(rule='jga-direct-input-source-identity/v1', source_authority_id=AUTH['source_authority_id'], source_instance_key=AUTH['bindings'][index]['source_instance_key']), sort_keys=True, separators=(',',':')))
        assert audio.source_identity == expected
        context = AnalysisContext(audio=audio)
        context = AudioPreprocessor().process(context)
        stem = NullSeparator().process(context).audio_stems[0]
        assert stem.name == 'Mix' and stem.id == expected
        observed = SourceUnderstandingService().process(context.audio_stems)
        assert observed[0].source_identity == expected
        assert DummySemanticBridge().translate(observed)[0].id == expected
        moved = tmp_path / f'renamed-{index}.wav'
        shutil.copyfile(path, moved)
        replay = FileAudioSource().load(str(moved), **binding(index))
        assert replay.source_identity == expected
        assert replay.asset_sha256 == audio.asset_sha256 == binding(index)['expected_sha256']
        ids.append(expected)
    assert len(set(ids)) == 3


def test_asset_identity_is_independent_of_authorized_instance():
    # Synthetic caller authority explicitly binds the same bytes to another instance.
    first = FileAudioSource().load(str(PATHS[0]), **binding(0))
    other = FileAudioSource().load(str(PATHS[0]), **{**binding(0), 'source_instance_key':'TEST-INDEPENDENT-INSTANCE'})
    assert first.asset_sha256 == other.asset_sha256
    assert first.source_identity != other.source_identity
    # Conversely an explicitly supplied test binding can retain the instance across assets.
    second_asset = FileAudioSource().load(str(PATHS[1]), **{**binding(0), 'expected_sha256':binding(1)['expected_sha256']})
    assert first.source_identity == second_asset.source_identity
    assert first.asset_sha256 != second_asset.asset_sha256


@pytest.mark.parametrize('kwargs', [dict(source_authority_id='x'), dict(source_authority_id='x',source_instance_key=''), dict(source_authority_id='x',source_instance_key='y'), dict(source_authority_id='x',source_instance_key='y',expected_sha256='0'*64)])
def test_invalid_authority_or_asset_binding_fails_closed(kwargs):
    with pytest.raises(ValueError, match='AD041_'):
        FileAudioSource().load(str(PATHS[0]), **kwargs)


def test_non_null_separator_has_no_ad041_authority():
    audio = FileAudioSource().load(str(PATHS[0]), **binding(0))
    context = AnalysisContext(audio=audio)
    context.processed_audio = audio.raw_audio
    stems = DummyMultiStemSeparator().process(context).audio_stems
    assert all(x.source_identity_rule == 'UNAUTHORIZED' for x in stems)
    assert all(x.id != audio.source_identity for x in stems)
    assert all(x.id != uuid5(NAMESPACE_URL, x.name) for x in stems)


def test_report_rejects_missing_authority_and_colliding_instances():
    from tests.reporting.test_rhythm_section_timing_report_service import AUTHORITY
    first = AuthorizedSourceInput(PATHS[0], 'Reference', 'TEMPORAL_REFERENCE', **binding(0))
    second = replace(first, label='Other display', role='ACCOMPANIMENT')
    with pytest.raises(RhythmSectionTimingReportError, match='AD041_SOURCE_IDENTITY_COLLISION'):
        RhythmSectionTimingReportService().build((first, second), **AUTHORITY)
    with pytest.raises(RhythmSectionTimingReportError, match='AD041_MISSING_DIRECT_INPUT_AUTHORITY'):
        RhythmSectionTimingReportService().build((first, replace(second, source_authority_id=None)), **AUTHORITY)


def test_report_rejects_non_null_separator_authority_claim():
    from tests.reporting.test_rhythm_section_timing_report_service import AUTHORITY
    from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
    sources = tuple(AuthorizedSourceInput(path, label, role, **binding(index)) for index,path,label,role in (
        (0,PATHS[0],'Drums','TEMPORAL_REFERENCE'), (1,PATHS[1],'Piano','ACCOMPANIMENT')))
    service = RhythmSectionTimingReportService(lambda: AnalysisPipeline(separator=DummyMultiStemSeparator()))
    with pytest.raises(RhythmSectionTimingReportError, match='AMBIGUOUS_EME_SOURCE_IDENTITY|AD041_UNAUTHORIZED_SOURCE_IDENTITY'):
        service.build(sources, **AUTHORITY)
