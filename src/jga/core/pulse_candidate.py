"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    pulse_candidate.py

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass


@dataclass
class PulseCandidate:
    """
    Evento candidato a rappresentare
    una pulsazione dell'ensemble.
    """

    # Tempo assoluto (secondi)
    time: float

    # Intensità dell'evento
    strength: float

    # Confidenza iniziale
    confidence: float = 1.0