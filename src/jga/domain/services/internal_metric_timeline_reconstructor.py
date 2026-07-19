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

    This service implements the Metric Projection stage defined by F-004.
    Projection never modifies the observed Pulse sequence.
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

        projected_pulses = self._project(pulses)

        return self._builder.build(projected_pulses)

    def _project(
        self,
        pulses: tuple[Pulse, ...],
    ) -> tuple[Pulse, ...]:

        self._validator.validate(pulses)

        projected = []

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
        Projects a Pulse into the Internal Metric Timeline.

        Current implementation preserves the Pulse unchanged.
        """

        return pulse
