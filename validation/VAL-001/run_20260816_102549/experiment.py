"""Blind double-bass peak-threshold sensitivity and post-blind validation."""

from __future__ import annotations

from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
from uuid import uuid4
from xml.etree import ElementTree

import librosa

from jga.audio.file_audio_source import FileAudioSource
from jga.core.pulse_candidate import PulseCandidate
from jga.engines.audio_preprocessor import AudioPreprocessor
from jga.engines.pulse_candidate_filter import PulseCandidateFilter
from jga.runtime.analysis_context import AnalysisContext


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
MANIFEST_PATH = RUN / "manifest.json"


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, indent=2, sort_keys=True).encode() + b"\n"


def write_json(path: Path, value: object) -> None:
    path.write_bytes(canonical_bytes(value))


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def observe(manifest: dict, delta: float) -> dict:
    asset = ROOT / manifest["blind_asset"]["path"]
    if checksum(asset) != manifest["blind_asset"]["sha256"]:
        raise RuntimeError("Double-bass asset checksum mismatch")
    audio = FileAudioSource().load(str(asset))
    context = AnalysisContext(audio=audio)
    AudioPreprocessor().process(context)
    base = manifest["baseline"]
    envelope = librosa.onset.onset_strength(
        y=context.processed_audio,
        sr=audio.sample_rate,
        hop_length=base["hop_length_samples"],
    )
    frames = librosa.onset.onset_detect(
        onset_envelope=envelope,
        sr=audio.sample_rate,
        hop_length=base["hop_length_samples"],
        units="frames",
        normalize=base["normalize"],
        pre_max=base["pre_max_frames"],
        post_max=base["post_max_frames"],
        pre_avg=base["pre_avg_frames"],
        post_avg=base["post_avg_frames"],
        wait=base["wait_frames"],
        delta=delta,
    )
    times = librosa.frames_to_time(
        frames,
        sr=audio.sample_rate,
        hop_length=base["hop_length_samples"],
    )
    raw = [
        PulseCandidate(
            time=float(time),
            strength=float(envelope[int(frame)]),
            confidence=1.0,
        )
        for frame, time in zip(frames, times)
    ]
    context.pulse_candidates = raw
    PulseCandidateFilter().process(context)
    filtered = context.pulse_candidates
    kept_frames = [
        round(item.time * audio.sample_rate / base["hop_length_samples"])
        for item in filtered
    ]
    return {
        "delta": delta,
        "raw_peak_count": len(raw),
        "filtered_pulse_candidate_count": len(filtered),
        "derived_eme_count": len(filtered),
        "frames": kept_frames,
        "pulse_candidates": [
            {
                "index": index,
                "frame": kept_frames[index],
                "timestamp_seconds": item.time,
                "strength": item.strength,
                "confidence": item.confidence,
            }
            for index, item in enumerate(filtered)
        ],
    }


def freeze_blind(manifest: dict) -> dict:
    first = {
        item["id"]: observe(manifest, item["delta"])
        for item in manifest["sensitivity_configurations"]
    }
    second = {
        item["id"]: observe(manifest, item["delta"])
        for item in manifest["sensitivity_configurations"]
    }
    if canonical_bytes(first) != canonical_bytes(second):
        raise RuntimeError("Blind sensitivity replay is not deterministic")
    baseline_frames = set(first["BASELINE"]["frames"])
    for result in first.values():
        frames = set(result["frames"])
        result["additional_frames_relative_to_baseline"] = sorted(
            frames - baseline_frames
        )
        result["missing_frames_relative_to_baseline"] = sorted(
            baseline_frames - frames
        )
        result["strictly_ordered"] = result["frames"] == sorted(result["frames"])
    return {
        "experiment_id": manifest["experiment_id"],
        "ground_truth_loaded": False,
        "byte_identical_replay": True,
        "configurations": first,
    }


def bass_onsets(source: Path) -> list[float]:
    root = ElementTree.parse(source).getroot()
    names = {
        item.attrib["id"]: item.findtext("part-name")
        for item in root.findall("./part-list/score-part")
    }
    part = next(
        item for item in root.findall("part")
        if names[item.attrib["id"]] == "Basso Verticale"
    )
    position = 0.0
    divisions = 1
    last_start = 0.0
    onsets = []
    for measure in part.findall("measure"):
        declared = measure.find("attributes/divisions")
        if declared is not None:
            divisions = int(declared.text)
        for item in list(measure):
            if item.tag == "backup":
                position -= int(item.findtext("duration")) / divisions
            elif item.tag == "forward":
                position += int(item.findtext("duration")) / divisions
            elif item.tag == "note":
                duration = int(item.findtext("duration", "0")) / divisions
                chord = item.find("chord") is not None
                grace = item.find("grace") is not None
                start = last_start if chord else position
                if not chord:
                    last_start = start
                ties = {tie.attrib.get("type") for tie in item.findall("tie")}
                continuation = "stop" in ties and "start" not in ties
                if item.find("rest") is None and not continuation:
                    onsets.append(start)
                if not chord and not grace:
                    position += duration
    return sorted(set(onsets))


def evaluate(manifest: dict, blind: dict) -> dict:
    source = ROOT / manifest["ground_truth_asset"]["path"]
    if checksum(source) != manifest["ground_truth_asset"]["sha256"]:
        raise RuntimeError("Ground Truth checksum mismatch")
    positions = bass_onsets(source)
    expected = [position * 60.0 / 78.0 for position in positions]
    bound = manifest["post_blind_mapping"]["correspondence_bound_seconds"]
    results = {}
    for config_id, observation in blind["configurations"].items():
        detected = [
            item["timestamp_seconds"] for item in observation["pulse_candidates"]
        ]
        symbolic_edges = [
            [j for j, candidate in enumerate(detected) if abs(candidate-target) <= bound]
            for target in expected
        ]
        candidate_edges = [
            [i for i, target in enumerate(expected) if abs(candidate-target) <= bound]
            for candidate in detected
        ]
        matches = [
            (i, edges[0]) for i, edges in enumerate(symbolic_edges)
            if len(edges) == 1 and len(candidate_edges[edges[0]]) == 1
        ]
        complete = (
            len(detected) == len(expected) == 28
            and len(matches) == 28
            and all(len(edges) == 1 for edges in symbolic_edges)
            and all(len(edges) == 1 for edges in candidate_edges)
        )
        results[config_id] = {
            "authoritative_event_count": len(expected),
            "pulse_candidate_count": len(detected),
            "derived_eme_count": len(detected),
            "correspondence_match_count": len(matches),
            "missed_symbolic_event_count": sum(len(x) != 1 for x in symbolic_edges),
            "extra_candidate_count": sum(len(x) != 1 for x in candidate_edges),
            "symbolic_events_with_multiple_candidates": sum(len(x) > 1 for x in symbolic_edges),
            "candidates_with_multiple_symbolic_events": sum(len(x) > 1 for x in candidate_edges),
            "status": "COMPLETE" if complete else ("PARTIAL" if matches else "FAILED"),
        }
    return {
        "ground_truth_loaded_after_blind_freeze": True,
        "score_positions_quarters": positions,
        "expected_timestamps_seconds": expected,
        "configurations": results,
        "experiment_status": (
            "COMPLETE"
            if any(item["status"] == "COMPLETE" for item in results.values())
            else "PARTIAL"
            if any(item["status"] == "PARTIAL" for item in results.values())
            else "FAILED"
        ),
    }


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())
    if manifest["status"] != "PREREGISTERED":
        raise RuntimeError("Experiment is not preregistered")
    blind = freeze_blind(manifest)
    write_json(RUN / "blind_populations.json", blind)
    frozen_sha256 = checksum(RUN / "blind_populations.json")
    post_blind = evaluate(manifest, blind)
    post_blind["blind_populations_sha256_before_ground_truth"] = frozen_sha256
    write_json(RUN / "post_blind_validation.json", post_blind)


if __name__ == "__main__":
    main()
