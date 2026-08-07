
def test_jga_val_004_consensus_pipeline_flow():

    from jga.pipeline.default_analysis_pipeline import (
        AnalysisPipeline,
    )

    from jga.separation.dummy_multi_stem_separator import (
        DummyMultiStemSeparator,
    )

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/validation/"
        "03 THE COST OF LIVING versione intro + 8 bar.mp3"
    )

    print("\n==============================")
    print("JGA-VAL-004 CONSENSUS PIPELINE FLOW")
    print("==============================")

    print(
        "Metric Contributors:",
        len(context.metric_contributors),
    )

    print(
        "Ensemble Metric Events:",
        len(context.ensemble_metric_events),
    )

    assert context.metric_contributors

    assert (
        context.ensemble_metric_events
        is not None
    )

