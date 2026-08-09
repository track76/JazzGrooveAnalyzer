"""Scientific validation boundary interfaces."""

from .immutable_analysis_representation import (
    ImmutableAnalysisRepresentation,
)
from .analysis_outputs import (
    AnalysisOutput,
    AnalysisOutputState,
    AnalysisSection,
    AnalysisTempo,
    AnalysisTimeSignature,
)

__all__ = [
    "AnalysisOutput",
    "AnalysisOutputState",
    "AnalysisSection",
    "AnalysisTempo",
    "AnalysisTimeSignature",
    "ImmutableAnalysisRepresentation",
]
