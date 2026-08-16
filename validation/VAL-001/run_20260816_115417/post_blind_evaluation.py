"""Evaluate the frozen blind result against Voice symbolic Ground Truth."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from statistics import median
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
MANIFEST = RUN / "manifest.json"


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True).encode() + b"\n"


def write_json(path: Path, value: object) -> None:
    path.write_bytes(canonical_bytes(value))


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def voice_events(source: Path) -> list[dict[str, object]]:
    root = ElementTree.parse(source).getroot()
    names = {
        item.attrib["id"]: item.findtext("part-name")
        for item in root.findall("./part-list/score-part")
    }
    part = next(
        item for item in root.findall("part")
        if names[item.attrib["id"]] == "Voce"
    )
    position = 0.0
    divisions = 1
    last_start = 0.0
    events = []
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
                pitch = item.find("pitch")
                if item.find("rest") is None and not continuation and pitch is not None:
                    step = pitch.findtext("step")
                    alter = int(pitch.findtext("alter", "0"))
                    octave = int(pitch.findtext("octave"))
                    semitone = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[step]
                    events.append({
                        "score_position_quarters": start,
                        "duration_quarters": duration,
                        "pitch_midi": 12 * (octave + 1) + semitone + alter,
                    })
                if not chord and not grace:
                    position += duration
    return events


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    external_root = Path(manifest["environment"]["external_run_root"])
    freeze_path = external_root / "blind_freeze.json"
    expected_freeze_file_sha256 = "c7dc882cfeebbd6238e681ec22f004f6f37fd50c5311dd23b272f7a031cd88f3"
    if file_sha256(freeze_path) != expected_freeze_file_sha256:
        raise RuntimeError("Frozen blind result checksum mismatch.")
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    if freeze["blind_status"] != "FROZEN" or freeze["ground_truth_loaded"]:
        raise RuntimeError("Blind phase was not validly frozen.")

    ground_truth_path = ROOT / "recordings/validation/ground_truth/03 THE COST OF LIVING versione intro + 8 bar.musicxml"
    expected_ground_truth_sha256 = "809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778"
    if file_sha256(ground_truth_path) != expected_ground_truth_sha256:
        raise RuntimeError("Ground Truth checksum mismatch.")
    symbolic = voice_events(ground_truth_path)
    inferred = sorted(
        freeze["frozen_blind_result"]["note_events"],
        key=lambda item: (item["onset_seconds"], item["offset_seconds"], item["pitch_midi"]),
    )
    consecutive = list(zip(inferred, inferred[1:]))
    exact_abutments = [
        (left, right) for left, right in consecutive
        if left["offset_seconds"] == right["onset_seconds"]
    ]
    exact_same_pitch_abutments = [
        (left, right) for left, right in exact_abutments
        if left["pitch_midi"] == right["pitch_midi"]
    ]
    overlaps = [
        (left, right) for left, right in consecutive
        if left["offset_seconds"] > right["onset_seconds"]
    ]
    durations = [item["offset_seconds"] - item["onset_seconds"] for item in inferred]
    confidences = [item["confidence"] for item in inferred]

    result = {
        "experiment_id": manifest["experiment_id"],
        "blind_freeze_file_sha256_before_ground_truth": expected_freeze_file_sha256,
        "blind_scientific_fingerprint": freeze["run_scientific_fingerprints"][0],
        "ground_truth_revealed_after_freeze": True,
        "ground_truth": {
            "path": str(ground_truth_path.relative_to(ROOT)),
            "sha256": expected_ground_truth_sha256,
            "voice_symbolic_event_count": len(symbolic),
            "voice_symbolic_events": symbolic,
        },
        "inferred_population": {
            "count": len(inferred),
            "chronological_span_seconds": [inferred[0]["onset_seconds"], inferred[-1]["offset_seconds"]],
            "duration_seconds": {
                "minimum": min(durations),
                "maximum": max(durations),
                "median": median(durations),
            },
            "confidence": {
                "minimum": min(confidences),
                "maximum": max(confidences),
                "median": median(confidences),
            },
            "exact_duplicate_count": freeze["frozen_blind_result"]["note_validation"]["exact_duplicate_event_count"],
            "exact_abutting_pair_count": len(exact_abutments),
            "exact_same_pitch_abutting_pair_count": len(exact_same_pitch_abutments),
            "chronologically_adjacent_overlap_count": len(overlaps),
            "events": inferred,
        },
        "population_comparison": {
            "observed_pulse_candidates": 150,
            "existing_structurally_authorized_eme": 108,
            "basic_pitch_inferred_events": len(inferred),
            "symbolic_events": len(symbolic),
            "inferred_minus_symbolic": len(inferred) - len(symbolic),
            "count_agreement": len(inferred) == len(symbolic),
        },
        "validation": {
            "ordering": "AVAILABLE DESCRIPTIVELY; raw Basic Pitch list order is not chronological, canonical comparison order is chronological",
            "temporal_distribution": "INFERRED events occupy the controlled audio scope; exact event identities are not assigned",
            "fragmentation": "ESTABLISHED AT POPULATION LEVEL and supported by exact same-pitch abutting inferred segments",
            "merging": "NOT SCIENTIFICALLY ESTABLISHED without authorized event-level score/audio correspondence",
            "duplicates": "NO EXACT DUPLICATE EVENT TUPLES",
            "missed_symbolic_events": "NOT QUANTIFIABLE without authorized event-level score/audio correspondence",
            "extra_inferred_events": "Population excess is 14; individual extras are not assigned without an authorized correspondence rule",
            "event_level_correspondence": "UNVALIDATED"
        },
        "outcome": "PARTIAL",
        "material_improvement": True,
        "production_integration_justified": False,
        "architecture_sufficient_for_future_adapter": True,
        "scientific_interpretation": "Pinned Basic Pitch materially reduces gross Voice transient fragmentation and produces reproducible pitch-bearing event hypotheses, but the 25-event population remains fragmented relative to 11 symbolic events and event identities cannot be validated under the current temporal-correspondence authority."
    }
    write_json(RUN / "post_blind_evaluation.json", result)


if __name__ == "__main__":
    main()
