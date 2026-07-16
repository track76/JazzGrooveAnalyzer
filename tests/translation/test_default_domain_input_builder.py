import pytest

from jga.translation.domain_input_builder import (
    DefaultDomainInputBuilder,
)


def test_default_domain_input_builder_not_implemented():

    builder = DefaultDomainInputBuilder()

    with pytest.raises(NotImplementedError):
        builder.build(None)
