#!/usr/bin/env python3
"""Freeze the CED-VAL-006 Bass-preservation Phase-1 result."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
EXTERNAL = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE1-01")
TRACK = "htdemucs/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1"
RUNS = ("B_run_1", "B_run_2", "C_run_1", "C_run_2")
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


def wav_authority(path: Path) -> dict[str, object]:
    with path.open("rb") as stream:
        if stream.read(4) != b"RIFF":
            raise RuntimeError(f"not RIFF:{path}")
        stream.read(4)
        if stream.read(4) != b"WAVE":
            raise RuntimeError(f"not WAVE:{path}")
        fmt = None
        data_size = None
        while True:
            header = stream.read(8)
            if not header:
                break
            chunk, size = struct.unpack("<4sI", header)
            content = stream.read(size)
            if size % 2:
                stream.read(1)
            if chunk == b"fmt ":
                fmt = struct.unpack("<HHIIHH", content[:16])
            elif chunk == b"data":
                data_size = size
        if fmt is None or data_size is None:
            raise RuntimeError(f"missing WAV authority:{path}")
    audio_format, channels, rate, _, block_align, bits = fmt
    frames = data_size // block_align
    return {
        "absolute_path": str(path), "sha256": digest(path),
        "technical_audio": {
            "riff_audio_format_code": audio_format,
            "encoding": {1: "SIGNED_LINEAR_PCM", 3: "IEEE_FLOAT"}.get(audio_format, "UNKNOWN"),
            "bits_per_sample": bits, "channels": channels, "sample_rate_hz": rate,
            "frame_count": frames, "sample_scope": f"[0,{frames})",
            "duration_seconds": frames / rate,
        },
    }


def main() -> int:
    stem_runs = {}
    for run in RUNS:
        root = EXTERNAL / run / TRACK
        stem_runs[run] = {
            "configuration": run[0],
            "stems": {name: wav_authority(root / name) for name in STEMS},
            "appledouble_excluded": sorted(str(path) for path in root.glob("._*")),
        }
    replay = {}
    for configuration in ("B", "C"):
        first, second = (stem_runs[f"{configuration}_run_1"], stem_runs[f"{configuration}_run_2"])
        replay[configuration] = "BYTE_IDENTICAL" if all(
            first["stems"][name]["sha256"] == second["stems"][name]["sha256"]
            for name in STEMS
        ) else "SCIENTIFICALLY_NONIDENTICAL"
    stems = {
        "authority_id": "GA-CEDVAL006-BASS-PRESERVATION-PHASE1-STEMS-01",
        "controlled_mix_sha256": "32845a5d05538524b19c8f857b0a908f6618cc4b95110a14169f1e450ddfe6e0",
        "model": "htdemucs", "model_signature": "955717e8",
        "checkpoint_sha256": "8726e21a993978c7ba086d3872e7608d7d5bfca646ca4aca459ffda844faa8b4",
        "runs": stem_runs, "replay": replay, "selection_or_averaging": "NONE",
    }
    stems["authority_fingerprint"] = sha256(canonical(stems)).hexdigest()
    (HERE / "generated_stem_authority.json").write_bytes(canonical(stems) + b"\n")

    scoring = json.loads((HERE / "scoring_execution_1.json").read_text())
    summaries = {}
    reports = {}
    for run in RUNS:
        value = scoring["runs"][run]
        summaries[run] = {
            "bass": {key: value["level_2"]["Double Bass"][key] for key in (
                "raw_separated_count", "matched_count", "original_only_count",
                "separated_only_count", "descriptive_precision", "descriptive_recall",
                "descriptive_f1", "absolute_displacement_statistics",
            )},
            "drums": {key: value["level_2"]["Drums"][key] for key in (
                "raw_separated_count", "matched_count", "original_only_count",
                "separated_only_count", "descriptive_precision", "descriptive_recall",
                "descriptive_f1", "absolute_displacement_statistics",
            )},
            "ad038": {key: value["level_3"]["ad038"][key] for key in (
                "separated", "mapped_relation_identity", "unscorable_relation_identity_count",
                "paired_nearest_displacement_difference_statistics",
            )},
            "ad040": value["level_3"]["ad040"],
        }
        path = HERE / f"canonical_report_{run}.json"
        report = json.loads(path.read_text())
        reports[run] = {"sha256": digest(path), "scientific_fingerprint": report["scientific_fingerprint"]}

    threshold = {
        "recall": 0.5924170616113744, "f1": 0.7212925562608193,
        "matched": 625, "original_only": 430,
    }
    improvement = {}
    for configuration in ("B", "C"):
        candidates = [summaries[f"{configuration}_run_{index}"]["bass"] for index in (1, 2)]
        improvement[configuration] = all(
            item["matched_count"] > threshold["matched"] and
            item["descriptive_recall"] > threshold["recall"] and
            item["descriptive_f1"] > threshold["f1"] and
            item["original_only_count"] < threshold["original_only"]
            for item in candidates
        )
    persistence = all(
        summary["bass"]["descriptive_recall"] <= threshold["recall"] and
        1055 - summary["bass"]["raw_separated_count"] >= 377
        for summary in summaries.values()
    )
    decision = ("MATERIAL_POPULATION_IMPROVEMENT" if any(improvement.values()) else
                "PERSISTENT_BASS_DEFICIT" if persistence else "MIXED_OR_INDETERMINATE")
    result = {
        "execution_id": "EXEC-CEDVAL006-BASS-PRESERVATION-PHASE1-01",
        "status": "COMPLETE",
        "preregistration": {
            "id": "H-CEDVAL006-BASS-PRESERVATION-PHASE1-01",
            "commit": "c8faaf7d91c6e04cc777c14e8308512c4d42ec28",
            "fingerprint": "b6d497595f07a3a68472a39419a18579b28ba3501188e04c8ac90d27da6711f8",
        },
        "stem_authority_fingerprint": stems["authority_fingerprint"],
        "separation_replay": replay,
        "canonical_reports": reports,
        "scoring": {
            "fingerprint": scoring["scoring_fingerprint"],
            "execution_1_sha256": digest(HERE / "scoring_execution_1.json"),
            "execution_2_sha256": digest(HERE / "scoring_execution_2.json"),
            "byte_identical_replay": (HERE / "scoring_execution_1.json").read_bytes() == (HERE / "scoring_execution_2.json").read_bytes(),
            "summaries": summaries,
        },
        "baseline_best": threshold,
        "material_improvement_by_configuration": improvement,
        "persistence_gate_satisfied": persistence,
        "decision_classification": decision,
        "effects": {
            "shifts_zero": "Removed separation/JGA run-to-run variability but did not exceed the frozen best baseline Bass recovery envelope.",
            "float32": "Did not improve Bass population recovery over deterministic 16-bit B; C produced two fewer Bass EME and matches.",
        },
        "firewall": {
            "latency_correction": "NONE", "h02_used": False, "strength_used": False,
            "production_code_changed": False, "alternative_models_executed": False,
            "preferred_run_selection": False, "averaging": False,
        },
    }
    result["result_fingerprint"] = sha256(canonical(result)).hexdigest()
    (HERE / "result.json").write_bytes(canonical(result) + b"\n")
    (HERE / "report.md").write_text(
        "# CED-VAL-006 Bass Preservation Phase 1 Result\n\n"
        f"Decision: **{decision}**\n\n"
        "B and C each replayed byte-identically. Removing random shift eliminated run-to-run variability but did not clear the frozen Bass recovery gate. Float32 output did not improve recovery over B. No correction, H02, strength, model change, run selection, averaging, or production change occurred.\n\n"
        f"Result fingerprint: `{result['result_fingerprint']}`\n"
    )
    names = [
        *(f"canonical_report_{run}.json" for run in RUNS), "score.py",
        "scoring_execution_1.json", "scoring_execution_2.json",
        "generated_stem_authority.json", "result.json", "report.md",
        "finalize.py", "verify.py",
    ]
    manifest = {
        "execution_id": result["execution_id"], "result_fingerprint": result["result_fingerprint"],
        "repository_artifacts": {name: digest(HERE / name) for name in names},
        "external_stems": {run: {name: item["sha256"] for name, item in details["stems"].items()}
                           for run, details in stem_runs.items()},
    }
    (HERE / "artifact_manifest.json").write_bytes(canonical(manifest) + b"\n")
    print(result["result_fingerprint"], decision)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
