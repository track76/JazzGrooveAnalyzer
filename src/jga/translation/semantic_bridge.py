from __future__ import annotations

from abc import ABC, abstractmethod

from jga.domain.sound_source import SoundSource
from jga.source_understanding.observed_source_collection import (
    ObservedSourceCollection,
)


class SemanticBridge(ABC):
    """
    Explicit architectural boundary between Source Understanding
    and the Domain model.

    Input:
        ObservedSourceCollection

    Output:
        tuple[SoundSource, ...]
    """

    @abstractmethod
    def translate(
        self,
        observations: ObservedSourceCollection,
    ) -> tuple[SoundSource, ...]:
        raise NotImplementedError
