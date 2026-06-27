"""
=========================================================
Jazz Groove Analyzer (JGA)

Analysis Pipeline

Author:
    Angelo Tracanna
=========================================================
"""

from jga.audio.audio_loader import AudioLoader

from jga.engines.audio_preprocessor import AudioPreprocessor
from jga.engines.intro_detector import IntroDetector
from jga.engines.pulse_candidate_detector import PulseCandidateDetector
from jga.engines.pulse_candidate_filter import PulseCandidateFilter

from jga.separation.dummy_separator import DummySeparator

from jga.runtime.analysis_context import AnalysisContext


class AnalysisPipeline:

    def __init__(self):

        self.loader = AudioLoader()
        self.preprocessor = AudioPreprocessor()
        self.separator = DummySeparator()
        self.intro_detector = IntroDetector()

        self.pulse_detector = PulseCandidateDetector()
        self.pulse_filter = PulseCandidateFilter()

    def analyze(self, filepath: str):

        # 1. Caricamento audio
        audio = self.loader.load(filepath)

        # 2. Creazione del contesto
        context = AnalysisContext(audio=audio)

        context.log.add("Audio loaded.")

        # 3. Preprocessing
        context = self.preprocessor.process(context)

        # 4. Source Separation
        context = self.separator.separate(context)
        
        # 5. Intro detection
        intro = self.intro_detector.detect(context.audio)

        context.log.add(
            f"Analysis starts at {intro.analysis_start_time:.3f} s"
        )
        # 6. Pulse Candidate Detection
        context = self.pulse_detector.process(context)

        # 7. Pulse Candidate Filtering
        context = self.pulse_filter.process(context)

        return context