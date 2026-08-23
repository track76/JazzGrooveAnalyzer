"""Controlled replay for H-VAL001-DRUM-RELATIVE-EME-01."""

from bisect import bisect_right
from collections import Counter
from dataclasses import asdict
from hashlib import sha256
import json

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.representation.builders.drum_relative_eme_localization_builder import (
    DrumRelativeEMELocalizationBuilder,
)


SOURCES = (
    ("Drums", "drums.wav", 63),
    ("Piano", "piano.wav", 49),
    ("Double Bass", "double_bass.wav", 27),
    ("Tenor Sax", "tenor_sax.wav", 16),
)
EXPERIMENT_ID = "H-VAL001-DRUM-RELATIVE-EME-01"


def canonical(value):
    if isinstance(value, dict):
        return {key: canonical(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    return str(value) if value.__class__.__name__ == "UUID" else value


def main():
    analyses = {
        name: AnalysisPipeline().analyze(
            f"recordings/validation/stems/{filename}"
        )
        for name, filename, _ in SOURCES
    }
    counts = {
        name: len(analyses[name].elementary_metric_events)
        for name, _, _ in SOURCES
    }
    drums = analyses["Drums"].elementary_metric_events
    targets = tuple(
        event
        for name in ("Piano", "Double Bass", "Tenor Sax")
        for event in analyses[name].elementary_metric_events
    )
    candidates = tuple(
        candidate
        for analysis in analyses.values()
        for candidate in analysis.domain_pulse_candidates
    )
    builder = DrumRelativeEMELocalizationBuilder()
    arguments = dict(
        target_events=targets,
        drum_events=drums,
        pulse_candidates=candidates,
        temporal_origin_seconds=0.0,
        analysis_execution_id=EXPERIMENT_ID,
    )
    first = builder.build(**arguments)
    second = builder.build(**arguments)

    ordered_drums = tuple(sorted(drums, key=lambda item: (item.timestamp, str(item.id))))
    timestamps = tuple(item.timestamp for item in ordered_drums)
    arithmetic_matches = True
    for item in first:
        boundary = bisect_right(timestamps, item.target_timestamp_seconds)
        preceding = ordered_drums[boundary - 1] if boundary else None
        following = ordered_drums[boundary] if boundary < len(ordered_drums) else None
        candidates_by_distance = sorted(
            ordered_drums,
            key=lambda drum: (
                abs(item.target_timestamp_seconds - drum.timestamp), str(drum.id)
            ),
        )
        minimum = abs(item.target_timestamp_seconds - candidates_by_distance[0].timestamp)
        tied = tuple(
            drum for drum in ordered_drums
            if abs(item.target_timestamp_seconds - drum.timestamp) == minimum
        )
        expected_nearest = min(tied, key=lambda drum: str(drum.id))
        if (
            preceding is not None and following is not None
            and abs(item.target_timestamp_seconds - preceding.timestamp)
            == abs(item.target_timestamp_seconds - following.timestamp) == minimum
        ):
            expected_nearest = preceding
        expected_fraction = None
        if preceding is not None and following is not None and preceding.timestamp != following.timestamp:
            expected_fraction = (
                (item.target_timestamp_seconds - preceding.timestamp)
                / (following.timestamp - preceding.timestamp)
            )
        arithmetic_matches &= all((
            item.preceding_drum_eme is None if preceding is None else item.preceding_drum_eme.eme_id == preceding.id,
            item.following_drum_eme is None if following is None else item.following_drum_eme.eme_id == following.id,
            item.distance_from_preceding_seconds == (None if preceding is None else item.target_timestamp_seconds - preceding.timestamp),
            item.distance_from_following_seconds == (None if following is None else item.target_timestamp_seconds - following.timestamp),
            item.nearest_drum_eme.eme_id == expected_nearest.id,
            item.nearest_displacement_seconds == item.target_timestamp_seconds - expected_nearest.timestamp,
            item.observed_interval_fraction == expected_fraction,
        ))

    source_by_id = {
        event.id: name
        for name, analysis in analyses.items()
        for event in analysis.elementary_metric_events
    }
    localized_counts = Counter(source_by_id[item.target_eme_id] for item in first)
    serialized = canonical([asdict(item) for item in first])
    fingerprint = sha256(json.dumps(serialized, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    expected = {name: count for name, _, count in SOURCES}
    target_ids = {item.id for item in targets}
    localized_ids = {item.target_eme_id for item in first}
    complete_provenance = all(
        item.target_supporting_observations
        and item.target_source_asset_sha256
        and item.target_temporal_scope
        and item.target_materialization_rule
        and item.analysis_execution_id
        and item.nearest_drum_eme is not None
        and item.nearest_drum_eme.supporting_observations
        and item.nearest_drum_eme.source_asset_sha256
        for item in first
    )
    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": "PASS",
        "eme_counts": counts,
        "total_eme": sum(counts.values()),
        "localized_counts": dict(localized_counts),
        "localization_records": len(first),
        "drum_eme_preserved": len(drums),
        "losses": len(target_ids - localized_ids),
        "merges": len(first) - len(localized_ids),
        "creations": len(localized_ids - target_ids),
        "timestamps_unchanged": all(
            item.target_timestamp_seconds
            == next(event.timestamp for event in targets if event.id == item.target_eme_id)
            for item in first
        ),
        "complete_provenance": complete_provenance,
        "independent_arithmetic_replay": arithmetic_matches,
        "deterministic_replay": first == second,
        "nearest_selection_status": dict(Counter(item.nearest_selection_status for item in first)),
        "boundary_results": {
            "before_first": sum(item.preceding_drum_eme is None for item in first),
            "after_last": sum(item.following_drum_eme is None for item in first),
        },
        "observed_interval_fraction": {
            "present": sum(item.observed_interval_fraction is not None for item in first),
            "not_produced": sum(item.observed_interval_fraction is None for item in first),
        },
        "declared_bpm_supplied": False,
        "declared_meter_supplied": False,
        "beat_reference_input_supplied": False,
        "voice_status": "DEFERRED",
        "scientific_fingerprint": fingerprint,
    }
    required = (
        counts == expected,
        len(first) == 92,
        len(drums) == 63,
        result["losses"] == result["merges"] == result["creations"] == 0,
        result["timestamps_unchanged"], complete_provenance,
        arithmetic_matches, first == second,
    )
    if not all(required):
        result["status"] = "FAIL"
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
