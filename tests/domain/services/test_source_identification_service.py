import pytest

from jga.domain.services.source_identification_service import (
    SourceIdentificationService,
)


def test_service_cannot_be_instantiated():

    with pytest.raises(TypeError):
        SourceIdentificationService()