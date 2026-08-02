from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from jga.domain.audio_stem import AudioStem
from jga.domain.services.source_identification_service import (
    SourceIdentificationService,
)
from jga.domain.sound_source import SoundSource


class DummySourceIdentificationService(
    SourceIdentificationService,
):
    """
    Dummy implementation that creates one SoundSource
    for each observed AudioStem.
    """

    def identify(
        self,
        audio_stems: tuple[AudioStem, ...],
    ) -> tuple[SoundSource, ...]:

        return tuple(
            SoundSource(
                id=uuid4(),
                name=stem.name,
                family="unknown",
                description=None,
                created_at=datetime.now(),
            )
            for stem in audio_stems
        )
