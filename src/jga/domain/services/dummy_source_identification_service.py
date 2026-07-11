from datetime import datetime
from uuid import uuid4

from jga.domain.audio_stem import AudioStem
from jga.domain.services.source_identification_service import (
    SourceIdentificationService,
)
from jga.domain.sound_source import SoundSource


class DummySourceIdentificationService(SourceIdentificationService):

    def identify(
        self,
        stems: tuple[AudioStem, ...],
    ) -> tuple[SoundSource, ...]:

        sources: list[SoundSource] = []

        for stem in stems:

            sources.append(
                SoundSource(
                    id=uuid4(),
                    name=stem.name,
                    family="unknown",
                    description=None,
                    created_at=datetime.now(),
                )
            )

        return tuple(sources)