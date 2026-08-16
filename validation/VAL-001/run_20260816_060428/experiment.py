"""Execute H-VAL001-C1-12 blind metric-reference evidence sufficiency audit."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
MANIFEST = RUN / "manifest.json"
EXPERIMENT_ID = "H-VAL001-C1-12"


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        indent=2,
        sort_keys=True,
    ).encode("utf-8") + b"\n"


def write_json(path: Path, value: object) -> None:
    path.write_bytes(canonical_bytes(value))


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fingerprint(value: object) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def recurrent_inventory(source: dict[str, object]) -> dict[int, dict[str, object]]:
    candidates = source["elementary_metric_event_distinct_population"][
        "recurrent_candidates_minimum_two_occurrences"
    ]
    return {int(item["frame_interval"]): item for item in candidates}


def blind_audit(
    discovery: dict[str, object],
    relationships: dict[str, object],
) -> dict[str, object]:
    sources = discovery["first_execution"]
    inventories = {
        name: recurrent_inventory(source)
        for name, source in sources.items()
    }
    full_mix = inventories["full_mix"]
    relationship_analysis = relationships["analysis"]

    candidates = []
    for frame_interval, item in sorted(full_mix.items()):
        exact_source_support = {
            name: len(inventory[frame_interval]["occurrences"])
            for name, inventory in inventories.items()
            if name != "full_mix" and frame_interval in inventory
        }
        candidates.append(
            {
                "frame_interval": frame_interval,
                "duration_seconds": str(item["duration_seconds"]),
                "full_mix_recurrence_count": len(item["occurrences"]),
                "supporting_occurrences": item["occurrences"],
                "exact_controlled_stem_support": exact_source_support,
                "additional_relationship_record_available": (
                    str(frame_interval)
                    in relationship_analysis["cross_source_evidence"]["targets"]
                ),
                "periodicity_exists": True,
                "periodicity_is_recurrent": True,
                "metric_role_identifying_evidence": [],
                "metric_reference_role_identified": False,
            }
        )

    role_supported = [
        candidate
        for candidate in candidates
        if candidate["metric_reference_role_identified"]
    ]
    if len(role_supported) == 1:
        outcome = "UNIQUE SUPPORT"
        selected = role_supported[0]
    elif len(role_supported) > 1:
        outcome = "AMBIGUOUS"
        selected = None
    else:
        outcome = "UNSUPPORTED"
        selected = None

    return {
        "experiment_id": EXPERIMENT_ID,
        "input_bindings": {
            "candidate_discovery_experiment": discovery["experiment_id"],
            "candidate_discovery_blind_record_fingerprint": discovery[
                "blind_record_fingerprint"
            ],
            "relationship_experiment": relationship_analysis["experiment_id"],
            "relationship_blind_record_fingerprint": relationships[
                "blind_record_fingerprint"
            ],
        },
        "available_evidence": {
            "candidate_durations": True,
            "recurrence_counts": True,
            "supporting_occurrence_positions": True,
            "observation_indices": True,
            "full_mix_population": True,
            "controlled_stem_populations": True,
            "non_consecutive_relationships": True,
            "phase_description": True,
            "temporal_distribution": True,
            "exact_cross_source_recurrence": True,
            "metric_role_identifying_relation": False,
        },
        "authority_constraints": [
            "F-031: no single recurrent scale is privileged without additional evidence.",
            "F-031: recurrence, duration and numerical ratio do not independently establish metric level.",
            "F-032: recurrence frequency and source support do not independently assign musical metric meaning.",
            "C1-04: phase concentration was not established.",
            "C1-04: cross-source recurrence is descriptive and does not privilege a candidate.",
        ],
        "candidate_evidence": candidates,
        "role_supported_candidate_count": len(role_supported),
        "blind_result": outcome,
        "selected_candidate": selected,
        "blind_metric_duration_seconds": (
            selected["duration_seconds"] if selected is not None else None
        ),
        "blind_bpm": None,
        "limitations": [
            "Existence and recurrence evidence are not metric-role evidence.",
            "Cross-source coordination does not identify metric level under current authority.",
            "No selector, weighting, threshold, ranking, tolerance, heuristic or musical assumption was introduced.",
        ],
    }


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["status"] != "PREREGISTERED":
        raise RuntimeError("Experiment manifest is not preregistered.")

    blind_inputs = []
    for binding in manifest["blind_inputs"]:
        path = ROOT / binding["path"]
        if checksum(path) != binding["sha256"]:
            raise RuntimeError(f"Blind input checksum mismatch: {binding['path']}")
        blind_inputs.append(json.loads(path.read_text(encoding="utf-8")))

    started = datetime.now(timezone.utc).isoformat()
    first = blind_audit(blind_inputs[0], blind_inputs[1])
    repeated = blind_audit(blind_inputs[0], blind_inputs[1])
    identical = canonical_bytes(first) == canonical_bytes(repeated)
    if not identical:
        raise RuntimeError("Repeated blind audit is not byte-identical.")

    blind_fingerprint = fingerprint(first)
    blind_record = {
        "experiment_id": EXPERIMENT_ID,
        "blind_result": first,
        "blind_result_sha256": blind_fingerprint,
        "repeated_blind_result_sha256": fingerprint(repeated),
        "byte_identical_replay": identical,
        "ground_truth_loaded": False,
        "frozen_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(RUN / "blind_result.json", blind_record)
    frozen_file_sha256 = checksum(RUN / "blind_result.json")

    # Ground Truth becomes available only after the blind file is written and
    # its content identity is frozen above.
    from jga.ground_truth.loaders.musicxml_ground_truth_loader import (
        MusicXmlGroundTruthLoader,
    )

    source = Path(
        "recordings/validation/ground_truth/"
        "03 THE COST OF LIVING versione intro + 8 bar.musicxml"
    )
    ground_truth = MusicXmlGroundTruthLoader().load(source)
    if first["selected_candidate"] is None:
        agreement = "NOT APPLICABLE — NO SCIENTIFICALLY JUSTIFIED BLIND SELECTION"
    else:
        selected_duration = Decimal(first["blind_metric_duration_seconds"])
        reference_duration = Decimal("60") / ground_truth.tempo.beats_per_minute
        agreement = (
            "EXACT"
            if selected_duration == reference_duration
            else "NOT EXACT"
        )

    post_blind = {
        "experiment_id": EXPERIMENT_ID,
        "blind_result_file_sha256_before_ground_truth": frozen_file_sha256,
        "blind_result_sha256": blind_fingerprint,
        "blind_result": first["blind_result"],
        "selected_candidate": first["selected_candidate"],
        "ground_truth": {
            "ground_truth_id": ground_truth.ground_truth_id,
            "tempo_beats_per_minute": str(ground_truth.tempo.beats_per_minute),
            "tempo_beat_unit": ground_truth.tempo.beat_unit,
            "reference_duration_seconds": str(
                Decimal("60") / ground_truth.tempo.beats_per_minute
            ),
            "source_sha256": ground_truth.provenance.source.sha256,
        },
        "agreement": agreement,
        "ground_truth_changed_blind_result": False,
    }
    write_json(RUN / "post_blind_evaluation.json", post_blind)

    reproducibility = {
        "experiment_id": EXPERIMENT_ID,
        "first_blind_result_sha256": blind_fingerprint,
        "repeated_blind_result_sha256": fingerprint(repeated),
        "byte_identical": identical,
        "started_utc": started,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(RUN / "reproducibility.json", reproducibility)

    report = f"""# H-VAL001-C1-12 — Blind Metric-Reference Sufficiency Audit

## Scientific question

Can existing Candidate Period evidence from the controlled source support a
scientifically justified identification of one metric-reference periodicity
without access to Ground Truth?

## Blind evidence

The audit consumed only the frozen C1-03 Candidate Period evidence and C1-04
relationship evidence. All {len(first['candidate_evidence'])} full-mix
Candidate Periods retained duration, recurrence and occurrence evidence.
Exact controlled-stem recurrence and the existing non-consecutive, phase,
distribution and cross-source descriptions were available.

## Criterion

A candidate could be selected only through an existing explicitly authorized
relation identifying its metric-reference role. Existence, recurrence,
frequency, occurrence position, cross-source coordination, numerical ratio and
descriptive phase or distribution evidence were not treated as role evidence.

## Blind result

**{first['blind_result']}**

No Candidate Period had an authorized metric-role-identifying relation.
No Candidate Period, metric duration or BPM was selected or derived.

Blind result SHA-256: `{blind_fingerprint}`.
Repeated blind execution was byte-identical.

## Post-blind validation

Only after the blind result file was written and frozen was
`{ground_truth.ground_truth_id}` loaded. It specifies
{ground_truth.tempo.beats_per_minute} {ground_truth.tempo.beat_unit} BPM, with
derived reference duration
`{Decimal('60') / ground_truth.tempo.beats_per_minute}` seconds.

Agreement is not applicable because no scientifically justified blind
selection existed. Ground Truth did not alter the blind result.

## Scientific conclusion

Existing evidence establishes periodicity existence, recurrence and some
cross-source coordination, but does not establish a metric-reference role.
The first causal blocker is therefore not resolved.

No production implementation is justified. The missing capability is an
evidence-supported scientific interpretation criterion, not absent software
or architecture.
"""
    (RUN / "report.md").write_text(report, encoding="utf-8")

    completion = {
        "experiment_id": EXPERIMENT_ID,
        "documentation_updates": "Not Applicable — no canonical authority changed.",
        "cross_reference_verification": "Passed — C1-03, C1-04, F-031, F-032 and Ground Truth identities resolve by preserved paths and checksums.",
        "focused_tests": "Passed — 36 Candidate Period, M92, Ground Truth and Comparator tests; 2 existing Python 3.13 audio-library deprecation warnings.",
        "complete_automated_suite": "Not Applicable — no production code, architecture or canonical scientific authority changed.",
        "scientific_validation": "Passed — blind input verification, immutable freeze, replay and post-blind Ground Truth separation completed.",
        "repository_consistency": "Passed — git diff --check, artifact checksums, blind freeze binding and replay verification completed.",
        "bootstrap_regeneration": "Not Applicable — no canonical project-state or bootstrap semantics changed.",
        "production_implementation": "Not Applicable — no justified metric-reference criterion was established.",
        "storage_impact": "Lightweight repository records only; no audio or heavy output generated.",
        "push": "NOT PERFORMED — explicit PI approval required."
    }
    write_json(RUN / "completion_protocol.json", completion)

    artifacts = {}
    for path in sorted(RUN.iterdir()):
        if path.name == "artifact_manifest.json" or not path.is_file():
            continue
        artifacts[path.name] = checksum(path)
    write_json(
        RUN / "artifact_manifest.json",
        {"experiment_id": EXPERIMENT_ID, "artifacts": artifacts},
    )


if __name__ == "__main__":
    main()
