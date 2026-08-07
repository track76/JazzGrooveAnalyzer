"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    source_pulse_candidate_builder.py

Description:
    Extracts source-specific pulse candidates
    from separated AudioStems.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

import librosa

from jga.core.metric_source import MetricSource
from jga.core.pulse_candidate import PulseCandidate
from jga.core.source_pulse_sequence import SourcePulseSequence

from jga.runtime.analysis_context import AnalysisContext
from jga.runtime.runtime_event import RuntimeEvent


class SourcePulseCandidateBuilder:
    """
    Extracts independent pulse candidates
    from each separated AudioStem.

    This component does not:
    - infer beat;
    - infer meter;
    - estimate BPM;
    - create domain objects.
    """

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        sequences = []

        if not context.audio_stems:
            context.source_pulse_sequences = sequences
            return context

        for stem in context.audio_stems:

            onset_frames = librosa.onset.onset_detect(
                y=stem.signal,
                sr=stem.sample_rate,
                units="frames",
            )

            onset_strength = librosa.onset.onset_strength(
                y=stem.signal,
                sr=stem.sample_rate,
            )

            onset_times = librosa.frames_to_time(
                onset_frames,
                sr=stem.sample_rate,
            )

            candidates = []

            for frame, time in zip(
                onset_frames,
                onset_times,
            ):

                candidates.append(
                    PulseCandidate(
                        time=float(time),
                        strength=float(
                            onset_strength[frame]
                        ),
                        confidence=1.0,
                    )
                )

            sequences.append(
                SourcePulseSequence(
                    source=MetricSource(
                        name=stem.name,
                        family="Unknown",
                        confidence=stem.confidence,
                        source_id=stem.id,
                    ),
                    pulse_candidates=candidates,
                )
            )

        context.source_pulse_sequences = sequences

        context.log.add(
            RuntimeEvent(
                event_id=(
                    "SOURCE_SPECIFIC_PULSE_CANDIDATES_CREATED"
                ),
                layer="ENGINE",
                component=(
                    "SourcePulseCandidateBuilder"
                ),
                message=(
                    f"{len(sequences)} "
                    "Source Pulse Sequences created."
                ),
                input_type="AudioStemCollection",
                output_type=(
                    "list[SourcePulseSequence]"
                ),
                metrics={
                    "source_sequences": len(sequences),
                },
            )
        )

        return context
