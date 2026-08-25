"""Read-only verifier for PR-CED-VAL-008-VARIABLE-TEMPO-BENCHMARK-001."""
from __future__ import annotations

from fractions import Fraction
import gzip
from hashlib import sha256
import json
from pathlib import Path
import struct
import wave
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "input_authority_manifest.json"
SCHEDULE_PATH = HERE / "symbolic_beat_reference.json"


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def wav_properties(path: Path) -> dict:
    with path.open("rb") as stream:
        if stream.read(4) != b"RIFF" or (stream.seek(8), stream.read(4))[1] != b"WAVE":
            raise RuntimeError(f"NOT_RIFF_WAVE: {path}")
        fmt = None
        data_size = None
        while True:
            chunk_id, size_raw = stream.read(4), stream.read(4)
            if not chunk_id or len(size_raw) != 4:
                break
            size = struct.unpack("<I", size_raw)[0]
            if chunk_id == b"fmt ":
                data = stream.read(size)
                fmt = struct.unpack("<HHIIHH", data[:16])
            elif chunk_id == b"data":
                data_size = size
                stream.seek(size + (size & 1), 1)
            else:
                stream.seek(size + (size & 1), 1)
    with wave.open(str(path), "rb") as wav:
        props = {"channels":wav.getnchannels(),"width":wav.getsampwidth(),"sample_rate":wav.getframerate(),"frames":wav.getnframes(),"compression":wav.getcomptype()}
    expected = {"channels":2,"width":3,"sample_rate":44100,"frames":1463433,"compression":"NONE"}
    if props != expected or fmt != (1,2,44100,264600,6,24) or data_size != 8780598:
        raise RuntimeError(f"WAV_AUTHORITY_CONFLICT: {path}: {props} {fmt} {data_size}")
    return props


def expected_schedule() -> list[list]:
    starts = [Fraction(0), Fraction(8), Fraction(88, 5), Fraction(856, 35)]
    bpms = [120, 100, 140, 110]
    result = []
    provenance = "CHECKSUM_BOUND_ABLETON_TEMPO_MAP_ANALYTIC_DERIVATION"
    for index in range(64):
        segment = index // 16
        seconds = starts[segment] + (index % 16) * Fraction(60, bpms[segment])
        samples = seconds * 44100
        floor = samples.numerator // samples.denominator
        ceiling = floor if samples.denominator == 1 else floor + 1
        result.append([index,index // 4 + 1,index % 4 + 1,bpms[segment],f"{seconds.numerator}/{seconds.denominator}",f"{samples.numerator}/{samples.denominator}",floor,ceiling,provenance])
    return result


def verify_live_set(path: Path) -> None:
    root = ET.fromstring(gzip.open(path, "rb").read())
    if root.attrib.get("Creator") != "Ableton Live 11.3.43":
        raise RuntimeError("ABLETON_CREATOR_CONFLICT")
    master = root.find(".//MasterTrack")
    if master is None:
        raise RuntimeError("MASTER_TRACK_MISSING")
    tempo_target = master.find(".//Tempo/AutomationTarget")
    if tempo_target is None:
        raise RuntimeError("TEMPO_TARGET_MISSING")
    target_id = tempo_target.attrib["Id"]
    envelope = None
    for candidate in master.findall("./AutomationEnvelopes/Envelopes/AutomationEnvelope"):
        target = candidate.find("./EnvelopeTarget/PointeeId")
        if target is not None and target.attrib.get("Value") == target_id:
            envelope = candidate
            break
    if envelope is None:
        raise RuntimeError("TEMPO_ENVELOPE_MISSING")
    observed = [(event.attrib["Time"], int(float(event.attrib["Value"]))) for event in envelope.findall("./Automation/Events/FloatEvent")]
    expected = [("-63072000",120),("16",120),("16",100),("32",100),("32",140),("48",140),("48",110)]
    if observed != expected:
        raise RuntimeError(f"TEMPO_MAP_CONFLICT: {observed}")
    signatures = {
        (
            item.find("Numerator").attrib.get("Value"),
            item.find("Denominator").attrib.get("Value"),
            item.find("Time").attrib.get("Value"),
        )
        for item in root.findall(".//RemoteableTimeSignature")
    }
    if signatures != {("4", "4", "0")}:
        raise RuntimeError(f"METER_CONFLICT: {signatures}")
    transport = root.find(".//Transport")
    if transport is None or transport.find("LoopStart").attrib.get("Value") != "0" or transport.find("LoopLength").attrib.get("Value") != "64":
        raise RuntimeError("RENDER_RANGE_CONFLICT")


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())
    schedule = json.loads(SCHEDULE_PATH.read_text())
    dataset = Path(manifest["dataset_root"])
    if sha256(canonical(manifest["manifest_basis"])).hexdigest() != manifest["dataset_fingerprint"]:
        raise RuntimeError("DATASET_FINGERPRINT_CONFLICT")
    if checksum(SCHEDULE_PATH) != manifest["manifest_basis"]["symbolic_beat_reference"]["sha256"]:
        raise RuntimeError("SCHEDULE_CHECKSUM_CONFLICT")
    expected_names = {"CED-VAL-008-VARIABLE-TEMPO-BENCHMARK-v0.1  DRUM GT.wav","CED-VAL-008-VARIABLE-TEMPO-BENCHMARK-v0.1  MARKER GT.wav"}
    actual_names = {p.name for p in (dataset / "raw").iterdir() if p.suffix.lower() == ".wav" and not p.name.startswith("._")}
    if actual_names != expected_names:
        raise RuntimeError(f"RAW_POPULATION_CONFLICT: {actual_names}")
    for asset in manifest["manifest_basis"]["assets"]:
        path = dataset / asset["relative_path"]
        if path.stat().st_size != asset["byte_size"] or checksum(path) != asset["sha256"]:
            raise RuntimeError(f"ASSET_CONFLICT: {path}")
        if path.suffix.lower() == ".wav":
            wav_properties(path)
    verify_live_set(dataset / manifest["manifest_basis"]["assets"][0]["relative_path"])
    expected = expected_schedule()
    if schedule["events"] != expected or schedule["beat_count"] != 64:
        raise RuntimeError("SYMBOLIC_SCHEDULE_CONFLICT")
    if [row[0] for row in expected] != list(range(64)):
        raise RuntimeError("SYMBOLIC_ORDER_CONFLICT")
    if [expected[i][5] for i in (0,16,32,48,63)] != ["0/1","352800/1","776160/1","1078560/1","15833160/11"]:
        raise RuntimeError("BOUNDARY_COORDINATE_CONFLICT")
    integer_count = sum(Fraction(row[5]).denominator == 1 for row in expected)
    if integer_count != 50 or schedule["non_integer_sample_coordinate_count"] != 14:
        raise RuntimeError("INTEGER_COORDINATE_COUNT_CONFLICT")
    print(json.dumps({"authority_id":manifest["authority_id"],"dataset_fingerprint":manifest["dataset_fingerprint"],"integer_sample_coordinates":50,"non_integer_sample_coordinates":14,"scientific_asset_count":3,"status":"PASS","symbolic_beat_count":64,"systems_executed":[]}, sort_keys=True))


if __name__ == "__main__":
    main()
