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

from dataclasses import dataclass
from pathlib import Path

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

    @property
    def filename(self) -> str:
        return self.path.name