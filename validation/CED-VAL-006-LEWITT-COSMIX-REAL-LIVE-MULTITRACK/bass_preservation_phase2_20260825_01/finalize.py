#!/usr/bin/env python3
"""Freeze the CED-VAL-006 Bass-preservation Phase-2 result."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
EXTERNAL = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE2-01")
RUNS = tuple(f"M{model}_run_{run}" for model in range(1, 4) for run in range(1, 3))
MODELS = {
    "M1": {"name": "htdemucs_ft", "track": "htdemucs_ft/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1", "stems": ("bass.wav", "drums.wav", "other.wav", "vocals.wav")},
    "M2": {"name": "htdemucs_6s", "track": "htdemucs_6s/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1", "stems": ("bass.wav", "drums.wav", "guitar.wav", "other.wav", "piano.wav", "vocals.wav")},
    "M3": {"name": "mdx_extra", "track": "mdx_extra/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1", "stems": ("bass.wav", "drums.wav", "other.wav", "vocals.wav")},
}


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
        if stream.read(4) != b"RIFF" or not stream.read(4) or stream.read(4) != b"WAVE":
            raise RuntimeError(f"not RIFF/WAVE:{path}")
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
        model_key = run[:2]
        model = MODELS[model_key]
        root = EXTERNAL / run / model["track"]
        stem_runs[run] = {
            "model": model["name"],
            "stems": {name: wav_authority(root / name) for name in model["stems"]},
            "appledouble_excluded": sorted(str(path) for path in root.glob("._*")),
        }
    replay = {}
    for model_key, model in MODELS.items():
        first, second = stem_runs[f"{model_key}_run_1"], stem_runs[f"{model_key}_run_2"]
        replay[model["name"]] = "BYTE_IDENTICAL" if all(
            first["stems"][name]["sha256"] == second["stems"][name]["sha256"]
            for name in model["stems"]
        ) else "SCIENTIFICALLY_NONIDENTICAL"
    stems = {
        "authority_id": "GA-CEDVAL006-BASS-PRESERVATION-PHASE2-STEMS-01",
        "controlled_mix_sha256": "32845a5d05538524b19c8f857b0a908f6618cc4b95110a14169f1e450ddfe6e0",
        "runs": stem_runs, "replay": replay,
        "native_mapping": {"drums.wav": "TEMPORAL_REFERENCE", "bass.wav": "Double Bass / ACCOMPANIMENT"},
        "selection_recombination_or_averaging": "NONE",
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
                "descriptive_f1", "absolute_displacement_statistics")},
            "drums": {key: value["level_2"]["Drums"][key] for key in (
                "raw_separated_count", "matched_count", "original_only_count",
                "separated_only_count", "descriptive_precision", "descriptive_recall",
                "descriptive_f1", "absolute_displacement_statistics")},
            "ad038": {key: value["level_3"]["ad038"][key] for key in (
                "separated", "mapped_relation_identity", "unscorable_relation_identity_count",
                "paired_nearest_displacement_difference_statistics")},
            "ad040": value["level_3"]["ad040"],
        }
        path = HERE / f"canonical_report_{run}.json"
        report = json.loads(path.read_text())
        reports[run] = {"sha256": digest(path), "scientific_fingerprint": report["scientific_fingerprint"]}

    baseline = {"matched": 625, "recall": 0.5924170616113744, "f1": 0.7212925562608193, "original_only": 430}
    clear = {}
    for model_key in MODELS:
        candidates = [summaries[f"{model_key}_run_{run}"]["bass"] for run in (1, 2)]
        clear[model_key] = all(
            item["matched_count"] > baseline["matched"] and
            item["descriptive_recall"] > baseline["recall"] and
            item["descriptive_f1"] > baseline["f1"] and
            item["original_only_count"] < baseline["original_only"]
            for item in candidates
        )
    partial = any(
        item["bass"]["matched_count"] > baseline["matched"] or
        item["bass"]["descriptive_recall"] > baseline["recall"] or
        item["bass"]["descriptive_f1"] > baseline["f1"] or
        item["bass"]["original_only_count"] < baseline["original_only"]
        for item in summaries.values()
    )
    decision = ("CLEAR_MODEL_IMPROVEMENT" if any(clear.values()) else
                "MODEL_DEPENDENT_MIXED_RESULT" if partial else
                "PERSISTENT_CROSS_MODEL_BASS_DEFICIT")
    result = {
        "execution_id": "EXEC-CEDVAL006-BASS-PRESERVATION-PHASE2-01",
        "status": "COMPLETE",
        "preregistration": {"id": "H-CEDVAL006-BASS-PRESERVATION-PHASE2-01", "commit": "ee769b9203389db6b891613c0e9db7ce9a7395e1", "fingerprint": "8c17046b5b0ef8ea4bc6a88e3b2334e56b07b3ffaff9b5fea7a8b42d0acc1f48"},
        "stem_authority_fingerprint": stems["authority_fingerprint"],
        "separation_replay": replay,
        "canonical_reports": reports,
        "scoring": {"fingerprint": scoring["scoring_fingerprint"], "execution_1_sha256": digest(HERE / "scoring_execution_1.json"), "execution_2_sha256": digest(HERE / "scoring_execution_2.json"), "byte_identical_replay": (HERE / "scoring_execution_1.json").read_bytes() == (HERE / "scoring_execution_2.json").read_bytes(), "summaries": summaries},
        "original_bass_eme_authority": 1055,
        "baseline_best": baseline,
        "phase1_deterministic": {"matched": 607, "recall": 0.5753554502369668, "f1": 0.7107728337236534, "original_only": 448},
        "clear_model_improvement_by_model": clear,
        "decision_classification": decision,
        "deferred_hypothesis": "POST_SEPARATION_BASS_COMPRESSION_DEFERRED_TO_PHASE_3",
        "firewall": {"latency_correction": "NONE", "h02_used": False, "strength_used": False, "production_code_changed": False, "stem_recombination": False, "preferred_run_selection": False, "averaging": False},
    }
    result["result_fingerprint"] = sha256(canonical(result)).hexdigest()
    (HERE / "result.json").write_bytes(canonical(result) + b"\n")
    (HERE / "report.md").write_text(
        "# CED-VAL-006 Bass Preservation Phase 2 Result\n\n"
        f"Decision: **{decision}**\n\n"
        "All three models replayed byte-identically. No model cleared the complete frozen baseline-best gate in both runs. htdemucs_ft and mdx_extra improved F1 over the baseline best and improved the complete population tuple over deterministic Phase-1 htdemucs, while htdemucs_6s degraded Bass recovery. The result is therefore model-dependent and mixed, not a clear model improvement.\n\n"
        "No correction, H02, strength, compression, stem recombination, run selection, averaging, or production change occurred. Bass compression remains deferred to Phase 3.\n\n"
        f"Result fingerprint: `{result['result_fingerprint']}`\n"
    )
    names = [*(f"canonical_report_{run}.json" for run in RUNS), "score.py", "scoring_execution_1.json", "scoring_execution_2.json", "generated_stem_authority.json", "result.json", "report.md", "finalize.py", "verify.py"]
    manifest = {"execution_id": result["execution_id"], "result_fingerprint": result["result_fingerprint"], "repository_artifacts": {name: digest(HERE / name) for name in names}, "external_stems": {run: {name: item["sha256"] for name, item in details["stems"].items()} for run, details in stem_runs.items()}}
    (HERE / "artifact_manifest.json").write_bytes(canonical(manifest) + b"\n")
    print(result["result_fingerprint"], decision)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
