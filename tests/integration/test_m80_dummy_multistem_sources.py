from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)


def test_m80_dummy_multistem_reaches_domain():

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    assert context.ensemble_analysis_result is not None

    print()
    print("==============================")
    print("MULTISTEM DEBUG")
    print("==============================")

    print(
        "Sources:",
        len(
            context.ensemble_analysis_result.sound_sources
        )
    )

    for source in (
        context.ensemble_analysis_result.sound_sources
    ):
        print(
            source.name
        )
