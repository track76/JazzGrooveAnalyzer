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

from dataclasses import dataclass, field
from uuid import UUID, uuid4

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

    # Identità stabile della sorgente
    # Compatibility objects are execution-local and explicitly unauthorized.
    # No name-derived identity fallback is permitted by AD-041.
    id: UUID = field(default_factory=uuid4)
    source_identity_rule: str = "UNAUTHORIZED"

    asset_sha256: str | None = None
    asset_path: str | None = None
    transformation_provenance: dict | None = None
