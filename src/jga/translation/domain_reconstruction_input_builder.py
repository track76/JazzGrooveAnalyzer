
from jga.runtime.analysis_context import AnalysisContext
from jga.translation.domain_reconstruction_input import (
    DomainReconstructionInput,
)


class DomainReconstructionInputBuilder:
    """
    Builds the explicit input contract for
    domain metric reconstruction.

    Converts Runtime Context information into
    a pure domain reconstruction input.
    """

    def build(
        self,
        context: AnalysisContext,
    ) -> DomainReconstructionInput:

        if context is None:
            raise ValueError(
                "AnalysisContext cannot be None."
            )

        if context.ensemble_analysis_result is None:
            raise ValueError(
                "EnsembleAnalysisResult required."
            )

        if context.metric_context is None:
            raise ValueError(
                "MetricContext required."
            )

        return DomainReconstructionInput(
            sound_sources=(
                context.ensemble_analysis_result.sound_sources
            ),
            metric_context=context.metric_context,
            metric_contributors=(
                context.ensemble_analysis_result.metric_contributors
            ),
            domain_pulse_candidates=(
                context.domain_pulse_candidates
            ),
            ensemble_metric_events=(
                context.ensemble_metric_events
            ),
        )
