from datetime import datetime

from jga.source_understanding.instrument_classification import (
    InstrumentClassification,
)
from jga.source_understanding.instrument_family import InstrumentFamily
from jga.source_understanding.observation_provenance import (
    ObservationProvenance,
)
from jga.source_understanding.observed_source import (
    ObservedSource,
)
from jga.source_understanding.observed_source_collection import (
    ObservedSourceCollection,
)
from jga.translation.dummy_semantic_bridge import (
    DummySemanticBridge,
)


def test_dummy_semantic_bridge_translates_observations():

    observations = ObservedSourceCollection(
        (
            ObservedSource(
                stem_id="bass",
                classification=InstrumentClassification(
                    family=InstrumentFamily.BASS,
                    instrument="Double Bass",
                    confidence=1.0,
                    classifier_name="Dummy",
                    classifier_version="0.1",
                ),
                provenance=ObservationProvenance(
                    stem_id="bass",
                    pipeline_stage="test",
                    created_at=datetime.now(),
                ),
            ),
        )
    )

    bridge = DummySemanticBridge()

    sound_sources = bridge.translate(observations)

    assert len(sound_sources) == 1
    assert sound_sources[0].name == "bass"
    assert sound_sources[0].family == "bass"
