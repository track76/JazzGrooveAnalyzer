"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    audio_preprocessor.py

Description:
    Audio Preprocessor Engine

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

import numpy as np

from jga.runtime.analysis_context import AnalysisContext
from jga.observation.signal_representation import SignalRepresentation


class AudioPreprocessor:
    """
    Versione 0.1

    Prepara il segnale audio per le analisi successive.

    Operazioni:
    - Conversione stereo → mono
    - Normalizzazione del segnale
    """

    def process(self, context: AnalysisContext) -> AnalysisContext:

        # Segnale originale
        audio = context.audio.raw_audio

        # Se il file è stereo, lo converte in mono
        if audio.ndim > 1:
            audio = np.mean(audio, axis=0)

        # Calcola il valore massimo assoluto
        peak = np.max(np.abs(audio))

        # Normalizzazione
        if peak > 0:
            context.processed_audio = audio / peak
        else:
            context.processed_audio = audio.copy()

        context.signal_representation = SignalRepresentation(
            samples=context.processed_audio,
            sample_rate=context.audio.sample_rate,
        )

        # Aggiorna il log
        context.log.add("Audio normalized.")

        return context