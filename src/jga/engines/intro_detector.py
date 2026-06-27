"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    intro_detector.py

Description:
    Intro Detection Engine

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass

from jga.core.audio_file import AudioFile


@dataclass
class IntroDetectionResult:
    """
    Result of the intro detection process.
    """

    analysis_start_time: float
    confidence: float


class IntroDetector:
    """
    Intro Detection Engine.

    Version 0.1

    For now the detector assumes that the musical
    analysis starts from the beginning of the file.

    Future versions will automatically identify
    the first metrically stable section of the
    ensemble.
    """

    def detect(self, audio: AudioFile) -> IntroDetectionResult:

        return IntroDetectionResult(
            analysis_start_time=0.0,
            confidence=1.0
        )