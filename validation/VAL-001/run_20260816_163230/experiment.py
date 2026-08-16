"""Run and freeze the blind Voice-only SOME proof of concept."""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import sys

import librosa
import numpy as np
import torch
import yaml


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


def array_scientific_sha256(value: np.ndarray) -> str:
    value = np.ascontiguousarray(value)
    digest = sha256()
    digest.update(str(value.dtype).encode())
    digest.update(canonical_bytes(list(value.shape)))
    digest.update(value.tobytes(order="C"))
    return digest.hexdigest()


def load_manifest() -> dict[str, object]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["status"] != "PREREGISTERED":
        raise RuntimeError("Manifest is not preregistered.")
    return manifest


def verify_inputs(manifest: dict[str, object]) -> tuple[Path, Path, Path]:
    audio = ROOT / manifest["input"]["path"]
    source = Path(manifest["environment"]["external_source"])
    checkpoint = Path(manifest["environment"]["external_checkpoint"])
    if file_sha256(audio) != manifest["input"]["sha256"]:
        raise RuntimeError("Voice input checksum mismatch.")
    if file_sha256(checkpoint) != manifest["model_freeze"]["extracted_files"]["0119_continuous256_5spk/model_ckpt_steps_100000_simplified.ckpt"]["sha256"]:
        raise RuntimeError("SOME checkpoint checksum mismatch.")
    config = checkpoint.with_name("config.yaml")
    if file_sha256(config) != manifest["model_freeze"]["extracted_files"]["0119_continuous256_5spk/config.yaml"]["sha256"]:
        raise RuntimeError("SOME config checksum mismatch.")
    return audio, source, checkpoint


def environment_record() -> dict[str, object]:
    packages = {}
    unreadable = 0
    for distribution in importlib.metadata.distributions():
        try:
            name = distribution.metadata.get("Name")
            if name:
                packages[name] = distribution.version
        except (OSError, UnicodeError):
            unreadable += 1
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "executable": sys.executable,
        "torch": torch.__version__,
        "torch_cuda_available": torch.cuda.is_available(),
        "torch_mps_available_but_unused": torch.backends.mps.is_available(),
        "effective_device": "cpu",
        "packages": dict(sorted(packages.items(), key=lambda item: item[0].lower())),
        "ignored_unreadable_metadata_entries": unreadable,
    }


def save_array(path: Path, value: np.ndarray) -> dict[str, object]:
    value = np.asarray(value)
    np.save(path, value, allow_pickle=False)
    return {
        "dtype": str(value.dtype),
        "shape": list(value.shape),
        "scientific_sha256": array_scientific_sha256(value),
        "file_sha256": file_sha256(path),
    }


def derived_events(segments: list[dict[str, np.ndarray]], offsets: list[float]) -> list[dict[str, object]]:
    events = []
    for chunk_index, (segment, offset) in enumerate(zip(segments, offsets)):
        cursor = float(offset)
        for segment_index, (pitch, duration, rest) in enumerate(zip(
            segment["note_midi"], segment["note_dur"], segment["note_rest"]
        )):
            onset = cursor
            cursor += float(duration)
            if not bool(rest) and cursor > onset:
                events.append({
                    "event_id": f"chunk-{chunk_index:03d}-segment-{segment_index:05d}",
                    "chunk_index": chunk_index,
                    "segment_index": segment_index,
                    "onset_seconds": onset,
                    "offset_seconds": cursor,
                    "duration_seconds": float(duration),
                    "pitch_midi": float(pitch),
                    "epistemic_status": "INFERRED",
                })
    return events


def run_once(label: str) -> None:
    manifest = load_manifest()
    audio_path, source_path, checkpoint = verify_inputs(manifest)
    sys.path.insert(0, str(source_path))
    from inference.me_infer import MIDIExtractionInference
    from utils.infer_utils import build_midi_file
    from utils.slicer2 import Slicer

    output = Path(manifest["environment"]["external_run_root"]) / label
    output.mkdir(parents=True, exist_ok=False)
    config = yaml.safe_load(checkpoint.with_name("config.yaml").read_text(encoding="utf-8"))
    inference = MIDIExtractionInference(config=config, model_path=checkpoint, device="cpu")
    if str(inference.device) != "cpu":
        raise RuntimeError("Inference device is not CPU.")
    waveform, native_sample_rate = librosa.load(audio_path, sr=config["audio_sample_rate"], mono=True)
    slicer = Slicer(sr=config["audio_sample_rate"], max_sil_kept=1000)
    chunks = slicer.slice(waveform)

    segments = []
    arrays = []
    offsets = []
    for chunk_index, chunk in enumerate(chunks):
        sample = inference.preprocess(chunk["waveform"])
        raw = inference.forward_model(sample)
        segment = inference.postprocess({name: value.clone() for name, value in raw.items()})
        offsets.append(float(chunk["offset"]))
        segments.append(segment)
        chunk_arrays = {}
        for name, tensor in sorted(raw.items()):
            value = tensor.detach().cpu().numpy()
            chunk_arrays[name] = save_array(output / f"chunk_{chunk_index:03d}_{name}.npy", value)
        for name, value in sorted(segment.items()):
            chunk_arrays[f"decoded_{name}"] = save_array(output / f"chunk_{chunk_index:03d}_decoded_{name}.npy", value)
        arrays.append({"chunk_index": chunk_index, "offset_seconds": float(chunk["offset"]), "arrays": chunk_arrays})

    events = derived_events(segments, offsets)
    midi = build_midi_file(offsets, segments)
    midi_path = output / "inference.mid"
    midi.save(midi_path)
    write_json(output / "inferred_events.json", events)
    array_scientific = [
        (entry["chunk_index"], name, record["scientific_sha256"])
        for entry in arrays for name, record in sorted(entry["arrays"].items())
    ]
    scientific = {
        "events": events,
        "array_scientific_sha256": array_scientific,
        "chunk_offsets_seconds": offsets,
    }
    record = {
        "experiment_id": manifest["experiment_id"],
        "run_label": label,
        "epistemic_status": "INFERRED",
        "ground_truth_loaded": False,
        "model_input": {"voice_wav_sha256": file_sha256(audio_path)},
        "official_config": config,
        "audio": {
            "sample_rate_hz": config["audio_sample_rate"],
            "librosa_returned_sample_rate_hz": native_sample_rate,
            "sample_count": int(waveform.shape[0]),
            "chunk_count": len(chunks),
            "chunk_offsets_seconds": offsets,
        },
        "arrays": arrays,
        "decoded_event_count": len(events),
        "events": events,
        "all_events_well_formed": all(
            math.isfinite(event["onset_seconds"])
            and math.isfinite(event["offset_seconds"])
            and event["onset_seconds"] < event["offset_seconds"]
            for event in events
        ),
        "midi_file_sha256": file_sha256(midi_path),
        "environment": environment_record(),
        "scientific_fingerprint": sha256(canonical_bytes(scientific)).hexdigest(),
    }
    write_json(output / "blind_run.json", record)
    print(json.dumps({
        "label": label,
        "event_count": len(events),
        "scientific_fingerprint": record["scientific_fingerprint"],
        "blind_run_sha256": file_sha256(output / "blind_run.json"),
    }, sort_keys=True))


def freeze() -> None:
    manifest = load_manifest()
    external = Path(manifest["environment"]["external_run_root"])
    records = [
        json.loads((external / label / "blind_run.json").read_text(encoding="utf-8"))
        for label in ("run_1", "run_2")
    ]
    fingerprints = [record["scientific_fingerprint"] for record in records]
    all_files = []
    for label in ("run_1", "run_2"):
        for path in sorted((external / label).iterdir()):
            all_files.append({
                "run": label,
                "name": path.name,
                "sha256": file_sha256(path),
                "bytes": path.stat().st_size,
            })
    names = sorted({item["name"] for item in all_files})
    byte_identical = all(
        file_sha256(external / "run_1" / name) == file_sha256(external / "run_2" / name)
        for name in names
    )
    freeze_record = {
        "experiment_id": manifest["experiment_id"],
        "blind_status": "FROZEN",
        "ground_truth_loaded": False,
        "run_scientific_fingerprints": fingerprints,
        "scientifically_identical": fingerprints[0] == fingerprints[1],
        "byte_identical_all_files": byte_identical,
        "decoded_event_counts": [record["decoded_event_count"] for record in records],
        "files": all_files,
        "frozen_blind_result": records[0],
    }
    freeze_record["blind_freeze_scientific_sha256"] = sha256(canonical_bytes(freeze_record)).hexdigest()
    write_json(external / "blind_freeze.json", freeze_record)
    print(json.dumps({
        "byte_identical": byte_identical,
        "scientifically_identical": freeze_record["scientifically_identical"],
        "counts": freeze_record["decoded_event_counts"],
        "blind_freeze_scientific_sha256": freeze_record["blind_freeze_scientific_sha256"],
        "blind_freeze_file_sha256": file_sha256(external / "blind_freeze.json"),
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
