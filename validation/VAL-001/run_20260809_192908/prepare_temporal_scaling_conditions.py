"""Prepare H-VAL001-C1-07 to the external audio-rendering boundary."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
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

EXPERIMENT_ID = "H-VAL001-C1-07"
DATASET_ID = "CED-VAL-001-TS-001"
DGR_ID = "DGR-CED-VAL-001-TS-001-001"
PROVENANCE_ID = "PR-CED-VAL-001-TS-001-001"
CONDITION_A_ID = "CED-VAL-001-TS-001-A"
CONDITION_B_ID = "CED-VAL-001-TS-001-B"
VAL_A_ID = "VAL-001-TS-A"
VAL_B_ID = "VAL-001-TS-B"
GT_A_ID = "GT-VAL-001-TS-A-v1"
GT_B_ID = "GT-VAL-001-TS-B-v1"


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


def normalized_symbolic_tree(path: Path) -> bytes:
    root = ET.parse(path).getroot()
    for per_minute in root.findall(".//per-minute"):
        per_minute.text = "__CONTROLLED_TEMPO__"
    return ET.tostring(root, encoding="utf-8")


def condition_manifest(
    condition_id: str,
    validation_item_id: str,
    ground_truth_id: str,
    tempo_bpm: str,
    suffix: str,
) -> dict[str, object]:
    xml_path = PACKAGE / f"symbolic/condition_{suffix}.musicxml"
    gt_path = PACKAGE / f"ground_truth/condition_{suffix}.ground_truth.json"
    return {
        "condition_id": condition_id,
        "validation_item_id": validation_item_id,
        "ground_truth_id": ground_truth_id,
        "authoritative_tempo": {
            "beats_per_minute": tempo_bpm,
            "beat_unit": "quarter",
        },
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


def main() -> None:
    source = SOURCE_XML.read_bytes()
    old = b"<per-minute>78</per-minute>"
    new = b"<per-minute>110</per-minute>"
    if source.count(old) != 2:
        raise ValueError("Expected exactly two authoritative tempo declarations")

    symbolic_a = PACKAGE / "symbolic/condition_a.musicxml"
    symbolic_b = PACKAGE / "symbolic/condition_b.musicxml"
    symbolic_a.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_XML, symbolic_a)
    symbolic_b.write_bytes(source.replace(old, new))

    if symbolic_a.read_bytes() != source:
        raise ValueError("Condition A is not the authoritative source bytes")
    if symbolic_b.read_bytes().count(new) != 2 or old in symbolic_b.read_bytes():
        raise ValueError("Condition B tempo replacement is incomplete")
    if normalized_symbolic_tree(symbolic_a) != normalized_symbolic_tree(symbolic_b):
        raise ValueError("A symbolic property other than tempo changed")

    source_gt = json.loads(SOURCE_GT.read_text(encoding="utf-8"))
    for suffix, gt_id, val_id, source_path in (
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
            PACKAGE / f"ground_truth/condition_{suffix}.ground_truth.json",
            definition,
        )

    audio_dir = PACKAGE / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    (audio_dir / "README.md").write_text(
        "# External audio boundary\n\n"
        "Place the six independently exported assets declared in the Dataset "
        "Generation Record in this directory. Do not substitute existing "
        "renders.\n",
        encoding="utf-8",
    )

    dgr_path = PACKAGE / "provenance/dataset_generation_record.md"
    dgr_path.parent.mkdir(parents=True, exist_ok=True)
    dgr_path.write_text(
        f"""# {DGR_ID} — Controlled Temporal-Scaling Dataset Generation Record

## Identities

- Controlled Dataset ID: `{DATASET_ID}`
- Dataset Generation Record ID: `{DGR_ID}`
- Provenance Revision ID: `{PROVENANCE_ID}`
- Condition A ID: `{CONDITION_A_ID}`
- Condition B ID: `{CONDITION_B_ID}`

## Declared Experimental Procedure

Condition A is an exact copy of the authoritative VAL-001 MusicXML source and
declares quarter note = 78 BPM. Condition B is derived from the same source by
changing only both authoritative `<per-minute>` declarations from `78` to
`110`. No JGA output participates in this transformation.

Symbolic event identities, document order, pitches, score positions, symbolic
durations, meter, instrumentation, dynamics, articulations and source identity
remain identical. Only authoritative tempo differs.

## Symbolic assets

- Condition A: `{symbolic_a.relative_to(ROOT)}` — `{file_sha256(symbolic_a)}`
- Condition B: `{symbolic_b.relative_to(ROOT)}` — `{file_sha256(symbolic_b)}`

## External rendering procedure

Render both conditions from score time zero using the same Sibelius version,
sound library, playback configuration, mixer settings and export settings.
Preserve leading, internal and trailing silence. Export each canonical WAV and
each repeated WAV independently. Do not reuse or time-stretch an existing
render.

Required WAV format: PCM, 24-bit, 44.1 kHz, stereo. The A and B sample counts
are expected to differ because tempo is the controlled variable; canonical and
repeat renders within each condition must preserve the same temporal extent.
Create one MP3 derivative from each canonical condition for the existing
schema-1 Validation Item binding, using identical MP3 export settings.

Generating application version, rendering-library version, generation date,
rendering configuration and MP3 encoder configuration remain `not specified`
until supplied by the human renderer. Licensing status is `not_specified`.
""",
        encoding="utf-8",
    )

    manifest = {
        "experiment_id": EXPERIMENT_ID,
        "controlled_dataset_id": DATASET_ID,
        "dataset_generation_record_id": DGR_ID,
        "provenance_revision_id": PROVENANCE_ID,
        "relationship": "conditions_differ_only_in_authoritative_tempo",
        "knowledge_classification": "Declared Experimental Procedure",
        "controlled_audio_format": {
            "sample_rate_hz": 44100,
            "bit_depth": 24,
            "channel_count": 2,
            "within_condition_repeat_sample_count_identical": True,
            "cross_condition_sample_count_identical": False,
        },
        "condition_a": condition_manifest(
            CONDITION_A_ID, VAL_A_ID, GT_A_ID, "78", "a"
        ),
        "condition_b": condition_manifest(
            CONDITION_B_ID, VAL_B_ID, GT_B_ID, "110", "b"
        ),
        "dataset_generation_record": {
            "repository_path": str(dgr_path.relative_to(PACKAGE)),
            "sha256": file_sha256(dgr_path),
        },
    }
    write_json(PACKAGE / "controlled_dataset_manifest.json", manifest)

    items = []
    for suffix, val_id, gt_id, title in (
        ("a", VAL_A_ID, GT_A_ID, "VAL-001 temporal scaling Condition A"),
        ("b", VAL_B_ID, GT_B_ID, "VAL-001 temporal scaling Condition B"),
    ):
        xml_path = PACKAGE / f"symbolic/condition_{suffix}.musicxml"
        items.append(
            {
                "validation_item_id": val_id,
                "ground_truth_id": gt_id,
                "authoritative_musicxml": {
                    "repository_path": str(xml_path.relative_to(ROOT)),
                    "sha256": file_sha256(xml_path),
                    "repository_revision": None,
                    "licensing_status": "not_specified",
                },
                "mp3_recording": {
                    "repository_path": str(
                        (PACKAGE / f"audio/condition_{suffix}.mp3").relative_to(ROOT)
                    ),
                    "sha256": "__REQUIRED_EXTERNAL_SHA256__",
                    "repository_revision": None,
                    "licensing_status": "not_specified",
                },
                "provenance": {"schema_version": "1", "item_version": "1"},
                "metadata": {"title": title},
            }
        )
    write_json(
        PACKAGE / "pending_catalog_items.json",
        {"status": "NOT_REGISTERED_EXTERNAL_AUDIO_REQUIRED", "items": items},
    )

    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    symbolic_validation = {
        "experiment_id": EXPERIMENT_ID,
        "repository_revision": revision,
        "condition_a_exact_authoritative_copy": symbolic_a.read_bytes() == source,
        "condition_a_sha256": file_sha256(symbolic_a),
        "condition_b_sha256": file_sha256(symbolic_b),
        "condition_a_tempo_declaration_count": symbolic_a.read_bytes().count(old),
        "condition_b_tempo_declaration_count": symbolic_b.read_bytes().count(new),
        "normalized_symbolic_content_identical": (
            normalized_symbolic_tree(symbolic_a)
            == normalized_symbolic_tree(symbolic_b)
        ),
        "intended_changed_variable": "authoritative_tempo",
        "condition_a_tempo": {"beats_per_minute": "78", "beat_unit": "quarter"},
        "condition_b_tempo": {"beats_per_minute": "110", "beat_unit": "quarter"},
        "jga_output_used_in_preparation": False,
        "audio_generation_status": "BLOCKED_EXTERNAL_RENDER_REQUIRED",
    }
    write_json(RUN / "symbolic_validation.json", symbolic_validation)

    write_json(
        RUN / "experiment_manifest.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "scientific_protocol": "SVP-001",
            "repository_revision": revision,
            "controlled_dataset_id": DATASET_ID,
            "dataset_generation_record_id": DGR_ID,
            "package_manifest_path": str(
                (PACKAGE / "controlled_dataset_manifest.json").relative_to(ROOT)
            ),
            "blind_configuration": {
                "condition_execution_identities": [
                    "BLIND-CONDITION-01",
                    "BLIND-CONDITION-02",
                ],
                "analysis_input": "canonical lossless WAV",
                "candidate_discovery": "AD-035 existing production configuration",
                "condition_assignment_hidden": True,
                "ground_truth_unavailable_until_blind_freeze": True,
                "identical_observation_configuration": True,
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
            "ground_truth_available_during_analysis": False,
            "musicxml_available_during_analysis": False,
            "condition_tempo_available_during_analysis": False,
            "analysis_pipeline": "existing approved AnalysisPipeline",
            "candidate_period_discovery": "AD-035 existing production mechanism",
            "discovery_configuration_identical": True,
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
            "temporal_scaling_assessment": "__REQUIRED_EVIDENCE_CLASSIFIED_RESULT__",
            "limitations": [],
        },
    )

    external = [
        f"controlled_dataset/audio/condition_{suffix}{ending}"
        for suffix in ("a", "b")
        for ending in (".wav", "_repeat.wav", ".mp3")
    ]
    write_json(
        RUN / "asset_status.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "external_required": external,
            "licensing_status": "not_specified",
            "package_validation_status": "BLOCKED_EXTERNAL_AUDIO_REQUIRED",
        },
    )

    (RUN / "report.md").write_text(
        f"""# {EXPERIMENT_ID} — Controlled Temporal-Scaling Preparation

## Status

Prepared to the external audio-rendering boundary. No blind analysis, Ground
Truth comparison, Candidate Period comparison or interpretation has executed.

## Conditions

- Condition A: `{CONDITION_A_ID}` — quarter note = 78 BPM
- Condition B: `{CONDITION_B_ID}` — quarter note = 110 BPM

Condition A is byte-identical to the authoritative VAL-001 MusicXML. Condition
B differs only in both authoritative `<per-minute>` values. Normalized symbolic
content is identical. No JGA output participated in preparation.

## External boundary

The six files listed in `asset_status.json` must be generated externally under
the procedure in `{dgr_path.relative_to(ROOT)}`. Blind analysis remains
prohibited until their identities, formats and within-condition repeat extents
are verified.
""",
        encoding="utf-8",
    )
    (RUN / "notes.md").write_text(
        "# H-VAL001-C1-07 notes\n\n"
        "- Tempo and condition identity remain unavailable during blind analysis.\n"
        "- Ground Truth is loaded only after both Candidate Populations are frozen.\n"
        "- Licensing remains `not_specified`; repository presence implies no rights.\n",
        encoding="utf-8",
    )
    (RUN / "runtime.log").write_text(
        "Preparation completed without JGA analysis.\n"
        "Terminal boundary: external lossless audio rendering required.\n",
        encoding="utf-8",
    )

    artifacts = {}
    for path in sorted(RUN.rglob("*")):
        if not path.is_file() or path.name == "artifact_manifest.json":
            continue
        artifacts[str(path.relative_to(RUN))] = file_sha256(path)
    write_json(
        RUN / "artifact_manifest.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "repository_revision": revision,
            "artifacts": artifacts,
        },
    )


if __name__ == "__main__":
    main()
