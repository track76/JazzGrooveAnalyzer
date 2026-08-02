from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m37_real_audio_behaviour_construction():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    assert context.internal_metric_timeline is not None

    assert context.behaviour_observations

    assert context.behaviour_profile is not None

    print()

    print("==============================")
    print("M37 REAL AUDIO BEHAVIOUR CONSTRUCTION")
    print("==============================")

    print(
        "Internal Metric Timeline:",
        context.internal_metric_timeline
    )

    print(
        "Behaviour observations:",
        len(
            context.behaviour_observations
        )
    )

    print(
        "Behaviour profile:",
        context.behaviour_profile
    )

    print(
        "Behaviour analytics:",
        context.behaviour_analytics_result is not None,
    )
