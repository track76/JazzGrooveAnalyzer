"""Blindly freeze three raw system outputs before Ground Truth access."""
from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import wave

import numpy as np

BASE = Path("validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK")
RUN = BASE / "run_20260824_212203"
PREREG = BASE / "preregistrations/H-CEDVAL007-THREE-SYSTEM-SYMBOLIC-BEAT-RECOVERY-01.md"
MANIFEST = BASE / "input_authority_manifest.json"
INPUT = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK/raw/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK-v0.1 DRUM GT.wav")
INPUT_SHA = "c673d2c104eb3eb31012154f1bd84ee81313b4fd36b61bf3913686f43e19bb0c"
DATASET_FP = "cd93455778d1484067f9a3caa3037b6467d27c7e8d5a8c0df694658bad2484e9"
PREREG_SHA = "9c7e44042b1bd17bd0c77d96b56fdc57769f3b64750c0a8e2a0c58d5892fd447"
JGA_PYTHON = Path(".venv/bin/python")
ESSENTIA_PYTHON = Path("/tmp/jga-essentia-2.1b6.dev1389/bin/python")
WHEEL = Path("/tmp/essentia-2.1b6.dev1389-cp313-cp313-macosx_15_0_arm64.whl")
WHEEL_SHA = "84e5167b95d9e74b2ddd928555d5a1e11997a458dae25e653544a953bc3068b9"
THREAD_ENV = {"OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "VECLIB_MAXIMUM_THREADS": "1", "PYTHONDONTWRITEBYTECODE": "1"}


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def verify_input() -> None:
    if checksum(PREREG) != PREREG_SHA or checksum(INPUT) != INPUT_SHA:
        raise RuntimeError("AUTHORITY_CHECKSUM_CONFLICT")
    manifest = json.loads(MANIFEST.read_text())
    if manifest["dataset_fingerprint"] != DATASET_FP or sha256(canonical(manifest["manifest_basis"])).hexdigest() != DATASET_FP:
        raise RuntimeError("DATASET_FINGERPRINT_CONFLICT")
    if not JGA_PYTHON.exists() or not ESSENTIA_PYTHON.exists() or checksum(WHEEL) != WHEEL_SHA:
        raise RuntimeError("RUNTIME_AUTHORITY_CONFLICT")


def build_mono() -> np.ndarray:
    with wave.open(str(INPUT), "rb") as wav:
        props = (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getnframes(), wav.getcomptype())
        if props != (2, 3, 44100, 1411200, "NONE"):
            raise RuntimeError(f"INPUT_FORMAT_CONFLICT:{props}")
        raw = wav.readframes(wav.getnframes())
    bytes3 = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 2, 3)
    unsigned = bytes3[:, :, 0].astype(np.int64) | (bytes3[:, :, 1].astype(np.int64) << 8) | (bytes3[:, :, 2].astype(np.int64) << 16)
    signed = np.where(unsigned & 0x800000, unsigned - 0x1000000, unsigned)
    mono = ((signed[:, 0] + signed[:, 1]) / (2 * 8388608)).astype(np.float32)
    if mono.shape != (1411200,) or mono.dtype != np.float32:
        raise RuntimeError("MONO_AUTHORITY_CONFLICT")
    return np.ascontiguousarray(mono)


def run(python: Path, script: Path, args: list[str], output: Path) -> dict:
    environment = os.environ.copy()
    environment.update(THREAD_ENV)
    subprocess.run([str(python), str(script), *args, str(output)], check=True, cwd=Path.cwd(), env=environment)
    return json.loads(output.read_text())


def replay_pair(python: Path, script: Path, args: list[str], temp: Path, label: str) -> dict:
    first_path = temp / f"{label}_pass_1.json"
    second_path = temp / f"{label}_pass_2.json"
    first = run(python, script, args, first_path)
    second = run(python, script, args, second_path)
    if first_path.read_bytes() != second_path.read_bytes():
        raise RuntimeError(f"{label.upper()}_REPLAY_CONFLICT")
    return first


def main(output: Path) -> None:
    verify_input()
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="cedval007-three-system-output-") as temp_name:
        temp = Path(temp_name)
        mono = build_mono()
        mono_hash = sha256(mono.tobytes(order="C")).hexdigest()
        mono_path = temp / "shared_mono.npy"
        np.save(mono_path, mono, allow_pickle=False)
        mono_authority = {
            "construction": "float32((int64(L)+int64(R))/(2*8388608))",
            "shape": [1411200],
            "dtype": "float32",
            "sample_rate_hz": 44100,
            "sample_zero_authority": "CED-VAL-007 distributed-file sample zero",
            "raw_bytes_sha256": mono_hash,
            "minimum": {"decimal": float(np.min(mono)), "binary32_hex_bytes": np.min(mono).tobytes().hex()},
            "maximum": {"decimal": float(np.max(mono)), "binary32_hex_bytes": np.max(mono).tobytes().hex()},
            "normalization": False,
            "trimming": False,
            "resampling": False,
        }
        # Frozen blind order: JGA, then librosa, then Essentia. No GT artifact is opened here.
        jga = replay_pair(JGA_PYTHON, RUN / "run_jga.py", [str(INPUT), INPUT_SHA], temp, "jga")
        write_json(output / "jga_raw_output.json", jga)
        librosa_output = replay_pair(JGA_PYTHON, RUN / "run_librosa.py", [str(mono_path), mono_hash], temp, "librosa")
        write_json(output / "librosa_raw_output.json", librosa_output)
        essentia = replay_pair(ESSENTIA_PYTHON, RUN / "run_essentia.py", [str(mono_path), mono_hash], temp, "essentia")
        write_json(output / "essentia_raw_output.json", essentia)
    write_json(output / "shared_mono_authority.json", mono_authority)
    combined_basis = {
        "input_sha256": INPUT_SHA,
        "shared_mono_raw_bytes_sha256": mono_authority["raw_bytes_sha256"],
        "system_fingerprints": {"JGA": jga["scientific_fingerprint"], "LIBROSA": librosa_output["scientific_fingerprint"], "ESSENTIA": essentia["scientific_fingerprint"]},
    }
    combined = {
        "status": "FROZEN_BEFORE_GROUND_TRUTH_ACCESS",
        "ground_truth_accessed_by_output_construction": False,
        "blind_freeze_order": ["JGA", "LIBROSA", "ESSENTIA"],
        "replay": {"JGA": "PASS_EXACT_TWO_FRESH_PROCESSES", "LIBROSA": "PASS_EXACT_TWO_FRESH_PROCESSES", "ESSENTIA": "PASS_EXACT_TWO_FRESH_PROCESSES"},
        "basis": combined_basis,
        "combined_raw_output_fingerprint": sha256(canonical(combined_basis)).hexdigest(),
    }
    write_json(output / "raw_system_output_authority.json", combined)
    print(json.dumps(combined, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: freeze_outputs.py OUTPUT_DIRECTORY")
    main(Path(sys.argv[1]))
