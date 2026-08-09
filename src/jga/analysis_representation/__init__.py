"""Materialization boundary for immutable analysis representations."""

from .materializer import CompletedAnalysisMaterializer, MaterializationProvenance
from .models import FrozenAnalysisRepresentation

__all__ = [
    "CompletedAnalysisMaterializer",
    "FrozenAnalysisRepresentation",
    "MaterializationProvenance",
]
