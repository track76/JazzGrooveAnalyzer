"""H-VAL001-C1-05 blind metric-level discrimination evidence audit.

This experiment-local program reads the frozen C1-03/C1-04 observations,
reproduces the current full-mix Pulse/IMT lineage twice, freezes the blind
record, and only then loads Ground Truth for numerical evaluation.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path
import subprocess

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.separation.dummy_multi_stem_separator import DummyMultiStemSeparator


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
EXPERIMENT_ID = "H-VAL001-C1-05"
C103 = ROOT / "validation/VAL-001/run_20260809_100843/blind_candidate_discovery.json"
C104 = ROOT / "validation/VAL-001/run_20260809_1344/blind_relationship_audit.json"
MP3 = ROOT / "recordings/validation/03 THE COST OF LIVING versione intro + 8 bar.mp3"
MUSICXML = ROOT / (
    "recordings/validation/ground_truth/"
    "03 THE COST OF LIVING versione intro + 8 bar.musicxml"
)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def fingerprint(value: object) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pulse_imt_execution() -> dict[str, object]:
    context = AnalysisPipeline(separator=DummyMultiStemSeparator()).analyze(str(MP3))
    beat_timestamps = [item.timestamp for item in context.beat_references]
    pulse_timestamps = [item.timestamp for item in context.pulses]
    timeline_timestamps = (
        [item.timestamp for item in context.internal_metric_timeline.pulses]
        if context.internal_metric_timeline is not None
        else []
    )
    cluster_event_counts = [len(item.events) for item in context.metric_clusters]
    evidence = {
        "filtered_pulse_candidate_count": len(context.pulse_candidates or ()),
        "candidate_period_count": len(context.candidate_period_population.candidates),
        "elementary_metric_event_count": len(context.elementary_metric_events),
        "beat_reference_count": len(beat_timestamps),
        "beat_reference_timestamps_seconds": beat_timestamps,
        "metric_cluster_count": len(context.metric_clusters),
        "metric_cluster_assigned_event_counts": cluster_event_counts,
        "pulse_count": len(pulse_timestamps),
        "pulse_timestamps_seconds": pulse_timestamps,
        "internal_metric_timeline_pulse_count": len(timeline_timestamps),
        "internal_metric_timeline_timestamps_seconds": timeline_timestamps,
        "beat_to_pulse_timestamps_identical": beat_timestamps == pulse_timestamps,
        "pulse_to_imt_timestamps_identical": pulse_timestamps == timeline_timestamps,
    }
    evidence["scientific_content_fingerprint"] = fingerprint(evidence)
    return evidence


def source_candidate_map(c103: dict[str, object]) -> dict[str, list[dict[str, object]]]:
    return {
        source["source_identity"]: source["pulse_candidate_population"][
            "recurrent_candidates_minimum_two_occurrences"
        ]
        for source in c103["first_execution"].values()
    }


def main() -> None:
    c103 = json.loads(C103.read_text(encoding="utf-8"))
    c104 = json.loads(C104.read_text(encoding="utf-8"))
    candidates = source_candidate_map(c103)
    relations = c104["analysis"]
    full = {item["frame_interval"]: item for item in candidates["full_mix"]}

    first = pulse_imt_execution()
    repeated = pulse_imt_execution()

    target_comparison: dict[str, object] = {}
    for target in (33, 66, 132):
        consecutive = full.get(target)
        cross = relations["cross_source_evidence"]["targets"][str(target)]
        exact_sources = sorted(
            source
            for source, evidence in cross.items()
            if evidence["exact_consecutive_occurrence_count"] > 0
        )
        relationship_source = relations["sources"]["full_mix"]
        target_comparison[str(target)] = {
            "full_mix_consecutive_occurrence_count": (
                consecutive["occurrence_count"] if consecutive else 0
            ),
            "full_mix_relative_frequency": (
                consecutive["relative_frequency"] if consecutive else 0.0
            ),
            "full_mix_support_scope_seconds": (
                consecutive["temporal_scope_seconds"] if consecutive else None
            ),
            "exact_consecutive_source_support": exact_sources,
            "exact_consecutive_source_support_count": len(exact_sources),
            "all_pair_support_by_source": {
                source: evidence["all_pair_support_count"]
                for source, evidence in sorted(cross.items())
            },
            "full_mix_non_consecutive_pair_count": relationship_source[
                "target_non_consecutive_lag_audit"
            ][str(target)]["non_consecutive_pair_count"],
            "full_mix_phase_evidence": relationship_source[
                "target_phase_audit"
            ].get(str(target)),
            "full_mix_temporal_distribution": relationship_source[
                "target_temporal_distribution_audit"
            ].get(str(target)),
        }

    full_frames = sorted(full)
    exact_integer_relations = []
    for smaller in full_frames:
        for larger in full_frames:
            if larger > smaller and larger % smaller == 0:
                exact_integer_relations.append(
                    {
                        "smaller_frames": smaller,
                        "larger_frames": larger,
                        "ratio": larger // smaller,
                    }
                )

    blind = {
        "experiment_id": EXPERIMENT_ID,
        "scientific_protocol": "SVP-001",
        "repository_revision": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "bootstrap_revision": "M93 / 44ffffa",
        "blind_boundary": (
            "Ground Truth was not loaded until this record had been serialized."
        ),
        "inputs": {
            "source_candidate_discovery_record": str(C103.relative_to(ROOT)),
            "source_candidate_discovery_fingerprint": c103["blind_record_fingerprint"],
            "source_relationship_audit_record": str(C104.relative_to(ROOT)),
            "source_relationship_audit_fingerprint": c104["blind_record_fingerprint"],
            "full_mix": {
                "path": str(MP3.relative_to(ROOT)),
                "sha256": file_sha256(MP3),
            },
            "controlled_wav_observation_assets": {
                source: {
                    "path": item["asset_path"],
                    "sha256": item["asset_sha256"],
                }
                for source, item in sorted(c103["first_execution"].items())
                if source != "full_mix"
            },
        },
        "candidate_comparison": target_comparison,
        "all_full_mix_candidate_counts": {
            str(frame): full[frame]["occurrence_count"] for frame in full_frames
        },
        "exact_integer_relations_among_full_mix_candidates": exact_integer_relations,
        "pulse_internal_metric_timeline_audit": first,
        "repeated_pulse_internal_metric_timeline_audit": repeated,
        "reproducibility": {
            "identical_scientific_content": (
                first["scientific_content_fingerprint"]
                == repeated["scientific_content_fingerprint"]
            ),
            "first_fingerprint": first["scientific_content_fingerprint"],
            "repeated_fingerprint": repeated["scientific_content_fingerprint"],
            "candidate_source_record_reproduced_identically_in_C1_03": c103[
                "deterministic_numerical_reproduction"
            ],
        },
        "blind_evidence_assessment": {
            "recurrence_count": (
                "Numerically distinguishes candidates but has no authorized mapping "
                "to metric level."
            ),
            "observation_coverage": (
                "Numerically distinguishes 33 and 66 frames but has no authorized "
                "mapping to metric level."
            ),
            "source_support": (
                "Numerically distinguishes candidates but cross-source recurrence is "
                "not metric interpretation."
            ),
            "candidate_relations": (
                "Exact numerical multiples occur; F-031 forbids treating ratio alone "
                "as metric hierarchy."
            ),
            "event_alignment": (
                "The experiment-local phase audit supplies descriptive residues but "
                "no candidate-independent metric identity."
            ),
            "pulse_and_imt": (
                "Pulse copies BeatReference timestamps and IMT preserves Pulse "
                "timestamps; neither is independent of the existing selected grid."
            ),
        },
        "blind_result": "BLIND EVIDENCE DOES NOT YET SUPPORT METRIC-LEVEL DISCRIMINATION",
    }
    blind["blind_record_fingerprint"] = fingerprint(blind)
    (RUN / "blind_metric_discrimination.json").write_text(
        json.dumps(blind, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    # The blind record exists before Ground Truth authority is imported and loaded.
    from jga.ground_truth.loaders import MusicXmlGroundTruthLoader

    ground_truth = MusicXmlGroundTruthLoader(repository_root=ROOT).load(
        MUSICXML.relative_to(ROOT)
    )
    quarter = Decimal("60") / ground_truth.tempo.beats_per_minute
    frame_duration = Decimal("512") / Decimal("44100")
    post = {
        "experiment_id": EXPERIMENT_ID,
        "blind_record_fingerprint": blind["blind_record_fingerprint"],
        "ground_truth": {
            "ground_truth_id": ground_truth.ground_truth_id,
            "validation_item_id": ground_truth.validation_item_id,
            "source_path": ground_truth.provenance.source.repository_path,
            "source_sha256": ground_truth.provenance.source.sha256,
            "tempo_beats_per_minute": str(ground_truth.tempo.beats_per_minute),
            "tempo_beat_unit": ground_truth.tempo.beat_unit,
        },
        "derived_reference_quantities": {
            "quarter_duration_seconds": str(quarter),
            "half_quarter_duration_seconds": str(quarter / Decimal("2")),
            "double_quarter_duration_seconds": str(quarter * Decimal("2")),
        },
        "candidate_numerical_comparison": {
            str(frame): {
                "duration_seconds": str(Decimal(frame) * frame_duration),
                "difference_from_quarter_seconds": str(
                    Decimal(frame) * frame_duration - quarter
                ),
                "difference_from_half_quarter_seconds": str(
                    Decimal(frame) * frame_duration - quarter / Decimal("2")
                ),
                "difference_from_double_quarter_seconds": str(
                    Decimal(frame) * frame_duration - quarter * Decimal("2")
                ),
            }
            for frame in (33, 66, 132)
        },
        "post_blind_assessment": (
            "The numerical proximity of frozen candidates to reference-derived "
            "durations evaluates the blind evidence but does not establish metric "
            "identity or change the blind result."
        ),
    }
    post["post_blind_record_fingerprint"] = fingerprint(post)
    (RUN / "post_blind_ground_truth_comparison.json").write_text(
        json.dumps(post, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    manifest = {
        "experiment_id": EXPERIMENT_ID,
        "title": "Candidate Metric-Level Discrimination Audit",
        "execution_started_utc": datetime.now(timezone.utc).isoformat(),
        "repository_revision": blind["repository_revision"],
        "bootstrap_revision": blind["bootstrap_revision"],
        "artifacts": {
            name: file_sha256(RUN / name)
            for name in (
                "experiment.py",
                "blind_metric_discrimination.json",
                "post_blind_ground_truth_comparison.json",
                "report.md",
                "notes.md",
                "runtime.log",
            )
        },
        "evidence_conflicts_preserved": [
            "Baseline Evidence Conflict",
            "Document-State Evidence Conflict",
            "Experimental Artifact Path Evidence Conflict",
            "LocalTempo Authority Evidence Conflict",
        ],
    }
    (RUN / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
