"""Fresh-process librosa runner for the frozen external benchmark."""
from hashlib import sha256
from importlib import metadata
import inspect
import json
import os
from pathlib import Path
import platform
import sys

import librosa
import numba
import numpy as np
import scipy


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def float_record(value):
    number = float(value)
    return {"decimal": number, "binary64_hex": number.hex()}


mono_path, expected_hash, output_path = map(Path, sys.argv[1:])
if metadata.version("librosa") != "0.11.0":
    raise RuntimeError("LIBROSA_DISTRIBUTION_AUTHORITY_CONFLICT")
mono = np.load(mono_path, allow_pickle=False)
actual_hash = sha256(mono.tobytes(order="C")).hexdigest()
if actual_hash != expected_hash.name or mono.dtype != np.float32 or mono.shape != (10068072,):
    raise RuntimeError("SHARED_MONO_AUTHORITY_CONFLICT")

tempo, beats = librosa.beat.beat_track(
    y=mono, sr=44100, onset_envelope=None, hop_length=512,
    start_bpm=120.0, tightness=100, trim=True, bpm=None, prior=None,
    units="frames", sparse=True,
)
tempo_array = np.asarray(tempo)
beat_array = np.asarray(beats)
if not np.issubdtype(beat_array.dtype, np.integer) or np.any(np.diff(beat_array) < 0):
    raise RuntimeError("TRACKER_OUTPUT_AUTHORITY_CONFLICT")
samples = beat_array.astype(np.int64) * 512
if np.any(beat_array < 0) or np.any(samples >= 10068072):
    raise RuntimeError("TRACKER_OUTPUT_AUTHORITY_CONFLICT")
seconds = samples.astype(np.float64) / 44100
intervals = np.diff(seconds)

record = {
    "tracker_id": "LIBROSA_BEAT_TRACK_0_11_0",
    "epistemic_status": "CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE",
    "status": "VALID_TRACKER_OUTPUT" if len(beat_array) else "EMPTY_TRACKER_OUTPUT",
    "package_authority": {
        "distribution": "librosa==0.11.0",
        "imported_version": librosa.__version__,
        "callable_signature": str(inspect.signature(librosa.beat.beat_track)),
        "callable_source_sha256": sha256(inspect.getsource(librosa.beat.beat_track).encode()).hexdigest(),
    },
    "environment": {
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "numba": numba.__version__,
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
        "api": "librosa.beat.beat_track",
        "y": "shared_frozen_float32_mono_array",
        "sr": 44100,
        "onset_envelope": None,
        "hop_length": 512,
        "start_bpm": 120.0,
        "tightness": 100,
        "trim": True,
        "bpm": None,
        "prior": None,
        "units": "frames",
        "sparse": True,
    },
    "shared_mono_raw_bytes_sha256": actual_hash,
    "native_outputs": {
        "tempo": {
            "native_type": type(tempo).__name__,
            "dtype": str(tempo_array.dtype),
            "shape": list(tempo_array.shape),
            "values": [float_record(value) for value in tempo_array.reshape(-1)],
            "semantics": "TRACKER_REPORTED_GLOBAL_TEMPO_DESCRIPTIVE_ONLY",
        },
        "beat_frames": {
            "native_type": type(beats).__name__,
            "dtype": str(beat_array.dtype),
            "shape": list(beat_array.shape),
            "values": [int(value) for value in beat_array],
        },
        "beat_samples": {
            "derivation": "512 * beat_frame",
            "values": [int(value) for value in samples],
        },
        "beat_seconds": {
            "derivation": "beat_sample / 44100",
            "values": [float_record(value) for value in seconds],
        },
        "derived_inter_beat_intervals_seconds": [float_record(value) for value in intervals],
        "confidence": {"status": "NOT_AVAILABLE_FROM_FROZEN_API"},
    },
    "frame_lattice": {"hop_samples": 512, "sample_rate_hz": 44100, "seconds": 512 / 44100},
    "licensing": "ISC; no distribution or production decision",
}
record["scientific_fingerprint"] = sha256(canonical(record)).hexdigest()
output_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
