from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)

from jga.domain.services.beat_period_estimator import (
    BeatPeriodEstimator,
)


def test_jga_val_001_beat_period():

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/validation/03 THE COST OF LIVING versione intro + 8 bar.mp3"
    )

    period = BeatPeriodEstimator().estimate(
        context.elementary_metric_events
    )

    print(
        "period:",
        period,
    )

    print(
        "bpm:",
        60 / period,
    )

    assert period is not None
