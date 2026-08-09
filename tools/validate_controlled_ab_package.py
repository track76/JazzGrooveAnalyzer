"""Validate a prepared controlled A/B experimental dataset package.

This is repository tooling, not JGA analysis logic. It verifies identities,
checksums, lossless-audio compatibility, and the declared event-removal
inventory before an SVP-001 execution may begin.
"""

from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
from pathlib import Path
import sys
import wave


PLACEHOLDER_PREFIX = "__REQUIRED_"
MANIFEST_NAME = "controlled_ab_manifest.json"


class PackageValidationError(ValueError):
    """Raised when a controlled A/B package is incomplete or inconsistent."""


def _sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PackageValidationError(f"Cannot read JSON: {path}") from error


def _find_placeholders(value: object, location: str = "root") -> list[str]:
    if isinstance(value, str):
        return [location] if value.startswith(PLACEHOLDER_PREFIX) else []
    if isinstance(value, list):
        return [
            item
            for index, member in enumerate(value)
            for item in _find_placeholders(member, f"{location}[{index}]")
        ]
    if isinstance(value, dict):
        return [
            item
            for key, member in value.items()
            for item in _find_placeholders(member, f"{location}.{key}")
        ]
    return []


def _required(mapping: dict[str, object], key: str, location: str) -> object:
    if key not in mapping:
        raise PackageValidationError(f"Missing {location}.{key}")
    return mapping[key]


def _asset(package_root: Path, data: dict[str, object], location: str) -> Path:
    relative = _required(data, "repository_path", location)
    expected = _required(data, "sha256", location)
    if not isinstance(relative, str) or not isinstance(expected, str):
        raise PackageValidationError(f"Invalid asset identity at {location}")
    path = package_root / relative
    if not path.is_file():
        raise PackageValidationError(f"Missing asset: {relative}")
    actual = _sha256(path)
    if actual != expected:
        raise PackageValidationError(
            f"Checksum mismatch for {relative}: expected {expected}, got {actual}"
        )
    return path


def _wav_identity(path: Path) -> tuple[int, int, int, int]:
    try:
        with wave.open(str(path), "rb") as stream:
            if stream.getcomptype() != "NONE":
                raise PackageValidationError(f"WAV is not PCM: {path}")
            return (
                stream.getframerate(),
                stream.getsampwidth() * 8,
                stream.getnchannels(),
                stream.getnframes(),
            )
    except (OSError, wave.Error) as error:
        raise PackageValidationError(f"Cannot read PCM WAV: {path}") from error


def _decimal(value: object, location: str) -> Decimal:
    if not isinstance(value, str):
        raise PackageValidationError(f"{location} must be a decimal string")
    try:
        return Decimal(value)
    except InvalidOperation as error:
        raise PackageValidationError(f"Invalid decimal at {location}") from error


def _validate_inventory(inventory: dict[str, object]) -> None:
    if inventory.get("declared_before_analysis") is not True:
        raise PackageValidationError(
            "Event removal must be declared before analysis"
        )
    if inventory.get("selected_independently_of_jga_output") is not True:
        raise PackageValidationError(
            "Event removal must be independent of JGA output"
        )
    entries = _required(inventory, "events", "inventory")
    if not isinstance(entries, list) or not entries:
        raise PackageValidationError("inventory.events must be non-empty")

    seen_a: set[str] = set()
    seen_b: set[str] = set()
    statuses: set[str] = set()
    for index, entry in enumerate(entries):
        location = f"inventory.events[{index}]"
        if not isinstance(entry, dict):
            raise PackageValidationError(f"{location} must be an object")
        event_a = _required(entry, "condition_a_event_id", location)
        status = _required(entry, "status", location)
        if not isinstance(event_a, str) or not event_a:
            raise PackageValidationError(f"Invalid {location}.condition_a_event_id")
        if event_a in seen_a:
            raise PackageValidationError(f"Duplicate Condition A event: {event_a}")
        seen_a.add(event_a)
        if status not in {"retained", "removed"}:
            raise PackageValidationError(f"Invalid {location}.status")
        statuses.add(status)

        onset_a = _decimal(
            entry.get("condition_a_onset_seconds"),
            f"{location}.condition_a_onset_seconds",
        )
        duration_a = _decimal(
            entry.get("condition_a_duration_seconds"),
            f"{location}.condition_a_duration_seconds",
        )
        if onset_a < 0 or duration_a <= 0:
            raise PackageValidationError(f"Invalid Condition A timing at {location}")

        event_b = entry.get("condition_b_event_id")
        onset_b = entry.get("condition_b_onset_seconds")
        duration_b = entry.get("condition_b_duration_seconds")
        if status == "removed":
            if any(value is not None for value in (event_b, onset_b, duration_b)):
                raise PackageValidationError(
                    f"Removed event must have no Condition B representation: {event_a}"
                )
            continue

        if not isinstance(event_b, str) or not event_b:
            raise PackageValidationError(f"Retained event lacks identity at {location}")
        if event_b in seen_b:
            raise PackageValidationError(f"Duplicate Condition B event: {event_b}")
        seen_b.add(event_b)
        if onset_a != _decimal(onset_b, f"{location}.condition_b_onset_seconds"):
            raise PackageValidationError(f"Retained-event onset changed: {event_a}")
        if duration_a != _decimal(
            duration_b, f"{location}.condition_b_duration_seconds"
        ):
            raise PackageValidationError(f"Retained-event duration changed: {event_a}")

    if statuses != {"retained", "removed"}:
        raise PackageValidationError(
            "Inventory must contain at least one retained and one removed event"
        )


def validate_package(package_root: Path) -> dict[str, object]:
    """Validate the prepared package and return measured evidence."""
    manifest_path = package_root / MANIFEST_NAME
    manifest = _load_json(manifest_path)
    if not isinstance(manifest, dict):
        raise PackageValidationError("Manifest must be a JSON object")

    placeholders = _find_placeholders(manifest)
    if placeholders:
        raise PackageValidationError(
            "Unresolved manifest placeholders: " + ", ".join(placeholders)
        )

    for key in (
        "controlled_dataset_id",
        "dataset_generation_record_id",
        "provenance_revision_id",
        "condition_a",
        "condition_b",
        "event_removal_inventory",
        "dataset_generation_record",
    ):
        _required(manifest, key, "manifest")

    conditions = []
    wav_measurements: dict[str, tuple[int, int, int, int]] = {}
    for name in ("condition_a", "condition_b"):
        condition = manifest[name]
        if not isinstance(condition, dict):
            raise PackageValidationError(f"manifest.{name} must be an object")
        for asset_name in (
            "authoritative_musicxml",
            "canonical_wav",
            "repeated_render_wav",
            "catalogue_mp3",
            "ground_truth_definition",
        ):
            asset_data = _required(condition, asset_name, f"manifest.{name}")
            if not isinstance(asset_data, dict):
                raise PackageValidationError(
                    f"manifest.{name}.{asset_name} must be an object"
                )
            path = _asset(package_root, asset_data, f"manifest.{name}.{asset_name}")
            if asset_name.endswith("wav"):
                wav_measurements[f"{name}.{asset_name}"] = _wav_identity(path)
            if asset_name == "ground_truth_definition":
                ground_truth = _load_json(path)
                if not isinstance(ground_truth, dict):
                    raise PackageValidationError(
                        f"Ground Truth definition must be an object: {path}"
                    )
                unresolved = _find_placeholders(
                    ground_truth, f"manifest.{name}.ground_truth_definition"
                )
                if unresolved:
                    raise PackageValidationError(
                        "Unresolved Ground Truth placeholders: "
                        + ", ".join(unresolved)
                    )
                if ground_truth.get("schema_version") != "1":
                    raise PackageValidationError(
                        f"{name} Ground Truth must use existing schema 1"
                    )
                if ground_truth.get("ground_truth_id") != condition.get(
                    "ground_truth_id"
                ):
                    raise PackageValidationError(
                        f"{name} Ground Truth identity does not bind"
                    )
                if ground_truth.get("validation_item_id") != condition.get(
                    "validation_item_id"
                ):
                    raise PackageValidationError(
                        f"{name} Validation Item identity does not bind"
                    )
        conditions.append(condition)

    inventory_data = manifest["event_removal_inventory"]
    dgr_data = manifest["dataset_generation_record"]
    if not isinstance(inventory_data, dict) or not isinstance(dgr_data, dict):
        raise PackageValidationError("Manifest provenance assets must be objects")
    inventory_path = _asset(package_root, inventory_data, "manifest.event_removal_inventory")
    dgr_path = _asset(
        package_root, dgr_data, "manifest.dataset_generation_record"
    )
    if PLACEHOLDER_PREFIX in dgr_path.read_text(encoding="utf-8"):
        raise PackageValidationError(
            "Dataset Generation Record contains unresolved placeholders"
        )
    inventory = _load_json(inventory_path)
    if not isinstance(inventory, dict):
        raise PackageValidationError("Event-removal inventory must be an object")
    inventory_placeholders = _find_placeholders(inventory, "inventory")
    if inventory_placeholders:
        raise PackageValidationError(
            "Unresolved inventory placeholders: " + ", ".join(inventory_placeholders)
        )
    _validate_inventory(inventory)
    if inventory.get("condition_a_id") != conditions[0].get("condition_id"):
        raise PackageValidationError("Inventory Condition A identity does not bind")
    if inventory.get("condition_b_id") != conditions[1].get("condition_id"):
        raise PackageValidationError("Inventory Condition B identity does not bind")
    if conditions[0].get("condition_id") == conditions[1].get("condition_id"):
        raise PackageValidationError("Condition identities must be distinct")

    unique_wav_identities = set(wav_measurements.values())
    if len(unique_wav_identities) != 1:
        raise PackageValidationError(
            "All canonical and repeated WAV assets must have identical "
            "sample rate, bit depth, channels, and sample count"
        )

    sample_rate, bit_depth, channels, sample_count = next(iter(unique_wav_identities))
    declared = manifest.get("controlled_audio_format")
    expected = {
        "sample_rate_hz": sample_rate,
        "bit_depth": bit_depth,
        "channel_count": channels,
        "sample_count_per_channel": sample_count,
    }
    if declared != expected:
        raise PackageValidationError(
            f"Declared controlled_audio_format does not match WAV evidence: {expected}"
        )

    return {
        "controlled_dataset_id": manifest["controlled_dataset_id"],
        "conditions": [condition["condition_id"] for condition in conditions],
        "wav_measurements": expected,
        "inventory_event_count": len(inventory["events"]),
        "package_manifest_sha256": _sha256(manifest_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package_root", type=Path)
    args = parser.parse_args()
    try:
        result = validate_package(args.package_root)
    except PackageValidationError as error:
        print(f"INVALID: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
