"""Minimum observational Candidate Period discovery defined by M92."""

from collections import defaultdict
from decimal import Decimal
from hashlib import sha256

from jga.core.candidate_period import (
    CandidatePeriod,
    CandidatePeriodObservationScope,
    CandidatePeriodOccurrence,
    CandidatePeriodPopulation,
    CandidatePeriodProvenance,
)
from jga.runtime.analysis_context import AnalysisContext


class CandidatePeriodDiscovery:
    """Preserve recurrent consecutive filtered PulseCandidate intervals."""

    MINIMUM_RECURRENCE_COUNT = 2

    def __init__(
        self,
        frame_length_samples: int,
        source_revision: str | None = None,
    ) -> None:
        if frame_length_samples <= 0:
            raise ValueError("frame_length_samples must be positive.")
        self.frame_length_samples = frame_length_samples
        self.source_revision = source_revision

    def process(self, context: AnalysisContext) -> AnalysisContext:
        candidates = tuple(
            sorted(
                context.pulse_candidates or (),
                key=lambda candidate: candidate.time,
            )
        )
        sample_rate = context.audio.sample_rate
        frames = tuple(
            round(
                candidate.time
                * sample_rate
                / self.frame_length_samples
            )
            for candidate in candidates
        )

        occurrences_by_interval: dict[
            int,
            list[CandidatePeriodOccurrence],
        ] = defaultdict(list)
        for start_index, (start, end) in enumerate(
            zip(frames, frames[1:])
        ):
            frame_interval = end - start
            if frame_interval <= 0:
                continue
            end_index = start_index + 1
            occurrences_by_interval[frame_interval].append(
                CandidatePeriodOccurrence(
                    start_observation_index=start_index,
                    end_observation_index=end_index,
                    start_seconds=Decimal(str(candidates[start_index].time)),
                    end_seconds=Decimal(str(candidates[end_index].time)),
                )
            )

        frame_duration_seconds = (
            self.frame_length_samples / sample_rate
        )
        periods = tuple(
            CandidatePeriod(
                duration_seconds=Decimal(
                    str(frame_interval * frame_duration_seconds)
                ),
                recurrence_evidence=tuple(occurrences),
            )
            for frame_interval, occurrences in sorted(
                occurrences_by_interval.items()
            )
            if len(occurrences) >= self.MINIMUM_RECURRENCE_COUNT
        )

        asset_path = context.audio.path.as_posix()
        asset_checksum = sha256(context.audio.path.read_bytes()).hexdigest()
        context.candidate_period_population = CandidatePeriodPopulation(
            observation_scope=CandidatePeriodObservationScope(
                observation_population_id=(
                    f"filtered-pulse-candidates:{asset_checksum}"
                ),
                source_identity=asset_path,
                start_seconds=Decimal("0"),
                end_seconds=Decimal(str(context.audio.duration)),
            ),
            provenance=CandidatePeriodProvenance(
                input_asset_path=asset_path,
                input_asset_sha256=asset_checksum,
                discovery_configuration=(
                    (
                        "frame_length_samples",
                        str(self.frame_length_samples),
                    ),
                    ("sample_rate_hz", str(sample_rate)),
                    (
                        "recurrence_definition",
                        "exact consecutive positive frame interval occurring at least twice",
                    ),
                ),
                source_revision=self.source_revision,
            ),
            measurement_unit="seconds",
            candidates=periods,
        )
        return context
