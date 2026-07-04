from jga.core.domain.audio_stem import AudioStem
from jga.core.domain.services.source_identification_service import (
    SourceIdentificationService,
)
from jga.core.domain.sound_source import SoundSource


class DummySourceIdentificationService(
    SourceIdentificationService,
):

    def identify(
        self,
        stems: tuple[AudioStem, ...],
    ) -> tuple[SoundSource, ...]:

        return tuple()