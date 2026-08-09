from dataclasses import FrozenInstanceError
from decimal import Decimal
import json
from pathlib import Path

import pytest

from jga.ground_truth.loaders import MusicXmlGroundTruthLoader


SOURCE = Path(
    "recordings/validation/ground_truth/"
    "03 THE COST OF LIVING versione intro + 8 bar.musicxml"
)


def test_loads_approved_ground_truth_identity_and_binding():
    ground_truth = MusicXmlGroundTruthLoader().load(SOURCE)

    assert ground_truth.ground_truth_id == "GT-VAL-001-v1"
    assert ground_truth.validation_item_id == "VAL-001"


def test_preserves_source_and_normalization_provenance():
    ground_truth = MusicXmlGroundTruthLoader().load(SOURCE)

    assert ground_truth.provenance.schema_version == "1"
    assert ground_truth.provenance.normalization_version == "1"
    assert ground_truth.provenance.source.repository_path == SOURCE.as_posix()
    assert ground_truth.provenance.source.sha256 == (
        "809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778"
    )
    assert ground_truth.provenance.source.repository_revision == (
        "c50abd435097b8f335a53b4146d9fa933764b15f"
    )


def test_represents_only_approved_metric_quantities():
    ground_truth = MusicXmlGroundTruthLoader().load(SOURCE)

    assert ground_truth.time_signature.beats == 4
    assert ground_truth.time_signature.beat_type == 4
    assert ground_truth.tempo.beats_per_minute == Decimal("78")
    assert ground_truth.tempo.beat_unit == "quarter"
    assert not hasattr(ground_truth, "beats")
    assert not hasattr(ground_truth, "events")


def test_preserves_pickup_and_full_measure_mapping():
    ground_truth = MusicXmlGroundTruthLoader().load(SOURCE)

    pickup = ground_truth.measures[0]
    assert pickup.source_measure_id == "1"
    assert pickup.normalized_full_measure is None
    assert pickup.is_pickup is True

    assert len(ground_truth.measures) == 13
    assert tuple(
        measure.normalized_full_measure for measure in ground_truth.measures[1:]
    ) == tuple(range(1, 13))
    assert ground_truth.measures[5].source_measure_id == "6"
    assert ground_truth.measures[5].normalized_full_measure == 5


def test_preserves_approved_section_boundaries():
    ground_truth = MusicXmlGroundTruthLoader().load(SOURCE)

    intro, section_a = ground_truth.sections
    assert (intro.name, intro.start_full_measure, intro.measure_count) == (
        "Intro",
        1,
        4,
    )
    assert (
        section_a.name,
        section_a.start_full_measure,
        section_a.measure_count,
    ) == ("A", 5, 8)


def test_preserves_original_and_canonical_instrument_designations():
    ground_truth = MusicXmlGroundTruthLoader().load(SOURCE)

    assert tuple(
        (
            instrument.source_part_name,
            instrument.source_instrument_name,
            instrument.canonical_category,
        )
        for instrument in ground_truth.instruments
    ) == (
        ("Voce", "Voice (2)", "Voice"),
        ("Sax Tenore", "Tenor Saxophone (2)", "Saxophone"),
        ("Piano", "Piano (2)", "Piano"),
        ("Basso Verticale", "Upright Bass", "Double Bass"),
        ("Set di batteria", "Drum Set (Jazz)", "Drum Set"),
    )


def test_ground_truth_is_deeply_immutable():
    ground_truth = MusicXmlGroundTruthLoader().load(SOURCE)

    with pytest.raises(FrozenInstanceError):
        ground_truth.ground_truth_id = "changed"

    with pytest.raises(FrozenInstanceError):
        ground_truth.provenance.schema_version = "changed"

    with pytest.raises(FrozenInstanceError):
        ground_truth.measures[0].is_pickup = False


def test_loading_is_deterministic():
    loader = MusicXmlGroundTruthLoader()

    assert loader.load(SOURCE) == loader.load(SOURCE)


def test_rejects_non_authoritative_source_identity(tmp_path):
    copy = tmp_path / SOURCE.name
    copy.write_bytes(SOURCE.read_bytes())

    definition_path = SOURCE.with_suffix(".ground_truth.json")
    definition = json.loads(definition_path.read_text())
    copied_definition = tmp_path / definition_path.name
    copied_definition.write_text(json.dumps(definition))

    with pytest.raises(ValueError, match="source identity"):
        MusicXmlGroundTruthLoader(
            repository_root=tmp_path,
            definition_path=Path(definition_path.name),
        ).load(Path(SOURCE.name))


def test_ground_truth_identity_and_normalization_are_loaded_from_data(tmp_path):
    source = tmp_path / SOURCE
    source.parent.mkdir(parents=True)
    source.write_bytes(SOURCE.read_bytes())

    definition_path = SOURCE.with_suffix(".ground_truth.json")
    definition = json.loads(definition_path.read_text())
    definition["ground_truth_id"] = "TEST-GROUND-TRUTH"
    definition["validation_item_id"] = "TEST-ITEM"
    destination = tmp_path / definition_path
    destination.write_text(json.dumps(definition))

    result = MusicXmlGroundTruthLoader(repository_root=tmp_path).load(SOURCE)

    assert result.ground_truth_id == "TEST-GROUND-TRUTH"
    assert result.validation_item_id == "TEST-ITEM"
    assert result.sections == MusicXmlGroundTruthLoader().load(SOURCE).sections
