"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    ensemble_metric_consensus.py

Description:
    Builds Ensemble Metric Events from temporal
    consensus among metric contributors.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.core.ensemble_metric_event import (
    EnsembleMetricEvent,
)

from jga.core.metric_contribution import (
    MetricContribution,
)

from jga.core.metric_source import (
    MetricSource,
)


class EnsembleMetricConsensus:
    """
    Initial deterministic implementation of the
    Ensemble Metric Consensus Layer.

    This component does not infer:
    - meter;
    - BPM metadata;
    - musical style.

    It only aggregates temporally compatible
    pulse observations.
    """

    CONSENSUS_WINDOW = 0.05

    def build(
        self,
        pulse_candidates,
        metric_contributors,
        metric_sources=None,
    ) -> tuple[EnsembleMetricEvent, ...]:

        if not pulse_candidates:
            return ()

        if not metric_contributors:
            return ()

        source_map = (
            metric_sources
            if metric_sources is not None
            else {}
        )

        known_sources = {
            contributor.sound_source_id
            for contributor in metric_contributors
        }

        candidates = sorted(
            (
                candidate
                for candidate in pulse_candidates
                if candidate.sound_source_id
                in known_sources
            ),
            key=lambda item: item.timestamp,
        )

        if not candidates:
            return ()

        events = []

        current_group = [
            candidates[0]
        ]

        for candidate in candidates[1:]:

            if (
                candidate.timestamp
                -
                current_group[-1].timestamp
                <= self.CONSENSUS_WINDOW
            ):

                current_group.append(candidate)

            else:

                events.append(
                    self._create_event(
                        current_group,
                        source_map,
                    )
                )

                current_group = [
                    candidate
                ]

        events.append(
            self._create_event(
                current_group,
                source_map,
            )
        )

        return tuple(events)

    def _create_event(
        self,
        candidates,
        source_map,
    ) -> EnsembleMetricEvent:

        contributions = []

        for candidate in candidates:

            source = source_map.get(
                candidate.sound_source_id,
                MetricSource(
                    name=str(
                        candidate.sound_source_id
                    ),
                    family="unknown",
                ),
            )

            contributions.append(
                MetricContribution(
                    source=source,
                    event_time=candidate.timestamp,
                    confidence=candidate.confidence,
                    pulse_candidate_id=candidate.id,
                    sound_source_id=candidate.sound_source_id,
                )
            )

        timestamps = [
            item.timestamp
            for item in candidates
        ]

        beat_time = (
            sum(timestamps)
            /
            len(timestamps)
        )

        return EnsembleMetricEvent(
            start_time=min(timestamps),
            end_time=max(timestamps),
            beat_time=beat_time,
            contributions=contributions,
            confidence=min(
                1.0,
                len(contributions) / 4.0,
            ),
        )
