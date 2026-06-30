"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    analysis_pipeline.py

Description:
    Main analysis pipeline.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.audio.audio_loader import AudioLoader

from jga.engines.audio_preprocessor import AudioPreprocessor
from jga.engines.intro_detector import IntroDetector

from jga.engines.pulse_candidate_detector import PulseCandidateDetector
from jga.engines.pulse_candidate_filter import PulseCandidateFilter
from jga.engines.pulse_interval_builder import PulseIntervalBuilder
from jga.engines.analysis_window_builder import AnalysisWindowBuilder
from jga.engines.metric_stability_analyzer import MetricStabilityAnalyzer

from jga.runtime.analysis_context import AnalysisContext
from jga.runtime.analysis_report import AnalysisReport

from jga.separation.dummy_separator import DummySeparator


class AnalysisPipeline:
    """
    Main JGA analysis pipeline.
    """

    def __init__(self):

        self.loader = AudioLoader()

        self.preprocessor = AudioPreprocessor()

        self.separator = DummySeparator()

        self.intro_detector = IntroDetector()

        self.pulse_detector = PulseCandidateDetector()

        self.pulse_filter = PulseCandidateFilter()

        self.interval_builder = PulseIntervalBuilder()

        self.window_builder = AnalysisWindowBuilder()

        self.stability = MetricStabilityAnalyzer()

    def analyze(
        self,
        filepath: str
    ) -> AnalysisContext:

        # Audio loading
        audio = self.loader.load(filepath)

        context = AnalysisContext(audio=audio)

        context.report = AnalysisReport(audio=audio)

        context.log.add("Audio loaded.")

        # Preprocessing
        context = self.preprocessor.process(context)

        # Source separation
        context = self.separator.separate(context)

        # Intro detection
        intro = self.intro_detector.detect(context.audio)

        context.log.add(
            f"Analysis starts at {intro.analysis_start_time:.3f} s"
        )

        # Pulse Candidates
        context = self.pulse_detector.process(context)

        context = self.pulse_filter.process(context)

        # Pulse Intervals
        context = self.interval_builder.process(context)

        # Analysis Windows
        context = self.window_builder.process(context)

        # Metric Stability
        context = self.stability.process(context)

        return context