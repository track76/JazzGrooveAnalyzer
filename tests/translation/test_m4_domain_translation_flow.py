from datetime import datetime
from pathlib import Path
from uuid import uuid4

from jga.core.audio_stem_collection import AudioStemCollection
from jga.core.metric_context import MetricContext
from jga.core.metric_source import MetricSource
from jga.core.pulse_candidate import PulseCandidate as CorePulseCandidate
from jga.core.source_pulse_sequence import SourcePulseSequence

from jga.domain.services.dummy_source_identification_service import (
    DummySourceIdentificationService,
)
from jga.domain.services.rule_based_ensemble_analysis_pipeline import (
    RuleBasedEnsembleAnalysisPipeline,
)
from jga.domain.services.rule_based_metric_contributor_assignment_service import (
    RuleBasedMetricContributorAssignmentService,
)
from jga.domain.services.rule_based_musical_function_assignment_service import (
    RuleBasedMusicalFunctionAssignmentService,
)

from jga.domain.audio_stem import AudioStem

from jga.translation.domain_input_builder import (
    DefaultDomainInputBuilder,
)

from jga.runtime.analysis_context import AnalysisContext


def create_builder():

    ensemble_pipeline = RuleBasedEnsembleAnalysisPipeline(
        source_identifier=DummySourceIdentificationService(),
        function_assigner=RuleBasedMusicalFunctionAssignmentService(),
        contributor_assigner=RuleBasedMetricContributorAssignmentService(),
    )

    return DefaultDomainInputBuilder(
        ensemble_pipeline=ensemble_pipeline,
    )


def test_m4_complete_domain_translation_flow():

    builder = create_builder()

    stem = AudioStem(
        id=uuid4(),
        recording_id=uuid4(),
        name="bass",
        audio_path=Path("bass.wav"),
        sample_rate=44100,
        duration=10.0,
        channels=1,
        created_at=datetime.now(),
    )

    candidate = CorePulseCandidate(
        time=1.25,
        strength=1.0,
        confidence=0.9,
    )

    sequence = SourcePulseSequence(
        source=MetricSource(
            name="bass",
            family="strings",
        ),
        pulse_candidates=[
            candidate,
        ],
    )

    context = AnalysisContext(
        audio=None,
        audio_stems=AudioStemCollection(
            (
                stem,
            )
        ),
        metric_context=MetricContext(
            source_pulse_sequences=(
                sequence,
            ),
            periodicity_segments=(),
            metric_segments=(),
        ),
    )

    result = builder.build(context)

    assert result.ensemble_analysis_result is not None

    assert len(
        result.domain_pulse_candidates
    ) == 1

    assert len(
        result.elementary_metric_events
    ) == 1

    event = result.elementary_metric_events[0]

    contributor = (
        result.ensemble_analysis_result.metric_contributors[0]
    )

    assert event.contributor_id == contributor.id


def test_m4_metric_source_sound_source_contract():

    builder = create_builder()

    stem = AudioStem(
        id=uuid4(),
        recording_id=uuid4(),
        name="Mix",
        audio_path=Path("mix.wav"),
        sample_rate=44100,
        duration=10.0,
        channels=1,
        created_at=datetime.now(),
    )

    candidate = CorePulseCandidate(
        time=1.25,
        strength=1.0,
        confidence=0.9,
    )

    sequence = SourcePulseSequence(
        source=MetricSource(
            name="Mix",
            family="unknown",
        ),
        pulse_candidates=[
            candidate,
        ],
    )

    context = AnalysisContext(
        audio=None,
        audio_stems=AudioStemCollection(
            (
                stem,
            )
        ),
        metric_context=MetricContext(
            source_pulse_sequences=(
                sequence,
            ),
            periodicity_segments=(),
            metric_segments=(),
        ),
    )

    result = builder.build(context)

    assert result.domain_pulse_candidates

    assert result.domain_pulse_candidates[0].sound_source_id == (
        result.ensemble_analysis_result.sound_sources[0].id
    )
