
from datetime import datetime
from uuid import uuid4

from jga.domain.pulse_candidate import (
    PulseCandidate,
)

from jga.domain.metric_contributor import (
    MetricContributor,
)

from jga.engines.ensemble_metric_consensus import (
    EnsembleMetricConsensus,
)


def test_jga_val_003_consensus_synthetic_flow():

    source_a = uuid4()
    source_b = uuid4()
    source_c = uuid4()

    now = datetime.now()

    contributors = (
        MetricContributor(
            id=uuid4(),
            sound_source_id=source_a,
            musical_function_id=uuid4(),
            active=True,
            created_at=now,
        ),
        MetricContributor(
            id=uuid4(),
            sound_source_id=source_b,
            musical_function_id=uuid4(),
            active=True,
            created_at=now,
        ),
        MetricContributor(
            id=uuid4(),
            sound_source_id=source_c,
            musical_function_id=uuid4(),
            active=True,
            created_at=now,
        ),
    )

    candidates = (
        # Event 1
        PulseCandidate(
            id=uuid4(),
            sound_source_id=source_a,
            timestamp=1.000,
            confidence=1.0,
            created_at=now,
        ),
        PulseCandidate(
            id=uuid4(),
            sound_source_id=source_b,
            timestamp=1.015,
            confidence=1.0,
            created_at=now,
        ),
        PulseCandidate(
            id=uuid4(),
            sound_source_id=source_c,
            timestamp=0.990,
            confidence=1.0,
            created_at=now,
        ),

        # Event 2
        PulseCandidate(
            id=uuid4(),
            sound_source_id=source_a,
            timestamp=2.000,
            confidence=1.0,
            created_at=now,
        ),
        PulseCandidate(
            id=uuid4(),
            sound_source_id=source_b,
            timestamp=2.010,
            confidence=1.0,
            created_at=now,
        ),
        PulseCandidate(
            id=uuid4(),
            sound_source_id=source_c,
            timestamp=2.005,
            confidence=1.0,
            created_at=now,
        ),

        # Event 3
        PulseCandidate(
            id=uuid4(),
            sound_source_id=source_a,
            timestamp=3.000,
            confidence=1.0,
            created_at=now,
        ),
        PulseCandidate(
            id=uuid4(),
            sound_source_id=source_b,
            timestamp=3.020,
            confidence=1.0,
            created_at=now,
        ),
        PulseCandidate(
            id=uuid4(),
            sound_source_id=source_c,
            timestamp=3.010,
            confidence=1.0,
            created_at=now,
        ),
    )

    events = (
        EnsembleMetricConsensus()
        .build(
            candidates,
            contributors,
        )
    )

    print("\n==============================")
    print("JGA-VAL-003 CONSENSUS SYNTHETIC FLOW")
    print("==============================")

    print(
        "Ensemble Metric Events:",
        len(events),
    )

    for event in events:
        print(
            "beat_time:",
            event.beat_time,
            "sources:",
            event.source_count,
        )

    assert len(events) == 3

    for event in events:
        assert event.source_count == 3
        assert event.confidence == 0.75
