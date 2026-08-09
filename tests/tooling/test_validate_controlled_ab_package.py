from hashlib import sha256
import json
from pathlib import Path
import wave

import pytest

from tools.validate_controlled_ab_package import (
    PackageValidationError,
    validate_package,
)


def _write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def _write_wav(path: Path, *, frames: int = 8) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as stream:
        stream.setnchannels(1)
        stream.setsampwidth(2)
        stream.setframerate(8000)
        stream.writeframes(b"\x00\x00" * frames)


def _asset(root: Path, relative: str) -> dict[str, str]:
    path = root / relative
    return {
        "repository_path": relative,
        "sha256": sha256(path.read_bytes()).hexdigest(),
    }


def _package(tmp_path: Path) -> Path:
    root = tmp_path / "package"
    for condition in ("a", "b"):
        _write(root / f"symbolic/condition_{condition}.musicxml", b"<score-partwise/>")
        ground_truth = {
            "ground_truth_id": f"GT-{condition.upper()}",
            "validation_item_id": f"VAL-{condition.upper()}",
            "schema_version": "1",
        }
        _write(
            root / f"ground_truth/condition_{condition}.ground_truth.json",
            json.dumps(ground_truth).encode(),
        )
        _write(root / f"audio/condition_{condition}.mp3", b"catalogue derivative")
        _write_wav(root / f"audio/condition_{condition}.wav")
        _write_wav(root / f"audio/condition_{condition}_repeat.wav")
    _write(root / "provenance/dataset_generation_record.md", b"declared procedure")

    inventory = {
        "inventory_id": "INVENTORY-1",
        "condition_a_id": "A",
        "condition_b_id": "B",
        "declared_before_analysis": True,
        "selected_independently_of_jga_output": True,
        "events": [
            {
                "condition_a_event_id": "event-1",
                "condition_a_onset_seconds": "0.0",
                "condition_a_duration_seconds": "0.5",
                "status": "retained",
                "condition_b_event_id": "event-1",
                "condition_b_onset_seconds": "0.0",
                "condition_b_duration_seconds": "0.5",
            },
            {
                "condition_a_event_id": "event-2",
                "condition_a_onset_seconds": "0.5",
                "condition_a_duration_seconds": "0.5",
                "status": "removed",
                "condition_b_event_id": None,
                "condition_b_onset_seconds": None,
                "condition_b_duration_seconds": None,
            },
        ],
    }
    inventory_path = root / "provenance/event_removal_inventory.json"
    _write(inventory_path, json.dumps(inventory).encode())

    def condition(name: str) -> dict[str, object]:
        return {
            "condition_id": name.upper(),
            "validation_item_id": f"VAL-{name.upper()}",
            "ground_truth_id": f"GT-{name.upper()}",
            "authoritative_musicxml": _asset(root, f"symbolic/condition_{name}.musicxml"),
            "ground_truth_definition": _asset(
                root, f"ground_truth/condition_{name}.ground_truth.json"
            ),
            "canonical_wav": _asset(root, f"audio/condition_{name}.wav"),
            "repeated_render_wav": _asset(
                root, f"audio/condition_{name}_repeat.wav"
            ),
            "catalogue_mp3": _asset(root, f"audio/condition_{name}.mp3"),
            "licensing_status": "not_specified",
        }

    manifest = {
        "controlled_dataset_id": "CED-TEST",
        "dataset_generation_record_id": "DGR-TEST",
        "provenance_revision_id": "PR-TEST",
        "relationship": "condition_b_is_declared_event_removal_from_condition_a",
        "knowledge_classification": "Declared Experimental Procedure",
        "controlled_audio_format": {
            "sample_rate_hz": 8000,
            "bit_depth": 16,
            "channel_count": 1,
            "sample_count_per_channel": 8,
        },
        "condition_a": condition("a"),
        "condition_b": condition("b"),
        "event_removal_inventory": _asset(
            root, "provenance/event_removal_inventory.json"
        ),
        "dataset_generation_record": _asset(
            root, "provenance/dataset_generation_record.md"
        ),
    }
    _write(
        root / "controlled_ab_manifest.json",
        json.dumps(manifest).encode(),
    )
    return root


def test_validates_complete_existing_structure_package(tmp_path: Path):
    root = _package(tmp_path)

    result = validate_package(root)

    assert result["controlled_dataset_id"] == "CED-TEST"
    assert result["conditions"] == ["A", "B"]
    assert result["inventory_event_count"] == 2
    assert result["wav_measurements"] == {
        "sample_rate_hz": 8000,
        "bit_depth": 16,
        "channel_count": 1,
        "sample_count_per_channel": 8,
    }


def test_rejects_unresolved_scientific_placeholders(tmp_path: Path):
    root = _package(tmp_path)
    manifest_path = root / "controlled_ab_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["controlled_dataset_id"] = "__REQUIRED_CONTROLLED_DATASET_ID__"
    manifest_path.write_text(json.dumps(manifest))

    with pytest.raises(PackageValidationError, match="Unresolved manifest"):
        validate_package(root)


def test_rejects_changed_retained_event_timing(tmp_path: Path):
    root = _package(tmp_path)
    inventory_path = root / "provenance/event_removal_inventory.json"
    inventory = json.loads(inventory_path.read_text())
    inventory["events"][0]["condition_b_onset_seconds"] = "0.1"
    inventory_path.write_text(json.dumps(inventory))
    manifest_path = root / "controlled_ab_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["event_removal_inventory"]["sha256"] = sha256(
        inventory_path.read_bytes()
    ).hexdigest()
    manifest_path.write_text(json.dumps(manifest))

    with pytest.raises(PackageValidationError, match="onset changed"):
        validate_package(root)


def test_rejects_different_audio_measurement_conditions(tmp_path: Path):
    root = _package(tmp_path)
    wav_path = root / "audio/condition_b_repeat.wav"
    _write_wav(wav_path, frames=9)
    manifest_path = root / "controlled_ab_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["condition_b"]["repeated_render_wav"]["sha256"] = sha256(
        wav_path.read_bytes()
    ).hexdigest()
    manifest_path.write_text(json.dumps(manifest))

    with pytest.raises(PackageValidationError, match="identical sample rate"):
        validate_package(root)
