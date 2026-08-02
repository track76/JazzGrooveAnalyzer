from __future__ import annotations

from dataclasses import dataclass

from jga.source_understanding.ensemble_profile import (
    EnsembleProfile,
)
from jga.source_understanding.observed_source_collection import (
    ObservedSourceCollection,
)


@dataclass(frozen=True, slots=True)
class SourceUnderstandingPipelineResult:
    """
    Complete output of the Source Understanding pipeline.

    It preserves both the semantic observations and the
    synthesized ensemble profile.
    """

    observed_sources: ObservedSourceCollection

    ensemble_profile: EnsembleProfile
