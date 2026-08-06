"""
Compatibility adapter for the legacy Reporting layer.

The canonical Analytical Score builder lives in the
Visualization layer.

This adapter preserves the public API while delegating
all construction to the Visualization implementation.
"""

from jga.runtime.analysis_context import (
    AnalysisContext,
)

from jga.visualization.analytical_score import (
    AnalyticalScore,
)

from jga.visualization.analytical_score_builder import (
    AnalyticalScoreBuilder as VisualizationAnalyticalScoreBuilder,
)


class AnalyticalScoreBuilder:
    """
    Compatibility adapter.

    Delegates to the canonical Visualization
    AnalyticalScoreBuilder.
    """

    def __init__(self):

        self._builder = (
            VisualizationAnalyticalScoreBuilder()
        )

    def build(
        self,
        context: AnalysisContext,
    ) -> AnalyticalScore:

        return self._builder.build(
            context,
        )
