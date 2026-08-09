"""Prepare H-VAL001-C1-06 symbolic A/B conditions without JGA analysis.

Condition B removes every even-numbered sounding onset event independently in
each MusicXML part. Tied continuations inherit the decision of their initiating
event. Removed duration is represented as silence while retained notes are not
retimed or otherwise altered.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
PACKAGE = RUN / "controlled_dataset"
SOURCE_XML = ROOT / (
    "recordings/validation/ground_truth/"
    "03 THE COST OF LIVING versione intro + 8 bar.musicxml"
)
SOURCE_GT = SOURCE_XML.with_suffix(".ground_truth.json")

EXPERIMENT_ID = "H-VAL001-C1-06"
DATASET_ID = "CED-VAL-001-RD-001"
DGR_ID = "DGR-CED-VAL-001-RD-001-001"
PROVENANCE_ID = "PR-CED-VAL-001-RD-001-001"
CONDITION_A_ID = "CED-VAL-001-RD-001-A"
CONDITION_B_ID = "CED-VAL-001-RD-001-B"
VAL_A_ID = "VAL-001-RD-A"
VAL_B_ID = "VAL-001-RD-B"
GT_A_ID = "GT-VAL-001-RD-A-v1"
GT_B_ID = "GT-VAL-001-RD-B-v1"
INVENTORY_ID = "ERI-CED-VAL-001-RD-001-001"


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def pitch_key(note: ET.Element) -> tuple[str, ...]:
    pitch = note.find("pitch")
    unpitched = note.find("unpitched")
    if pitch is not None:
        sounding = (
            "pitch",
            pitch.findtext("step", ""),
            pitch.findtext("alter", "0"),
            pitch.findtext("octave", ""),
        )
    elif unpitched is not None:
        sounding = (
            "unpitched",
            unpitched.findtext("display-step", ""),
            unpitched.findtext("display-octave", ""),
        )
    else:
        raise ValueError("Sounding note has neither pitch nor unpitched identity")
    return sounding + (note.findtext("voice", ""), note.findtext("staff", ""))


def tie_types(note: ET.Element) -> set[str]:
    return {tie.get("type", "") for tie in note.findall("tie")}


def replace_with_rest(note: ET.Element) -> None:
    for tag in (
        "pitch",
        "unpitched",
        "chord",
        "tie",
        "accidental",
        "stem",
        "notehead",
        "beam",
        "notations",
        "lyric",
    ):
        for child in list(note.findall(tag)):
            note.remove(child)
    note.insert(0, ET.Element("rest"))


def note_duration(note: ET.Element, divisions: int) -> Fraction:
    duration = note.findtext("duration")
    if duration is None:
        raise ValueError("Eligible sounding note has no duration")
    return Fraction(int(duration), divisions)


def collect_events(
    root: ET.Element,
) -> tuple[list[dict[str, object]], dict[int, bool], dict[str, dict[str, int]]]:
    events: list[dict[str, object]] = []
    decisions: dict[int, bool] = {}
    counts: dict[str, dict[str, int]] = {}

    for part in root.findall("part"):
        part_id = part.get("id")
        if part_id is None:
            raise ValueError("MusicXML part has no identity")
        ordinal = 0
        absolute_quarters = Fraction(0)
        divisions = 0
        active_ties: dict[tuple[str, ...], dict[str, object]] = {}

        for measure_index, measure in enumerate(part.findall("measure"), start=1):
            division_text = measure.findtext("./attributes/divisions")
            if division_text is not None:
                divisions = int(division_text)
            if divisions <= 0:
                raise ValueError(f"No divisions established for {part_id}")

            cursor = Fraction(0)
            measure_extent = Fraction(0)
            previous_note_onset = Fraction(0)
            note_document_index = 0

            for child in list(measure):
                if child.tag == "backup":
                    cursor -= Fraction(int(child.findtext("duration", "0")), divisions)
                    continue
                if child.tag == "forward":
                    cursor += Fraction(int(child.findtext("duration", "0")), divisions)
                    measure_extent = max(measure_extent, cursor)
                    continue
                if child.tag != "note":
                    continue

                note_document_index += 1
                duration = note_duration(child, divisions)
                is_chord = child.find("chord") is not None
                onset = previous_note_onset if is_chord else cursor
                if not is_chord:
                    previous_note_onset = onset
                    cursor += duration
                    measure_extent = max(measure_extent, cursor)
                if child.find("rest") is not None:
                    continue

                key = pitch_key(child)
                ties = tie_types(child)
                if "stop" in ties:
                    event = active_ties.get(key)
                    if event is None:
                        raise ValueError(
                            f"Unmatched tie continuation in {part_id} measure "
                            f"{measure.get('number')}"
                        )
                    event["duration_quarters"] += duration
                else:
                    ordinal += 1
                    retained = ordinal % 2 == 1
                    event_id = f"{part_id}-E{ordinal:04d}"
                    event = {
                        "event_id": event_id,
                        "part_id": part_id,
                        "ordinal": ordinal,
                        "source_measure_id": measure.get("number", str(measure_index)),
                        "measure_document_index": measure_index,
                        "note_document_index": note_document_index,
                        "voice": child.findtext("voice", ""),
                        "staff": child.findtext("staff", ""),
                        "sounding_identity": key[:4],
                        "onset_quarters": absolute_quarters + onset,
                        "duration_quarters": duration,
                        "retained": retained,
                    }
                    events.append(event)
                decisions[id(child)] = bool(event["retained"])

                if "start" in ties:
                    active_ties[key] = event
                elif "stop" in ties:
                    active_ties.pop(key, None)

            absolute_quarters += measure_extent

        if active_ties:
            raise ValueError(f"Unclosed ties remain in {part_id}")
        part_events = [event for event in events if event["part_id"] == part_id]
        counts[part_id] = {
            "eligible_sounding_events": len(part_events),
            "retained_events": sum(bool(event["retained"]) for event in part_events),
            "removed_events": sum(not bool(event["retained"]) for event in part_events),
        }

    return events, decisions, counts


def transform_condition_b(root: ET.Element, decisions: dict[int, bool]) -> None:
    for measure in root.findall("./part/measure"):
        children = list(measure)
        index = 0
        while index < len(children):
            first = children[index]
            if first.tag != "note" or first.find("chord") is not None:
                index += 1
                continue
            group = [first]
            next_index = index + 1
            while (
                next_index < len(children)
                and children[next_index].tag == "note"
                and children[next_index].find("chord") is not None
            ):
                group.append(children[next_index])
                next_index += 1

            sounding = [note for note in group if note.find("rest") is None]
            removed = [note for note in sounding if not decisions[id(note)]]
            retained = [note for note in sounding if decisions[id(note)]]
            if removed:
                if not retained:
                    replace_with_rest(group[0])
                    for note in group[1:]:
                        measure.remove(note)
                elif group[0] in retained:
                    for note in removed:
                        measure.remove(note)
                else:
                    promoted = retained[0]
                    chord = promoted.find("chord")
                    if chord is not None:
                        promoted.remove(chord)
                    for note in removed:
                        measure.remove(note)
            index = next_index


def musicxml_bytes(root: ET.Element, source_bytes: bytes) -> bytes:
    ET.indent(root, space=" ")
    body = ET.tostring(root, encoding="UTF-8", xml_declaration=True)
    doctype = next(
        line for line in source_bytes.splitlines() if line.startswith(b"<!DOCTYPE")
    )
    first_line, remainder = body.split(b"\n", 1)
    return first_line + b"\n" + doctype + b"\n" + remainder + b"\n"


def symbolic_signature(root: ET.Element) -> dict[str, object]:
    return {
        "time_signatures": [
            (item.findtext("beats"), item.findtext("beat-type"))
            for item in root.findall("./part/measure/attributes/time")
        ],
        "metronome_indications": [
            (item.findtext("beat-unit"), item.findtext("per-minute"))
            for item in root.findall(".//metronome")
        ],
        "parts": [
            (part.get("id"), part.findtext("part-name"))
            for part in root.findall("./part-list/score-part")
        ],
        "measure_identities": {
            part.get("id", ""): [measure.get("number") for measure in part.findall("measure")]
            for part in root.findall("part")
        },
    }


def temporal_extents(root: ET.Element) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for part in root.findall("part"):
        divisions = 0
        extents = []
        for measure in part.findall("measure"):
            division_text = measure.findtext("./attributes/divisions")
            if division_text is not None:
                divisions = int(division_text)
            cursor = Fraction(0)
            extent = Fraction(0)
            for child in list(measure):
                duration_text = child.findtext("duration")
                if duration_text is None:
                    continue
                duration = Fraction(int(duration_text), divisions)
                if child.tag == "backup":
                    cursor -= duration
                elif child.tag == "forward":
                    cursor += duration
                    extent = max(extent, cursor)
                elif child.tag == "note" and child.find("chord") is None:
                    cursor += duration
                    extent = max(extent, cursor)
            extents.append(str(extent))
        result[part.get("id", "")] = extents
    return result


def event_signature(event: dict[str, object]) -> tuple[object, ...]:
    return (
        event["part_id"],
        tuple(event["sounding_identity"]),
        event["onset_quarters"],
        event["duration_quarters"],
        event["source_measure_id"],
        event["voice"],
        event["staff"],
    )


def main() -> None:
    source_bytes = SOURCE_XML.read_bytes()
    source_root = ET.fromstring(source_bytes)
    condition_b_root = deepcopy(source_root)

    events, source_decisions, counts = collect_events(source_root)
    _, condition_b_decisions, _ = collect_events(condition_b_root)
    if list(source_decisions.values()) != list(condition_b_decisions.values()):
        raise ValueError("Deep-copied symbolic decisions are not deterministic")
    transform_condition_b(condition_b_root, condition_b_decisions)

    symbolic_a = PACKAGE / "symbolic/condition_a.musicxml"
    symbolic_b = PACKAGE / "symbolic/condition_b.musicxml"
    symbolic_a.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_XML, symbolic_a)
    symbolic_b.write_bytes(musicxml_bytes(condition_b_root, source_bytes))

    parsed_a = ET.parse(symbolic_a).getroot()
    parsed_b = ET.parse(symbolic_b).getroot()
    signature_a = symbolic_signature(parsed_a)
    signature_b = symbolic_signature(parsed_b)
    if signature_a != signature_b:
        raise ValueError("Condition B changed controlled symbolic authority")
    extents_a = temporal_extents(parsed_a)
    extents_b = temporal_extents(parsed_b)
    if extents_a != extents_b:
        raise ValueError("Condition B changed symbolic temporal structure")
    condition_b_events, _, _ = collect_events(parsed_b)
    retained_signatures = [
        event_signature(event) for event in events if bool(event["retained"])
    ]
    condition_b_signatures = [event_signature(event) for event in condition_b_events]
    if retained_signatures != condition_b_signatures:
        raise ValueError("Condition B changed retained-event content or timing")

    quarter_seconds = Decimal(60) / Decimal(78)
    inventory_events = []
    for event in events:
        onset = Decimal(event["onset_quarters"].numerator) / Decimal(
            event["onset_quarters"].denominator
        ) * quarter_seconds
        duration = Decimal(event["duration_quarters"].numerator) / Decimal(
            event["duration_quarters"].denominator
        ) * quarter_seconds
        retained = bool(event["retained"])
        inventory_events.append(
            {
                "condition_a_event_id": event["event_id"],
                "condition_a_onset_seconds": str(onset),
                "condition_a_duration_seconds": str(duration),
                "status": "retained" if retained else "removed",
                "condition_b_event_id": event["event_id"] if retained else None,
                "condition_b_onset_seconds": str(onset) if retained else None,
                "condition_b_duration_seconds": str(duration) if retained else None,
                "part_id": event["part_id"],
                "stable_symbolic_ordinal": event["ordinal"],
                "source_measure_id": event["source_measure_id"],
                "measure_document_index": event["measure_document_index"],
                "note_document_index": event["note_document_index"],
                "voice": event["voice"],
                "staff": event["staff"],
                "sounding_identity": list(event["sounding_identity"]),
            }
        )

    inventory = {
        "inventory_id": INVENTORY_ID,
        "condition_a_id": CONDITION_A_ID,
        "condition_b_id": CONDITION_B_ID,
        "rule": (
            "Within each MusicXML part, retain odd-numbered sounding onset "
            "events and remove even-numbered events in document order; tied "
            "continuations inherit the initiating event decision."
        ),
        "declared_before_analysis": True,
        "selected_independently_of_jga_output": True,
        "events": inventory_events,
    }
    inventory_path = PACKAGE / "provenance/event_removal_inventory.json"
    write_json(inventory_path, inventory)

    source_gt = json.loads(SOURCE_GT.read_text(encoding="utf-8"))
    for condition, gt_id, val_id, source_path in (
        ("a", GT_A_ID, VAL_A_ID, symbolic_a),
        ("b", GT_B_ID, VAL_B_ID, symbolic_b),
    ):
        definition = deepcopy(source_gt)
        definition["ground_truth_id"] = gt_id
        definition["validation_item_id"] = val_id
        definition["source"] = {
            "repository_path": str(source_path.relative_to(ROOT)),
            "sha256": file_sha256(source_path),
            "repository_revision": None,
        }
        write_json(
            PACKAGE / f"ground_truth/condition_{condition}.ground_truth.json",
            definition,
        )

    dgr_path = PACKAGE / "provenance/dataset_generation_record.md"
    dgr_path.write_text(
        f"""# {DGR_ID} — Controlled Rhythmic-Density Dataset Generation Record

## Identities

- Controlled Dataset ID: `{DATASET_ID}`
- Dataset Generation Record ID: `{DGR_ID}`
- Provenance Revision ID: `{PROVENANCE_ID}`
- Condition A ID: `{CONDITION_A_ID}`
- Condition B ID: `{CONDITION_B_ID}`
- Event-removal inventory ID: `{INVENTORY_ID}`

## Declared Experimental Procedure

Condition A is an exact copy of the authoritative VAL-001 MusicXML source.
Condition B was mechanically derived without JGA analysis. Within every score
part, sounding onset events were counted in stable MusicXML document order.
Odd ordinals were retained and even ordinals were removed. All segments of a
tied event inherited the initiating event decision. Removed duration was
represented as silence; retained notes were not retimed.

The following remain declared identical: meter, tempo, instrumentation,
retained-event timing, temporal origin, total duration, rendering
configuration, sample rate, bit depth, and channel configuration.

## Symbolic assets

- Condition A: `{symbolic_a.relative_to(ROOT)}` — `{file_sha256(symbolic_a)}`
- Condition B: `{symbolic_b.relative_to(ROOT)}` — `{file_sha256(symbolic_b)}`
- Inventory: `{inventory_path.relative_to(ROOT)}` — `{file_sha256(inventory_path)}`

## Rendering boundary

No authoritative repository rendering mechanism is available. Required audio
assets remain externally generated. Rendering configuration and generation
date are `not specified` until the human export is completed. Licensing status
is `not_specified`; no permission is inferred from repository presence.

Required export: PCM WAV, 24-bit, 44.1 kHz, stereo, exported from score time
zero with identical settings and identical total sample count for A, A repeat,
B, and B repeat. Leading, internal, and trailing silence must be preserved.
""",
        encoding="utf-8",
    )

    def condition_manifest(
        condition_id: str, val_id: str, gt_id: str, suffix: str
    ) -> dict[str, object]:
        xml_path = PACKAGE / f"symbolic/condition_{suffix}.musicxml"
        gt_path = PACKAGE / f"ground_truth/condition_{suffix}.ground_truth.json"
        return {
            "condition_id": condition_id,
            "validation_item_id": val_id,
            "ground_truth_id": gt_id,
            "authoritative_musicxml": {
                "repository_path": str(xml_path.relative_to(PACKAGE)),
                "sha256": file_sha256(xml_path),
            },
            "ground_truth_definition": {
                "repository_path": str(gt_path.relative_to(PACKAGE)),
                "sha256": file_sha256(gt_path),
            },
            "canonical_wav": {
                "repository_path": f"audio/condition_{suffix}.wav",
                "sha256": "__REQUIRED_EXTERNAL_SHA256__",
            },
            "repeated_render_wav": {
                "repository_path": f"audio/condition_{suffix}_repeat.wav",
                "sha256": "__REQUIRED_EXTERNAL_SHA256__",
            },
            "catalogue_mp3": {
                "repository_path": f"audio/condition_{suffix}.mp3",
                "sha256": "__REQUIRED_EXTERNAL_SHA256__",
            },
            "licensing_status": "not_specified",
        }

    manifest = {
        "controlled_dataset_id": DATASET_ID,
        "dataset_generation_record_id": DGR_ID,
        "provenance_revision_id": PROVENANCE_ID,
        "relationship": "condition_b_is_declared_event_removal_from_condition_a",
        "knowledge_classification": "Declared Experimental Procedure",
        "controlled_audio_format": {
            "sample_rate_hz": 44100,
            "bit_depth": 24,
            "channel_count": 2,
            "sample_count_per_channel": "__REQUIRED_IDENTICAL_EXTERNAL_SAMPLE_COUNT__",
        },
        "condition_a": condition_manifest(CONDITION_A_ID, VAL_A_ID, GT_A_ID, "a"),
        "condition_b": condition_manifest(CONDITION_B_ID, VAL_B_ID, GT_B_ID, "b"),
        "event_removal_inventory": {
            "repository_path": str(inventory_path.relative_to(PACKAGE)),
            "sha256": file_sha256(inventory_path),
        },
        "dataset_generation_record": {
            "repository_path": str(dgr_path.relative_to(PACKAGE)),
            "sha256": file_sha256(dgr_path),
        },
    }
    write_json(PACKAGE / "controlled_ab_manifest.json", manifest)

    def pending_catalog_item(
        val_id: str, gt_id: str, suffix: str, title: str
    ) -> dict[str, object]:
        xml_path = PACKAGE / f"symbolic/condition_{suffix}.musicxml"
        return {
            "validation_item_id": val_id,
            "ground_truth_id": gt_id,
            "authoritative_musicxml": {
                "repository_path": str(xml_path.relative_to(ROOT)),
                "sha256": file_sha256(xml_path),
                "repository_revision": "__REQUIRED_COMMITTED_ASSET_REVISION__",
                "licensing_status": "not_specified",
            },
            "mp3_recording": {
                "repository_path": str(
                    (PACKAGE / f"audio/condition_{suffix}.mp3").relative_to(ROOT)
                ),
                "sha256": "__REQUIRED_EXTERNAL_SHA256__",
                "repository_revision": "__REQUIRED_COMMITTED_ASSET_REVISION__",
                "licensing_status": "not_specified",
            },
            "provenance": {"schema_version": "1", "item_version": "1"},
            "metadata": {"title": title},
        }

    write_json(
        PACKAGE / "pending_catalog_items.json",
        {
            "status": "NOT_REGISTERED_EXTERNAL_AUDIO_REQUIRED",
            "items": [
                pending_catalog_item(
                    VAL_A_ID,
                    GT_A_ID,
                    "a",
                    "VAL-001 controlled density Condition A",
                ),
                pending_catalog_item(
                    VAL_B_ID,
                    GT_B_ID,
                    "b",
                    "VAL-001 controlled density Condition B",
                ),
            ],
        },
    )

    symbolic_validation = {
        "experiment_id": EXPERIMENT_ID,
        "repository_revision": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "source_musicxml": {
            "repository_path": str(SOURCE_XML.relative_to(ROOT)),
            "sha256": file_sha256(SOURCE_XML),
        },
        "condition_a_exact_source_copy": symbolic_a.read_bytes() == source_bytes,
        "condition_a_sha256": file_sha256(symbolic_a),
        "condition_b_sha256": file_sha256(symbolic_b),
        "controlled_symbolic_signature_identical": signature_a == signature_b,
        "temporal_extents_identical": extents_a == extents_b,
        "retained_event_content_and_timing_identical": (
            retained_signatures == condition_b_signatures
        ),
        "controlled_symbolic_signature": signature_a,
        "part_event_counts": counts,
        "total_eligible_sounding_events": len(events),
        "total_retained_events": sum(bool(event["retained"]) for event in events),
        "total_removed_events": sum(not bool(event["retained"]) for event in events),
        "condition_b_sounding_event_count": len(condition_b_events),
        "inventory_sha256": file_sha256(inventory_path),
        "audio_generation_status": "BLOCKED_EXTERNAL_RENDER_REQUIRED",
    }
    write_json(RUN / "symbolic_validation.json", symbolic_validation)

    write_json(
        RUN / "experiment_manifest.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "scientific_protocol": "SVP-001",
            "repository_revision": symbolic_validation["repository_revision"],
            "bootstrap_revision": "M93 / 44ffffa",
            "controlled_dataset_id": DATASET_ID,
            "dataset_generation_record_id": DGR_ID,
            "package_manifest_path": str(
                (PACKAGE / "controlled_ab_manifest.json").relative_to(ROOT)
            ),
            "blind_configuration": {
                "analysis_input": "canonical lossless WAV for each neutral condition",
                "candidate_discovery": "AD-035 existing production configuration",
                "condition_assignment_hidden": True,
                "ground_truth_unavailable_until_blind_freeze": True,
            },
            "status": "PREPARED_TO_EXTERNAL_AUDIO_BOUNDARY",
        },
    )

    write_json(
        RUN / "blind_execution_configuration.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "condition_execution_identities": [
                "BLIND-CONDITION-01",
                "BLIND-CONDITION-02",
            ],
            "assignment_storage": (
                "Condition assignment remains outside blind analytical input "
                "until both populations are frozen."
            ),
            "analysis_pipeline": "existing approved AnalysisPipeline",
            "candidate_period_discovery": "AD-035 existing production mechanism",
            "audio_input": "canonical PCM WAV for each condition",
            "identical_configuration_required": True,
            "ground_truth_available_during_analysis": False,
            "musicxml_available_during_analysis": False,
            "event_removal_inventory_available_during_analysis": False,
            "status": "BLOCKED_EXTERNAL_AUDIO_REQUIRED",
        },
    )

    write_json(
        RUN / "post_blind_evaluation_structure.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "blind_record_fingerprint": "__REQUIRED_AFTER_BLIND_FREEZE__",
            "condition_assignment": "__REQUIRED_AFTER_BLIND_FREEZE__",
            "condition_a_ground_truth_id": GT_A_ID,
            "condition_b_ground_truth_id": GT_B_ID,
            "condition_a_validation_record_id": "__REQUIRED_AFTER_EXECUTION__",
            "condition_b_validation_record_id": "__REQUIRED_AFTER_EXECUTION__",
            "candidate_population_comparison": "__REQUIRED_FROZEN_NUMERICAL_EVIDENCE__",
            "invariance_assessment": "__REQUIRED_EVIDENCE_CLASSIFIED_RESULT__",
            "limitations": [],
        },
    )

    write_json(
        RUN / "asset_status.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "generated": [
                str(symbolic_a.relative_to(ROOT)),
                str(symbolic_b.relative_to(ROOT)),
                str(inventory_path.relative_to(ROOT)),
                str(dgr_path.relative_to(ROOT)),
                str(
                    (PACKAGE / "ground_truth/condition_a.ground_truth.json").relative_to(
                        ROOT
                    )
                ),
                str(
                    (PACKAGE / "ground_truth/condition_b.ground_truth.json").relative_to(
                        ROOT
                    )
                ),
            ],
            "external_required": [
                "controlled_dataset/audio/condition_a.wav",
                "controlled_dataset/audio/condition_a_repeat.wav",
                "controlled_dataset/audio/condition_b.wav",
                "controlled_dataset/audio/condition_b_repeat.wav",
                "controlled_dataset/audio/condition_a.mp3",
                "controlled_dataset/audio/condition_b.mp3",
            ],
            "licensing_status": "not_specified",
            "package_validator_status": "BLOCKED_EXTERNAL_AUDIO_REQUIRED",
        },
    )

    (RUN / "runtime.log").write_text(
        "Command: PYTHONPATH=src python "
        "validation/VAL-001/run_20260809_171404/prepare_symbolic_conditions.py\n"
        "Result: exit 0\n"
        "JGA analytical output used for removal: no\n"
        "Terminal boundary: external lossless audio rendering required\n"
        "Command: python tools/validate_controlled_ab_package.py "
        "validation/VAL-001/run_20260809_171404/controlled_dataset\n"
        "Result: exit 1 (expected fail-closed external-asset boundary)\n",
        encoding="utf-8",
    )

    artifacts = {}
    for path in sorted(RUN.rglob("*")):
        if (
            not path.is_file()
            or path.name == "artifact_manifest.json"
            or "__pycache__" in path.parts
        ):
            continue
        artifacts[str(path.relative_to(RUN))] = file_sha256(path)
    write_json(
        RUN / "artifact_manifest.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "repository_revision": symbolic_validation["repository_revision"],
            "artifacts": artifacts,
        },
    )


if __name__ == "__main__":
    main()
