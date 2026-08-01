
from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m27_chain_trace():

    pipeline = AnalysisPipeline()

    context = pipeline.analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    print()
    print("==============================")
    print("M27 CHAIN TRACE")
    print("==============================")

    print(
        "diagnostic:",
        context.behaviour_diagnostic_result
    )

    print(
        "analytics diagnostic:",
        context.behaviour_analytics_result
        .behaviour_diagnostic_result
    )

    print(
        "scientific report:",
        context.scientific_report
    )

    print(
        "scientific evidence:",
        context.scientific_report
        .scientific_evidence
        if context.scientific_report
        else None
    )

