"""Execute H-VAL001-EME-PHASE-01 without musical Ground Truth access."""

from __future__ import annotations

import hashlib
import json
import math
import multiprocessing
import os
import platform
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

import numpy as np
import scipy
from scipy.optimize import linear_sum_assignment
from scipy.special import i0e, i1e, logsumexp

from jga.domain.declared_metric_reference import (
    DeclaredMetricReference,
    MetricReferenceProvenance,
)
from jga.domain.declared_metric_timeline import (
    DeclaredAnalysisScope,
    DeclaredQuarterPhaseOrigin,
)
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline


EXPERIMENT_ID = "H-VAL001-EME-PHASE-01"
PREREG_SHA256 = "8e33eb2530fc6823209a457b173da03dea46ba64104a8eea6d085c32ec3a3ebf"
INPUT_SHA256 = "ce684b7062d78c96de4e2520dc9dfbededf605aaf671ec2f03814d97347f5785"
MUSICXML_SHA256 = "809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778"
SCOPE_END = Decimal(1865728) / Decimal(44100)
PERIOD = Decimal(10) / Decimal(13)
PHASE_RESOLUTION = float(Decimal(832) / Decimal(55125))
BOOTSTRAPS = 2000
BOOTSTRAP_STABILITY = 0.95
SERIAL_DIGITS = 12
EM_MAX_ITER = 1000
EM_TOLERANCE = 1e-10
INITIALIZATION_COUNT = 8
ROOT = Path(__file__).resolve().parents[3]
RUN_DIR = Path(__file__).resolve().parent
PREREG = ROOT / "validation/VAL-001/preregistrations/H-VAL001-EME-PHASE-01.md"
INPUT = ROOT / "validation/VAL-001/run_20260816_180111/result.json"
SOURCES = (
    ("Drums", "drums.wav", "d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd", 63),
    ("Piano", "piano.wav", "26fa1158f375598cc7c01e04379c00547ef1787f6862eb2f29a36aafd9007c7e", 49),
    ("Double Bass", "double_bass.wav", "31d6f2e34d360c6f8f75362187433f2a2c1f5eb5cbbfe627305e99d07d8be6c5", 27),
    ("Tenor Sax", "tenor_sax.wav", "89dd7e5c6063d3c4d5e4ac59c9119c265df4257dfb1b4a1e01b5f117ee87182e", 16),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_seed(contributor: str) -> int:
    raw = hashlib.sha256(f"{EXPERIMENT_ID}:{contributor}".encode()).digest()
    return int.from_bytes(raw[:8], "big")


def a1(kappa: float | np.ndarray) -> float | np.ndarray:
    return i1e(kappa) / i0e(kappa)


def inverse_a1(resultant: float, maximum: float) -> float:
    if resultant <= 1e-15:
        return 0.0
    resultant = min(resultant, float(a1(maximum)))
    if resultant < 0.53:
        estimate = 2 * resultant + resultant**3 + 5 * resultant**5 / 6
    elif resultant < 0.85:
        estimate = -0.4 + 1.39 * resultant + 0.43 / (1 - resultant)
    else:
        estimate = 1 / (resultant**3 - 4 * resultant**2 + 3 * resultant)
    estimate = min(maximum, max(0.0, estimate))
    for _ in range(8):
        ratio = float(a1(estimate)) if estimate > 0 else 0.0
        derivative = 1.0 - ratio * ratio - (ratio / estimate if estimate > 0 else 0.5)
        if derivative <= 0:
            break
        updated = min(maximum, max(0.0, estimate - (ratio - resultant) / derivative))
        if abs(updated - estimate) <= 1e-12 * max(1.0, estimate):
            return updated
        estimate = updated
    return estimate


TARGET_RESULTANT = math.exp(-0.5 * (2.0 * math.pi * PHASE_RESOLUTION) ** 2)
KAPPA_MAX = inverse_a1(TARGET_RESULTANT, 1e8)


def log_von_mises(theta: np.ndarray, center: float, kappa: float) -> np.ndarray:
    log_i0 = math.log(float(i0e(kappa))) + abs(kappa)
    return kappa * np.cos(theta - center) - math.log(2.0 * math.pi) - log_i0


def circular_sd_turns(kappa: float) -> float:
    if kappa <= 0.0:
        return math.inf
    return math.sqrt(max(0.0, -2.0 * math.log(float(a1(kappa))))) / (2.0 * math.pi)


@dataclass(frozen=True)
class Fit:
    k: int
    admissible: bool
    convergence: bool
    rejection_reason: str | None
    log_likelihood: float
    bic: float
    iterations: int
    centers: tuple[float, ...]
    kappas: tuple[float, ...]
    circular_sd: tuple[float, ...]
    weights: tuple[float, ...]
    effective_memberships: tuple[float, ...]


def serialize_number(value: float) -> float:
    return round(float(value), SERIAL_DIGITS)


def uniform_fit(n: int) -> Fit:
    ll = -n * math.log(2.0 * math.pi)
    return Fit(0, True, True, None, ll, -2.0 * ll, 0, (), (), (), (), ())


def initialization(theta: np.ndarray, k: int, start: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    # Equally spaced centers with preregistered deterministic rotations do not
    # encode expected musical locations. Data enter only during likelihood fit.
    offset = (start / INITIALIZATION_COUNT) * (2.0 * math.pi / k)
    centers = (offset + 2.0 * math.pi * np.arange(k) / k) % (2.0 * math.pi)
    weights = np.full(k, 1.0 / k)
    kappas = np.ones(k)
    return centers, kappas, weights


def one_em(theta: np.ndarray, k: int, start: int) -> tuple[bool, int, float, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    centers, kappas, weights = initialization(theta, k, start)
    previous = -math.inf
    responsibilities = np.empty((len(theta), k))
    converged = False
    for iteration in range(1, EM_MAX_ITER + 1):
        log_i0 = np.log(i0e(kappas)) + np.abs(kappas)
        log_terms = (
            np.log(np.maximum(weights, 1e-300))[None, :]
            + kappas[None, :] * np.cos(theta[:, None] - centers[None, :])
            - math.log(2.0 * math.pi)
            - log_i0[None, :]
        )
        normalizer = logsumexp(log_terms, axis=1)
        ll = float(normalizer.sum())
        responsibilities = np.exp(log_terms - normalizer[:, None])
        effective = responsibilities.sum(axis=0)
        weights = effective / len(theta)
        for j in range(k):
            vector = np.sum(responsibilities[:, j] * np.exp(1j * theta))
            centers[j] = float(np.angle(vector) % (2.0 * math.pi))
            resultant = abs(vector) / max(float(effective[j]), 1e-300)
            kappas[j] = inverse_a1(float(resultant), KAPPA_MAX)
        if abs(ll - previous) <= EM_TOLERANCE:
            converged = True
            break
        previous = ll
    log_i0 = np.log(i0e(kappas)) + np.abs(kappas)
    log_terms = (
        np.log(np.maximum(weights, 1e-300))[None, :]
        + kappas[None, :] * np.cos(theta[:, None] - centers[None, :])
        - math.log(2.0 * math.pi)
        - log_i0[None, :]
    )
    normalizer = logsumexp(log_terms, axis=1)
    ll = float(normalizer.sum())
    responsibilities = np.exp(log_terms - normalizer[:, None])
    effective = responsibilities.sum(axis=0)
    return converged, iteration, ll, centers, kappas, weights, effective


def all_em(theta: np.ndarray, k: int) -> list[tuple[bool, int, float, np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
    initial = [initialization(theta, k, start) for start in range(INITIALIZATION_COUNT)]
    centers = np.stack([item[0] for item in initial])
    kappas = np.stack([item[1] for item in initial])
    weights = np.stack([item[2] for item in initial])
    previous = np.full(INITIALIZATION_COUNT, -math.inf)
    converged = np.zeros(INITIALIZATION_COUNT, dtype=bool)
    iterations = np.full(INITIALIZATION_COUNT, EM_MAX_ITER, dtype=int)
    for iteration in range(1, EM_MAX_ITER + 1):
        log_i0 = np.log(i0e(kappas)) + np.abs(kappas)
        log_terms = (
            np.log(np.maximum(weights, 1e-300))[:, None, :]
            + kappas[:, None, :] * np.cos(theta[None, :, None] - centers[:, None, :])
            - math.log(2.0 * math.pi)
            - log_i0[:, None, :]
        )
        normalizer = logsumexp(log_terms, axis=2)
        likelihoods = normalizer.sum(axis=1)
        responsibilities = np.exp(log_terms - normalizer[:, :, None])
        effective = responsibilities.sum(axis=1)
        new_weights = effective / len(theta)
        vectors = np.sum(responsibilities * np.exp(1j * theta)[None, :, None], axis=1)
        new_centers = np.angle(vectors) % (2.0 * math.pi)
        resultants = np.abs(vectors) / np.maximum(effective, 1e-300)
        new_kappas = np.empty_like(kappas)
        for start in range(INITIALIZATION_COUNT):
            for component in range(k):
                new_kappas[start, component] = inverse_a1(float(resultants[start, component]), KAPPA_MAX)
        newly_converged = (~converged) & (np.abs(likelihoods - previous) <= EM_TOLERANCE)
        iterations[newly_converged] = iteration
        active = ~converged
        weights[active] = new_weights[active]
        centers[active] = new_centers[active]
        kappas[active] = new_kappas[active]
        converged |= newly_converged
        previous[active] = likelihoods[active]
        if np.all(converged):
            break
    results = []
    for start in range(INITIALIZATION_COUNT):
        log_i0 = np.log(i0e(kappas[start])) + np.abs(kappas[start])
        terms = (
            np.log(np.maximum(weights[start], 1e-300))[None, :]
            + kappas[start][None, :] * np.cos(theta[:, None] - centers[start][None, :])
            - math.log(2.0 * math.pi)
            - log_i0[None, :]
        )
        normalizer = logsumexp(terms, axis=1)
        responsibilities = np.exp(terms - normalizer[:, None])
        results.append(
            (
                bool(converged[start]),
                int(iterations[start]),
                float(normalizer.sum()),
                centers[start].copy(),
                kappas[start].copy(),
                weights[start].copy(),
                responsibilities.sum(axis=0),
            )
        )
    return results


def fit_model(phases: np.ndarray, k: int) -> Fit:
    theta = phases * (2.0 * math.pi)
    attempts = all_em(theta, k)
    best = max(attempts, key=lambda item: (item[2], -item[1]))
    converged, iterations, ll, centers, kappas, weights, effective = best
    order = np.argsort(centers)
    centers = centers[order] / (2.0 * math.pi)
    kappas, weights, effective = kappas[order], weights[order], effective[order]
    dispersions = np.array([circular_sd_turns(value) for value in kappas])
    reasons: list[str] = []
    if not converged:
        reasons.append("NON_CONVERGENCE")
    if np.any(effective < 3.0):
        reasons.append("EFFECTIVE_MEMBERSHIP_BELOW_3")
    if np.any(dispersions + 1e-15 < PHASE_RESOLUTION):
        reasons.append("BELOW_MEASUREMENT_RESOLUTION")
    admissible = not reasons
    p = 3 * k - 1
    bic = p * math.log(len(phases)) - 2.0 * ll
    return Fit(
        k,
        admissible,
        converged,
        ";".join(reasons) or None,
        serialize_number(ll),
        serialize_number(bic),
        iterations,
        tuple(serialize_number(value % 1.0) for value in centers),
        tuple(serialize_number(value) for value in kappas),
        tuple(serialize_number(value) for value in dispersions),
        tuple(serialize_number(value) for value in weights),
        tuple(serialize_number(value) for value in effective),
    )


def fit_candidates(phases: np.ndarray) -> tuple[list[Fit], Fit]:
    fits = [uniform_fit(len(phases))]
    fits.extend(fit_model(phases, k) for k in range(1, len(phases) // 3 + 1))
    admissible = [fit for fit in fits if fit.admissible]
    selected = min(admissible, key=lambda fit: (fit.bic, fit.k))
    return fits, selected


def match_components(reference: Fit, candidate: Fit) -> tuple[np.ndarray, np.ndarray, np.ndarray] | None:
    if reference.k == 0 or candidate.k != reference.k:
        return None
    distance = np.empty((reference.k, candidate.k))
    for i, left in enumerate(reference.centers):
        for j, right in enumerate(candidate.centers):
            delta = abs(left - right)
            distance[i, j] = min(delta, 1.0 - delta)
    rows, cols = linear_sum_assignment(distance)
    ordered = cols[np.argsort(rows)]
    centers = np.asarray(candidate.centers)[ordered]
    weights = np.asarray(candidate.weights)[ordered]
    kappas = np.asarray(candidate.kappas)[ordered]
    unwrapped = np.empty_like(centers)
    for index, (center, origin) in enumerate(zip(centers, reference.centers, strict=True)):
        unwrapped[index] = origin + ((center - origin + 0.5) % 1.0 - 0.5)
    return unwrapped, weights, kappas


def bootstrap_fit(phases: np.ndarray) -> Fit:
    return fit_candidates(phases)[1]


def percentile_interval(values: list[float], circular: bool = False) -> list[float] | None:
    if not values:
        return None
    low, high = np.percentile(np.asarray(values), [2.5, 97.5])
    if circular:
        return [serialize_number(low % 1.0), serialize_number(high % 1.0)]
    return [serialize_number(low), serialize_number(high)]


def analyze_phases(phases: np.ndarray, contributor: str) -> dict[str, Any]:
    fits, selected = fit_candidates(phases)
    seed = stable_seed(contributor)
    rng = np.random.default_rng(seed)
    selected_counts: Counter[int] = Counter()
    matched_centers = [[] for _ in range(selected.k)]
    matched_weights = [[] for _ in range(selected.k)]
    matched_kappas = [[] for _ in range(selected.k)]
    bootstrap_records: list[dict[str, Any]] = []
    sample_indices_population = [
        rng.integers(0, len(phases), size=len(phases)) for _ in range(BOOTSTRAPS)
    ]
    bootstrap_populations = [phases[indices] for indices in sample_indices_population]
    worker_count = min(12, os.cpu_count() or 1)
    with multiprocessing.get_context("spawn").Pool(worker_count) as pool:
        bootstrap_fits = pool.map(bootstrap_fit, bootstrap_populations, chunksize=4)
    for index, (sample_indices, bootstrap_selected) in enumerate(
        zip(sample_indices_population, bootstrap_fits, strict=True)
    ):
        selected_counts[bootstrap_selected.k] += 1
        matched = match_components(selected, bootstrap_selected)
        if matched is not None:
            centers, weights, kappas = matched
            for component in range(selected.k):
                matched_centers[component].append(float(centers[component]))
                matched_weights[component].append(float(weights[component]))
                matched_kappas[component].append(float(kappas[component]))
        bootstrap_records.append(
            {
                "bootstrap_index": index,
                "sample_indices": sample_indices.tolist(),
                "selected_k": bootstrap_selected.k,
                "selected_bic": bootstrap_selected.bic,
                "centers": list(bootstrap_selected.centers),
                "weights": list(bootstrap_selected.weights),
                "kappas": list(bootstrap_selected.kappas),
            }
        )
    selected_frequency = selected_counts[selected.k] / BOOTSTRAPS
    components = []
    for index in range(selected.k):
        correspondence = len(matched_centers[index]) / BOOTSTRAPS
        components.append(
            {
                "component": index,
                "center": selected.centers[index],
                "kappa": selected.kappas[index],
                "circular_sd": selected.circular_sd[index],
                "weight": selected.weights[index],
                "effective_membership": selected.effective_memberships[index],
                "bootstrap_correspondence_frequency": serialize_number(correspondence),
                "center_95_interval": percentile_interval(matched_centers[index], circular=True),
                "weight_95_interval": percentile_interval(matched_weights[index]),
                "kappa_95_interval": percentile_interval(matched_kappas[index]),
            }
        )
    stable = selected.k > 0 and selected_frequency >= BOOTSTRAP_STABILITY and all(
        item["bootstrap_correspondence_frequency"] >= BOOTSTRAP_STABILITY for item in components
    )
    if selected.k == 0:
        classification = "NO_STABLE_PHASE_STRUCTURE"
    elif not stable:
        classification = "INSUFFICIENT_EVIDENCE"
    elif selected.k == 1:
        classification = "ONE_STABLE_PHASE_POPULATION"
    elif selected.k == 2:
        classification = "TWO_STABLE_PHASE_POPULATIONS"
    else:
        classification = "MORE_THAN_TWO_STABLE_PHASE_POPULATIONS"
    return {
        "seed": seed,
        "selected_k": selected.k,
        "selected_model": asdict(selected),
        "candidate_models": [asdict(fit) for fit in fits],
        "bootstrap_selected_k_counts": {str(k): selected_counts[k] for k in sorted(selected_counts)},
        "bootstrap_selected_k_frequencies": {
            str(k): serialize_number(selected_counts[k] / BOOTSTRAPS) for k in sorted(selected_counts)
        },
        "components": components,
        "stable": stable,
        "classification": classification,
        "bootstrap_records": bootstrap_records,
    }


def controlled_analysis(filename: str, checksum: str):
    tempo_provenance = MetricReferenceProvenance(
        "GT-VAL-001-v1", "authoritative controlled-source MusicXML", MUSICXML_SHA256,
        "complete controlled performance",
    )
    asset_provenance = MetricReferenceProvenance(
        f"CED-VAL-001-{filename}", "authoritative controlled audio asset", checksum,
        "complete controlled performance",
    )
    return AnalysisPipeline().analyze(
        str(ROOT / f"recordings/validation/stems/{filename}"),
        declared_metric_reference=DeclaredMetricReference(Decimal("78"), "quarter", tempo_provenance),
        declared_quarter_phase_origin=DeclaredQuarterPhaseOrigin(Decimal("0"), asset_provenance),
        declared_analysis_scope=DeclaredAnalysisScope(Decimal("0"), SCOPE_END, checksum, asset_provenance),
    )


def input_population(label: str, filename: str, checksum: str, count: int) -> tuple[list[dict[str, Any]], np.ndarray]:
    analysis = controlled_analysis(filename, checksum)
    events = {event.id: event for event in analysis.elementary_metric_events}
    candidates = {candidate.id: candidate for candidate in analysis.domain_pulse_candidates}
    rows = []
    for association in analysis.elementary_metric_event_associations:
        event = events[association.elementary_metric_event_id]
        support = [candidates[item] for item in event.supporting_pulse_candidate_ids]
        rows.append(
            {
                "eme_id": str(event.id),
                "absolute_timestamp": serialize_number(event.timestamp),
                "normalized_phase": serialize_number(association.normalized_phase),
                "circular_real": serialize_number(math.cos(2.0 * math.pi * association.normalized_phase)),
                "circular_imag": serialize_number(math.sin(2.0 * math.pi * association.normalized_phase)),
                "contributor_id": str(event.contributor_id),
                "sound_source_id": str(event.sound_source_id),
                "supporting_pulse_candidate_ids": [str(item.id) for item in support],
                "observation_indices": [item.observation_index for item in support],
                "observation_provenance_ids": [item.observation_provenance_id for item in support],
                "source_asset_sha256": event.source_asset_sha256,
                "preceding_beat_reference_id": str(association.beat_reference_id),
                "following_beat_reference_id": (
                    str(association.following_beat_reference_id) if association.following_beat_reference_id else None
                ),
                "temporal_scope": association.temporal_scope,
                "localization_rule": association.association_rule,
            }
        )
    if len(rows) != count:
        raise RuntimeError(f"{label}: expected {count} EME, got {len(rows)}")
    phases = np.asarray([row["normalized_phase"] for row in rows], dtype=float)
    return rows, phases


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def scientific_view(result: dict[str, Any]) -> dict[str, Any]:
    return {
        label: {
            "selected_k": data["analysis"]["selected_k"],
            "selected_model": data["analysis"]["selected_model"],
            "candidate_models": data["analysis"]["candidate_models"],
            "bootstrap_selected_k_counts": data["analysis"]["bootstrap_selected_k_counts"],
            "components": data["analysis"]["components"],
            "stable": data["analysis"]["stable"],
            "classification": data["analysis"]["classification"],
        }
        for label, data in result["contributors"].items()
    }


def execute() -> dict[str, Any]:
    if sha256(PREREG) != PREREG_SHA256 or sha256(INPUT) != INPUT_SHA256:
        raise RuntimeError("Frozen preregistration or input checksum mismatch")
    contributors = {}
    for label, filename, checksum, count in SOURCES:
        rows, phases = input_population(label, filename, checksum, count)
        contributors[label] = {
            "eme_count": len(rows),
            "phase_range": [serialize_number(phases.min()), serialize_number(phases.max())],
            "events": rows,
            "analysis": analyze_phases(phases, label),
        }
    return {
        "experiment_id": EXPERIMENT_ID,
        "epistemic_status": "DERIVED_EVIDENCE",
        "preregistration_sha256": PREREG_SHA256,
        "input_sha256": INPUT_SHA256,
        "ground_truth_accessed": False,
        "musical_interpretation_performed": False,
        "voice_status": "DEFERRED",
        "configuration": {
            "quarter_origin": "0",
            "quarter_period": "10/13",
            "scope": "[0,1865728/44100)",
            "phase_resolution": "832/55125",
            "bootstrap_resamples": BOOTSTRAPS,
            "bootstrap_stability": BOOTSTRAP_STABILITY,
            "em_max_iterations": EM_MAX_ITER,
            "em_tolerance": EM_TOLERANCE,
            "deterministic_initializations": INITIALIZATION_COUNT,
            "serialization_digits": SERIAL_DIGITS,
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "bootstrap_worker_count": min(12, os.cpu_count() or 1),
        },
        "contributors": contributors,
    }


def main() -> None:
    first = execute()
    replay = {}
    for label, data in first["contributors"].items():
        phases = np.asarray([event["normalized_phase"] for event in data["events"]])
        fits, selected = fit_candidates(phases)
        replay[label] = {
            "selected_k": selected.k,
            "selected_model": asdict(selected),
            "candidate_models": [asdict(fit) for fit in fits],
        }
    first_fingerprint = hashlib.sha256(canonical_json(scientific_view(first))).hexdigest()
    first_full_fit = {
        label: {
            "selected_k": data["analysis"]["selected_k"],
            "selected_model": data["analysis"]["selected_model"],
            "candidate_models": data["analysis"]["candidate_models"],
        }
        for label, data in first["contributors"].items()
    }
    replay_fingerprint = hashlib.sha256(canonical_json(replay)).hexdigest()
    full_fit_fingerprint = hashlib.sha256(canonical_json(first_full_fit)).hexdigest()
    replay_passed = full_fit_fingerprint == replay_fingerprint
    first["scientific_fingerprint"] = first_fingerprint
    first["full_fit_fingerprint"] = full_fit_fingerprint
    first["deterministic_replay_fingerprint"] = replay_fingerprint
    first["deterministic_replay"] = replay_passed
    if not replay_passed:
        raise RuntimeError("Scientific replay mismatch")
    (RUN_DIR / "result.json").write_text(json.dumps(first, indent=2, sort_keys=True) + "\n")
    (RUN_DIR / "replay_result.json").write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
