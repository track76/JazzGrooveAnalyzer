from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)


def test_jga_val_001_baseline():

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/validation/03 THE COST OF LIVING versione intro + 8 bar.mp3"
    )

    print("\n==============================")
    print("JGA-VAL-001 BASELINE")
    print("==============================")

    print(
        "Audio:",
        context.audio,
    )

    if context.ensemble_profile:
        print(
            "Ensemble:",
            context.ensemble_profile,
        )

    if context.reconstructed_measures:
        print(
            "Measures:",
            len(
                context.reconstructed_measures
            ),
        )

        print(
            "First measure:",
            context.reconstructed_measures[0],
        )

    if context.metric_context:
        print(
            "Metric context:",
            context.metric_context,
        )

    assert context is not None
