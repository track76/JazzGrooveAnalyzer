import pytest

from jga.runtime.analysis_context import AnalysisContext
from jga.translation.domain_input_builder import (
    DefaultDomainInputBuilder,
)


def test_build_raises_for_none_context():

    builder = DefaultDomainInputBuilder()

    with pytest.raises(ValueError):
        builder.build(None)


def test_build_returns_same_context():

    builder = DefaultDomainInputBuilder()

    context = AnalysisContext(audio=None)

    assert builder.build(context) is context
