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

    Implements F-004 Metric Projection.
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

        self._validator.validate(pulses)

        projected: list[Pulse] = []

        for pulse in pulses:
            projected.append(
                self._project_pulse(pulse)
            )

        return tuple(projected)

    def _project_pulse(
        self,
        pulse: Pulse,
    ) -> Pulse:
        """
        F-004 Metric Projection.

        Physical time is preserved.
        Musical meaning is preserved.
        Pulse identity is preserved.
        """

        return pulse
