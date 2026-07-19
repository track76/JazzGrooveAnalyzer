from jga.domain.internal_metric_timeline import InternalMetricTimeline
from jga.domain.pulse import Pulse
from jga.domain.services.internal_metric_timeline_builder import (
    InternalMetricTimelineBuilder,
)
from jga.domain.services.pulse_sequence_validator import (
    PulseSequenceValidator,
)


class InternalMetricTimelineReconstructor:
    """
    Reconstructs the Internal Metric Timeline from a Pulse sequence.

    Implements the Metric Projection stage defined by F-004.

    Metric Projection operates on the Pulse sequence as a whole.
    It never modifies individual Pulse entities.
    """

    def __init__(
        self,
        validator: PulseSequenceValidator | None = None,
        builder: InternalMetricTimelineBuilder | None = None,
    ) -> None:
        self._validator = validator or PulseSequenceValidator()
        self._builder = builder or InternalMetricTimelineBuilder()

    def reconstruct(
        self,
        pulses: tuple[Pulse, ...],
    ) -> InternalMetricTimeline:

        projected = self._project(pulses)

        return self._builder.build(projected)

    def _project(
        self,
        pulses: tuple[Pulse, ...],
    ) -> tuple[Pulse, ...]:
        """
        Performs Metric Projection on the complete Pulse sequence.

        Scientific invariants (F-004):

        - physical timestamps are preserved;
        - Pulse identity is preserved;
        - chronological ordering is preserved;
        - projection is deterministic;
        - no arbitrary musical interpretation is introduced.
        """

        self._validator.validate(pulses)

        return pulses
