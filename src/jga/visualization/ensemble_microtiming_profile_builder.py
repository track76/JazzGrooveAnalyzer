"""
Ensemble Microtiming Profile Builder.

Builds collective microtiming profiles
from analytical metric events.
"""

from statistics import mean

from jga.visualization.metric_event_detail import (
    MetricEventDetail,
)

from jga.visualization.ensemble_microtiming_profile import (
    EnsembleMicrotimingProfile,
)


class EnsembleMicrotimingProfileBuilder:
    """
    Builds ensemble microtiming profiles.
    """

    def build(
        self,
        events: tuple[MetricEventDetail, ...],
        measure_number: int,
    ) -> tuple[
        EnsembleMicrotimingProfile,
        ...
    ]:

        if not events:
            return ()

        groups: dict[
            float,
            list[MetricEventDetail],
        ] = {}

        for event in events:

            groups.setdefault(
                event.beat_position,
                [],
            ).append(
                event
            )

        profiles = []

        for beat_position, group in groups.items():

            offsets = tuple(
                event.offset_ms
                for event in group
            )

            profiles.append(
                EnsembleMicrotimingProfile(
                    measure_number=measure_number,

                    beat_position=beat_position,

                    events=tuple(group),

                    mean_offset_ms=mean(offsets),

                    min_offset_ms=min(offsets),

                    max_offset_ms=max(offsets),

                    spread_ms=(
                        max(offsets)
                        -
                        min(offsets)
                    ),
                )
            )

        return tuple(profiles)
