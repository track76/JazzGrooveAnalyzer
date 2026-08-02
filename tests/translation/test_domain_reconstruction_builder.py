
from jga.translation.domain_reconstruction_builder import (
    DefaultDomainReconstructionBuilder,
)


def test_domain_reconstruction_builder_exists():

    builder = DefaultDomainReconstructionBuilder()

    assert builder is not None
