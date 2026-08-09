import json
from pathlib import Path
from xml.etree import ElementTree as ET

from jga.ground_truth.loaders import MusicXmlGroundTruthLoader


RUN = Path("validation/VAL-001/run_20260809_192908")
PACKAGE = RUN / "controlled_dataset"
AUTHORITATIVE = Path(
    "recordings/validation/ground_truth/"
    "03 THE COST OF LIVING versione intro + 8 bar.musicxml"
)


def _normalized_tree(path: Path) -> bytes:
    root = ET.parse(path).getroot()
    for per_minute in root.findall(".//per-minute"):
        per_minute.text = "__CONTROLLED_TEMPO__"
    return ET.tostring(root, encoding="utf-8")


def test_condition_a_is_exact_authoritative_source():
    assert (PACKAGE / "symbolic/condition_a.musicxml").read_bytes() == (
        AUTHORITATIVE.read_bytes()
    )


def test_condition_b_changes_only_authoritative_tempo_declarations():
    condition_a = PACKAGE / "symbolic/condition_a.musicxml"
    condition_b = PACKAGE / "symbolic/condition_b.musicxml"

    assert condition_a.read_bytes().count(b"<per-minute>78</per-minute>") == 2
    assert condition_b.read_bytes().count(b"<per-minute>110</per-minute>") == 2
    assert b"<per-minute>78</per-minute>" not in condition_b.read_bytes()
    assert _normalized_tree(condition_a) == _normalized_tree(condition_b)


def test_existing_ground_truth_schema_preserves_only_tempo_contrast():
    loaded = []
    for suffix in ("a", "b"):
        loaded.append(
            MusicXmlGroundTruthLoader(
                definition_path=(
                    PACKAGE / f"ground_truth/condition_{suffix}.ground_truth.json"
                )
            ).load(PACKAGE / f"symbolic/condition_{suffix}.musicxml")
        )

    condition_a, condition_b = loaded
    assert str(condition_a.tempo.beats_per_minute) == "78"
    assert str(condition_b.tempo.beats_per_minute) == "110"
    assert condition_a.tempo.beat_unit == condition_b.tempo.beat_unit == "quarter"
    assert condition_a.time_signature == condition_b.time_signature
    assert condition_a.instruments == condition_b.instruments
    assert condition_a.measures == condition_b.measures
    assert condition_a.sections == condition_b.sections


def test_package_remains_fail_closed_at_external_audio_boundary():
    status = json.loads((RUN / "asset_status.json").read_text())
    assert status["package_validation_status"] == "BLOCKED_EXTERNAL_AUDIO_REQUIRED"
    assert status["external_required"] == [
        "controlled_dataset/audio/condition_a.wav",
        "controlled_dataset/audio/condition_a_repeat.wav",
        "controlled_dataset/audio/condition_a.mp3",
        "controlled_dataset/audio/condition_b.wav",
        "controlled_dataset/audio/condition_b_repeat.wav",
        "controlled_dataset/audio/condition_b.mp3",
    ]
