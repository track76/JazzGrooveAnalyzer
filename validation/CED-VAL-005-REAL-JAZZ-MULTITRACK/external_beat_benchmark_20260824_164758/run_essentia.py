"""Fresh-process Essentia runner for the frozen external benchmark."""
from hashlib import sha256
from importlib import metadata
import json
import os
from pathlib import Path
import platform
import sys

import essentia
import essentia.standard as es
import numpy as np
import yaml
import six


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


mono_path, expected_hash, output_path = map(Path, sys.argv[1:])
if metadata.version("essentia") != "2.1b6.dev1389":
    raise RuntimeError("ESSENTIA_DISTRIBUTION_AUTHORITY_CONFLICT")
mono = np.load(mono_path, allow_pickle=False)
actual_hash = sha256(mono.tobytes(order="C")).hexdigest()
if actual_hash != expected_hash.name or mono.dtype != np.float32 or mono.shape != (10068072,):
    raise RuntimeError("SHARED_MONO_AUTHORITY_CONFLICT")

algorithm = es.RhythmExtractor2013(method="multifeature", minTempo=40, maxTempo=208)
bpm, ticks, confidence, estimates, intervals = algorithm(mono)
ticks_array = np.asarray(ticks)
estimates_array = np.asarray(estimates)
intervals_array = np.asarray(intervals)


def float_record(value):
    number = float(value)
    return {"decimal": number, "binary64_hex": number.hex()}


if not np.all(np.isfinite(ticks_array)) or np.any(np.diff(ticks_array) < 0):
    raise RuntimeError("TRACKER_OUTPUT_AUTHORITY_CONFLICT")
if np.any(ticks_array < 0) or np.any(ticks_array > 10068072 / 44100):
    raise RuntimeError("TRACKER_OUTPUT_AUTHORITY_CONFLICT")

record = {
    "tracker_id": "ESSENTIA_RHYTHMEXTRACTOR2013_MULTIFEATURE",
    "epistemic_status": "CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE",
    "status": "VALID_TRACKER_OUTPUT" if len(ticks_array) else "EMPTY_TRACKER_OUTPUT",
    "package_authority": {
        "distribution": "essentia==2.1b6.dev1389",
        "imported_version": essentia.__version__,
        "wheel": "essentia-2.1b6.dev1389-cp313-cp313-macosx_15_0_arm64.whl",
        "wheel_sha256": "84e5167b95d9e74b2ddd928555d5a1e11997a458dae25e653544a953bc3068b9",
    },
    "environment": {
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "numpy": np.__version__,
        "pyyaml": yaml.__version__,
        "six": six.__version__,
        "thread_environment": {name: os.environ.get(name) for name in (
            "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"
        )},
        "device": "CPU",
        "random_seed": "NOT_USED",
        "installed_distributions": sorted(
            {f"{item.metadata['Name']}=={item.version}" for item in metadata.distributions()}
        ),
    },
    "configuration": {
        "algorithm": "RhythmExtractor2013",
        "mode": "standard",
        "method": "multifeature",
        "minTempo": 40,
        "maxTempo": 208,
        "sample_rate_hz": 44100,
        "input_loader": "shared_frozen_float32_mono_array",
    },
    "shared_mono_raw_bytes_sha256": actual_hash,
    "native_outputs": {
        "bpm": float_record(bpm),
        "ticks": {
            "native_type": type(ticks).__name__,
            "dtype": str(ticks_array.dtype),
            "shape": list(ticks_array.shape),
            "seconds": [float_record(value) for value in ticks_array],
            "scaled_sample_values_non_authoritative": [float_record(float(value) * 44100) for value in ticks_array],
        },
        "confidence": {"semantics": "TRACK_LEVEL_MULTIFEATURE_CONFIDENCE_NOT_PER_BEAT", **float_record(confidence)},
        "estimates": {
            "native_type": type(estimates).__name__,
            "dtype": str(estimates_array.dtype),
            "shape": list(estimates_array.shape),
            "bpm_values": [float_record(value) for value in estimates_array],
        },
        "bpmIntervals": {
            "native_type": type(intervals).__name__,
            "dtype": str(intervals_array.dtype),
            "shape": list(intervals_array.shape),
            "seconds": [float_record(value) for value in intervals_array],
        },
    },
    "licensing": "AGPLv3/open non-commercial path; no distribution or production authority",
}
record["scientific_fingerprint"] = sha256(canonical(record)).hexdigest()
output_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
