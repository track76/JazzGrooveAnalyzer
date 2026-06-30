"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    audio_stem.py

Description:
    Represents a separated audio source.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class AudioStem:
    """
    One separated audio source.
    """

    # Nome della sorgente
    name: str

    # Segnale audio
    signal: np.ndarray

    # Frequenza di campionamento
    sample_rate: int

    # Algoritmo che ha prodotto la separazione
    source: str = "Unknown"

    # Affidabilità della separazione
    confidence: float = 1.0