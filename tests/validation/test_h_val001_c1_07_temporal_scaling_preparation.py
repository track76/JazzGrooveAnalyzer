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


def test_completed_package_passes_asset_validation():
    status = json.loads((RUN / "asset_status.json").read_text())
    validation = json.loads((RUN / "audio_asset_validation.json").read_text())

    assert status["package_validation_status"] == "VALID"
    assert status["external_required"] == []
    assert validation["result"] == "VALID"
    assert validation["condition_b_distinct_from_c1_06"] is True
    assert validation["wav_measurements"]["a"]["canonical"] == {
        "bit_depth": 24,
        "channel_count": 2,
        "codec": "PCM",
        "duration_seconds": 44.977052154195015,
        "file_sha256": "33f8089ca9a09f711674dc272d7e3b6e2437080539aa046ed244158e599a08fd",
        "sample_count_per_channel": 1983488,
        "sample_rate_hz": 44100,
    }
    assert validation["wav_measurements"]["b"]["canonical"] == {
        "bit_depth": 24,
        "channel_count": 2,
        "codec": "PCM",
        "duration_seconds": 33.34385487528345,
        "file_sha256": "d05a259bc2f8468c9160cfec6efa7643bc1176354898fcf9e8336db09bee7c10",
        "sample_count_per_channel": 1470464,
        "sample_rate_hz": 44100,
    }


def test_blind_boundary_and_replay_are_preserved():
    blind = json.loads((RUN / "blind_results.json").read_text())

    assert blind["ground_truth_available"] is False
    assert blind["musicxml_available_to_analysis"] is False
    assert blind["condition_tempo_available_to_analysis"] is False
    assert blind["condition_assignment_revealed"] is False
    assert all(
        replay["identical"] for replay in blind["deterministic_replay"].values()
    )
    assert blind["independent_render_population_equality"] == {
        "BLIND-CONDITION-01": True,
        "BLIND-CONDITION-02": True,
    }


def test_blind_candidate_populations_are_frozen_without_interpretation():
    blind = json.loads((RUN / "blind_results.json").read_text())
    condition_a = blind["executions"]["BLIND-CONDITION-01"]
    condition_b = blind["executions"]["BLIND-CONDITION-02"]

    assert condition_a["pulse_candidate_count"] == 39
    assert condition_b["pulse_candidate_count"] == 39
    assert [candidate["duration_frames"] for candidate in condition_a["candidates"]] == [
        32, 33, 34, 66, 67, 99, 100, 133, 232
    ]
    assert [candidate["duration_frames"] for candidate in condition_b["candidates"]] == [
        23, 24, 47, 71, 116, 165
    ]


def test_post_blind_result_preserves_indeterminacy_without_tolerance():
    post = json.loads((RUN / "post_blind_evaluation.json").read_text())

    assert post["ground_truth"]["condition_a_tempo"] == {
        "beat_unit": "quarter",
        "beats_per_minute": "78",
    }
    assert post["ground_truth"]["condition_b_tempo"] == {
        "beat_unit": "quarter",
        "beats_per_minute": "110",
    }
    assert post["exact_authoritative_scale_pairs"] == []
    assert post["scientific_classification"] == "EVIDENCE INSUFFICIENT"
    assert "tolerance" in post["classification_rule"].lower()
