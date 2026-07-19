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

    This service implements the Metric Projection stage defined
    by F-004. Projection never modifies the observed Pulse
    sequence and preserves every physical timestamp.
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

        return self._builder.build(
            self._project(pulses)
        )

    def _project(
        self,
        pulses: tuple[Pulse, ...],
    ) -> tuple[Pulse, ...]:

        self._validator.validate(pulses)

        return tuple(
            self._project_pulse(pulse)
            for pulse in pulses
        )

    def _project_pulse(
        self,
        pulse: Pulse,
    ) -> Pulse:
        """
        Projects a Pulse into the Internal Metric Timeline.

        F-004 invariants:

        - physical timestamp is preserved;
        - Pulse identity is preserved;
        - no musical information is altered.
        """

        return pulse
