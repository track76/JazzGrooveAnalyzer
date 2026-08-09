import json
from pathlib import Path

from jga.ground_truth.loaders import MusicXmlGroundTruthLoader
from tools.validate_controlled_ab_package import validate_package


RUN = Path("validation/VAL-001/run_20260809_171404")
PACKAGE = RUN / "controlled_dataset"
AUTHORITATIVE = Path(
    "recordings/validation/ground_truth/"
    "03 THE COST OF LIVING versione intro + 8 bar.musicxml"
)


def test_condition_a_is_exact_authoritative_symbolic_source():
    assert (PACKAGE / "symbolic/condition_a.musicxml").read_bytes() == (
        AUTHORITATIVE.read_bytes()
    )


def test_condition_b_preserves_only_odd_symbolic_events():
    inventory = json.loads(
        (PACKAGE / "provenance/event_removal_inventory.json").read_text()
    )
    events = inventory["events"]

    assert len(events) == 197
    assert sum(event["status"] == "retained" for event in events) == 99
    assert sum(event["status"] == "removed" for event in events) == 98
    assert all(
        (event["stable_symbolic_ordinal"] % 2 == 1)
        == (event["status"] == "retained")
        for event in events
    )
    assert all(
        event["condition_a_onset_seconds"]
        == event["condition_b_onset_seconds"]
        and event["condition_a_duration_seconds"]
        == event["condition_b_duration_seconds"]
        for event in events
        if event["status"] == "retained"
    )


def test_existing_ground_truth_schema_loads_both_symbolic_conditions():
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
    assert condition_a.tempo == condition_b.tempo
    assert condition_a.time_signature == condition_b.time_signature
    assert condition_a.instruments == condition_b.instruments
    assert condition_a.measures == condition_b.measures
    assert condition_a.sections == condition_b.sections


def test_completed_package_passes_fail_closed_validation():
    result = validate_package(PACKAGE)

    assert result["controlled_dataset_id"] == "CED-VAL-001-RD-001"
    assert result["inventory_event_count"] == 197
    assert result["wav_measurements"] == {
        "sample_rate_hz": 44100,
        "bit_depth": 24,
        "channel_count": 2,
        "sample_count_per_channel": 1983488,
    }


def test_blind_record_preserves_boundary_and_deterministic_replay():
    blind = json.loads((RUN / "blind_results.json").read_text())

    assert blind["ground_truth_available"] is False
    assert blind["musicxml_available_to_analysis"] is False
    assert blind["event_removal_inventory_available_to_analysis"] is False
    assert blind["condition_assignment_revealed"] is False
    assert all(
        replay["identical"] for replay in blind["deterministic_replay"].values()
    )


def test_repeat_renders_preserve_exact_candidate_duration_counts():
    evaluation = json.loads((RUN / "post_blind_evaluation.json").read_text())

    assert evaluation["canonical_repeat_exact_duration_count_equality"] == {
        "condition_a": True,
        "condition_b": True,
    }
    assert evaluation["exact_shared_candidate_durations_seconds"] == [
        "0.3831292517006803",
        "0.7662585034013606",
        "0.7778684807256236",
        "1.1493877551020408",
        "1.1609977324263039",
        "1.5441269841269842",
    ]


def test_validation_chain_preserves_not_produced_states():
    chain = json.loads((RUN / "validation_chain_results.json").read_text())
    expected = {
        "tempo": "NOT_PRODUCED",
        "time_signature": "NOT_PRODUCED",
        "sections": "NOT_PRODUCED",
        "instrumentation": "NOT_PRODUCED",
    }

    assert chain["condition_a"]["comparison_states"] == expected
    assert chain["condition_b"]["comparison_states"] == expected
    assert chain["condition_a"]["scientific_validation_record_id"].startswith(
        "JGA-SVR-"
    )
    assert chain["condition_b"]["scientific_validation_record_id"].startswith(
        "JGA-SVR-"
    )


def test_repeat_render_difference_is_preserved_without_equivalence_claim():
    audio = json.loads((RUN / "audio_asset_validation.json").read_text())

    for condition in ("a", "b"):
        canonical = audio["conditions"][condition]["canonical"]
        repeated = audio["conditions"][condition]["repeat"]
        difference = audio["conditions"][condition]["difference"]
        assert canonical["sample_rate_hz"] == repeated["sample_rate_hz"] == 44100
        assert canonical["sample_count_per_channel"] == repeated[
            "sample_count_per_channel"
        ] == 1983488
        assert difference["file_bytes_identical"] is False
        assert difference["sample_values_identical"] is False
