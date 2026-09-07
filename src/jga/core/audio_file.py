"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    audio_file.py

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass, field
from pathlib import Path
from uuid import UUID, uuid4

import numpy as np


@dataclass
class AudioFile:
    """
    Contiene tutte le informazioni relative
    ad una registrazione audio acquisita dal JGA.
    """

    # Percorso del file
    path: Path

    # Raw Audio Signal (RAS)
    raw_audio: np.ndarray

    # Frequenza di campionamento
    sample_rate: int

    # Durata in secondi
    duration: float

    # Numero di canali
    channels: int

    # Formato del file
    format: str

    # Unbound legacy inputs have execution-local identity only, never AD-041 authority.
    source_identity: UUID = field(default_factory=uuid4)
    source_authority_id: str | None = None
    source_instance_key: str | None = None
    asset_sha256: str | None = None
    source_identity_rule: str = "UNAUTHORIZED"

    transformation_provenance: dict | None = None

    @property
    def filename(self) -> str:
        return self.path.name
