import json
from pathlib import Path

import pytest

from jga.ground_truth.loaders import MusicXmlGroundTruthLoader
from tools.validate_controlled_ab_package import (
    PackageValidationError,
    validate_package,
)


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


def test_fail_closed_package_gate_stops_at_external_audio_boundary():
    with pytest.raises(PackageValidationError, match="Unresolved manifest"):
        validate_package(PACKAGE)
