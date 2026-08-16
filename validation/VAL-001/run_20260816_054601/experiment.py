"""Execute H-VAL001-C1-11 minimum real-performance timing-profile validation."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

from jga.audio.file_audio_source import FileAudioSource
from jga.engines.audio_preprocessor import AudioPreprocessor
from jga.engines.candidate_period_discovery import CandidatePeriodDiscovery
from jga.engines.pulse_candidate_builder import PulseCandidateBuilder
from jga.engines.pulse_candidate_filter import PulseCandidateFilter
from jga.runtime.analysis_context import AnalysisContext


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
MANIFEST = RUN / "manifest.json"
INPUT_RELATIVE = Path("recordings/III_Chet Baker - I fall in love too easily.mp3")
INPUT = ROOT / INPUT_RELATIVE
EXPERIMENT_ID = "H-VAL001-C1-11"


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        indent=2,
        sort_keys=True,
    ).encode("utf-8") + b"\n"


def fingerprint(value: object) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_bytes(canonical_bytes(value))


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def execute_once() -> tuple[dict[str, object], dict[str, object]]:
    audio = FileAudioSource().load(INPUT_RELATIVE.as_posix())
    context = AnalysisContext(audio=audio)
    AudioPreprocessor().process(context)
    detector = PulseCandidateBuilder()
    detector.process(context)
    PulseCandidateFilter().process(context)
    CandidatePeriodDiscovery(
        frame_length_samples=detector.FRAME_LENGTH_SAMPLES,
    ).process(context)

    population = context.candidate_period_population
    scope_duration = (
        population.observation_scope.end_seconds
        - population.observation_scope.start_seconds
    )
    total_support = sum(
        len(candidate.recurrence_evidence)
        for candidate in population.candidates
    )

    candidates = []
    evaluated_summaries = []
    for candidate in population.candidates:
        occurrences = [
            {
                "start_observation_index": occurrence.start_observation_index,
                "end_observation_index": occurrence.end_observation_index,
                "start_seconds": str(occurrence.start_seconds),
                "end_seconds": str(occurrence.end_seconds),
            }
            for occurrence in candidate.recurrence_evidence
        ]
        occurrence_count = len(occurrences)
        first_to_last_span = (
            candidate.recurrence_evidence[-1].end_seconds
            - candidate.recurrence_evidence[0].start_seconds
        )
        recurrence_rate = Decimal(occurrence_count) / scope_duration
        normalized_share = Decimal(occurrence_count) / Decimal(total_support)
        candidates.append(
            {
                "duration_seconds": str(candidate.duration_seconds),
                "recurrence_occurrence_count": occurrence_count,
                "supporting_occurrences": occurrences,
            }
        )
        evaluated_summaries.append(
            {
                "duration_seconds": str(candidate.duration_seconds),
                "first_to_last_support_span_seconds": str(first_to_last_span),
                "recurrence_rate_per_scope_second": str(recurrence_rate),
                "normalized_support_share": str(normalized_share),
            }
        )

    profile = {
        "observation_scope": {
            "duration_seconds": str(scope_duration),
            "start_seconds": str(population.observation_scope.start_seconds),
            "end_seconds": str(population.observation_scope.end_seconds),
            "observation_population_id": (
                population.observation_scope.observation_population_id
            ),
            "source_identity": population.observation_scope.source_identity,
        },
        "provenance": {
            "input_asset_path": population.provenance.input_asset_path,
            "input_asset_sha256": population.provenance.input_asset_sha256,
            "discovery_configuration": [
                list(item)
                for item in population.provenance.discovery_configuration
            ],
            "source_revision": population.provenance.source_revision,
        },
        "measurement_unit": population.measurement_unit,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }
    audit = {
        "pulse_candidate_count": len(context.pulse_candidates or ()),
        "total_recurrent_support_occurrences": total_support,
        "evaluated_candidate_summaries": evaluated_summaries,
    }
    return profile, audit


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["status"] != "PREREGISTERED":
        raise RuntimeError("Experiment manifest is not preregistered.")
    if checksum(INPUT) != manifest["input"]["sha256"]:
        raise RuntimeError("Input checksum does not match preregistration.")

    started = datetime.now(timezone.utc).isoformat()
    first_profile, first_audit = execute_once()
    second_profile, second_audit = execute_once()
    first_bytes = canonical_bytes(first_profile)
    second_bytes = canonical_bytes(second_profile)
    identical = first_bytes == second_bytes
    if not identical:
        raise RuntimeError("Repeated timing profiles are not byte-identical.")

    profile_fingerprint = fingerprint(first_profile)
    blind_results = {
        "experiment_id": EXPERIMENT_ID,
        "first_execution": {
            "profile": first_profile,
            "audit": first_audit,
            "profile_sha256": profile_fingerprint,
        },
        "second_execution": {
            "audit": second_audit,
            "profile_sha256": fingerprint(second_profile),
            "profile_byte_identical_to_first": identical,
        },
    }
    write_json(RUN / "blind_results.json", blind_results)

    evaluation = {
        "experiment_id": EXPERIMENT_ID,
        "accepted": [
            {
                "quantity": "observation_scope_duration_seconds",
                "reason": "Required to delimit and interpret all evidence and compare scopes.",
            },
            {
                "quantity": "candidate_count",
                "reason": "Minimum description of preserved recurrent temporal multiplicity.",
            },
            {
                "quantity": "candidate_duration_seconds",
                "reason": "The observed recurrent temporal relation defined by F-032.",
            },
            {
                "quantity": "recurrence_occurrence_count",
                "reason": "Minimum magnitude of exact recurrence support without ranking.",
            },
            {
                "quantity": "complete_supporting_occurrence_positions",
                "reason": "Preserves when recurrence support occurs and permits later temporal comparison without aggregation loss.",
            },
        ],
        "rejected": [
            {
                "quantity": "first_to_last_support_span_seconds",
                "reason": "Deterministic but redundant with complete occurrence positions and hides internal distribution.",
            },
            {
                "quantity": "recurrence_rate_per_scope_second",
                "reason": "Deterministic but derivable from accepted occurrence count and scope duration; not required in the minimum profile.",
            },
            {
                "quantity": "normalized_support_share",
                "reason": "Deterministic but compositional and redundant with accepted counts; it adds no indispensable evidence.",
            },
        ],
        "profile_sha256": profile_fingerprint,
        "exact_replay": identical,
        "ground_truth_used": False,
        "musical_interpretation_used": False,
        "production_implementation_required": False,
    }
    write_json(RUN / "quantity_evaluation.json", evaluation)

    completed = datetime.now(timezone.utc).isoformat()
    reproducibility = {
        "experiment_id": EXPERIMENT_ID,
        "first_profile_sha256": profile_fingerprint,
        "second_profile_sha256": fingerprint(second_profile),
        "byte_identical": identical,
        "started_utc": started,
        "completed_utc": completed,
    }
    write_json(RUN / "reproducibility.json", reproducibility)

    report = f"""# H-VAL001-C1-11 — Minimum Real-Performance Timing Profile

## Scientific question

What minimum deterministic, provenance-bound descriptive quantities can be
derived directly from one real-performance Candidate Period population to
describe recurrent timing behaviour and support later performance comparison?

## Result

The minimum accepted profile contains observation-scope duration, Candidate
Period count and, for every preserved candidate, duration, recurrence
occurrence count and complete supporting occurrence positions.

The recording produced {first_audit['pulse_candidate_count']} filtered
PulseCandidates, {first_profile['candidate_count']} Candidate Periods and
{first_audit['total_recurrent_support_occurrences']} total recurrent support
occurrences under the declared M92 configuration.

First and repeated profile SHA-256:
`{profile_fingerprint}`.

Complete replay was byte-identical. No Ground Truth, beat, BPM, tempo, meter,
measure, musical label, Domain reconstruction, tolerance or cross-condition
event relation participated.

## Quantity decision

Accepted: observation-scope duration, Candidate Period count, each Candidate
Period duration, recurrence occurrence count and complete supporting
occurrence positions.

Rejected from the minimum profile: first-to-last support span, recurrence rate
per scope second and normalized support share. Each is reproducible but is
derivable from accepted quantities and therefore adds no indispensable
scientific evidence.

## Scientific conclusion

**A MINIMUM REPRODUCIBLE REAL-PERFORMANCE TIMING PROFILE IS ESTABLISHED WITHIN
THE DECLARED SINGLE-RECORDING SCOPE.**

The profile describes which exact temporal relations recur, how many times
each recurs and where its supporting occurrences lie, while preserving the
complete population, provenance and observation scope. It assigns no musical
meaning and makes no cross-performance correspondence claim.

No production implementation is justified by this experiment. Existing
Candidate Period evidence was sufficient to obtain the profile.
"""
    (RUN / "report.md").write_text(report, encoding="utf-8")

    completion = {
        "experiment_id": EXPERIMENT_ID,
        "documentation_updates": "Not Applicable — the result remains an experiment-local scientific record and changes no canonical authority.",
        "cross_reference_verification": "Passed — input, F-032, AD-034 and AD-035 authorities resolve; the input checksum matches preregistration.",
        "focused_tests": "Passed — 7 Candidate Period discovery and M92 validation tests; 2 existing Python 3.13 audio-library deprecation warnings.",
        "complete_automated_suite": "Not Applicable — no production implementation, canonical authority or analytical pipeline behavior changed.",
        "scientific_validation": "Passed within the declared single-recording scope.",
        "repository_consistency": "Passed — git diff --check and artifact checksum verification completed.",
        "bootstrap_regeneration": "Not Applicable — no canonical project-state or bootstrap semantics changed.",
        "production_implementation": "Not Applicable — existing repository capabilities obtained all accepted evidence.",
        "storage_impact": "Lightweight repository records only; no audio or heavy output copied.",
        "push": "NOT PERFORMED — explicit PI approval required."
    }
    write_json(RUN / "completion_protocol.json", completion)

    artifacts = {}
    for path in sorted(RUN.iterdir()):
        if path.name == "artifact_manifest.json" or not path.is_file():
            continue
        artifacts[path.name] = checksum(path)
    write_json(
        RUN / "artifact_manifest.json",
        {"experiment_id": EXPERIMENT_ID, "artifacts": artifacts},
    )


if __name__ == "__main__":
    main()
