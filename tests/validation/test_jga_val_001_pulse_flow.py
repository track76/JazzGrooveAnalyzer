from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)


def test_jga_val_001_pulse_flow():

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/validation/03 THE COST OF LIVING versione intro + 8 bar.mp3"
    )

    print("\n==============================")
    print("JGA-VAL-001 PULSE FLOW")
    print("==============================")

    print(
        "Pulse candidates:",
        len(context.pulse_candidates)
        if context.pulse_candidates
        else 0
    )

    if context.pulse_candidates:

        print("FIRST 10")

        for pulse in context.pulse_candidates[:10]:
            print(pulse)
