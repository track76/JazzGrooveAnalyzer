"""
=========================================================
Jazz Groove Analyzer (JGA)

Basic Feature Extractor

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

import numpy as np

from jga.core.audio_stem import AudioStem
from jga.source_understanding.feature_extractor import FeatureExtractor
from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet


class BasicFeatureExtractor(FeatureExtractor):

    def _spectral_representation(
        self,
        signal: np.ndarray,
        sample_rate: int,
    ) -> tuple[np.ndarray, np.ndarray]:

        spectrum = np.abs(np.fft.rfft(signal))

        frequencies = np.fft.rfftfreq(
            len(signal),
            d=1.0 / sample_rate,
        )

        return spectrum, frequencies

    def extract(
        self,
        stem: AudioStem,
    ) -> FeatureSet:

        feature_set = FeatureSet()

        signal = np.asarray(stem.signal, dtype=float)

        duration = len(signal) / stem.sample_rate

        rms = float(
            np.sqrt(
                np.mean(np.square(signal))
            )
        )

        if len(signal) < 2:
            zcr = 0.0
        else:
            crossings = np.sum(
                (signal[:-1] >= 0) != (signal[1:] >= 0)
            )
            zcr = float(
                crossings / (len(signal) - 1)
            )

        spectrum, frequencies = self._spectral_representation(
            signal,
            stem.sample_rate,
        )

        total_energy = np.sum(spectrum)

        if total_energy == 0.0:

            centroid = 0.0
            bandwidth = 0.0
            rolloff = 0.0

        else:

            centroid = float(
                np.sum(
                    frequencies * spectrum
                ) / total_energy
            )

            bandwidth = float(
                np.sqrt(
                    np.sum(
                        spectrum
                        * (frequencies - centroid) ** 2
                    ) / total_energy
                )
            )

            cumulative = np.cumsum(spectrum)

            threshold = 0.95 * total_energy

            index = np.searchsorted(
                cumulative,
                threshold,
            )

            rolloff = float(
                frequencies[index]
            )

        feature_set.set(
            FeatureName.DURATION,
            duration,
        )

        feature_set.set(
            FeatureName.RMS,
            rms,
        )

        feature_set.set(
            FeatureName.ZERO_CROSSING_RATE,
            zcr,
        )

        feature_set.set(
            FeatureName.SPECTRAL_CENTROID,
            centroid,
        )

        feature_set.set(
            FeatureName.SPECTRAL_BANDWIDTH,
            bandwidth,
        )

        feature_set.set(
            FeatureName.SPECTRAL_ROLLOFF,
            rolloff,
        )

        return feature_set
