"""Execute the frozen two-tracker external beat-position benchmark."""
from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import wave

import numpy as np

BASE = Path("validation/CED-VAL-005-REAL-JAZZ-MULTITRACK")
RUN = BASE / "external_beat_benchmark_20260824_164758"
PREREG = BASE / "preregistrations/H-CEDVAL005-EXTERNAL-BEAT-POSITION-FEASIBILITY-01.md"
INPUT = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-005-REAL-JAZZ-MULTITRACK/raw/MaurizioPagnuttiSextet_AllTheGinIsGone_Full/09_Overheads.wav")
INPUT_SHA = "0569a396cff95b130042fc71093e8ba3460e3c0fe0034cb86d2158027d585f3a"
PREREG_SHA = "b0269880bda305ed59ddef3353e60eab28d1a98ceaa0ce5cd7cde4ca193d042b"
PREREG_COMMIT = "c08dacabf2ca276636fd61ae6b0689d8b186a79c"
STUDY_ID = "H-CEDVAL005-EXTERNAL-BEAT-POSITION-FEASIBILITY-01"
EXECUTION_ID = "EXEC-CEDVAL005-EXTERNAL-BEAT-BENCHMARK-20260824-164758"
ESSENTIA_PYTHON = Path("/tmp/jga-essentia-2.1b6.dev1389/bin/python")
WHEEL = Path("/tmp/essentia-2.1b6.dev1389-cp313-cp313-macosx_15_0_arm64.whl")
WHEEL_SHA = "84e5167b95d9e74b2ddd928555d5a1e11997a458dae25e653544a953bc3068b9"
THREAD_ENV = {
    "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1", "VECLIB_MAXIMUM_THREADS": "1",
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def checksum(path):
    digest = sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def build_mono(path):
    with wave.open(str(path), "rb") as wav:
        props = (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getnframes(), wav.getcomptype())
        if props != (2, 3, 44100, 10068072, "NONE"):
            raise RuntimeError(f"INPUT_FORMAT_AUTHORITY_CONFLICT: {props}")
        raw = wav.readframes(wav.getnframes())
    bytes3 = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 2, 3)
    unsigned = (
        bytes3[:, :, 0].astype(np.int64)
        | (bytes3[:, :, 1].astype(np.int64) << 8)
        | (bytes3[:, :, 2].astype(np.int64) << 16)
    )
    signed = np.where(unsigned & 0x800000, unsigned - 0x1000000, unsigned)
    mono = ((signed[:, 0] + signed[:, 1]) / (2 * 8388608)).astype(np.float32)
    if mono.shape != (10068072,) or mono.dtype != np.float32:
        raise RuntimeError("MONO_AUTHORITY_CONFLICT")
    return np.ascontiguousarray(mono)


def run_fresh(python, script, mono_path, mono_hash, output):
    environment = os.environ.copy()
    environment.update(THREAD_ENV)
    subprocess.run(
        [str(python), str(script), str(mono_path), mono_hash, str(output)],
        check=True, cwd=Path.cwd(), env=environment,
    )
    return json.loads(output.read_text())


def without_fingerprint(record):
    return {key: value for key, value in record.items() if key != "scientific_fingerprint"}


def describe(values):
    if not values:
        return None
    data = np.asarray(values, dtype=np.float64)
    return {
        "count": len(values), "min": float(np.min(data)), "max": float(np.max(data)),
        "mean": float(np.mean(data)), "median": float(np.median(data)),
        "population_sd": float(np.std(data, ddof=0)),
    }


def main():
    if checksum(INPUT) != INPUT_SHA or checksum(PREREG) != PREREG_SHA:
        raise RuntimeError("AUTHORITY_CHECKSUM_CONFLICT")
    if not ESSENTIA_PYTHON.exists() or checksum(WHEEL) != WHEEL_SHA:
        raise RuntimeError("ESSENTIA_ENVIRONMENT_AUTHORITY_CONFLICT")
    with tempfile.TemporaryDirectory(prefix="jga-cedval005-external-beat-") as temp_name:
        temp = Path(temp_name)
        mono = build_mono(INPUT)
        mono_hash = sha256(mono.tobytes(order="C")).hexdigest()
        mono_path = temp / "shared_mono_float32.npy"
        np.save(mono_path, mono, allow_pickle=False)
        mono_authority = {
            "shape": list(mono.shape), "dtype": str(mono.dtype),
            "sample_count": int(mono.size), "sample_rate_hz": 44100,
            "raw_bytes_sha256": mono_hash,
            "npy_temporary_file_sha256": checksum(mono_path),
            "minimum": {"decimal": float(np.min(mono)), "binary32_hex_bytes": np.min(mono).tobytes().hex()},
            "maximum": {"decimal": float(np.max(mono)), "binary32_hex_bytes": np.max(mono).tobytes().hex()},
            "construction": "float32((int64(L)+int64(R))/(2*8388608))",
            "temporal_origin": "distributed-file sample zero",
        }
        essentia_passes = [
            run_fresh(ESSENTIA_PYTHON, RUN / "run_essentia.py", mono_path, mono_hash, temp / f"essentia_pass_{index}.json")
            for index in (1, 2)
        ]
        if canonical(essentia_passes[0]) != canonical(essentia_passes[1]):
            raise RuntimeError("ESSENTIA_DETERMINISTIC_REPLAY_FAILURE")
        librosa_passes = [
            run_fresh(Path(sys.executable), RUN / "run_librosa.py", mono_path, mono_hash, temp / f"librosa_pass_{index}.json")
            for index in (1, 2)
        ]
        if canonical(librosa_passes[0]) != canonical(librosa_passes[1]):
            raise RuntimeError("LIBROSA_DETERMINISTIC_REPLAY_FAILURE")
    essentia = essentia_passes[0]
    librosa = librosa_passes[0]
    essentia["deterministic_replay"] = "PASS_EXACT_TWO_FRESH_PROCESS_EXECUTIONS"
    essentia["scientific_fingerprint"] = sha256(canonical(without_fingerprint(essentia))).hexdigest()
    librosa["deterministic_replay"] = "PASS_EXACT_TWO_FRESH_PROCESS_EXECUTIONS"
    librosa["scientific_fingerprint"] = sha256(canonical(without_fingerprint(librosa))).hexdigest()
    essentia_intervals = [item["decimal"] for item in essentia["native_outputs"]["bpmIntervals"]["seconds"]]
    librosa_intervals = [item["decimal"] for item in librosa["native_outputs"]["derived_inter_beat_intervals_seconds"]]
    combined_basis = {
        "schema": "JGA-EXTERNAL-BEAT-POSITION-FEASIBILITY/v1",
        "study_id": STUDY_ID, "execution_id": EXECUTION_ID,
        "preregistration_commit": PREREG_COMMIT,
        "input_sha256": INPUT_SHA, "shared_mono_authority": mono_authority,
        "essentia_scientific_fingerprint": essentia["scientific_fingerprint"],
        "librosa_scientific_fingerprint": librosa["scientific_fingerprint"],
        "epistemic_status": "CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE",
        "blind_freeze_completed_before_jga_access": True,
        "firewalls": {
            "jga_eme_accessed": False, "jga_comparison_performed": False,
            "readme_bpm_used": False, "human_validation_performed": False,
            "h02_used": False, "strength_accessed": False,
            "jga_core_changed": False, "production_code_changed": False,
            "raw_assets_changed": False, "historical_authorities_changed": False,
            "constant_bpm_grid_constructed": False,
        },
    }
    combined_fingerprint = sha256(canonical(combined_basis)).hexdigest()
    result = {
        "status": "PASS_FROZEN_EXTERNAL_TWO_TRACKER_OUTPUTS",
        **combined_basis,
        "combined_benchmark_fingerprint": combined_fingerprint,
        "essentia_summary": {
            "status": essentia["status"],
            "reported_bpm": essentia["native_outputs"]["bpm"],
            "beat_count": len(essentia["native_outputs"]["ticks"]["seconds"]),
            "beat_time_scope_seconds": None if not essentia["native_outputs"]["ticks"]["seconds"] else [
                essentia["native_outputs"]["ticks"]["seconds"][0], essentia["native_outputs"]["ticks"]["seconds"][-1]
            ],
            "inter_beat_interval_summary_seconds": describe(essentia_intervals),
            "confidence": essentia["native_outputs"]["confidence"],
        },
        "librosa_summary": {
            "status": librosa["status"],
            "reported_tempo": librosa["native_outputs"]["tempo"],
            "beat_count": len(librosa["native_outputs"]["beat_frames"]["values"]),
            "beat_frame_scope": None if not librosa["native_outputs"]["beat_frames"]["values"] else [
                librosa["native_outputs"]["beat_frames"]["values"][0], librosa["native_outputs"]["beat_frames"]["values"][-1]
            ],
            "beat_sample_scope": None if not librosa["native_outputs"]["beat_samples"]["values"] else [
                librosa["native_outputs"]["beat_samples"]["values"][0], librosa["native_outputs"]["beat_samples"]["values"][-1]
            ],
            "beat_time_scope_seconds": None if not librosa["native_outputs"]["beat_seconds"]["values"] else [
                librosa["native_outputs"]["beat_seconds"]["values"][0], librosa["native_outputs"]["beat_seconds"]["values"][-1]
            ],
            "inter_beat_interval_summary_seconds": describe(librosa_intervals),
        },
    }
    write_json(RUN / "shared_mono_authority.json", mono_authority)
    write_json(RUN / "essentia_output.json", essentia)
    write_json(RUN / "librosa_output.json", librosa)
    write_json(RUN / "result.json", result)
    write_json(RUN / "input_manifest.json", {
        "study_id": STUDY_ID, "execution_id": EXECUTION_ID,
        "preregistration_sha256": PREREG_SHA, "preregistration_commit": PREREG_COMMIT,
        "input_path": str(INPUT), "input_sha256": INPUT_SHA,
        "input_properties": {"channels": 2, "sample_width_bytes": 3, "sample_rate_hz": 44100, "sample_count": 10068072},
        "essentia_wheel_sha256": WHEEL_SHA,
        "orchestrator_environment": {"python": sys.version, "platform": platform.platform(), "machine": platform.machine(), "numpy": np.__version__},
    })
    write_json(RUN / "completion_protocol.json", {
        "status": result["status"], "authority_gate": "PASS",
        "essentia_replay": essentia["deterministic_replay"],
        "librosa_replay": librosa["deterministic_replay"],
        "combined_benchmark_fingerprint": combined_fingerprint,
        **combined_basis["firewalls"],
    })
    (RUN / "report.md").write_text(
        f"# {STUDY_ID} Frozen Result\n\n"
        f"Execution: `{EXECUTION_ID}`\n\n"
        f"Status: **{result['status']}**\n\n"
        f"Combined benchmark fingerprint: `{combined_fingerprint}`.\n\n"
        "Essentia and librosa outputs replayed exactly across two fresh-process executions each. "
        "Both remain `CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE`. No JGA EME was accessed and no JGA comparison or musical interpretation occurred.\n"
    )
    artifacts = [
        "execute.py", "run_essentia.py", "run_librosa.py", "verify.py", "shared_mono_authority.json",
        "essentia_output.json", "librosa_output.json", "result.json", "input_manifest.json",
        "completion_protocol.json", "report.md",
    ]
    write_json(RUN / "artifact_manifest.json", {
        "study_id": STUDY_ID, "execution_id": EXECUTION_ID,
        "combined_benchmark_fingerprint": combined_fingerprint,
        "artifacts": {name: checksum(RUN / name) for name in artifacts},
    })
    print(json.dumps({
        "status": result["status"], "execution_id": EXECUTION_ID,
        "shared_mono_authority": mono_authority,
        "essentia": result["essentia_summary"], "essentia_fingerprint": essentia["scientific_fingerprint"],
        "librosa": result["librosa_summary"], "librosa_fingerprint": librosa["scientific_fingerprint"],
        "combined_benchmark_fingerprint": combined_fingerprint,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
