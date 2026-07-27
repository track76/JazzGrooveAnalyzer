"""
=========================================================
Jazz Groove Analyzer (JGA)

Analytical Score Validation

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
=========================================================
"""

import sys

from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.reporting.builders.analytical_score_builder import (
    AnalyticalScoreBuilder,
)

from jga.reporting.renderers.ascii_renderer import (
    AnalyticalScoreAsciiRenderer,
)


def main():

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "python tools/render_analytical_score.py <audiofile>"
        )

        return

    pipeline = AnalysisPipeline()

    context = pipeline.analyze(
        sys.argv[1],
    )

    print()
    print("=" * 60)
    print("REPORTING VALIDATION")
    print("=" * 60)
    print()

    print(
        "Audio:",
        context.audio.path.name,
    )

    print(
        "Metric Clusters:",
        len(context.metric_clusters),
    )

    print(
        "Beat References:",
        len(context.beat_references),
    )

    print(
        "Pulses:",
        len(context.pulses),
    )

    print(
        "Behaviour Observations:",
        len(context.behaviour_observations),
    )

    print(
        "Behaviour Descriptors:",
        len(context.behaviour_descriptors),
    )

    print()

    score = (
        AnalyticalScoreBuilder().build(
            context,
        )
    )

    renderer = (
        AnalyticalScoreAsciiRenderer()
    )

    print(renderer.render(score))


if __name__ == "__main__":
    main()

