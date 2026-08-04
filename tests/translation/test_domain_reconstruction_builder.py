
from jga.translation.domain_reconstruction_builder import (
    DefaultDomainReconstructionBuilder,
)


def test_domain_reconstruction_builder_exists():

    builder = DefaultDomainReconstructionBuilder()

    assert builder is not None


from jga.domain.services.beat_reconstruction_engine import (
    BeatReconstructionEngine,
)


def test_builder_uses_beat_reconstruction_engine():

    builder = DefaultDomainReconstructionBuilder()

    assert isinstance(
        builder.beat_builder,
        BeatReconstructionEngine,
    )
