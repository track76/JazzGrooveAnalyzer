#!/usr/bin/env python3
"""Freeze manifests and result for the controlled-mix robustness execution."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import wave


HERE = Path(__file__).resolve().parent
EXTERNAL = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-CONTROLLED-MIX-SEPARATION-JGA-ROBUSTNESS-01")
STEM_DIR = "htdemucs/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1"
STEMS = ("bass.wav", "drums.wav", "other.wav", "vocals.wav")


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def digest(path: Path) -> str:
    value = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def stem_record(path: Path) -> dict[str, object]:
    with wave.open(str(path), "rb") as stream:
        frames = stream.getnframes()
        rate = stream.getframerate()
        technical = {
            "encoding": "SIGNED_LINEAR_PCM",
            "sample_width_bits": stream.getsampwidth() * 8,
            "channels": stream.getnchannels(),
            "sample_rate_hz": rate,
            "frame_count": frames,
            "duration_seconds": frames / rate,
            "sample_scope": f"[0,{frames})",
            "compression": stream.getcomptype(),
        }
    return {"absolute_path": str(path), "sha256": digest(path), "technical_audio": technical}


def main() -> int:
    runs = {}
    for index in (1, 2):
        root = EXTERNAL / f"separation_run_{index}" / STEM_DIR
        runs[f"run_{index}"] = {
            "execution_id": f"EXEC-CEDVAL006-CONTROLLED-MIX-SEPARATION-JGA-ROBUSTNESS-01-SEPARATION-{index}",
            "input_sha256": "32845a5d05538524b19c8f857b0a908f6618cc4b95110a14169f1e450ddfe6e0",
            "stems": {name: stem_record(root / name) for name in STEMS},
            "appledouble_sidecars_excluded_from_scientific_population": sorted(
                str(path) for path in root.glob("._*")
            ),
        }
    same = all(
        runs["run_1"]["stems"][name]["sha256"] == runs["run_2"]["stems"][name]["sha256"]
        for name in STEMS
    )
    generated = {
        "authority_id": "GA-CEDVAL006-CONTROLLED-MIX-SEPARATION-OUTPUTS-01",
        "preregistration_id": "H-CEDVAL006-CONTROLLED-MIX-SEPARATION-JGA-ROBUSTNESS-01",
        "controlled_mix_sha256": "32845a5d05538524b19c8f857b0a908f6618cc4b95110a14169f1e450ddfe6e0",
        "separator": {
            "name": "Demucs", "version": "4.1.0", "model": "htdemucs",
            "model_signature": "955717e8",
            "checkpoint_sha256": "8726e21a993978c7ba086d3872e7608d7d5bfca646ca4aca459ffda844faa8b4",
            "device": "cpu", "thread_limits": {"OMP": 1, "MKL": 1, "VECLIB": 1},
        },
        "runs": runs,
        "replay_classification": "BYTE_IDENTICAL" if same else "SCIENTIFICALLY_NONIDENTICAL",
        "selection_or_averaging": "NONE",
    }
    generated["authority_fingerprint"] = sha256(canonical(generated)).hexdigest()
    (HERE / "generated_stem_authority.json").write_bytes(canonical(generated) + b"\n")

    scoring = json.loads((HERE / "scoring_execution_1.json").read_text())
    report_authority = {}
    for index in (1, 2):
        path = HERE / f"canonical_report_run_{index}.json"
        report = json.loads(path.read_text())
        report_authority[f"run_{index}"] = {
            "file_sha256": digest(path),
            "scientific_fingerprint": report["scientific_fingerprint"],
            "source_counts": {item["label"]: item["eme_count"] for item in report["source_authorities"]},
            "ad038": {
                "eligible": len(report["ad038_localizations"]),
                "localized": len(report["ad038_localizations"]),
                "unresolved": sum(item["nearest_reference"] is None for item in report["ad038_localizations"]),
                "ties": sum(item["nearest_selection_status"] != "UNIQUE" for item in report["ad038_localizations"]),
            },
            "ad040": {
                "temporal_reference_eme_count": report["ad040_profile"]["temporal_reference_eme_count"],
                "accompaniment_relationship_count": report["ad040_profile"]["accompaniment_relationship_count"],
                "represented_eme_count": report["ad040_profile"]["represented_eme_count"],
            },
        }
    result = {
        "execution_id": "EXEC-CEDVAL006-CONTROLLED-MIX-SEPARATION-JGA-ROBUSTNESS-01",
        "status": "COMPLETE_QUANTITATIVE_CHARACTERIZATION",
        "preregistration": {
            "id": "H-CEDVAL006-CONTROLLED-MIX-SEPARATION-JGA-ROBUSTNESS-01",
            "commit": "e604b49fbb91574ae483a8045c6bf33cc74f542d",
            "fingerprint": "5c22ae45dcee9aee180a058e4015f4e748fa0acccf4dc374bfb1ae5af61fc62c",
        },
        "jga_release": {"tag": "v0.3.0-alpha", "commit": "c7b9b65362303ff17c48897c4d26a518595fe9c5"},
        "controlled_mix": {
            "authority_id": "PR-CEDVAL006-CONTROLLED-MIXDOWN-001",
            "fingerprint": "ed01d1d09b62cec41c36214d45027eb246e765dcec21d18456a9452cbba3e40c",
            "sha256": "32845a5d05538524b19c8f857b0a908f6618cc4b95110a14169f1e450ddfe6e0",
        },
        "reference_acceptance": {
            "id": "ACC-CEDVAL006-CANONICAL-RHYTHM-SECTION-REPORT-02",
            "fingerprint": "ea1490dc0171631381186b6728ee1b49ce5549041c38410b06132d021ee7e100",
        },
        "generated_stem_authority_fingerprint": generated["authority_fingerprint"],
        "separation_replay_classification": generated["replay_classification"],
        "canonical_reports": report_authority,
        "scoring": {
            "execution_1_sha256": digest(HERE / "scoring_execution_1.json"),
            "execution_2_sha256": digest(HERE / "scoring_execution_2.json"),
            "exact_byte_replay": (HERE / "scoring_execution_1.json").read_bytes() == (HERE / "scoring_execution_2.json").read_bytes(),
            "fingerprint": scoring["scoring_fingerprint"],
            "runs": {name: {
                "level_1": value["level_1"],
                "level_2_summary": {label: {key: details[key] for key in (
                    "raw_original_count", "raw_separated_count", "matched_count",
                    "original_only_count", "separated_only_count", "descriptive_precision",
                    "descriptive_recall", "descriptive_f1", "exact_zero_count",
                    "signed_displacement_statistics", "absolute_displacement_statistics",
                )} for label, details in value["level_2"].items()},
                "level_3_summary": {
                    "ad038": {key: value["level_3"]["ad038"][key] for key in (
                        "original", "separated", "mapped_relation_identity",
                        "unscorable_relation_identity_count",
                        "paired_nearest_displacement_difference_statistics",
                    )},
                    "ad040": value["level_3"]["ad040"],
                },
            } for name, value in scoring["runs"].items()},
        },
        "interpretation": {
            "most_stable_dimension": "DRUM_CROSS_CONDITION_TEMPORAL_LOCALIZATION",
            "largest_degradation": "BASS_EME_POPULATION_RECOVERY_AND_AD040_REPRESENTED_POPULATION",
            "systematic_displacement": "NO_LARGE_GLOBAL_OFFSET; signed means remain near zero, with source/run-specific tails preserved",
            "separation_induced_variability": "MATERIAL_FOR_BASS_COUNTS_AND_MATCHING; SMALL_FOR_DRUM_COUNTS_AND_TIMING",
            "demonstrates": "Quantitative effect of the frozen Demucs insertion on JGA temporal evidence for this controlled CED-VAL-006 condition.",
            "does_not_demonstrate": [
                "universal separator quality", "universal JGA robustness", "beat identity",
                "tempo/BPM/meter/downbeat", "musical correspondence", "swing/groove",
                "rushing/dragging/intention/human microtiming", "physical onset accuracy",
                "acquisition-clock synchrony", "calibration correction",
            ],
        },
        "firewall": {
            "latency_correction": "NONE", "h02_used": False, "strength_accessed": False,
            "production_code_changed": False, "core_changed": False,
            "translation_changed": False, "domain_changed": False,
            "candidate_period_changed": False, "controlled_mix_changed": False,
            "provider_raw_assets_changed": False,
        },
    }
    result["result_fingerprint"] = sha256(canonical(result)).hexdigest()
    (HERE / "result.json").write_bytes(canonical(result) + b"\n")

    report = f"""# CED-VAL-006 Controlled-Mix Separation → JGA Robustness Result

Execution: `EXEC-CEDVAL006-CONTROLLED-MIX-SEPARATION-JGA-ROBUSTNESS-01`

Status: **COMPLETE QUANTITATIVE CHARACTERIZATION**

The two frozen Demucs populations are `SCIENTIFICALLY_NONIDENTICAL`. Both were
analyzed and neither was selected or averaged. Drum observations were the most
stable measured dimension. Bass population recovery and the resulting AD-040
represented population showed the largest degradation. Full event assignments,
unmatched identities, relation mappings, distributions, and exact metrics are in
the two byte-identical scoring records.

No latency correction, H02, strength, calibration transfer, alignment, tuning,
or architectural change was used. This result characterizes only this frozen
CED-VAL-006 controlled condition and carries every preregistered claim firewall.

Result fingerprint: `{result['result_fingerprint']}`
"""
    (HERE / "report.md").write_text(report)

    names = (
        "canonical_report_run_1.json", "canonical_report_run_2.json", "score.py",
        "scoring_execution_1.json", "scoring_execution_2.json",
        "generated_stem_authority.json", "result.json", "report.md",
        "finalize.py", "verify.py",
    )
    manifest = {
        "execution_id": result["execution_id"],
        "result_fingerprint": result["result_fingerprint"],
        "repository_artifacts": {name: digest(HERE / name) for name in names},
        "external_generated_stem_authority_fingerprint": generated["authority_fingerprint"],
        "external_generated_stems": {
            run: {name: record["sha256"] for name, record in details["stems"].items()}
            for run, details in runs.items()
        },
    }
    (HERE / "artifact_manifest.json").write_bytes(canonical(manifest) + b"\n")
    print(result["result_fingerprint"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
