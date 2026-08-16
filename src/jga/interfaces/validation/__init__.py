"""Scientific validation boundary interfaces."""

from .immutable_analysis_representation import (
    ImmutableAnalysisRepresentation,
)
from .analysis_outputs import (
    AnalysisOutput,
    AnalysisOutputProvenance,
    AnalysisOutputState,
    AnalysisSection,
    AnalysisTempo,
    AnalysisTimeSignature,
)

__all__ = [
    "AnalysisOutput",
    "AnalysisOutputProvenance",
    "AnalysisOutputState",
    "AnalysisSection",
    "AnalysisTempo",
    "AnalysisTimeSignature",
    "ImmutableAnalysisRepresentation",
]
