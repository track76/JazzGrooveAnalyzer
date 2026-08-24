"""Fresh-process frozen Essentia raw-output constructor; no Ground Truth access."""
from __future__ import annotations

from hashlib import sha256
from importlib import metadata
import json
from pathlib import Path
import platform
import sys

import essentia
import essentia.standard as es
import numpy as np


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def float_record(value) -> dict:
    number = float(value)
    return {"decimal": number, "binary64_hex": number.hex()}


mono_path, expected_hash, output_path = map(Path, sys.argv[1:])
if metadata.version("essentia") != "2.1b6.dev1389":
    raise RuntimeError("ESSENTIA_VERSION_CONFLICT")
mono = np.load(mono_path, allow_pickle=False)
actual_hash = sha256(mono.tobytes(order="C")).hexdigest()
if actual_hash != expected_hash.name or mono.dtype != np.float32 or mono.shape != (1411200,):
    raise RuntimeError("SHARED_MONO_AUTHORITY_CONFLICT")
algorithm = es.RhythmExtractor2013(method="multifeature", minTempo=40, maxTempo=208)
bpm, ticks, confidence, estimates, intervals = algorithm(mono)
tick_array = np.asarray(ticks)
if not np.all(np.isfinite(tick_array)) or np.any(np.diff(tick_array) < 0):
    raise RuntimeError("OUTPUT_AUTHORITY_CONFLICT")
outputs = [{
    "native_output_index": index,
    "output_id": f"ESSENTIA-BEAT-{index:04d}",
    "beat_seconds": float(value),
    "beat_seconds_binary64_hex": float(value).hex(),
} for index, value in enumerate(tick_array)]
record = {
    "system": "ESSENTIA",
    "epistemic_status": "BEAT_TRACKER_OUTPUT",
    "input_mono_raw_bytes_sha256": actual_hash,
    "raw_output_count": len(outputs),
    "outputs": outputs,
    "reported_bpm": float_record(bpm),
    "confidence": {"semantics": "TRACK_LEVEL_MULTIFEATURE_CONFIDENCE", **float_record(confidence)},
    "intervals": [float_record(value) for value in np.asarray(intervals)],
    "estimates": [float_record(value) for value in np.asarray(estimates)],
    "configuration": {"algorithm": "RhythmExtractor2013", "method": "multifeature", "minTempo": 40, "maxTempo": 208, "sample_rate_hz": 44100, "resampling": False},
    "package_authority": {"distribution": "essentia==2.1b6.dev1389", "imported_version": essentia.__version__, "wheel_sha256": "84e5167b95d9e74b2ddd928555d5a1e11997a458dae25e653544a953bc3068b9"},
    "environment": {"python": sys.version, "platform": platform.platform(), "numpy": np.__version__, "thread_limits": 1},
    "ground_truth_accessed": False,
    "known_bpm_supplied": False,
}
record["scientific_fingerprint"] = sha256(canonical(record)).hexdigest()
output_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
