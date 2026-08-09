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
    CandidatePeriodReproducibility,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_RECORD = (
    REPOSITORY_ROOT
    / "validation"
    / "VAL-001"
    / "run_20260809_100843"
    / "blind_candidate_discovery.json"
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
            experiment_id=record["experiment_id"],
            run_id=record["run_id"],
            source_revision=record["repository_revision"],
            scientific_protocol_id=record["scientific_protocol"],
            input_asset_path=source["asset_path"],
            input_asset_sha256=source["asset_sha256"],
        ),
        reproducibility=CandidatePeriodReproducibility(
            measurement_unit="seconds",
            sample_rate_hz=source["sample_rate"],
            frame_length_samples=source["hop_length"],
            first_execution_fingerprint=record[
                "first_execution_fingerprint"
            ],
            repeated_execution_fingerprint=record[
                "repeated_execution_fingerprint"
            ],
        ),
        candidates=candidates,
    )


def test_population_preserves_controlled_experimental_evidence() -> None:
    population = _population_from_preserved_evidence()

    assert population.observation_scope.source_identity == "full_mix"
    assert population.observation_scope.end_seconds == Decimal("42.24")
    assert population.provenance.experiment_id == "H-VAL001-C1-03"
    assert population.provenance.run_id == "run_20260809_100843"
    assert population.reproducibility.sample_rate_hz == 44100
    assert population.reproducibility.frame_length_samples == 512
    assert len(population.candidates) == 12
    assert population.candidates[3].duration_seconds == Decimal(
        "0.3831292517006803"
    )
    assert len(population.candidates[3].recurrence_evidence) == 16


def test_population_preserves_reproducibility_fingerprints() -> None:
    population = _population_from_preserved_evidence()

    assert (
        population.reproducibility.first_execution_fingerprint
        == "2825974a1c91c2b1645240e712bd90e27a568fba1336c82cebe27527c8bc43b9"
    )
    assert (
        population.reproducibility.repeated_execution_fingerprint
        == population.reproducibility.first_execution_fingerprint
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
        CandidatePeriodReproducibility,
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
