"""
Metric Offset Calculator

M16
"""

class MetricOffsetCalculator:
    """
    Computes the observed temporal displacement
    between one ElementaryMetricEvent and one
    BeatReference.
    """

    def compute(
        self,
        event,
        beat_reference,
    ) -> float:

        return self.compute_seconds(event, beat_reference) * 1000.0

    def compute_seconds(
        self,
        event,
        beat_reference,
    ) -> float:
        """Return the neutral signed displacement in physical seconds."""

        return event.timestamp - beat_reference.timestamp
