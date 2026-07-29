from __future__ import annotations

from dataclasses import dataclass, field

from jga.domain.stable_region import StableRegion
from jga.domain.transition_region import TransitionRegion


@dataclass(frozen=True)
class EvolutionEpisode:
    """
    Represents one complete behavioural evolution episode.

    An EvolutionEpisode is composed of StableRegions and
    TransitionRegions preserving temporal ordering.
    """

    stable_regions: tuple[StableRegion, ...] = field(default_factory=tuple)

    transition_regions: tuple[TransitionRegion, ...] = field(default_factory=tuple)

    @property
    def stable_region_count(self) -> int:
        return len(self.stable_regions)

    @property
    def transition_region_count(self) -> int:
        return len(self.transition_regions)

    @property
    def is_empty(self) -> bool:
        return (
            self.stable_region_count == 0
            and self.transition_region_count == 0
        )
