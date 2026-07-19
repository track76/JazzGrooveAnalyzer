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
    Software implementation of the mathematical transformation τ₇.

    τ₇ reconstructs the Internal Metric Timeline from an ordered
    Pulse sequence.
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

        reconstructed_sequence = self._reconstruct_sequence(pulses)

        return self._builder.build(reconstructed_sequence)

    def _reconstruct_sequence(
        self,
        pulses: tuple[Pulse, ...],
    ) -> tuple[Pulse, ...]:
        """
        Implements the mathematical transformation τ₇.

        Scientific invariants:

        - Pulse identity is preserved.
        - Physical timestamps are preserved.
        - Chronological ordering is preserved.
        - Temporal continuity is preserved.
        - The reconstruction is deterministic.
        """

        self._validator.validate(pulses)

        return pulses
