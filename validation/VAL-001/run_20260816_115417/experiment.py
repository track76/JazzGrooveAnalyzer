"""Run and freeze the blind Voice-only Basic Pitch proof of concept."""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import sys

import numpy as np


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


def array_sha256(value: np.ndarray) -> str:
    value = np.ascontiguousarray(value)
    digest = sha256()
    digest.update(str(value.dtype).encode())
    digest.update(canonical_bytes(list(value.shape)))
    digest.update(value.tobytes(order="C"))
    return digest.hexdigest()


def scientific_fingerprint(record: dict[str, object]) -> str:
    scientific = {
        "arrays": record["arrays"],
        "note_events": record["note_events"],
    }
    return sha256(canonical_bytes(scientific)).hexdigest()


def normalize_note_event(event: tuple) -> dict[str, object]:
    onset, offset, pitch, confidence, pitch_bends = event
    return {
        "onset_seconds": float(onset),
        "offset_seconds": float(offset),
        "pitch_midi": int(pitch),
        "confidence": float(confidence),
        "pitch_bends": None if pitch_bends is None else [int(value) for value in pitch_bends],
    }


def validate_notes(notes: list[dict[str, object]]) -> dict[str, object]:
    ordered = all(
        (notes[index]["onset_seconds"], notes[index]["offset_seconds"], notes[index]["pitch_midi"])
        <= (notes[index + 1]["onset_seconds"], notes[index + 1]["offset_seconds"], notes[index + 1]["pitch_midi"])
        for index in range(len(notes) - 1)
    )
    valid = all(
        math.isfinite(note["onset_seconds"])
        and math.isfinite(note["offset_seconds"])
        and math.isfinite(note["confidence"])
        and note["onset_seconds"] < note["offset_seconds"]
        and 0 <= note["pitch_midi"] <= 127
        for note in notes
    )
    identities = [canonical_bytes(note) for note in notes]
    return {
        "chronologically_ordered": ordered,
        "all_events_well_formed": valid,
        "exact_duplicate_event_count": len(identities) - len(set(identities)),
    }


def load_manifest() -> dict[str, object]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["status"] != "PREREGISTERED":
        raise RuntimeError("Manifest is not preregistered.")
    return manifest


def verify_inputs(manifest: dict[str, object]) -> tuple[Path, Path]:
    audio_path = ROOT / manifest["input"]["path"]
    if file_sha256(audio_path) != manifest["input"]["sha256"]:
        raise RuntimeError("Voice input checksum mismatch.")

    from basic_pitch.inference import ICASSP_2022_MODEL_PATH

    model_path = Path(ICASSP_2022_MODEL_PATH)
    for relative, expected in manifest["model_freeze"]["model_component_sha256"].items():
        if file_sha256(model_path / relative) != expected:
            raise RuntimeError(f"Model component checksum mismatch: {relative}")
    return audio_path, model_path


def environment_record() -> dict[str, object]:
    distributions = {}
    unreadable_metadata = 0
    for distribution in importlib.metadata.distributions():
        try:
            name = distribution.metadata.get("Name")
            if name:
                distributions[name] = distribution.version
        except (OSError, UnicodeError):
            # External HFS metadata sidecars are not Python distributions and
            # may not be UTF-8. They are operational, not scientific inputs.
            unreadable_metadata += 1
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "executable": sys.executable,
        "packages": dict(sorted(distributions.items(), key=lambda item: item[0].lower())),
        "ignored_unreadable_metadata_entries": unreadable_metadata,
    }


def run_once(label: str) -> None:
    manifest = load_manifest()
    audio_path, model_path = verify_inputs(manifest)
    external_root = Path(manifest["environment"]["external_run_root"])
    output_dir = external_root / label
    output_dir.mkdir(parents=True, exist_ok=False)

    from basic_pitch.inference import predict

    model_output, midi, raw_notes = predict(audio_path, model_or_model_path=model_path)
    notes = [normalize_note_event(event) for event in raw_notes]
    array_records = {}
    for name, value in sorted(model_output.items()):
        array = np.asarray(value)
        path = output_dir / f"{name}.npy"
        np.save(path, array, allow_pickle=False)
        array_records[name] = {
            "dtype": str(array.dtype),
            "shape": list(array.shape),
            "scientific_sha256": array_sha256(array),
            "file_sha256": file_sha256(path),
        }

    midi_path = output_dir / "inference.mid"
    midi.write(str(midi_path))
    write_json(output_dir / "note_events.json", notes)
    record = {
        "experiment_id": manifest["experiment_id"],
        "run_label": label,
        "epistemic_status": "INFERRED",
        "ground_truth_loaded": False,
        "input_sha256": file_sha256(audio_path),
        "model_path": str(model_path),
        "arrays": array_records,
        "note_events": notes,
        "note_event_count": len(notes),
        "note_validation": validate_notes(notes),
        "midi_file_sha256": file_sha256(midi_path),
        "environment": environment_record(),
    }
    record["scientific_fingerprint"] = scientific_fingerprint(record)
    write_json(output_dir / "blind_run.json", record)
    print(json.dumps({
        "label": label,
        "count": len(notes),
        "scientific_fingerprint": record["scientific_fingerprint"],
        "record_sha256": file_sha256(output_dir / "blind_run.json"),
    }, sort_keys=True))


def freeze() -> None:
    manifest = load_manifest()
    external_root = Path(manifest["environment"]["external_run_root"])
    records = [
        json.loads((external_root / label / "blind_run.json").read_text(encoding="utf-8"))
        for label in ("run_1", "run_2")
    ]
    fingerprints = [record["scientific_fingerprint"] for record in records]
    identical = fingerprints[0] == fingerprints[1]
    freeze_record = {
        "experiment_id": manifest["experiment_id"],
        "ground_truth_loaded": False,
        "blind_status": "FROZEN",
        "run_scientific_fingerprints": fingerprints,
        "scientific_outputs_identical": identical,
        "note_event_counts": [record["note_event_count"] for record in records],
        "first_run_record_sha256": file_sha256(external_root / "run_1" / "blind_run.json"),
        "second_run_record_sha256": file_sha256(external_root / "run_2" / "blind_run.json"),
        "frozen_blind_result": records[0],
    }
    freeze_record["blind_freeze_sha256"] = sha256(canonical_bytes(freeze_record)).hexdigest()
    write_json(external_root / "blind_freeze.json", freeze_record)
    print(json.dumps({
        "identical": identical,
        "counts": freeze_record["note_event_counts"],
        "blind_freeze_sha256": freeze_record["blind_freeze_sha256"],
        "freeze_file_sha256": file_sha256(external_root / "blind_freeze.json"),
    }, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("run", "freeze"))
    parser.add_argument("--label")
    arguments = parser.parse_args()
    if arguments.command == "run":
        if arguments.label not in {"run_1", "run_2"}:
            raise SystemExit("run requires --label run_1 or run_2")
        run_once(arguments.label)
    else:
        freeze()


if __name__ == "__main__":
    main()
