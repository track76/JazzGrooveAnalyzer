
from datetime import datetime
from uuid import uuid4

from jga.domain.metric_contributor import (
    MetricContributor,
)
from jga.translation.domain_reconstruction_builder import (
    DefaultDomainReconstructionBuilder,
)
from jga.translation.domain_reconstruction_input import (
    DomainReconstructionInput,
)


def test_domain_reconstruction_builder_flow():

    builder = (
        DefaultDomainReconstructionBuilder()
    )

    contributor = MetricContributor(
        id=uuid4(),
        sound_source_id=uuid4(),
        musical_function_id=uuid4(),
        active=True,
        created_at=datetime.now(),
    )

    result = builder.build(
        DomainReconstructionInput(
            sound_sources=(),
            metric_context=None,
            metric_contributors=(
                contributor,
            ),
            domain_pulse_candidates=(),
        )
    )

    assert result is not None
    assert result.elementary_metric_events == ()
    assert result.beat_references == ()
    assert result.metric_clusters == ()
    assert result.pulses == ()
    assert result.internal_metric_timeline is None
