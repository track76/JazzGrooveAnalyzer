"""Freeze corrected CED-VAL-002 CalibrationSymbolicEvent authority only."""

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import xml.etree.ElementTree as ET


DATASET_FINGERPRINT = "631eaf017cfaf335ee2945bfbe0df19221a0a0d069fee3602880eda7a851ade1"
PROVENANCE_REVISION = "PR-CED-VAL-002-SWING-002"
SOURCE = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-002-SWING/symbolic/CED-VAL-002-swing.musicxml")
SOURCE_SHA256 = "0ae6ed241699b65f2e6d120c08f18e132781109f5f3d35335a9efe094e2ceb39"
OUTPUT = Path("validation/CED-VAL-002-SWING/run_20260823_170857/calibration_symbolic_events.json")
PARTS = {"P1": "Piano", "P3": "Double Bass", "P4": "Drums"}
EXPECTED = {"Drums": 192, "Double Bass": 127, "Piano": 64}


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def frecord(value: Fraction) -> dict:
    return {"exact": f"{value.numerator}/{value.denominator}", "numerator": value.numerator, "denominator": value.denominator}


def text(element: ET.Element, name: str, default: str = "") -> str:
    child = element.find(name)
    return default if child is None or child.text is None else child.text.strip()


def descriptor(note: ET.Element) -> str:
    pitch = note.find("pitch")
    if pitch is not None:
        return "".join((text(pitch, "step"), text(pitch, "alter", "0"), text(pitch, "octave")))
    unpitched = note.find("unpitched")
    if unpitched is not None:
        return "unpitched:" + "".join((text(unpitched, "display-step"), text(unpitched, "display-octave")))
    return "unidentified"


def main() -> None:
    if checksum(SOURCE) != SOURCE_SHA256:
        raise RuntimeError("corrected MusicXML checksum mismatch")
    root = ET.parse(SOURCE).getroot()
    per_minutes = tuple(Fraction(node.text.strip()) for node in root.findall(".//per-minute") if node.text)
    beat_units = tuple(node.text.strip() for node in root.findall(".//metronome/beat-unit") if node.text)
    if not per_minutes or set(per_minutes) != {Fraction(150)} or set(beat_units) != {"quarter"}:
        raise RuntimeError("symbolic temporal declaration mismatch")
    seconds_per_quarter = Fraction(60) / per_minutes[0]
    attacks = {source: defaultdict(list) for source in PARTS.values()}
    exclusions = []
    part_summaries = {}
    for part in root.findall("part"):
        part_id = part.attrib["id"]
        if part_id not in PARTS:
            continue
        source = PARTS[part_id]
        divisions = None
        part_position = Fraction(0)
        attack_count = rest_count = tied_count = 0
        for measure_ordinal, measure in enumerate(part.findall("measure"), start=1):
            measure_number = measure.attrib.get("number", str(measure_ordinal))
            division_node = measure.find("attributes/divisions")
            if division_node is not None and division_node.text:
                divisions = int(division_node.text.strip())
            if divisions is None or divisions <= 0:
                raise RuntimeError(f"missing divisions: {part_id}/{measure_number}")
            cursor = maximum = Fraction(0)
            previous_non_chord = None
            note_ordinal = 0
            for child in measure:
                if child.tag == "backup":
                    cursor -= Fraction(int(text(child, "duration")), divisions)
                    if cursor < 0:
                        raise RuntimeError("negative MusicXML cursor")
                    previous_non_chord = None
                    continue
                if child.tag == "forward":
                    cursor += Fraction(int(text(child, "duration")), divisions)
                    maximum = max(maximum, cursor)
                    previous_non_chord = None
                    continue
                if child.tag != "note":
                    continue
                note_ordinal += 1
                duration_text = text(child, "duration")
                duration = Fraction(int(duration_text), divisions) if duration_text else Fraction(0)
                is_chord = child.find("chord") is not None
                if is_chord:
                    if previous_non_chord is None:
                        raise RuntimeError("chord without anchor")
                    onset = previous_non_chord
                else:
                    onset = cursor
                    previous_non_chord = onset
                locator = {"part_id": part_id, "measure_number": measure_number, "measure_ordinal": measure_ordinal, "note_ordinal": note_ordinal, "voice": text(child, "voice", "unspecified"), "staff": text(child, "staff", "unspecified"), "descriptor": descriptor(child)}
                if child.find("rest") is not None:
                    rest_count += 1
                    exclusions.append({**locator, "reason": "REST"})
                elif "stop" in {tie.attrib.get("type", "") for tie in child.findall("tie")}:
                    tied_count += 1
                    exclusions.append({**locator, "reason": "TIED_CONTINUATION"})
                else:
                    attacks[source][part_position + onset].append(locator)
                    attack_count += 1
                if not is_chord:
                    cursor += duration
                    maximum = max(maximum, cursor)
            part_position += maximum
        part_summaries[source] = {"part_id": part_id, "measure_count": len(part.findall("measure")), "duration_quarters": frecord(part_position), "attack_note_count": attack_count, "rest_count": rest_count, "tied_continuation_count": tied_count}
    events = []
    for source in ("Drums", "Double Bass", "Piano"):
        for onset, constituents in sorted(attacks[source].items()):
            ordered = tuple(sorted(constituents, key=lambda item: (item["part_id"], item["measure_ordinal"], item["note_ordinal"])))
            identity_payload = {"dataset_fingerprint": DATASET_FINGERPRINT, "provenance_revision": PROVENANCE_REVISION, "source": source, "onset_quarters": f"{onset.numerator}/{onset.denominator}", "constituents": ordered}
            identity = sha256(json.dumps(identity_payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            events.append({"calibration_symbolic_event_id": f"CSE-{identity}", "source": source, "symbolic_onset_quarters": frecord(onset), "t_gt_seconds": frecord(onset * seconds_per_quarter), "constituent_notes": ordered})
    counts = {source: sum(event["source"] == source for event in events) for source in EXPECTED}
    if counts != EXPECTED:
        raise RuntimeError(f"symbolic population mismatch: {counts}")
    scientific = {"schema_revision": "1", "dataset_fingerprint": DATASET_FINGERPRINT, "provenance_revision": PROVENANCE_REVISION, "musicxml_sha256": SOURCE_SHA256, "seconds_per_quarter": frecord(seconds_per_quarter), "events": events, "exclusions": exclusions}
    fingerprint = sha256(json.dumps(scientific, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    payload = {**scientific, "part_summaries": part_summaries, "population_counts": counts, "scientific_fingerprint": fingerprint}
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "counts": counts, "scientific_fingerprint": fingerprint, "sha256": checksum(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
