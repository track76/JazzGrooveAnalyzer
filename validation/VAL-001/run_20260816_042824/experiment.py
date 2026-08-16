"""Execute H-VAL001-C1-13 blind phase-conditioned strength audit."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.separation.null_separator import NullSeparator


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
MANIFEST = RUN / "manifest.json"
EXPERIMENT_ID = "H-VAL001-C1-13"
FRAME_LENGTH = 512


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, indent=2, sort_keys=True
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


def observe(asset: dict[str, str]) -> dict[str, object]:
    path = ROOT / asset["path"]
    if checksum(path) != asset["sha256"]:
        raise RuntimeError(f"Asset checksum mismatch: {asset['path']}")
    context = AnalysisPipeline(separator=NullSeparator()).analyze(str(path))
    sample_rate = context.audio.sample_rate
    observations = []
    for index, candidate in enumerate(context.pulse_candidates or ()):
        frame = round(candidate.time * sample_rate / FRAME_LENGTH)
        observations.append(
            {
                "observation_index": index,
                "frame": frame,
                "timestamp_seconds": candidate.time,
                "strength": candidate.strength,
                "confidence": candidate.confidence,
                "phase_residue_frames": {
                    "33": frame % 33,
                    "66": frame % 66,
                    "132": frame % 132,
                },
            }
        )
    periods = {
        int(
            Decimal(str(candidate.duration_seconds))
            * sample_rate
            / FRAME_LENGTH
        ): len(candidate.recurrence_evidence)
        for candidate in context.candidate_period_population.candidates
    }
    return {
        "source": asset["source"],
        "asset_path": asset["path"],
        "asset_sha256": asset["sha256"],
        "sample_rate_hz": sample_rate,
        "frame_length_samples": FRAME_LENGTH,
        "temporal_scope_seconds": [0.0, context.audio.duration],
        "pulse_candidate_count": len(observations),
        "candidate_hierarchy_occurrence_counts": {
            str(interval): periods.get(interval, 0)
            for interval in (33, 66, 132)
        },
        "pulse_candidates": observations,
    }


def blind_execution(manifest: dict[str, object]) -> dict[str, object]:
    evidence = [observe(asset) for asset in manifest["blind_assets"]]
    observations_reproduced = all(
        item["pulse_candidate_count"] > 0 for item in evidence
    )
    authorized_role_relation = False
    result = (
        "FAILED TEST"
        if observations_reproduced and not authorized_role_relation
        else "FAILED TEST"
    )
    return {
        "experiment_id": EXPERIMENT_ID,
        "ground_truth_loaded": False,
        "candidate_hierarchy_frames": [33, 66, 132],
        "phase_conditioned_strength_evidence": evidence,
        "observations_reproduced": observations_reproduced,
        "authorized_metric_role_decision_relation_available": (
            authorized_role_relation
        ),
        "blind_result": result,
        "selected_candidate_frames": None,
        "reason": (
            "Existing onset strength is reproducible as a physical quantity, "
            "but repository authority supplies no non-arbitrary relation that "
            "maps raw source-specific strength by exact phase to metric role. "
            "The preregistered rule prohibits deriving that relation from the "
            "observed outcomes."
        ),
        "prohibited_inferences_applied": [],
    }


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["status"] != "PREREGISTERED":
        raise RuntimeError("Experiment is not preregistered")

    started = datetime.now(timezone.utc).isoformat()
    first = blind_execution(manifest)
    second = blind_execution(manifest)
    if canonical_bytes(first) != canonical_bytes(second):
        raise RuntimeError("Blind replay is not byte-identical")

    result_sha256 = fingerprint(first)
    blind_record = {
        "experiment_id": EXPERIMENT_ID,
        "manifest_sha256": checksum(MANIFEST),
        "blind_result": first,
        "blind_result_sha256": result_sha256,
        "repeated_blind_result_sha256": fingerprint(second),
        "byte_identical_replay": True,
        "ground_truth_loaded": False,
        "frozen_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(RUN / "blind_result.json", blind_record)
    frozen_file_sha256 = checksum(RUN / "blind_result.json")

    # Ground Truth is imported and loaded only after the blind record exists
    # and its file checksum has been frozen above.
    from jga.ground_truth.loaders.musicxml_ground_truth_loader import (
        MusicXmlGroundTruthLoader,
    )

    ground_truth_source = ROOT / (
        "recordings/validation/ground_truth/"
        "03 THE COST OF LIVING versione intro + 8 bar.musicxml"
    )
    ground_truth = MusicXmlGroundTruthLoader().load(ground_truth_source)
    reference_duration = Decimal("60") / ground_truth.tempo.beats_per_minute
    post_blind = {
        "experiment_id": EXPERIMENT_ID,
        "blind_result_file_sha256_before_ground_truth": frozen_file_sha256,
        "blind_result_sha256": result_sha256,
        "blind_result": first["blind_result"],
        "selected_candidate_frames": None,
        "ground_truth": {
            "ground_truth_id": ground_truth.ground_truth_id,
            "tempo_beats_per_minute": str(ground_truth.tempo.beats_per_minute),
            "tempo_beat_unit": ground_truth.tempo.beat_unit,
            "reference_duration_seconds": str(reference_duration),
            "source_sha256": ground_truth.provenance.source.sha256,
        },
        "agreement": "NOT APPLICABLE — BLIND TEST FAILED",
        "ground_truth_changed_blind_result": False,
    }
    write_json(RUN / "post_blind_evaluation.json", post_blind)
    write_json(
        RUN / "reproducibility.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "first_blind_result_sha256": result_sha256,
            "repeated_blind_result_sha256": fingerprint(second),
            "byte_identical": True,
            "started_utc": started,
            "completed_utc": datetime.now(timezone.utc).isoformat(),
        },
    )

    source_rows = "\n".join(
        f"| {item['source']} | {item['pulse_candidate_count']} | "
        f"{item['candidate_hierarchy_occurrence_counts']['33']} | "
        f"{item['candidate_hierarchy_occurrence_counts']['66']} | "
        f"{item['candidate_hierarchy_occurrence_counts']['132']} |"
        for item in first["phase_conditioned_strength_evidence"]
    )
    report = f"""# H-VAL001-C1-13 — Blind Phase-Conditioned Strength Audit

## Preregistered procedure

The unchanged production pipeline reproduced PulseCandidate timestamp,
strength, confidence and source evidence for every authoritative controlled
audio asset. Exact frame residues modulo 33, 66 and 132 were preserved without
selecting a phase origin. Raw strength was neither normalized nor ranked and
was never compared across sources.

Metric-reference assignment required an already-authorized, preregistered,
literature-grounded relation mapping phase-conditioned strength to metric role
while rejecting both adjacent hierarchy levels. Absence of that relation was
preregistered as `FAILED TEST`.

## Blind result

**{first['blind_result']}**

Existing onset-strength observations were reproduced deterministically, but
JGA authority contains no non-arbitrary rule converting their source-specific
phase distributions into metric-reference role. Creating a rule from these
outcomes was prohibited. No candidate was selected.

Blind result SHA-256: `{result_sha256}`.

## Candidate hierarchy evidence

Counts are exact consecutive Candidate Period occurrences reproduced by the
unchanged pipeline; zero means absent in that source population.

| Source | PulseCandidates | 33 | 66 | 132 |
|---|---:|---:|---:|---:|
{source_rows}

Every PulseCandidate's raw strength and exact phase residues are preserved in
`blind_result.json`. These are physical observations, not accent or metric
roles.

## Post-blind comparison

Only after the blind record was written and frozen was
`{ground_truth.ground_truth_id}` loaded. It specifies
{ground_truth.tempo.beats_per_minute} {ground_truth.tempo.beat_unit} BPM and a
reference duration of `{reference_duration}` seconds. Agreement is not
applicable because the blind test selected no metric-reference candidate.
Ground Truth did not alter the blind result.

## Scientific conclusion and branch stop

Phase-conditioned onset strength does not currently provide an authorized
blind discriminator among 33, 66 and 132 frames. Autonomous metric-reference
inference remains scientifically unresolved. Under the approved hard stop,
this metric-reference discrimination branch is closed and deferred.

The shortest architecture-consistent route to useful timing analysis is to
accept an explicitly declared, provenance-bound metric context as Domain input
while preserving Candidate Periods and PulseCandidates as observed/derived
evidence. Declared context must remain labeled as declared and must never be
reported as automatically recognized.
"""
    (RUN / "report.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
