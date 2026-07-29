from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BoundaryEvidence:
    """
    Scientific evidence indicating an observable
    behavioural discontinuity.

    This object belongs to the scientific
    representation layer and precedes the
    construction of BehaviourState.
    """

    observation_index: int
