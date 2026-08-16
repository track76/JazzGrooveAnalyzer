from jga.domain.services.reconstructed_measure_builder import (
    ReconstructedMeasureBuilder,
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

        if context.declared_metric_reference is None:

            return

        if context.declared_meter is None:

            return

        if context.internal_metric_signature is None:

            return

        context.reconstructed_measures = (
            self.builder.build(

                beat_references=(
                    context.beat_references
                ),

                metric_clusters=(
                    context.metric_clusters
                ),

                metric_signature=context.internal_metric_signature,

                internal_bpm=float(
                    context.declared_metric_reference.beats_per_minute
                ),

                declared_metric_reference=(
                    context.declared_metric_reference
                ),

                declared_meter=context.declared_meter,

            )
        )
