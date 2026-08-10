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
from jga.operational.external_storage import ExternalStorage

from jga.reporting.builders.analytical_score_builder import (
    AnalyticalScoreBuilder,
)

from jga.reporting.renderers.ascii_renderer import (
    AnalyticalScoreAsciiRenderer,
)

from jga.visualization.renderers.analytical_score_renderer import (
    AnalyticalScoreRenderer,
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

    output_path = ExternalStorage.from_environment().directory(
        "renders",
        "analytical_score",
    ) / (
        "jga_final_analytical_groove_score.png"
    )

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

    figure = (
        AnalyticalScoreRenderer()
        .render(score)
    )

    figure.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    print()

    print(
        "PNG exported:"
    )

    print(
        output_path
    )


if __name__ == "__main__":
    main()
