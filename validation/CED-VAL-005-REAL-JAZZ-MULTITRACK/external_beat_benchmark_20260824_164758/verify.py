"""Verify the frozen external beat-position benchmark authority."""
from hashlib import sha256
import json
from pathlib import Path

RUN = Path("validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/external_beat_benchmark_20260824_164758")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def checksum(path):
    digest = sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


manifest = json.loads((RUN / "artifact_manifest.json").read_text())
result = json.loads((RUN / "result.json").read_text())
essentia = json.loads((RUN / "essentia_output.json").read_text())
librosa = json.loads((RUN / "librosa_output.json").read_text())
mono = json.loads((RUN / "shared_mono_authority.json").read_text())
for name, expected in manifest["artifacts"].items():
    assert checksum(RUN / name) == expected, name
for tracker in (essentia, librosa):
    basis = {key: value for key, value in tracker.items() if key != "scientific_fingerprint"}
    assert sha256(canonical(basis)).hexdigest() == tracker["scientific_fingerprint"]
    assert tracker["deterministic_replay"] == "PASS_EXACT_TWO_FRESH_PROCESS_EXECUTIONS"
    assert tracker["epistemic_status"] == "CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE"
assert mono["shape"] == [10068072] and mono["dtype"] == "float32"
assert len(essentia["native_outputs"]["ticks"]["seconds"]) == 468
assert len(essentia["native_outputs"]["bpmIntervals"]["seconds"]) == 467
frames = librosa["native_outputs"]["beat_frames"]["values"]
samples = librosa["native_outputs"]["beat_samples"]["values"]
seconds = librosa["native_outputs"]["beat_seconds"]["values"]
assert len(frames) == len(samples) == len(seconds) == 464
for frame, sample, second in zip(frames, samples, seconds):
    assert sample == 512 * frame
    value = sample / 44100
    assert value == second["decimal"] and value.hex() == second["binary64_hex"]
basis = {
    key: result[key] for key in (
        "schema", "study_id", "execution_id", "preregistration_commit",
        "input_sha256", "shared_mono_authority", "essentia_scientific_fingerprint",
        "librosa_scientific_fingerprint", "epistemic_status",
        "blind_freeze_completed_before_jga_access", "firewalls",
    )
}
assert sha256(canonical(basis)).hexdigest() == result["combined_benchmark_fingerprint"]
assert all(value is False for value in result["firewalls"].values())
assert result["blind_freeze_completed_before_jga_access"] is True
print("PASS_FROZEN_EXTERNAL_TWO_TRACKER_OUTPUTS")
print(result["combined_benchmark_fingerprint"])
