from datetime import datetime

from jga.source_understanding.ensemble_profile import EnsembleProfile
from jga.source_understanding.instrument_classification import (
    InstrumentClassification,
)
from jga.source_understanding.instrument_family import InstrumentFamily
from jga.source_understanding.observation_provenance import (
    ObservationProvenance,
)
from jga.source_understanding.observed_source import ObservedSource
from jga.source_understanding.observed_source_collection import (
    ObservedSourceCollection,
)
from jga.source_understanding.services.ensemble_profile_builder import (
    EnsembleProfileBuilder,
)


def make_source(family: InstrumentFamily) -> ObservedSource:
    stem_id = family.name.lower()

    return ObservedSource(
        stem_id=stem_id,
        classification=InstrumentClassification(
            family=family,
            instrument=None,
            confidence=1.0,
            classifier_name="Dummy",
            classifier_version="0.1",
        ),
        provenance=ObservationProvenance(
            stem_id=stem_id,
            pipeline_stage="test",
            created_at=datetime.now(),
        ),
    )


def test_builder_creates_ensemble_profile():
    observed = ObservedSourceCollection(
        (
            make_source(InstrumentFamily.BASS),
            make_source(InstrumentFamily.PERCUSSION),
            make_source(InstrumentFamily.CHORDAL),
        )
    )

    builder = EnsembleProfileBuilder()

    profile = builder.build(observed)

    assert isinstance(profile, EnsembleProfile)
    assert profile.size == 3
    assert InstrumentFamily.BASS in profile.families
    assert InstrumentFamily.PERCUSSION in profile.families
    assert InstrumentFamily.CHORDAL in profile.families


def test_builder_handles_empty_collection():
    builder = EnsembleProfileBuilder()

    profile = builder.build(
        ObservedSourceCollection(tuple())
    )

    assert profile.size == 0
    assert profile.confidence == 0.0
