from jga.geometry.engines import (
    DefaultScientificBehaviourGeometryEngine,
)

from jga.runtime.analysis_context import AnalysisContext


class ScientificBehaviourGeometryEngineRunner:
    """
    Runtime adapter connecting scientific behaviour
    geometry with AnalysisContext.
    """

    def __init__(self) -> None:

        self._engine = (
            DefaultScientificBehaviourGeometryEngine()
        )

    def run(
        self,
        context: AnalysisContext,
    ) -> None:

        if context.metric_clusters is None:
            return

        if context.stability_curve is None:
            return

        context.scientific_geometric_plane = (
            self._engine.project(
                context.metric_clusters,
                context.stability_curve,
            )
        )
