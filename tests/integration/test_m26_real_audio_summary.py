from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m26_real_audio_summary():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    result = (
        context.behaviour_analytics_result
    )

    assert result is not None

    print()
    print("==============================")
    print("M26 REAL AUDIO SUMMARY")
    print("==============================")

    print(
        "Descriptors:",
        len(
            result.descriptor_set.descriptors
        )
    )

    print(
        "Descriptor names:"
    )

    for descriptor in (
        result.descriptor_set.descriptors[:10]
    ):
        print(
            "-",
            descriptor.name,
            "=",
            descriptor.value,
        )

    print()

    print(
        "Analytical structure:",
        result.analytical_structure is not None,
    )

