import pytest

from jga.core.domain.services.pulse_candidate_extractor import (
    PulseCandidateExtractor,
)


def test_extractor_cannot_be_instantiated():

    with pytest.raises(TypeError):
        PulseCandidateExtractor()