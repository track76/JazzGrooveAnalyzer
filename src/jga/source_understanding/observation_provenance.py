from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class ObservationProvenance:
    """
    Minimal provenance attached to an observation.

    Tracks where and when the observation was produced,
    without carrying the original AudioStem.
    """

    stem_id: str

    pipeline_stage: str

    created_at: datetime
