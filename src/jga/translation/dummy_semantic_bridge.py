from __future__ import annotations

from datetime import datetime

from jga.domain.sound_source import SoundSource
from jga.source_understanding.observed_source_collection import (
    ObservedSourceCollection,
)
from jga.translation.semantic_bridge import SemanticBridge


class DummySemanticBridge(SemanticBridge):
    """
    Temporary implementation of the Semantic Bridge.

    Performs a deterministic one-to-one translation from
    ObservedSource to SoundSource.
    """

    def translate(
        self,
        observations: ObservedSourceCollection,
    ) -> tuple[SoundSource, ...]:

        return tuple(
            SoundSource(
                id=source.source_identity,
                name=source.stem_id,
                family=source.classification.family.value,
                description=None,
                created_at=datetime.now(),
            )
            for source in observations
        )
