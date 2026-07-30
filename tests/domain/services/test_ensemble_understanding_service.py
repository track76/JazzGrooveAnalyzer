from datetime import datetime
from uuid import uuid4

from jga.domain.ensemble_profile import EnsembleProfile
from jga.domain.services.ensemble_understanding_service import (
    EnsembleUnderstandingService,
)
from jga.source_understanding.instrument_classification import (
    InstrumentClassification,
)
from jga.source_understanding.instrument_family import (
    InstrumentFamily,
)
from jga.source_understanding.observed_source import (
    ObservedSource,
)
from jga.source_understanding.observed_source_collection import (
    ObservedSourceCollection,
)


def test_ensemble_understanding_creates_profile():

    observed = ObservedSourceCollection(
        (
            ObservedSource(
                stem_id="bass",
                classification=InstrumentClassification(
                    family=InstrumentFamily.BASS,
                    instrument="bass",
                    confidence=0.9,
                    classifier_name="test",
                    classifier_version="0.1",
                ),
            ),
        )
    )

    service = EnsembleUnderstandingService()

    profile = service.analyze(observed)

    assert isinstance(
        profile,
        EnsembleProfile,
    )

    assert len(profile.sound_sources) == 1

    assert len(
        profile.source_function_assignments
    ) == 1
