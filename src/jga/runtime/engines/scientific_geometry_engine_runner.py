from jga.geometry.engines import (
    DefaultScientificGeometryEngine,
)

from jga.runtime.analysis_context import AnalysisContext


class ScientificGeometryEngineRunner:
    """
    Runtime adapter connecting Geometry with AnalysisContext.
    """

    def __init__(self) -> None:
        self._engine = DefaultScientificGeometryEngine()

    def run(
        self,
        context: AnalysisContext,
    ) -> None:
        context.scientific_geometric_plane = (
            self._engine.project(
                context.metric_clusters
            )
        )
