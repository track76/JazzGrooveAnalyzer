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

from hashlib import sha256

import numpy as np

from jga.observation.signal_representation import (
    SignalRepresentation,
)
from jga.runtime.analysis_context import AnalysisContext
from jga.runtime.runtime_event import RuntimeEvent


class AudioPreprocessor:
    """
    Versione 0.1

    Prepara il segnale audio per le analisi successive.

    Operazioni:
    - Conversione stereo → mono
    - Normalizzazione del segnale
    """

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

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

        if context.audio.transformation_provenance is not None:
            # Identity and WAV asset authority survive this representation change.
            prepared = np.asarray(context.processed_audio, dtype="<f4", order="C")
            context.audio.transformation_provenance["detector_preparation"] = {
                "method": "jga-per-file-channel-mean-peak-normalization/v1",
                "source_identity": str(context.audio.source_identity),
                "input_separated_wav_sha256": context.audio.asset_sha256,
                "input_channels": context.audio.channels,
                "channel_rule": "numpy.mean(raw_audio, axis=0) if ndim > 1; otherwise unchanged",
                "normalization_rule": "divide by max(abs(mono)) if positive; otherwise copy",
                "peak_before_normalization": float(peak),
                "sample_rate_hz": context.audio.sample_rate,
                "input_frame_count": int(context.audio.raw_audio.shape[-1]),
                "output_frame_count": int(prepared.size),
                "sample_index_mapping": "identity; no shift, resampling, trimming or padding",
                "prepared_encoding": "IEEE754 float32 little-endian contiguous sample order",
                "prepared_signal_sha256": sha256(prepared.tobytes()).hexdigest(),
            }

        context.signal_representation = (
            SignalRepresentation(
                samples=context.processed_audio,
                sample_rate=context.audio.sample_rate,
            )
        )

        # Runtime Event
        context.log.add(
            RuntimeEvent(
                event_id="AUDIO_NORMALIZED",
                layer="ENGINE",
                component="AudioPreprocessor",
                message="Audio normalized.",
                input_type="AudioFile",
                output_type="SignalRepresentation",
            )
        )

        return context
