"""Build frozen CalibrationSymbolicEvent authority without loading JGA events."""

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import xml.etree.ElementTree as ET


RUN_ID = "run_20260823_070702"
GROUND_TRUTH_ID = "GT-VAL-001-v1"
SOURCE = Path(
    "recordings/validation/ground_truth/"
    "03 THE COST OF LIVING versione intro + 8 bar.musicxml"
)
SOURCE_SHA256 = "809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778"
OUTPUT = Path(f"validation/VAL-001/{RUN_ID}/calibration_symbolic_events.json")
PARTS = {
    "P2": "Tenor Sax",
    "P3": "Piano",
    "P5": "Double Bass",
    "P6": "Drums",
}
STEM_BINDINGS = {
    "Drums": {
        "path": "recordings/validation/stems/drums.wav",
        "sha256": "d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd",
    },
    "Piano": {
        "path": "recordings/validation/stems/piano.wav",
        "sha256": "26fa1158f375598cc7c01e04379c00547ef1787f6862eb2f29a36aafd9007c7e",
    },
    "Double Bass": {
        "path": "recordings/validation/stems/double_bass.wav",
        "sha256": "31d6f2e34d360c6f8f75362187433f2a2c1f5eb5cbbfe627305e99d07d8be6c5",
    },
    "Tenor Sax": {
        "path": "recordings/validation/stems/tenor_sax.wav",
        "sha256": "89dd7e5c6063d3c4d5e4ac59c9119c265df4257dfb1b4a1e01b5f117ee87182e",
    },
}


def fraction_record(value: Fraction) -> dict[str, int | str]:
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "numerator": value.numerator,
        "denominator": value.denominator,
    }


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def element_text(element: ET.Element, name: str, default: str = "") -> str:
    child = element.find(name)
    return default if child is None or child.text is None else child.text.strip()


def note_descriptor(note: ET.Element) -> str:
    pitch = note.find("pitch")
    if pitch is not None:
        return "".join(
            (
                element_text(pitch, "step"),
                element_text(pitch, "alter", "0"),
                element_text(pitch, "octave"),
            )
        )
    unpitched = note.find("unpitched")
    if unpitched is not None:
        return "unpitched:" + "".join(
            (
                element_text(unpitched, "display-step"),
                element_text(unpitched, "display-octave"),
            )
        )
    return "unidentified"


def build() -> dict:
    if checksum(SOURCE) != SOURCE_SHA256:
        raise RuntimeError("MusicXML checksum mismatch")
    for binding in STEM_BINDINGS.values():
        if checksum(Path(binding["path"])) != binding["sha256"]:
            raise RuntimeError(f"Stem checksum mismatch: {binding['path']}")

    root = ET.parse(SOURCE).getroot()
    per_minutes = tuple(
        Fraction(item.text.strip())
        for item in root.findall(".//per-minute")
        if item.text
    )
    beat_units = tuple(
        item.text.strip()
        for item in root.findall(".//metronome/beat-unit")
        if item.text
    )
    if not per_minutes or set(per_minutes) != {Fraction(78, 1)}:
        raise RuntimeError(f"Non-unique symbolic temporal conversion: {per_minutes}")
    if set(beat_units) != {"quarter"}:
        raise RuntimeError(f"Unsupported symbolic beat units: {beat_units}")
    seconds_per_quarter = Fraction(60, 1) / per_minutes[0]

    attacks_by_source_time: dict[str, dict[Fraction, list[dict]]] = {
        source: defaultdict(list) for source in PARTS.values()
    }
    exclusions = []
    part_summaries = {}

    for part in root.findall("part"):
        part_id = part.attrib["id"]
        if part_id not in PARTS:
            continue
        source_name = PARTS[part_id]
        divisions = None
        part_position_quarters = Fraction(0, 1)
        rest_count = 0
        tied_continuation_count = 0
        attack_note_count = 0

        for measure_ordinal, measure in enumerate(part.findall("measure"), start=1):
            measure_number = measure.attrib.get("number", str(measure_ordinal))
            divisions_element = measure.find("attributes/divisions")
            if divisions_element is not None and divisions_element.text:
                divisions = int(divisions_element.text.strip())
            if divisions is None or divisions <= 0:
                raise RuntimeError(f"Missing divisions for {part_id} measure {measure_number}")

            cursor = Fraction(0, 1)
            maximum_cursor = Fraction(0, 1)
            previous_non_chord_onset = None
            note_ordinal = 0
            for child in measure:
                if child.tag == "backup":
                    cursor -= Fraction(int(element_text(child, "duration")), divisions)
                    if cursor < 0:
                        raise RuntimeError(f"Negative cursor in {part_id} measure {measure_number}")
                    previous_non_chord_onset = None
                    continue
                if child.tag == "forward":
                    cursor += Fraction(int(element_text(child, "duration")), divisions)
                    maximum_cursor = max(maximum_cursor, cursor)
                    previous_non_chord_onset = None
                    continue
                if child.tag != "note":
                    continue

                note_ordinal += 1
                duration_text = element_text(child, "duration")
                duration = (
                    Fraction(int(duration_text), divisions)
                    if duration_text
                    else Fraction(0, 1)
                )
                is_chord = child.find("chord") is not None
                if is_chord:
                    if previous_non_chord_onset is None:
                        raise RuntimeError(
                            f"Chord without anchor in {part_id} measure {measure_number}"
                        )
                    onset_in_measure = previous_non_chord_onset
                else:
                    onset_in_measure = cursor
                    previous_non_chord_onset = onset_in_measure

                locator = {
                    "part_id": part_id,
                    "measure_number": measure_number,
                    "measure_ordinal": measure_ordinal,
                    "note_ordinal": note_ordinal,
                    "voice": element_text(child, "voice", "unspecified"),
                    "staff": element_text(child, "staff", "unspecified"),
                    "descriptor": note_descriptor(child),
                }
                if child.find("rest") is not None:
                    rest_count += 1
                    exclusions.append({**locator, "reason": "REST"})
                else:
                    tie_types = {
                        tie.attrib.get("type", "") for tie in child.findall("tie")
                    }
                    if "stop" in tie_types:
                        tied_continuation_count += 1
                        exclusions.append({**locator, "reason": "TIED_CONTINUATION"})
                    else:
                        absolute_quarters = part_position_quarters + onset_in_measure
                        attacks_by_source_time[source_name][absolute_quarters].append(locator)
                        attack_note_count += 1

                if not is_chord:
                    cursor += duration
                    maximum_cursor = max(maximum_cursor, cursor)

            part_position_quarters += maximum_cursor

        part_summaries[source_name] = {
            "part_id": part_id,
            "measure_count": len(part.findall("measure")),
            "duration_quarters": fraction_record(part_position_quarters),
            "attack_note_count": attack_note_count,
            "rest_count": rest_count,
            "tied_continuation_count": tied_continuation_count,
        }

    events = []
    for source_name in ("Drums", "Piano", "Double Bass", "Tenor Sax"):
        for onset_quarters, constituents in sorted(
            attacks_by_source_time[source_name].items(), key=lambda item: item[0]
        ):
            ordered_constituents = tuple(
                sorted(
                    constituents,
                    key=lambda item: (
                        item["part_id"],
                        item["measure_ordinal"],
                        item["note_ordinal"],
                    ),
                )
            )
            onset_seconds = onset_quarters * seconds_per_quarter
            identity_payload = {
                "ground_truth_id": GROUND_TRUTH_ID,
                "source": source_name,
                "onset_quarters": f"{onset_quarters.numerator}/{onset_quarters.denominator}",
                "constituents": ordered_constituents,
            }
            identity = sha256(
                json.dumps(identity_payload, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest()
            events.append(
                {
                    "calibration_symbolic_event_id": f"CSE-{identity}",
                    "source": source_name,
                    "symbolic_onset_quarters": fraction_record(onset_quarters),
                    "t_gt_seconds": fraction_record(onset_seconds),
                    "constituent_notes": ordered_constituents,
                }
            )

    counts = {
        source: sum(event["source"] == source for event in events)
        for source in ("Drums", "Piano", "Double Bass", "Tenor Sax")
    }
    scientific_content = {
        "schema_revision": "1",
        "ground_truth_id": GROUND_TRUTH_ID,
        "musicxml_sha256": SOURCE_SHA256,
        "seconds_per_quarter": fraction_record(seconds_per_quarter),
        "events": events,
        "exclusions": exclusions,
    }
    fingerprint = sha256(
        json.dumps(scientific_content, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "authority_status": "SUFFICIENT",
        "schema_revision": "1",
        "ground_truth_id": GROUND_TRUTH_ID,
        "controlled_dataset_id": "CED-VAL-001",
        "generation_record_id": "DGR-CED-VAL-001-001",
        "provenance_revision_id": "PR-CED-VAL-001-001",
        "musicxml": {"path": str(SOURCE), "sha256": SOURCE_SHA256},
        "symbolic_temporal_conversion": {
            "authority": "checksum-bound MusicXML metronome declarations",
            "declaration_count": len(per_minutes),
            "seconds_per_quarter": fraction_record(seconds_per_quarter),
            "inferred": False,
        },
        "sample_zero_relationship": "MusicXML score time zero = WAV sample zero",
        "rendered_stems": STEM_BINDINGS,
        "sample_rate_hz": 44100,
        "sample_count_per_channel": 1865728,
        "symbolic_event_counts": counts,
        "part_summaries": part_summaries,
        "events": events,
        "exclusions": exclusions,
        "scientific_fingerprint": fingerprint,
        "jga_observed_events_accessed": False,
    }


def main() -> None:
    authority = build()
    OUTPUT.write_text(
        json.dumps(authority, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"AUTHORITY_STATUS={authority['authority_status']}")
    print(f"COUNTS={authority['symbolic_event_counts']}")
    print(f"FINGERPRINT={authority['scientific_fingerprint']}")
    print(f"OUTPUT={OUTPUT}")
    print("JGA_OBSERVED_EVENTS_ACCESSED=False")


if __name__ == "__main__":
    main()
