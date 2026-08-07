
def test_jga_val_001_periodicity_flow():

    from jga.pipeline.default_analysis_pipeline import (
        AnalysisPipeline,
    )

    from jga.separation.dummy_multi_stem_separator import (
        DummyMultiStemSeparator,
    )

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/validation/03 THE COST OF LIVING versione intro + 8 bar.mp3"
    )

    print("\n==============================")
    print("JGA-VAL-001 PERIODICITY FLOW")
    print("==============================")

    print(
        "Periodicity segments:",
        context.periodicity_segments
    )

    print(
        "Metric segments:",
        context.metric_segments
    )

    if context.periodicity_segments:

        for index, segment in enumerate(
            context.periodicity_segments
        ):
            print("\nSEGMENT", index)
            print(segment)

    assert context is not None

