from jga.core.audio_stem_collection import AudioStemCollection
from jga.core.metric_context import MetricContext
from jga.runtime.analysis_context import AnalysisContext

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

from jga.translation.domain_input_builder import (
    DefaultDomainInputBuilder,
)


def create_builder() -> DefaultDomainInputBuilder:

    pipeline = RuleBasedEnsembleAnalysisPipeline(
        source_identifier=DummySourceIdentificationService(),
        function_assigner=RuleBasedMusicalFunctionAssignmentService(),
        contributor_assigner=RuleBasedMetricContributorAssignmentService(),
    )

    return DefaultDomainInputBuilder(
        ensemble_pipeline=pipeline,
    )


def test_build_requires_metric_context():

    builder = create_builder()

    context = AnalysisContext(
        audio=None,
        audio_stems=AudioStemCollection(()),
    )

    try:
        builder.build(context)
        assert False
    except ValueError:
        assert True


def test_build_returns_same_context_with_translation():

    builder = create_builder()

    context = AnalysisContext(
        audio=None,
        audio_stems=AudioStemCollection(()),
        metric_context=MetricContext(
            source_pulse_sequences=(),
            periodicity_segments=(
                object(),
            ),
            metric_segments=(),
        ),
    )

    result = builder.build(context)

    assert result is context
    assert result.ensemble_analysis_result is not None
    assert result.domain_pulse_candidates == ()
