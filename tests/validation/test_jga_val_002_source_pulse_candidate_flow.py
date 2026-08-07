
def test_jga_val_002_source_pulse_candidate_flow():

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
    print("JGA-VAL-002 SOURCE PULSE CANDIDATE FLOW")
    print("==============================")

    print(
        "Source Pulse Sequences:",
        len(context.source_pulse_sequences)
    )

    for sequence in context.source_pulse_sequences:

        print(
            "SOURCE:",
            sequence.source.name,
            "EVENTS:",
            sequence.event_count,
        )

        assert sequence.source is not None

        assert sequence.event_count > 0

    assert (
        context.source_pulse_sequences
        is not None
    )

    assert (
        len(context.source_pulse_sequences)
        > 0
    )
