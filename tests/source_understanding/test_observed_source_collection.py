from datetime import datetime

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


def make_source(stem_id: str) -> ObservedSource:
    return ObservedSource(
        stem_id=stem_id,
        classification=InstrumentClassification(
            family=InstrumentFamily.UNKNOWN,
            instrument=None,
            confidence=0.0,
            classifier_name="DummyClassifier",
            classifier_version="0.1.0",
        ),
        provenance=ObservationProvenance(
            stem_id=stem_id,
            pipeline_stage="test",
            created_at=datetime.now(),
        ),
    )


def test_collection_behaves_like_sequence():
    collection = ObservedSourceCollection(
        (
            make_source("stem_1"),
            make_source("stem_2"),
        )
    )

    assert len(collection) == 2
    assert collection[0].stem_id == "stem_1"
    assert collection[1].stem_id == "stem_2"


def test_collection_is_iterable():
    collection = ObservedSourceCollection(
        (
            make_source("a"),
            make_source("b"),
            make_source("c"),
        )
    )

    ids = [source.stem_id for source in collection]

    assert ids == ["a", "b", "c"]
