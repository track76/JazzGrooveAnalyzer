from __future__ import annotations

from datetime import datetime

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
) -> ObservedSourceCollection:
    """
    Canonical test builder for semantic observations.
    """

    observed = ObservedSource(
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
