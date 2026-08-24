"""Build and verify the read-only CED-VAL-006 raw input authority."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import struct

import soundfile as sf

ROOT = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/raw")
HERE = Path(__file__).resolve().parent
AUTHORITY_ID = "PR-CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK-001"
EXPECTED_SCIENTIFIC_ASSETS = {
    "BASS - DI.wav", "BASS DTP 640 REX Dynamic Capsule.wav", "Cosmix Video.mov",
    "Dums Overheads LCT 640 TS-Dual Output Mode.wav", "GUIT MTP 440.wav",
    "Kick DTP 640 REX Condenser Capsule.wav", "Kick DTP 640 REX Dynamic Capsule.wav",
    "LEWITT_exploitation-rights.pdf", "Rhodes MTP 440.wav", "ROOM LEFT LCT 640 TS.wav",
    "Room Mono LCT 550.wav", "Room Mono MTP 550.wav", "ROOM RIGHT LCT 640 TS.wav",
    "Snare MTP 440.wav", "VOX  LCT 240 PRO.wav", "VOX LCT 440 PURE.wav",
    "VOX LCT 640 TS.wav",
}


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


def wav_header(path: Path) -> dict:
    with path.open("rb") as stream:
        if stream.read(4) != b"RIFF":
            raise RuntimeError(f"NOT_RIFF: {path.name}")
        stream.seek(8)
        if stream.read(4) != b"WAVE":
            raise RuntimeError(f"NOT_WAVE: {path.name}")
        while True:
            chunk_id = stream.read(4)
            if not chunk_id:
                break
            chunk_size_data = stream.read(4)
            if len(chunk_size_data) != 4:
                break
            size = struct.unpack("<I", chunk_size_data)[0]
            if chunk_id == b"fmt ":
                data = stream.read(size)
                audio_format, channels, sample_rate = struct.unpack("<HHI", data[:8])
                bits = struct.unpack("<H", data[14:16])[0]
                return {
                    "riff_container": "RIFF/WAVE",
                    "format_code": audio_format,
                    "header_channels": channels,
                    "header_sample_rate_hz": sample_rate,
                    "header_bits_per_sample": bits,
                }
            stream.seek(size + (size & 1), 1)
    raise RuntimeError(f"WAV_FMT_MISSING: {path.name}")


def first_nonzero(path: Path) -> int | None:
    with sf.SoundFile(str(path)) as stream:
        position = 0
        while True:
            block = stream.read(65536, dtype="int32", always_2d=True)
            if len(block) == 0:
                return None
            indices = (block != 0).any(axis=1).nonzero()[0]
            if len(indices):
                return position + int(indices[0])
            position += len(block)


def walk_atoms(data: bytes, start: int = 0, end: int | None = None):
    end = len(data) if end is None else end
    position = start
    containers = {b"moov", b"trak", b"mdia", b"minf", b"stbl", b"edts", b"dinf", b"udta", b"meta"}
    while position + 8 <= end:
        size = struct.unpack(">I", data[position:position + 4])[0]
        atom_type = data[position + 4:position + 8]
        header = 8
        if size == 1:
            size = struct.unpack(">Q", data[position + 8:position + 16])[0]
            header = 16
        elif size == 0:
            size = end - position
        if size < header or position + size > end:
            break
        yield position, size, atom_type, header
        child_start = position + header + (4 if atom_type == b"meta" else 0)
        if atom_type in containers:
            yield from walk_atoms(data, child_start, position + size)
        position += size


def mov_metadata(path: Path) -> dict:
    data = path.read_bytes()
    movie = {}
    tracks = []
    for position, size, atom_type, header in walk_atoms(data):
        payload = position + header
        if atom_type == b"mvhd":
            version = data[payload]
            offset = payload + 4
            if version == 0:
                timescale = struct.unpack(">I", data[offset + 8:offset + 12])[0]
                duration = struct.unpack(">I", data[offset + 12:offset + 16])[0]
            else:
                timescale = struct.unpack(">I", data[offset + 16:offset + 20])[0]
                duration = struct.unpack(">Q", data[offset + 20:offset + 28])[0]
            movie = {"timescale": timescale, "duration_units": duration, "duration_seconds": duration / timescale}
    for outer_position, outer_size, outer_type, outer_header in walk_atoms(data):
        if outer_type != b"trak":
            continue
        timescale = duration = width = height = None
        codecs = []
        for position, size, atom_type, header in walk_atoms(data, outer_position + outer_header, outer_position + outer_size):
            payload = position + header
            if atom_type == b"mdhd":
                version = data[payload]
                offset = payload + 4
                if version == 0:
                    timescale = struct.unpack(">I", data[offset + 8:offset + 12])[0]
                    duration = struct.unpack(">I", data[offset + 12:offset + 16])[0]
                else:
                    timescale = struct.unpack(">I", data[offset + 16:offset + 20])[0]
                    duration = struct.unpack(">Q", data[offset + 20:offset + 28])[0]
            elif atom_type == b"tkhd":
                width = struct.unpack(">I", data[position + size - 8:position + size - 4])[0] / 65536
                height = struct.unpack(">I", data[position + size - 4:position + size])[0] / 65536
            elif atom_type == b"stsd":
                count = struct.unpack(">I", data[payload + 4:payload + 8])[0]
                entry = payload + 8
                for _ in range(count):
                    entry_size = struct.unpack(">I", data[entry:entry + 4])[0]
                    codecs.append(data[entry + 4:entry + 8].decode("latin1"))
                    entry += entry_size
        tracks.append({
            "timescale": timescale,
            "duration_units": duration,
            "duration_seconds": None if not timescale else duration / timescale,
            "display_width": width,
            "display_height": height,
            "sample_entry_codecs": codecs,
        })
    return {"container": "Apple QuickTime MOV", "movie_header": movie, "tracks": tracks}


def build_asset(path: Path) -> dict:
    relative = path.relative_to(ROOT).as_posix()
    record = {
        "filename": path.name,
        "relative_path": relative,
        "file_type": path.suffix.lower().lstrip(".").upper(),
        "byte_size": path.stat().st_size,
        "sha256": checksum(path),
    }
    if path.suffix.lower() == ".wav":
        info = sf.info(str(path))
        header = wav_header(path)
        if header["format_code"] != 1 or header["header_bits_per_sample"] != 24:
            raise RuntimeError(f"UNEXPECTED_PCM_AUTHORITY: {path.name}")
        if (header["header_channels"], header["header_sample_rate_hz"]) != (info.channels, info.samplerate):
            raise RuntimeError(f"WAV_HEADER_CONFLICT: {path.name}")
        record.update({
            "container": "RIFF/WAVE",
            "codec": "LINEAR_PCM",
            "pcm_representation": "SIGNED_24_BIT_LITTLE_ENDIAN_INTEGER",
            "sample_rate_hz": info.samplerate,
            "channel_count": info.channels,
            "frame_count_per_channel": info.frames,
            "duration_seconds_exact": f"{info.frames}/{info.samplerate}",
            "duration_seconds_decimal": info.frames / info.samplerate,
            "sample_coordinate_scope": [0, info.frames - 1],
            "first_nonzero_frame_scope_diagnostic": first_nonzero(path),
            "first_nonzero_interpretation": "FILE_SCOPE_DIAGNOSTIC_ONLY_NOT_MUSICAL_OR_PHYSICAL_ONSET",
        })
    elif path.suffix.lower() == ".mov":
        record["technical_metadata"] = mov_metadata(path)
        record["scientific_role"] = "SUPPORTING_PROVENANCE_ONLY_NO_TIMING_ANALYSIS_OR_GROUND_TRUTH"
    elif path.suffix.lower() == ".pdf":
        record.update({
            "container": "PDF-1.3",
            "page_count": 1,
            "scientific_role": "SUPPLIED_RIGHTS_DOCUMENT",
        })
    return record


def derive() -> dict:
    if not ROOT.is_dir():
        raise RuntimeError("DATASET_ROOT_NOT_FOUND")
    files = sorted((path for path in ROOT.rglob("*") if path.is_file()), key=lambda p: p.relative_to(ROOT).as_posix().encode())
    scientific_paths = [path for path in files if not path.name.startswith("._")]
    sidecar_paths = [path for path in files if path.name.startswith("._")]
    if {path.relative_to(ROOT).as_posix() for path in scientific_paths} != EXPECTED_SCIENTIFIC_ASSETS:
        raise RuntimeError("SCIENTIFIC_ASSET_POPULATION_CONFLICT")
    assets = [build_asset(path) for path in scientific_paths]
    sidecars = [{
        "filename": path.name,
        "relative_path": path.relative_to(ROOT).as_posix(),
        "file_type": "APPLEDOUBLE_SIDECAR",
        "byte_size": path.stat().st_size,
        "sha256": checksum(path),
        "scientific_authority": False,
    } for path in sidecar_paths]
    manifest_basis = {
        "schema": "JGA-REAL-LIVE-RAW-MULTITRACK-ASSET-MANIFEST/v1",
        "dataset_id": "CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK",
        "external_root": str(ROOT),
        "directory_structure": {"root": ".", "layout": "FLAT", "subdirectories": []},
        "scientifically_relevant_assets": assets,
        "filesystem_metadata_sidecars": sidecars,
    }
    dataset_fingerprint = sha256(canonical(manifest_basis)).hexdigest()
    return {
        **manifest_basis,
        "authority_id": AUTHORITY_ID,
        "status": "FROZEN_CANDIDATE_REAL_LIVE_MULTITRACK_AUTHORITY",
        "scientifically_relevant_asset_count": len(assets),
        "wav_asset_count": sum(item["file_type"] == "WAV" for item in assets),
        "appledouble_sidecar_count": len(sidecars),
        "dataset_fingerprint": dataset_fingerprint,
        "provenance": {
            "provider": "LEWITT GmbH / LEWITT Content Team",
            "official_page_url": "https://www.lewitt-audio.com/blog/mix-it-baby",
            "official_page_retrieval_date": "2026-08-24",
            "provider_claims": [
                "LEWITT describes a live recording session at COSMIX Studios in Vienna.",
                "LEWITT describes the downloadable material as a live recording of the band, including drums and upright/double bass.",
                "LEWITT states that no editing and no tuning was applied to these tracks and calls them the RAW tracks.",
                "LEWITT documents the drum microphone configuration on the page.",
                "LEWITT states that double bass used the dynamic capsule of a DTP 640 REX and a DI.",
                "LEWITT states that a performance video is supplied and shows microphone placement at its beginning.",
            ],
            "provider_claim_limit": "Claims are preserved as provider declarations and do not establish undocumented acquisition-clock, origin, export, physical-onset, detector, correspondence, isolation, or human-microtiming authority.",
        },
        "rights_authority": {
            "relative_path": "LEWITT_exploitation-rights.pdf",
            "sha256": next(item["sha256"] for item in assets if item["relative_path"] == "LEWITT_exploitation-rights.pdf"),
            "supported_summary": "Publication and public releases require naming the original artist and song. Copyright and owner rights are reserved. Commercial exploitation is not allowed, and the document states that infringement will be prosecuted by the artist.",
            "interpretation_limit": "No permission or restriction beyond the supplied one-page document is inferred.",
        },
        "source_population": {
            "Drums candidate observation channels": [
                "Dums Overheads LCT 640 TS-Dual Output Mode.wav",
                "Kick DTP 640 REX Condenser Capsule.wav",
                "Kick DTP 640 REX Dynamic Capsule.wav",
                "Snare MTP 440.wav",
            ],
            "Double Bass candidate observation channels": [
                "BASS - DI.wav", "BASS DTP 640 REX Dynamic Capsule.wav",
            ],
            "Guitar": ["GUIT MTP 440.wav"],
            "Rhodes": ["Rhodes MTP 440.wav"],
            "Room": [
                "ROOM LEFT LCT 640 TS.wav", "Room Mono LCT 550.wav",
                "Room Mono MTP 550.wav", "ROOM RIGHT LCT 640 TS.wav",
            ],
            "Vocal takes": ["VOX  LCT 240 PRO.wav", "VOX LCT 440 PURE.wav", "VOX LCT 640 TS.wav"],
        },
        "technical_scope": {
            "all_wav_readable": True,
            "common_sample_rate_hz": 48000,
            "common_pcm_representation": "SIGNED_24_BIT_LITTLE_ENDIAN_INTEGER",
            "channel_counts_present": [1, 2],
            "frame_scope_groups": {
                "11912868_frames_248.184750_seconds": 14,
                "11869358_frames_247.27829166666666_seconds": 1,
            },
            "full_cross_file_frame_scope_equality": False,
            "candidate_drums_and_double_bass_frame_scope_equality": True,
            "first_nonzero_diagnostics_are_not_onsets": True,
        },
        "acquisition_authority_audit": {
            "applied_protocol": "PR-JGA-REAL-AUDIO-ACQUISITION-AUTHORITY-01",
            "overall_classification": "ACQUISITION_AUTHORITY_PARTIAL",
            "live_same_performance": "SUPPORTED_BY_PRIMARY_PROVIDER_DECLARATION_FOR_THE_LIVE_BAND_RECORDING",
            "common_acquisition_system": "UNESTABLISHED_NOT_EXPLICITLY_DOCUMENTED_AT_REQUIRED_SYSTEM_ROUTING_LEVEL",
            "shared_hardware_clock": "UNESTABLISHED_NOT_EXPLICITLY_DOCUMENTED",
            "simultaneous_capture": "SUPPORTED_BY_PROVIDER_LIVE_BAND_RECORDING_DESCRIPTION_BUT_TECHNICAL_CAPTURE_RECORD_NOT_SUPPLIED",
            "common_timeline_file_origin": "UNESTABLISHED_NOT_EXPLICITLY_DOCUMENTED",
            "timing_edit_history": "PARTIAL_PROVIDER_STATES_NO_EDITING_AND_NO_TUNING_BUT_EXHAUSTIVE_TIMING_PROCESS_AND_EXPORT_HISTORY_NOT_DOCUMENTED",
            "export_authority": "UNESTABLISHED_FILES_FOR_ALL_DAWS_IDENTIFIED_BUT_COMMON_RANGE_ORIGIN_AND_EXPORT_CONFIGURATION_NOT_DOCUMENTED",
            "source_identity": "SUPPORTED_BY_EXACT_FILENAMES_AND_PROVIDER_MICROPHONE_DI_DOCUMENTATION",
            "distributed_file_coordinate": "PER_FILE_SAMPLE_COORDINATES_ESTABLISHED;_14_OF_15_WAVS_HAVE_IDENTICAL_SCOPE;_CROSS_FILE_SESSION_TIME_ORIGIN_UNESTABLISHED",
            "post_export_integrity": "PASS_CHECKSUM_BOUND_TWO_PASS_READ_ONLY_VERIFICATION",
            "physical_onset_ground_truth": "NOT_ESTABLISHED",
            "calibration_applicability": "UNESTABLISHED",
        },
        "bounded_use_authority": {
            "scientifically_usable": True,
            "maximum_authorized_claim": "Provenance-bound, deterministic source-labelled observations may be made on immutable per-file coordinates, and neutral distributed-file geometry may be studied only with the explicit limitation that common acquisition clock and exact session-time origin remain unestablished.",
            "unauthorized_claims": [
                "acquisition-time or sample-accurate human microtiming", "physical onset",
                "event correspondence", "source isolation", "detector accuracy", "calibration transfer",
                "synchronization, rushing, dragging, swing, groove, intention, or performance quality",
            ],
        },
        "analytical_source_decision": {
            "status": "NOT_SELECTED_NOT_FROZEN",
            "recommendation_only": {
                "Drums": "Use the original unmodified stereo file Dums Overheads LCT 640 TS-Dual Output Mode.wav as the minimal broad Drum representation.",
                "Double Bass": "Use the original unmodified mono file BASS - DI.wav as the minimal direct Double Bass representation.",
                "rationale": "Direct selection avoids derived mixing and preserves exact supplied file coordinates; the recommendation is independent of JGA output and requires PI review before authority freeze.",
            },
        },
        "firewalls": {
            "jga_executed": False, "h02_used": False, "strength_accessed": False,
            "production_code_changed": False, "raw_assets_changed": False,
            "derived_assets_created": False, "historical_authorities_changed": False,
        },
    }


def freeze(pass_one: Path, pass_two: Path) -> None:
    if pass_one.read_bytes() != pass_two.read_bytes():
        raise RuntimeError("AUTHORITY_CONFLICT_TWO_PASS_DISAGREEMENT")
    record = json.loads(pass_one.read_text())
    if record != derive():
        raise RuntimeError("AUTHORITY_CONFLICT_FREEZE_REPLAY")
    write_json(HERE / "input_authority_manifest.json", record)
    print(json.dumps({
        "status": "PASS",
        "authority_id": AUTHORITY_ID,
        "asset_count": record["scientifically_relevant_asset_count"],
        "wav_count": record["wav_asset_count"],
        "dataset_fingerprint": record["dataset_fingerprint"],
        "two_pass_replay": "PASS_BYTE_IDENTICAL_INDEPENDENT_READS",
    }, indent=2, sort_keys=True))


def verify_frozen() -> None:
    frozen = json.loads((HERE / "input_authority_manifest.json").read_text())
    current = derive()
    if frozen != current:
        raise RuntimeError("FROZEN_AUTHORITY_VERIFICATION_FAILURE")
    print(json.dumps({
        "status": "PASS",
        "authority_id": frozen["authority_id"],
        "dataset_fingerprint": frozen["dataset_fingerprint"],
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
        verify_frozen()


if __name__ == "__main__":
    main()
