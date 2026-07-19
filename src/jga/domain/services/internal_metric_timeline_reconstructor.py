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
    Reconstructs an InternalMetricTimeline from a validated Pulse sequence.
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

        validated_pulses = self._prepare(pulses)

        return self._builder.build(validated_pulses)

    def _prepare(
        self,
        pulses: tuple[Pulse, ...],
    ) -> tuple[Pulse, ...]:

        self._validator.validate(pulses)

        return pulses
