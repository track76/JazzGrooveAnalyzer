"""Fresh-process frozen librosa raw-output constructor; no Ground Truth access."""
from __future__ import annotations

from hashlib import sha256
from importlib import metadata
import inspect
import json
from pathlib import Path
import platform
import sys

import librosa
import numpy as np


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


mono_path, expected_hash, output_path = map(Path, sys.argv[1:])
if metadata.version("librosa") != "0.11.0":
    raise RuntimeError("LIBROSA_VERSION_CONFLICT")
mono = np.load(mono_path, allow_pickle=False)
actual_hash = sha256(mono.tobytes(order="C")).hexdigest()
if actual_hash != expected_hash.name or mono.dtype != np.float32 or mono.shape != (1411200,):
    raise RuntimeError("SHARED_MONO_AUTHORITY_CONFLICT")
tempo, beats = librosa.beat.beat_track(
    y=mono,
    sr=44100,
    onset_envelope=None,
    hop_length=512,
    tightness=100,
    trim=True,
    bpm=None,
    prior=None,
    units="frames",
    sparse=True,
)
beat_array = np.asarray(beats)
if not np.issubdtype(beat_array.dtype, np.integer) or np.any(np.diff(beat_array) < 0):
    raise RuntimeError("OUTPUT_AUTHORITY_CONFLICT")
samples = beat_array.astype(np.int64) * 512
seconds = samples.astype(np.float64) / 44100
outputs = [{
    "native_output_index": index,
    "output_id": f"LIBROSA-BEAT-{index:04d}",
    "beat_frame": int(frame),
    "beat_sample": int(sample),
    "beat_seconds": float(time),
    "beat_seconds_binary64_hex": float(time).hex(),
} for index, (frame, sample, time) in enumerate(zip(beat_array, samples, seconds))]
tempo_array = np.asarray(tempo).reshape(-1)
record = {
    "system": "LIBROSA",
    "epistemic_status": "BEAT_TRACKER_OUTPUT",
    "input_mono_raw_bytes_sha256": actual_hash,
    "raw_output_count": len(outputs),
    "outputs": outputs,
    "reported_tempo": [{"decimal": float(value), "binary64_hex": float(value).hex()} for value in tempo_array],
    "configuration": {
        "api": "librosa.beat.beat_track",
        "sr": 44100,
        "onset_envelope": None,
        "hop_length": 512,
        "start_bpm": "OMITTED_LIBRARY_DEFAULT_NOT_GROUND_TRUTH_INPUT",
        "tightness": 100,
        "trim": True,
        "bpm": None,
        "prior": None,
        "units": "frames",
        "sparse": True,
    },
    "package_authority": {"distribution": "librosa==0.11.0", "imported_version": librosa.__version__, "callable_signature": str(inspect.signature(librosa.beat.beat_track))},
    "environment": {"python": sys.version, "platform": platform.platform(), "numpy": np.__version__},
    "ground_truth_accessed": False,
    "known_bpm_supplied": False,
}
record["scientific_fingerprint"] = sha256(canonical(record)).hexdigest()
output_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
