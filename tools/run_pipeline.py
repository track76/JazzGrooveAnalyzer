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


def main() -> int:

    if len(sys.argv) != 2:
        print("Usage:")
        print("python tools/run_pipeline.py <audiofile>")
        return 1

    filepath = sys.argv[1]

    pipeline = AnalysisPipeline()

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

    print()

    print("Analysis Log")
    print("------------------------------------------")

    for entry in context.log:
        print(
            f"[{entry.timestamp:%H:%M:%S}] {entry.message}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
