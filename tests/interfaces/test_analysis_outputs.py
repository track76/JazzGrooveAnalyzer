from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from jga.interfaces.validation import (
    AnalysisOutput,
    AnalysisOutputState,
    AnalysisTempo,
)


def test_present_output_requires_a_value():
    with pytest.raises(ValueError):
        AnalysisOutput(AnalysisOutputState.PRESENT)


def test_non_present_output_cannot_contain_a_value():
    with pytest.raises(ValueError):
        AnalysisOutput(
            AnalysisOutputState.UNAVAILABLE,
            AnalysisTempo(Decimal("78"), "quarter"),
        )


def test_analysis_output_and_value_are_immutable():
    output = AnalysisOutput(
        AnalysisOutputState.PRESENT,
        AnalysisTempo(Decimal("78"), "quarter"),
    )

    with pytest.raises(FrozenInstanceError):
        output.state = AnalysisOutputState.EMPTY

    with pytest.raises(FrozenInstanceError):
        output.value.beat_unit = "half"
