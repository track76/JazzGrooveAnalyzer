from jga.core.domain.services.dummy_source_identification_service import (
    DummySourceIdentificationService,
)


def test_identify_returns_empty_tuple():

    service = DummySourceIdentificationService()

    result = service.identify(())

    assert result == ()