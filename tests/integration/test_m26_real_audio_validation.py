from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m26_real_audio_validation():

    pipeline = AnalysisPipeline()

    context = pipeline.analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    result = (
        context.behaviour_analytics_result
    )

    assert result is not None

    print()
    print("================================")
    print("M26 REAL AUDIO VALIDATION")
    print("================================")

    print()
    print("Descriptor count:")
    print(
        len(
            result.descriptor_set.descriptors
        )
    )

    print()
    print("Analytical structure:")
    print(
        result.analytical_structure
    )

    print()
    print("Behaviour diagnostic result:")

    print(
        getattr(
            result,
            "behaviour_diagnostic_result",
            "NOT PRESENT",
        )
    )
