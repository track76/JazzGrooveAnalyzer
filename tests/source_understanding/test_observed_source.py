from datetime import datetime

from jga.source_understanding.instrument_classification import (
    InstrumentClassification,
)
from jga.source_understanding.instrument_family import InstrumentFamily
from jga.source_understanding.observation_provenance import (
    ObservationProvenance,
)
from jga.source_understanding.observed_source import ObservedSource


def test_observed_source_creation():
    classification = InstrumentClassification(
        family=InstrumentFamily.BASS,
        instrument="Double Bass",
        confidence=0.98,
        classifier_name="DummyClassifier",
        classifier_version="0.1.0",
    )

    source = ObservedSource(
        stem_id="stem_001",
        classification=classification,
        provenance=ObservationProvenance(
            stem_id="stem_001",
            pipeline_stage="test",
            created_at=datetime.now(),
        ),
    )

    assert source.stem_id == "stem_001"
    assert source.classification == classification
    assert source.provenance.stem_id == "stem_001"


def test_observed_source_is_frozen():
    classification = InstrumentClassification(
        family=InstrumentFamily.UNKNOWN,
        instrument=None,
        confidence=0.0,
        classifier_name="DummyClassifier",
        classifier_version="0.1.0",
    )

    source = ObservedSource(
        stem_id="stem_x",
        classification=classification,
        provenance=ObservationProvenance(
            stem_id="stem_x",
            pipeline_stage="test",
            created_at=datetime.now(),
        ),
    )

    assert source.classification.family is InstrumentFamily.UNKNOWN
