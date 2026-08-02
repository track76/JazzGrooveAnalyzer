from dataclasses import dataclass

from jga.source_understanding.instrument_classification import (
    InstrumentClassification,
)
from jga.source_understanding.observation_provenance import (
    ObservationProvenance,
)


@dataclass(frozen=True, slots=True)
class ObservedSource:
    """
    Result of observing one separated audio stem.

    This object belongs to the observation layer and precedes
    the translation into the domain model.
    """

    stem_id: str
    classification: InstrumentClassification
    provenance: ObservationProvenance
