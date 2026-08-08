def test_jga_val_001_consensus_flow():

    from collections import Counter

    from jga.pipeline.default_analysis_pipeline import (
        AnalysisPipeline,
    )

    from jga.separation.dummy_multi_stem_separator import (
        DummyMultiStemSeparator,
    )

    from jga.engines.ensemble_metric_consensus import (
        EnsembleMetricConsensus,
    )

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/validation/03 THE COST OF LIVING versione intro + 8 bar.mp3"
    )

    print("\n==============================")
    print("JGA-VAL-001 CONSENSUS FLOW")
    print("==============================")

    assert context is not None

    assert context.ensemble_analysis_result is not None

    contributors = (
        context.ensemble_analysis_result.metric_contributors
    )

    assert contributors is not None

    engine = EnsembleMetricConsensus()

    events = engine.build(
        pulse_candidates=(
            context.domain_pulse_candidates
        ),
        metric_contributors=contributors,
    )

    print(
        "Metric Contributors:",
        len(contributors)
    )

    print(
        "Ensemble Metric Events:",
        len(events)
    )

    for index, event in enumerate(events[:10]):

        print("\nEVENT", index)
        print(event)

    #
    # Scientific validation
    #

    assert len(contributors) == 5

    source_observations = Counter(
        (
            sequence.source.source_id,
            candidate.time,
            candidate.strength,
            candidate.confidence,
        )
        for sequence in context.metric_context.source_pulse_sequences
        for candidate in sequence.pulse_candidates
    )
    domain_observations = Counter(
        (
            candidate.sound_source_id,
            candidate.timestamp,
            candidate.strength,
            candidate.confidence,
        )
        for candidate in context.domain_pulse_candidates
    )

    assert domain_observations == source_observations

    assert len(events) > 0

    first_event = events[0]

    assert first_event.source_count == 5

    assert first_event.confidence == 1.0

    assert (
        first_event.start_time
        ==
        first_event.end_time
    )

    assert (
        first_event.beat_time
        ==
        first_event.start_time
    )
