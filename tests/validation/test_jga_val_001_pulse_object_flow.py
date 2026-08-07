from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)


def test_jga_val_001_pulse_object_flow():

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/validation/03 THE COST OF LIVING versione intro + 8 bar.mp3"
    )

    print("\n==============================")
    print("JGA-VAL-001 PULSE OBJECT FLOW")
    print("==============================")

    print(
        "Pulses:",
        len(context.pulses)
    )

    for pulse in context.pulses[:10]:
        print(pulse)
