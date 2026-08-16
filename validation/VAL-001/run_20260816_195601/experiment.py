"""Execute H-VAL001-RHYTHM-STRENGTH-01 without Ground Truth access."""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

import librosa
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
PREREG = ROOT / "validation/VAL-001/preregistrations/H-VAL001-RHYTHM-STRENGTH-01.md"
PARENT_INPUT = ROOT / "validation/VAL-001/run_20260816_192519/blind_input.json"
PARENT_RESULT = ROOT / "validation/VAL-001/run_20260816_192519/blind_result.json"
PREREG_SHA256 = "8887de8754f13d8a2ad1d5b92918a135dbbd787ca1edcc34a15997e7a6f2aa94"
PARENT_INPUT_SHA256 = "25ee4d610f6a3130f0b4f001b1908c8dad443d34ee30413905f6fd377202c9e8"
PARENT_RESULT_SHA256 = "0f6d8162053142893d4f938f32c73174b26dd8c783a457ad98e6e491ecb369cd"
SR = 44100
HOP = 512
SOURCES = {
    "Drums": ("drums.wav", "d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd"),
    "Double Bass": ("double_bass.wav", "31d6f2e34d360c6f8f75362187433f2a2c1f5eb5cbbfe627305e99d07d8be6c5"),
    "Piano": ("piano.wav", "26fa1158f375598cc7c01e04379c00547ef1787f6862eb2f29a36aafd9007c7e"),
}


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def recover_events(label: str, population: dict) -> list[dict]:
    filename, asset_sha = SOURCES[label]
    path = ROOT / "recordings/validation/stems" / filename
    if sha256(path) != asset_sha:
        raise RuntimeError(f"asset identity mismatch: {label}")
    signal, sample_rate = librosa.load(path, sr=None, mono=False)
    if sample_rate != SR:
        raise RuntimeError(f"sample-rate mismatch: {label}")
    if signal.ndim > 1:
        signal = np.mean(signal, axis=0)
    peak = np.max(np.abs(signal))
    signal = signal / peak if peak > 0 else signal.copy()
    envelope = librosa.onset.onset_strength(y=signal, sr=sample_rate)
    recovered = []
    for item in population["events"]:
        frame = int(round(item["absolute_timestamp_seconds"] * SR / HOP))
        time = float(librosa.frames_to_time(frame, sr=SR, hop_length=HOP))
        strength = float(envelope[frame])
        source_id = item["sound_source_id"]
        index = item["observation_indices"][0]
        identity = ":".join((
            "domain-pulse-candidate/v2", asset_sha, source_id, str(index),
            time.hex(), strength.hex(), float(1.0).hex(),
        ))
        candidate_id = str(uuid5(NAMESPACE_URL, identity))
        if candidate_id != item["supporting_pulse_candidate_ids"][0]:
            raise RuntimeError(f"supporting observation identity mismatch: {label}:{index}")
        recovered.append({
            "eme_id": item["eme_id"], "pulse_candidate_id": candidate_id,
            "timestamp_seconds": time, "frame_index": frame,
            "strength": strength, "source_asset_sha256": asset_sha,
        })
    return recovered


def scoped(events: list[dict], scope: str) -> list[dict]:
    if scope == "FULL":
        return events
    lo, hi = events[0]["frame_index"], events[-1]["frame_index"]
    midpoint = (lo + hi) / 2
    return [e for e in events if (e["frame_index"] < midpoint) == (scope == "EARLY")]


def association(events: list[dict], period: int) -> float | None:
    strengths = np.asarray([e["strength"] for e in events], dtype=float)
    deviations = strengths - strengths.mean()
    denominator = float(np.abs(deviations).sum())
    if denominator == 0:
        return None
    frames = np.asarray([e["frame_index"] for e in events], dtype=float)
    vector = np.sum(deviations * np.exp(2j * math.pi * frames / period))
    return round(float(abs(vector) / denominator), 12)


def execute() -> dict:
    if sha256(PREREG) != PREREG_SHA256 or sha256(PARENT_INPUT) != PARENT_INPUT_SHA256:
        raise RuntimeError("preregistered input integrity failure")
    if sha256(PARENT_RESULT) != PARENT_RESULT_SHA256:
        raise RuntimeError("frozen candidate integrity failure")
    parent_input = json.loads(PARENT_INPUT.read_text())
    parent = json.loads(PARENT_RESULT.read_text())
    candidates = {c["common_period_id"]: c for c in parent["common_period_candidates"]}
    relations = parent["hierarchical_relationships"]
    source_results = {}
    for label in SOURCES:
        events = recover_events(label, parent_input["populations"][label])
        measurements = {}
        for candidate_id, candidate in candidates.items():
            lower, upper = candidate["common_measurement_intersection_frames"]
            per_scope = {}
            for scope in ("FULL", "EARLY", "LATE"):
                subset = scoped(events, scope)
                values = {str(p): association(subset, p) for p in range(lower, upper + 1)}
                per_scope[scope] = {"event_count": len(subset), "association_by_period": values}
            measurements[candidate_id] = per_scope
        relation_results = []
        for relation in relations:
            short_id = relation["shorter_candidate_id"]
            long_id = relation["longer_candidate_id"]
            directions = []
            for scope in ("FULL", "EARLY", "LATE"):
                short_values = measurements[short_id][scope]["association_by_period"].values()
                long_values = measurements[long_id][scope]["association_by_period"].values()
                comparisons = [
                    "SHORT" if s > l else "LONG" if l > s else "TIE"
                    for s in short_values for l in long_values
                ]
                directions.append(comparisons[0] if len(set(comparisons)) == 1 else "MIXED")
            preference = directions[0] if len(set(directions)) == 1 and directions[0] in ("SHORT", "LONG") else "UNRESOLVED"
            relation_results.append({"short_id": short_id, "long_id": long_id,
                                     "full_early_late": directions, "preference": preference})
        preferences = {r["preference"] for r in relation_results}
        source_preference = (
            "SHORT_PREFERRED" if preferences == {"SHORT"} else
            "LONG_PREFERRED" if preferences == {"LONG"} else
            "EQUIVALENT_UNRESOLVED"
        )
        source_results[label] = {
            "event_count": len(events), "events": events, "measurements": measurements,
            "relation_results": relation_results, "source_preference": source_preference,
        }
    votes = [v["source_preference"] for v in source_results.values()]
    short, long = votes.count("SHORT_PREFERRED"), votes.count("LONG_PREFERRED")
    if short and long:
        classification = "SOURCE_DISAGREEMENT"
    elif short >= 2:
        classification = "SHORT_PREFERRED"
    elif long >= 2:
        classification = "LONG_PREFERRED"
    else:
        classification = "EQUIVALENT_UNRESOLVED"
    result = {
        "experiment_id": "H-VAL001-RHYTHM-STRENGTH-01", "status": "BLIND_FROZEN",
        "epistemic_status": "DERIVED_EVIDENCE", "preregistration_sha256": PREREG_SHA256,
        "parent_input_sha256": PARENT_INPUT_SHA256, "parent_result_sha256": PARENT_RESULT_SHA256,
        "ground_truth_accessed": False, "declared_context_accessed": False,
        "voice_status": "DEFERRED", "source_results": source_results,
        "blind_classification": classification,
        "environment": {"python": sys.version, "platform": platform.platform(),
                        "numpy": np.__version__, "librosa": librosa.__version__},
    }
    result["scientific_fingerprint"] = hashlib.sha256(canonical(result)).hexdigest()
    return result


first = execute()
second = execute()
if canonical(first) != canonical(second):
    raise RuntimeError("deterministic replay failure")
(RUN / "blind_result.json").write_bytes(canonical(first) + b"\n")
result_sha = sha256(RUN / "blind_result.json")
freeze = {"experiment_id": first["experiment_id"], "blind_result_sha256": result_sha,
          "scientific_fingerprint": first["scientific_fingerprint"],
          "blind_classification": first["blind_classification"],
          "deterministic_replay": "PASS", "ground_truth_accessed": False}
(RUN / "blind_freeze.json").write_bytes(canonical(freeze) + b"\n")
