"""
=========================================================
Jazz Groove Analyzer (JGA)

Pipeline Validation Runner

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
=========================================================
"""

import sys

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline

from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)

from jga.reporting.builders.analytical_score_builder import (
    AnalyticalScoreBuilder,
)

from jga.reporting.renderers.ascii_renderer import (
    AnalyticalScoreAsciiRenderer,
)


def main() -> int:

    multi_mode = "--multi" in sys.argv

    arguments = [
        arg
        for arg in sys.argv[1:]
        if arg != "--multi"
    ]

    if len(arguments) != 1:
        print("Usage:")
        print(
            "python tools/run_pipeline.py [--multi] <audiofile>"
        )
        return 1

    filepath = arguments[0]

    separator = None

    if multi_mode:
        separator = DummyMultiStemSeparator()

    pipeline = AnalysisPipeline(
        separator=separator,
    )

    context = pipeline.analyze(filepath)

    print()
    print("==========================================")
    print("PIPELINE COMPLETED")
    print("==========================================")
    print()

    print(
        "Metric Context:",
        context.metric_context is not None,
    )

    print(
        "Elementary Metric Events:",
        len(context.elementary_metric_events),
    )

    print(
        "Beat References:",
        len(context.beat_references),
    )

    print(
        "Metric Clusters:",
        len(context.metric_clusters),
    )

    print(
        "Reconstructed Measures:",
        len(context.reconstructed_measures),
    )

    if context.reconstructed_measures:

        first_measure = (
            context.reconstructed_measures[0]
        )

        print(
            "First Measure Beat References:",
            len(first_measure.beat_references),
        )

        print(
            "First Measure Metric Clusters:",
            len(first_measure.metric_clusters),
        )

        if first_measure.metric_clusters:

            print(
                "First Cluster Events:",
                len(
                    first_measure.metric_clusters[0].events
                ),
            )

    print(
        "Pulses:",
        len(context.pulses),
    )

    print(
        "Internal Metric Timeline:",
        context.internal_metric_timeline is not None,
    )

    print(
        "Behaviour Observations:",
        len(context.behaviour_observations),
    )

    print(
        "Behaviour Profile:",
        context.behaviour_profile is not None,
    )

    print(
        "Behaviour Descriptors:",
        len(context.behaviour_descriptors),
    )

    print(
        "Descriptor Set:",
        context.descriptor_set is not None,
    )

    print(
        "Analytical Structure:",
        context.analytical_structure is not None,
    )

    print(
        "Behaviour Analytics Result:",
        context.behaviour_analytics_result is not None,
    )

    print(
        "Scientific Geometric Plane:",
        context.scientific_geometric_plane is not None,
    )

    print(
        "Scientific Behaviour Space:",
        context.scientific_behaviour_space is not None,
    )

    if context.scientific_behaviour_space is not None:

        print(
            "Behaviour Trajectories:",
            context.scientific_behaviour_space.trajectory_count,
        )

        if (
            context.scientific_behaviour_space.first_trajectory
            is not None
        ):
            print(
                "Behaviour Points:",
                context.scientific_behaviour_space.first_trajectory.point_count,
            )

    print(
        "Behaviour Observation Frames:",
        len(context.behaviour_observation_frames),
    )

    print(
        "Behaviour Change Events:",
        len(context.behaviour_change_events),
    )

    print()

    print("Analysis Log")
    print("------------------------------------------")

    for entry in context.log:
        print(
            f"[{entry.timestamp:%H:%M:%S}] {entry.message}"
        )

    print()

    print("Analytical Score")
    print("------------------------------------------")

    score_builder = AnalyticalScoreBuilder()

    score = score_builder.build(
        context,
    )

    renderer = AnalyticalScoreAsciiRenderer()

    print(
        renderer.render(score)
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
