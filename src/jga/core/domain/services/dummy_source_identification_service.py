from datetime import datetime
from uuid import uuid4

from jga.core.domain.audio_stem import AudioStem
from jga.core.domain.services.source_identification_service import (
    SourceIdentificationService,
)
from jga.core.domain.sound_source import SoundSource


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