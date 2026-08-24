"""Read-only verifier for PR-CED-VAL-007-CONTROLLED-BEAT-BENCHMARK-001."""
from __future__ import annotations

import gzip
from hashlib import sha256
import json
from pathlib import Path
import struct
import wave
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "input_authority_manifest.json"
SCHEDULE = HERE / "symbolic_beat_reference.json"
DATASET = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK")


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def wav_properties(path: Path) -> dict:
    with path.open("rb") as stream:
        if stream.read(4) != b"RIFF":
            raise RuntimeError(f"NOT_RIFF: {path}")
        stream.seek(8)
        if stream.read(4) != b"WAVE":
            raise RuntimeError(f"NOT_WAVE: {path}")
        fmt = None
        data_size = None
        while True:
            chunk_id = stream.read(4)
            size_raw = stream.read(4)
            if not chunk_id or len(size_raw) != 4:
                break
            size = struct.unpack("<I", size_raw)[0]
            if chunk_id == b"fmt ":
                data = stream.read(size)
                fmt = {
                    "format": struct.unpack("<H", data[0:2])[0],
                    "channels": struct.unpack("<H", data[2:4])[0],
                    "sample_rate": struct.unpack("<I", data[4:8])[0],
                    "block_align": struct.unpack("<H", data[12:14])[0],
                    "bits": struct.unpack("<H", data[14:16])[0],
                }
            elif chunk_id == b"data":
                data_size = size
                stream.seek(size + (size & 1), 1)
            else:
                stream.seek(size + (size & 1), 1)
        if fmt is None or data_size is None:
            raise RuntimeError(f"INCOMPLETE_WAV: {path}")
    with wave.open(str(path), "rb") as wav:
        props = {"channels": wav.getnchannels(), "width": wav.getsampwidth(), "sample_rate": wav.getframerate(), "frames": wav.getnframes(), "compression": wav.getcomptype()}
    expected = {"channels": 2, "width": 3, "sample_rate": 44100, "frames": 1411200, "compression": "NONE"}
    if props != expected or fmt != {"format": 1, "channels": 2, "sample_rate": 44100, "block_align": 6, "bits": 24} or data_size != 8467200:
        raise RuntimeError(f"WAV_AUTHORITY_CONFLICT: {path}: {props} {fmt} {data_size}")
    return props


def track_events(root: ET.Element, track_name: str) -> list[tuple[float, int, float, float, str, str]]:
    for track in root.findall(".//MidiTrack"):
        name = track.find("./Name/EffectiveName")
        if name is None or name.attrib.get("Value") != track_name:
            continue
        events = []
        clips = track.findall(".//MainSequencer/ClipTimeable/ArrangerAutomation/Events/MidiClip")
        if len(clips) != 16:
            raise RuntimeError(f"CLIP_COUNT_CONFLICT: {track_name}")
        for clip in clips:
            clip_time = float(clip.attrib["Time"])
            groove = clip.find("./GrooveSettings/GrooveId")
            if groove is None or groove.attrib.get("Value") != "-1":
                raise RuntimeError(f"GROOVE_CONFLICT: {track_name}")
            for key_track in clip.findall(".//Notes/KeyTracks/KeyTrack"):
                key = int(key_track.find("./MidiKey").attrib["Value"])
                for event in key_track.findall("./Notes/MidiNoteEvent"):
                    events.append((clip_time + float(event.attrib["Time"]), key, float(event.attrib["Velocity"]), float(event.attrib["VelocityDeviation"]), event.attrib["Probability"], event.attrib["IsEnabled"]))
        return sorted(events)
    raise RuntimeError(f"TRACK_MISSING: {track_name}")


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    computed_fingerprint = sha256(canonical(manifest["manifest_basis"])).hexdigest()
    if computed_fingerprint != manifest["dataset_fingerprint"]:
        raise RuntimeError(f"DATASET_FINGERPRINT_CONFLICT: {computed_fingerprint}")
    for asset in manifest["manifest_basis"]["assets"]:
        path = DATASET / asset["relative_path"]
        if path.stat().st_size != asset["byte_size"] or checksum(path) != asset["sha256"]:
            raise RuntimeError(f"ASSET_CONFLICT: {path}")
        if path.suffix.lower() == ".wav":
            wav_properties(path)

    live_path = DATASET / manifest["manifest_basis"]["assets"][0]["relative_path"]
    root = ET.fromstring(gzip.open(live_path, "rb").read())
    if root.attrib.get("Creator") != "Ableton Live 11.3.43":
        raise RuntimeError("ABLETON_CREATOR_CONFLICT")
    tempo = root.find(".//MasterTrack//Tempo/Manual")
    if tempo is None or tempo.attrib.get("Value") != "120":
        raise RuntimeError("TEMPO_CONFLICT")
    drum = track_events(root, "DRUM GT")
    marker = track_events(root, "MARKER GT")
    expected_times = [float(i) for i in range(64)]
    for name, events, key in (("DRUM GT", drum, 48), ("MARKER GT", marker, 60)):
        if [event[0] for event in events] != expected_times:
            raise RuntimeError(f"TEMPORAL_SCHEDULE_CONFLICT: {name}")
        if any(event[1:] != (key, 100.0, 0.0, "1", "true") for event in events):
            raise RuntimeError(f"MIDI_EVENT_AUTHORITY_CONFLICT: {name}")
    if [event[0] for event in drum] != [event[0] for event in marker]:
        raise RuntimeError("TEMPORAL_IDENTITY_CONFLICT")

    schedule = json.loads(SCHEDULE.read_text())
    expected = [[i, 22050 * i, f"{i}/2" if i % 2 else f"{i // 2}/1"] for i in range(64)]
    if schedule["events"] != expected:
        raise RuntimeError("SYMBOLIC_REFERENCE_CONFLICT")
    print(json.dumps({"authority_id": manifest["authority_id"], "dataset_fingerprint": computed_fingerprint, "scientific_asset_count": len(manifest["manifest_basis"]["assets"]), "wav_count": 5, "symbolic_beat_count": 64, "temporal_schedule_identity": True, "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
