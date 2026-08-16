from jga.domain.beat_reference import BeatReference
from jga.domain.metric_cluster import MetricCluster
from jga.domain.internal_metric_signature import (
    InternalMetricSignature,
)
from jga.domain.reconstructed_measure import (
    ReconstructedMeasure,
)
from jga.domain.declared_metric_reference import DeclaredMetricReference
from jga.domain.declared_meter import DeclaredMeter


class ReconstructedMeasureBuilder:
    """
    Builds reconstructed measures by grouping
    Beat References according to the reconstructed
    Internal Metric Signature.

    MetricClusters are preserved and associated
    with their corresponding metric movements.
    """

    def build(
        self,
        beat_references: tuple[
            BeatReference,
            ...
        ],
        metric_signature: InternalMetricSignature,
        internal_bpm: float,
        declared_metric_reference: DeclaredMetricReference | None = None,
        declared_meter: DeclaredMeter | None = None,
        metric_clusters: tuple[
            MetricCluster,
            ...
        ] = (),
    ) -> tuple[
        ReconstructedMeasure,
        ...
    ]:

        if not beat_references:
            return ()

        measures = []

        pulses_per_measure = (
            metric_signature.beats_per_measure
            *
            metric_signature.pulses_per_beat
        )

        for measure_number, start in enumerate(
            range(
                0,
                len(beat_references),
                pulses_per_measure,
            ),
            start=1,
        ):

            group = beat_references[
                start:start + pulses_per_measure
            ]

            if len(group) < pulses_per_measure:
                break

            group_ids = {
                beat.id
                for beat in group
            }

            clusters = tuple(
                cluster
                for cluster in metric_clusters
                if cluster.beat_reference.id
                in group_ids
            )

            measures.append(

                ReconstructedMeasure(

                    number=measure_number,

                    time_signature=str(
                        metric_signature
                    ),

                    internal_bpm=internal_bpm,

                    start_time_seconds=group[0].timestamp,

                    end_time_seconds=(
                        group[-1].timestamp
                        +
                        (
                            60.0
                            /
                            internal_bpm
                        )
                    ),

                    beat_references=group,

                    metric_clusters=clusters,

                    declared_metric_reference=declared_metric_reference,

                    declared_meter=declared_meter,

                )

            )

        return tuple(measures)
