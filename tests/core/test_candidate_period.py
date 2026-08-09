import json
from dataclasses import FrozenInstanceError, fields
from decimal import Decimal
from pathlib import Path

from pytest import mark, raises

from jga.core.candidate_period import (
    CandidatePeriod,
    CandidatePeriodObservationScope,
    CandidatePeriodOccurrence,
    CandidatePeriodPopulation,
    CandidatePeriodProvenance,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_RECORD = (
    REPOSITORY_ROOT
    / "validation"
    / "VAL-001"
    / "run_20260809_100843"
    / "blind_candidate_discovery.json"
)
RELATIONSHIP_AUDIT_MANIFEST = (
    REPOSITORY_ROOT
    / "validation"
    / "VAL-001"
    / "run_20260809_1344"
    / "manifest.json"
)


def _decimal(value: object) -> Decimal:
    return Decimal(str(value))


def _population_from_preserved_evidence(
    source_name: str = "full_mix",
) -> CandidatePeriodPopulation:
    record = json.loads(EXPERIMENT_RECORD.read_text())
    source = record["first_execution"][source_name]
    evidence = source["elementary_metric_event_distinct_population"]

    candidates = tuple(
        CandidatePeriod(
            duration_seconds=_decimal(candidate["duration_seconds"]),
            recurrence_evidence=tuple(
                CandidatePeriodOccurrence(
                    start_observation_index=occurrence["start_event_index"],
                    end_observation_index=occurrence["end_event_index"],
                    start_seconds=_decimal(occurrence["start_seconds"]),
                    end_seconds=_decimal(occurrence["end_seconds"]),
                )
                for occurrence in candidate["occurrences"]
            ),
        )
        for candidate in evidence[
            "recurrent_candidates_minimum_two_occurrences"
        ]
    )

    return CandidatePeriodPopulation(
        observation_scope=CandidatePeriodObservationScope(
            observation_population_id=(
                f"{source_name}:elementary_metric_event_distinct_population"
            ),
            source_identity=source["source_identity"],
            start_seconds=Decimal("0"),
            end_seconds=_decimal(source["audio_duration_seconds"]),
        ),
        provenance=CandidatePeriodProvenance(
            input_asset_path=source["asset_path"],
            input_asset_sha256=source["asset_sha256"],
            discovery_configuration=(
                ("sample_rate_hz", str(source["sample_rate"])),
                ("frame_length_samples", str(source["hop_length"])),
                (
                    "recurrence_definition",
                    record["discovery_configuration"]["recurrence_definition"],
                ),
            ),
            source_revision=record["repository_revision"],
        ),
        measurement_unit="seconds",
        candidates=candidates,
    )


def test_population_preserves_controlled_experimental_evidence() -> None:
    population = _population_from_preserved_evidence()

    assert population.observation_scope.source_identity == "full_mix"
    assert population.observation_scope.end_seconds == Decimal("42.24")
    assert population.measurement_unit == "seconds"
    assert ("sample_rate_hz", "44100") in (
        population.provenance.discovery_configuration
    )
    assert ("frame_length_samples", "512") in (
        population.provenance.discovery_configuration
    )
    assert len(population.candidates) == 12
    assert population.candidates[3].duration_seconds == Decimal(
        "0.3831292517006803"
    )
    assert len(population.candidates[3].recurrence_evidence) == 16


def test_population_does_not_require_experimental_validation_metadata() -> None:
    population = _population_from_preserved_evidence()

    provenance_fields = {
        field.name for field in fields(type(population.provenance))
    }
    assert provenance_fields.isdisjoint(
        {
            "experiment_id",
            "run_id",
            "scientific_protocol_id",
            "first_execution_fingerprint",
            "repeated_execution_fingerprint",
        }
    )


def test_candidate_period_population_is_deeply_immutable() -> None:
    population = _population_from_preserved_evidence()

    with raises(FrozenInstanceError):
        population.candidates = ()
    with raises(FrozenInstanceError):
        population.observation_scope.source_identity = "changed"
    with raises(FrozenInstanceError):
        population.candidates[0].duration_seconds = Decimal("1")
    with raises(FrozenInstanceError):
        population.candidates[0].recurrence_evidence[0].end_seconds = Decimal(
            "1"
        )


def test_candidate_period_requires_recurrence_evidence() -> None:
    occurrence = CandidatePeriodOccurrence(
        start_observation_index=0,
        end_observation_index=1,
        start_seconds=Decimal("0"),
        end_seconds=Decimal("0.5"),
    )

    with raises(ValueError, match="at least two"):
        CandidatePeriod(
            duration_seconds=Decimal("0.5"),
            recurrence_evidence=(occurrence,),
        )


def test_representation_contains_no_metric_interpretation_fields() -> None:
    representation_fields = set()
    for representation_type in (
        CandidatePeriodOccurrence,
        CandidatePeriod,
        CandidatePeriodObservationScope,
        CandidatePeriodProvenance,
        CandidatePeriodPopulation,
    ):
        representation_fields.update(
            field.name for field in fields(representation_type)
        )
    forbidden_fields = {
        "beat",
        "bpm",
        "tempo",
        "tactus",
        "subdivision",
        "meter",
        "confidence",
        "stability",
        "persistence",
        "locality",
        "ranking",
        "selection",
    }

    assert representation_fields.isdisjoint(forbidden_fields)


def test_source_revision_is_optional_for_runtime_population() -> None:
    provenance = CandidatePeriodProvenance(
        input_asset_path="recordings/example.wav",
        input_asset_sha256="a" * 64,
        discovery_configuration=(("frame_length_samples", "512"),),
    )

    assert provenance.source_revision is None


def test_validation_metadata_remains_in_scientific_record() -> None:
    manifest = json.loads(RELATIONSHIP_AUDIT_MANIFEST.read_text())

    assert manifest["experiment_id"] == "H-VAL001-C1-04"
    assert manifest["run_id"] == "run_20260809_1344"
    assert manifest["scientific_protocol"] == "SVP-001"
    assert manifest["blind_record_fingerprint"]
    assert manifest["post_blind_record_fingerprint"]


@mark.parametrize(
    ("source_name", "expected_candidate_count"),
    (
        ("double_bass", 4),
        ("drums", 6),
        ("piano", 10),
        ("tenor_sax", 2),
        ("voice", 23),
    ),
)
def test_population_preserves_each_controlled_wav_source(
    source_name: str,
    expected_candidate_count: int,
) -> None:
    population = _population_from_preserved_evidence(source_name)

    assert population.observation_scope.source_identity == source_name
    assert len(population.candidates) == expected_candidate_count
    assert population.provenance.input_asset_path.endswith(f"{source_name}.wav")
    assert len(population.provenance.input_asset_sha256) == 64
