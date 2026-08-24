"""Freeze and verify the PI-selected CED-VAL-006 analytical inputs."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import struct

import soundfile as sf

HERE = Path(__file__).resolve().parent
ROOT = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/raw")
DATASET_MANIFEST = HERE / "input_authority_manifest.json"
AUTHORITY_ID = "PR-CEDVAL006-ANALYTICAL-INPUTS-001"
DATASET_AUTHORITY_ID = "PR-CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK-001"
DATASET_FINGERPRINT = "9d837f710fbf3292c80490d499bc96df0a8fe1140bc9139b65de8a553c4c2eca"
DATASET_COMMIT = "0ac756e1abef8e1c25fe4cc501db008e064210b1"
SELECTIONS = (
    ("Drums", "TEMPORAL_REFERENCE", "Dums Overheads LCT 640 TS-Dual Output Mode.wav"),
    ("Double Bass", "ACCOMPANIMENT", "BASS - DI.wav"),
)


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def header_authority(path: Path) -> dict:
    with path.open("rb") as stream:
        if stream.read(4) != b"RIFF":
            raise RuntimeError(f"AUTHORITY_CONFLICT_NOT_RIFF: {path.name}")
        stream.seek(8)
        if stream.read(4) != b"WAVE":
            raise RuntimeError(f"AUTHORITY_CONFLICT_NOT_WAVE: {path.name}")
        while True:
            chunk_id = stream.read(4)
            size_bytes = stream.read(4)
            if not chunk_id or len(size_bytes) != 4:
                break
            size = struct.unpack("<I", size_bytes)[0]
            if chunk_id == b"fmt ":
                data = stream.read(size)
                format_code, channels, sample_rate = struct.unpack("<HHI", data[:8])
                bits = struct.unpack("<H", data[14:16])[0]
                return {"format_code": format_code, "channels": channels, "sample_rate_hz": sample_rate, "bits_per_sample": bits}
            stream.seek(size + (size & 1), 1)
    raise RuntimeError(f"AUTHORITY_CONFLICT_FMT_MISSING: {path.name}")


def verify_asset(filename: str, frozen: dict) -> dict:
    path = ROOT / filename
    if not path.is_file() or path.resolve() != (ROOT / frozen["relative_path"]).resolve():
        raise RuntimeError(f"AUTHORITY_CONFLICT_PATH: {filename}")
    observed_hash = checksum(path)
    if observed_hash != frozen["sha256"]:
        raise RuntimeError(f"AUTHORITY_CONFLICT_SHA256: {filename}")
    header = header_authority(path)
    info = sf.info(str(path))
    measured = {
        "container": "RIFF/WAVE",
        "codec": "LINEAR_PCM",
        "pcm_representation": "SIGNED_24_BIT_LITTLE_ENDIAN_INTEGER",
        "sample_rate_hz": info.samplerate,
        "channel_count": info.channels,
        "frame_count_per_channel": info.frames,
        "duration_seconds_exact": f"{info.frames}/{info.samplerate}",
        "duration_seconds_decimal": info.frames / info.samplerate,
        "sample_coordinate_scope": [0, info.frames - 1],
        "byte_size": path.stat().st_size,
    }
    expected = {
        "container": frozen["container"],
        "codec": frozen["codec"],
        "pcm_representation": frozen["pcm_representation"],
        "sample_rate_hz": frozen["sample_rate_hz"],
        "channel_count": frozen["channel_count"],
        "frame_count_per_channel": frozen["frame_count_per_channel"],
        "duration_seconds_exact": frozen["duration_seconds_exact"],
        "duration_seconds_decimal": frozen["duration_seconds_decimal"],
        "sample_coordinate_scope": frozen["sample_coordinate_scope"],
        "byte_size": frozen["byte_size"],
    }
    if measured != expected:
        raise RuntimeError(f"AUTHORITY_CONFLICT_TECHNICAL_PROPERTIES: {filename}")
    if header != {"format_code": 1, "channels": info.channels, "sample_rate_hz": info.samplerate, "bits_per_sample": 24}:
        raise RuntimeError(f"AUTHORITY_CONFLICT_PCM_HEADER: {filename}")
    return {
        "filename": filename,
        "original_relative_path": frozen["relative_path"],
        "absolute_path": str(path),
        "sha256": observed_hash,
        **measured,
        "asset_handling": "ORIGINAL_RAW_FILE_SELECTED_WITHOUT_DERIVATION_OR_PROCESSING",
        "bleed_handling": "PRESERVED_UNCHANGED_IF_PRESENT",
    }


def derive() -> dict:
    manifest = json.loads(DATASET_MANIFEST.read_text())
    if (manifest["authority_id"], manifest["dataset_fingerprint"]) != (DATASET_AUTHORITY_ID, DATASET_FINGERPRINT):
        raise RuntimeError("AUTHORITY_CONFLICT_DATASET_IDENTITY")
    by_path = {item["relative_path"]: item for item in manifest["scientifically_relevant_assets"]}
    selected = []
    for source, role, filename in SELECTIONS:
        if filename not in by_path:
            raise RuntimeError(f"AUTHORITY_CONFLICT_MANIFEST_PATH: {filename}")
        selected.append({
            "analytical_source": source,
            "analytical_role": role,
            "source_label": filename.removesuffix(".wav"),
            **verify_asset(filename, by_path[filename]),
        })
    scopes = {(item["sample_rate_hz"], item["frame_count_per_channel"], tuple(item["sample_coordinate_scope"])) for item in selected}
    if scopes != {(48000, 11912868, (0, 11912867))}:
        raise RuntimeError("AUTHORITY_CONFLICT_COMMON_DISTRIBUTED_SCOPE")
    record = {
        "schema": "JGA-REAL-AUDIO-ANALYTICAL-INPUT-AUTHORITY/v1",
        "authority_id": AUTHORITY_ID,
        "status": "FROZEN_ANALYTICAL_INPUT_AUTHORITY",
        "dataset_authority": {
            "id": DATASET_AUTHORITY_ID,
            "fingerprint": DATASET_FINGERPRINT,
            "authority_commit": DATASET_COMMIT,
        },
        "selection_authority": "PI_APPROVED_MINIMAL_DIRECT_RAW_SOURCE_SELECTION",
        "external_root": str(ROOT) + "/",
        "selected_inputs": selected,
        "verification": {
            "required_pass_count": 2,
            "method": "TWO_FRESH_PROCESS_READ_ONLY_SHA256_RIFF_HEADER_AND_LIBSNDFILE_TECHNICAL_VERIFICATION",
            "paths_match_frozen_dataset_manifest": True,
            "checksums_match_frozen_dataset_manifest": True,
            "technical_properties_match_frozen_dataset_manifest": True,
            "common_distributed_scope_verified": True,
            "result": "PASS",
        },
        "timeline_authority": {
            "status": "COMMON_DISTRIBUTED_FILE_SAMPLE_INDEX_SCOPE",
            "file_local_sample_zero": 0,
            "sample_rate_hz": 48000,
            "frame_count_per_channel": 11912868,
            "duration_seconds_exact": "11912868/48000",
            "sample_coordinate_scope": [0, 11912867],
            "common_session_time_sample_zero_origin": "UNESTABLISHED_NOT_EXPLICITLY_DOCUMENTED",
            "common_hardware_acquisition_clock": "UNESTABLISHED_NOT_EXPLICITLY_DOCUMENTED",
        },
        "preserved_dataset_authority": {
            "live_performance": "SUPPORTED_BY_PRIMARY_LEWITT_PROVIDER_DECLARATION_FOR_THE_LIVE_BAND_RECORDING",
            "raw_no_editing_no_tuning": "SUPPORTED_EXACTLY_TO_THE_EXTENT_DECLARED_BY_LEWITT",
            "common_acquisition_system": "UNESTABLISHED_WHERE_NOT_DOCUMENTED",
            "physical_onset_ground_truth": "NOT_ESTABLISHED",
            "calibration_applicability": "UNESTABLISHED",
            "overall_acquisition_authority": "ACQUISITION_AUTHORITY_PARTIAL",
        },
        "processing_firewall": {
            "derived_analytical_assets_created": False,
            "mixing": False, "trimming": False, "shifting": False, "alignment": False,
            "normalization": False, "resampling": False, "filtering": False, "gating": False,
            "denoising": False, "compression": False, "eq": False, "transient_processing": False,
            "source_separation": False, "quantization": False, "warping": False,
            "timing_correction": False,
        },
        "scientific_firewalls": {
            "jga_executed": False, "external_tracker_executed": False,
            "h02_used": False, "strength_accessed": False, "readme_or_external_bpm_used": False,
            "musical_interpretation_performed": False, "cedval005_compared": False,
            "production_code_changed": False, "raw_assets_changed": False,
            "historical_authorities_changed": False,
        },
        "maximum_authorized_claim": "The exact original unmodified Drum overhead and Bass DI files are provenance-bound analytical inputs for a future bounded CED-VAL-006 observational study on their equal distributed-file sample-index scope, without common-clock, session-origin, physical-onset, calibration, correspondence, or human-microtiming authority.",
    }
    record["analytical_input_fingerprint"] = sha256(canonical(record)).hexdigest()
    return record


def freeze(pass_one: Path, pass_two: Path) -> None:
    if pass_one.read_bytes() != pass_two.read_bytes():
        raise RuntimeError("AUTHORITY_CONFLICT_TWO_PASS_DISAGREEMENT")
    record = json.loads(pass_one.read_text())
    if record != derive():
        raise RuntimeError("AUTHORITY_CONFLICT_FREEZE_REPLAY")
    write_json(HERE / "analytical_input_authority.json", record)
    print(json.dumps({
        "status": "PASS",
        "authority_id": AUTHORITY_ID,
        "analytical_input_fingerprint": record["analytical_input_fingerprint"],
        "two_pass_verification": "PASS_BYTE_IDENTICAL_TWO_FRESH_PROCESS_EXECUTIONS",
    }, indent=2, sort_keys=True))


def verify() -> None:
    frozen = json.loads((HERE / "analytical_input_authority.json").read_text())
    if frozen != derive():
        raise RuntimeError("FROZEN_ANALYTICAL_INPUT_AUTHORITY_FAILURE")
    print(json.dumps({
        "status": "PASS",
        "authority_id": AUTHORITY_ID,
        "analytical_input_fingerprint": frozen["analytical_input_fingerprint"],
        "raw_assets_unchanged": True,
    }, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    derive_parser = subparsers.add_parser("derive")
    derive_parser.add_argument("output", type=Path)
    freeze_parser = subparsers.add_parser("freeze")
    freeze_parser.add_argument("pass_one", type=Path)
    freeze_parser.add_argument("pass_two", type=Path)
    subparsers.add_parser("verify")
    args = parser.parse_args()
    if args.command == "derive":
        write_json(args.output, derive())
    elif args.command == "freeze":
        freeze(args.pass_one, args.pass_two)
    else:
        verify()


if __name__ == "__main__":
    main()
