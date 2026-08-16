
from jga.domain.services.beat_reconstruction_engine import (
    BeatReconstructionEngine,
)
from jga.domain.services.elementary_metric_event_builder import (
    ElementaryMetricEventBuilder,
)
from jga.domain.services.elementary_metric_event_association_service import (
    ElementaryMetricEventAssociationService,
)
from jga.domain.services.internal_metric_timeline_reconstructor import (
    InternalMetricTimelineReconstructor,
)
from jga.domain.services.metric_cluster_builder import (
    MetricClusterBuilder,
)
from jga.domain.services.pulse_builder import (
    PulseBuilder,
)
from jga.domain.internal_metric_signature import InternalMetricSignature

from jga.interfaces.translation.domain_reconstruction_builder import (
    DomainReconstructionBuilder,
)

from jga.translation.domain_reconstruction_input import (
    DomainReconstructionInput,
)

from jga.translation.domain_reconstruction_result import (
    DomainReconstructionResult,
)


class DefaultDomainReconstructionBuilder(
    DomainReconstructionBuilder
):
    """
    Default implementation of domain reconstruction.

    Orchestrates the deterministic reconstruction flow
    from metric input to reconstructed domain objects.
    """

    def __init__(self) -> None:

        self.eme_builder = (
            ElementaryMetricEventBuilder()
        )

        self.eme_association_service = (
            ElementaryMetricEventAssociationService()
        )

        self.beat_builder = (
            BeatReconstructionEngine()
        )

        self.cluster_builder = (
            MetricClusterBuilder()
        )

        self.pulse_builder = (
            PulseBuilder()
        )

        self.timeline_reconstructor = (
            InternalMetricTimelineReconstructor()
        )

    def build(
        self,
        reconstruction_input: DomainReconstructionInput,
    ) -> DomainReconstructionResult:

        declared_meter = reconstruction_input.declared_meter
        internal_metric_signature = (
            InternalMetricSignature(
                numerator=declared_meter.numerator,
                denominator=declared_meter.denominator,
                pulses_per_beat=4,
            )
            if declared_meter is not None
            else None
        )

        beats = self.beat_builder.reconstruct(
            reconstruction_input.ensemble_metric_events,
            declared_metric_reference=(
                reconstruction_input.declared_metric_reference
            ),
            declared_quarter_phase_origin=(
                reconstruction_input.declared_quarter_phase_origin
            ),
            declared_analysis_scope=(
                reconstruction_input.declared_analysis_scope
            ),
        )

        associations = self.eme_association_service.associate(
            reconstruction_input.domain_pulse_candidates,
            reconstruction_input.metric_contributors,
            beats,
        )

        events = self.eme_builder.build(associations)

        clusters = self.cluster_builder.build(
            beats,
            events,
        )

        pulses = self.pulse_builder.build(
            clusters,
        )

        if not pulses:
            return DomainReconstructionResult(
                domain_pulse_candidates=(
                    reconstruction_input.domain_pulse_candidates
                ),
                elementary_metric_events=events,
                beat_references=beats,
                metric_clusters=clusters,
                pulses=pulses,
                internal_metric_timeline=None,
                internal_metric_signature=internal_metric_signature,
                elementary_metric_event_associations=associations,
            )

        timeline = (
            self.timeline_reconstructor.reconstruct(
                pulses,
            )
        )

        return DomainReconstructionResult(
            domain_pulse_candidates=(
                reconstruction_input.domain_pulse_candidates
            ),
            elementary_metric_events=events,
            beat_references=beats,
            metric_clusters=clusters,
            pulses=pulses,
            internal_metric_timeline=timeline,
            internal_metric_signature=internal_metric_signature,
            elementary_metric_event_associations=associations,
        )
