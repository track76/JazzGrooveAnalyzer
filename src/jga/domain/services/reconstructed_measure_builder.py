from jga.domain.beat_reference import BeatReference
from jga.domain.internal_metric_signature import (
    InternalMetricSignature,
)
from jga.domain.reconstructed_measure import (
    ReconstructedMeasure,
)


class ReconstructedMeasureBuilder:
    """
    Builds reconstructed measures by grouping
    Beat References according to the reconstructed
    Internal Metric Signature.
    """

    def build(
        self,
        beat_references: tuple[
            BeatReference,
            ...
        ],
        metric_signature: InternalMetricSignature,
        internal_bpm: float,
    ) -> tuple[
        ReconstructedMeasure,
        ...
    ]:

        if not beat_references:
            return ()

        measures = []

        beats_per_measure = (
            metric_signature.beats_per_measure
        )

        for measure_number, start in enumerate(
            range(
                0,
                len(beat_references),
                beats_per_measure,
            ),
            start=1,
        ):

            group = beat_references[
                start:start + beats_per_measure
            ]

            if len(group) < beats_per_measure:
                break

            measures.append(

                ReconstructedMeasure(

                    number=measure_number,

                    time_signature=str(
                        metric_signature
                    ),

                    internal_bpm=internal_bpm,

                    start_time_seconds=group[0].timestamp,

                    end_time_seconds=group[-1].timestamp,

                    beat_references=group,

                    metric_clusters=(),

                )

            )

        return tuple(measures)

