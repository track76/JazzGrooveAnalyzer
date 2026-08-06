from jga.domain.services.reconstructed_measure_builder import (
    ReconstructedMeasureBuilder,
)

from jga.domain.internal_metric_signature import (
    InternalMetricSignature,
)

from jga.runtime.analysis_context import (
    AnalysisContext,
)


class ReconstructedMeasureRunner:
    """
    Builds reconstructed measures from the
    internal metric reconstruction.
    """

    def __init__(self):

        self.builder = (
            ReconstructedMeasureBuilder()
        )

    def run(
        self,
        context: AnalysisContext,
    ) -> None:

        if not context.beat_references:

            return

        signature = InternalMetricSignature(

            numerator=4,

            denominator=4,

            pulses_per_beat=4,

        )

        context.reconstructed_measures = (
            self.builder.build(

                beat_references=(
                    context.beat_references
                ),

                metric_clusters=(
                    context.metric_clusters
                ),

                metric_signature=signature,

                internal_bpm=120.0,

            )
        )
