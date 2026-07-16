from jga.translation.domain_input_builder import (
    DomainInputBuilder,
)


def test_translator_can_be_instantiated():

    builder = DomainInputBuilder()

    assert builder is not None
