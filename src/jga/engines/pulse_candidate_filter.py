"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    pulse_candidate_filter.py

Purpose:
    Filter Pulse Candidates before metric analysis.

Input:
    AnalysisContext

Output:
    AnalysisContext

Author:
    Angelo Tracanna

Copyright © 2026
=========================================================
"""

from jga.runtime.analysis_context import AnalysisContext


class PulseCandidateFilter:

    """
    Version 0.1

    Rimuove i Pulse Candidate poco affidabili.
    """

    MIN_STRENGTH = 0.10

    MIN_DISTANCE = 0.030      # 30 ms

    def process(self, context: AnalysisContext) -> AnalysisContext:

        candidates = context.pulse_candidates

        if candidates is None:
            return context

        filtered = []

        previous = None

        for candidate in candidates:

            if candidate.strength < self.MIN_STRENGTH:
                continue

            if previous is not None:

                if candidate.time - previous.time < self.MIN_DISTANCE:

                    if candidate.strength > previous.strength:
                        filtered[-1] = candidate
                        previous = candidate

                    continue

            filtered.append(candidate)

            previous = candidate

        context.pulse_candidates = filtered

        context.log.add(
            f"{len(filtered)} Pulse Candidates after filtering."
        )

        return context