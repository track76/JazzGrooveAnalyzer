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

        return (
            event.timestamp
            - beat_reference.timestamp
        ) * 1000.0
