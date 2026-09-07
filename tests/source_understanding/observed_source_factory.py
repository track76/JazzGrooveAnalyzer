from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from jga.source_understanding.instrument_classification import (
    InstrumentClassification,
)
from jga.source_understanding.instrument_family import (
    InstrumentFamily,
)
from jga.source_understanding.observation_provenance import (
    ObservationProvenance,
)
from jga.source_understanding.observed_source import (
    ObservedSource,
)
from jga.source_understanding.observed_source_collection import (
    ObservedSourceCollection,
)


def make_observed_sources(
    stem_id: str = "bass",
    family: InstrumentFamily = InstrumentFamily.BASS,
    instrument: str = "Double Bass",
    source_identity: UUID | None = None,
) -> ObservedSourceCollection:
    """
    Canonical test builder for semantic observations.
    """

    observed = ObservedSource(
        source_identity=source_identity if source_identity is not None else uuid4(),
        stem_id=stem_id,
        classification=InstrumentClassification(
            family=family,
            instrument=instrument,
            confidence=1.0,
            classifier_name="pytest",
            classifier_version="1.0",
        ),
        provenance=ObservationProvenance(
            stem_id=stem_id,
            pipeline_stage="pytest",
            created_at=datetime.now(),
        ),
    )

    return ObservedSourceCollection((observed,))
