from jga.domain.elementary_metric_event import ElementaryMetricEvent


class ElementaryMetricEventBuilder:
    """
    Builds ElementaryMetricEvent objects from DSP pulse intervals.
    """

    def build(
        self,
        pulse_intervals,
    ) -> tuple[ElementaryMetricEvent, ...]:

        if not pulse_intervals:
            return ()

        raise NotImplementedError