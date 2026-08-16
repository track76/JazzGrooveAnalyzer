"""Blind execution of H-VAL001-RHYTHM-ROLE-01."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import platform
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np


EXPERIMENT_ID = "H-VAL001-RHYTHM-ROLE-01"
INPUT_SHA256 = "0f6d8162053142893d4f938f32c73174b26dd8c783a457ad98e6e491ecb369cd"
PREREG_SHA256 = "2abfeee83cec547e5efd57ffd06e7e2c83d3eb674122e6072339830d8df19605"
BOOTSTRAPS = 2000
SERIAL_DIGITS = 12
RUN_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
INPUT = ROOT / "validation/VAL-001/run_20260816_192519/blind_result.json"
PREREG = ROOT / "validation/VAL-001/preregistrations/H-VAL001-RHYTHM-ROLE-01.md"
SHORT_IDS = (
    "RCP-d5ffc083c273a55acad93186be4b3190150babb558a247c1bc626811139e3d7d",
    "RCP-c953167752e31df8a6822d7f8228819c8c85eb90fe97423476770d8d20ff21cb",
    "RCP-49fac2900de54fd737e4b6ce57177fab0e68f3e2145e70197d8ed6ff1da8eeb9",
    "RCP-cb42f47c336f7a91b8b578d72b5282a356f08c849423d1d4c94d327ba21e7ea0",
)
LONG_IDS = (
    "RCP-e1f164f0c17452afde41470ffd078bc18a624e92111780eca8e709b4c3a99660",
    "RCP-a0e4cbece9254e5af4bd0364e04ee6b537d3a7bc5c5e5361dfd25eae82b448c5",
    "RCP-aa3105c88891efbae9adcd9efffd5ae96a77dcb022d0a2a4c16ad6afed3b7780",
    "RCP-7c1efed257ebb311645aaf5a2b574bc320da23b5640fe870b3d8f06207218cdf",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def rounded(value: float) -> float:
    return round(float(value), SERIAL_DIGITS)


def scope_events(frames: np.ndarray, scope: str) -> np.ndarray:
    if scope == "FULL":
        return frames
    midpoint = (float(frames.min()) + float(frames.max())) / 2.0
    if scope == "EARLY":
        return frames[frames < midpoint]
    return frames[frames >= midpoint]


def cycle_inventory(frames: np.ndarray, period: int, origin: int) -> tuple[list[int], list[float], list[int], int]:
    lower = float(frames.min()) - 0.5
    upper = float(frames.max()) + 0.5
    first_cycle = math.floor((lower - origin) / period)
    last_cycle = math.floor((upper - origin - 1e-15) / period)
    cycle_ids = list(range(first_cycle, last_cycle + 1))
    counts = Counter(math.floor((float(frame) - origin) / period) for frame in frames)
    exposures = []
    complete = 0
    for cycle in cycle_ids:
        start = origin + cycle * period
        end = start + period
        exposure = max(0.0, min(upper, end) - max(lower, start)) / period
        exposures.append(exposure)
        if abs(exposure - 1.0) <= 1e-12:
            complete += 1
    return cycle_ids, exposures, [counts[cycle] for cycle in cycle_ids], complete


def poisson_model(
    cycle_ids: list[int], exposures: list[float], counts: list[int], length: int,
    period: int, origin: int,
) -> dict[str, Any]:
    rates = []
    for cycle_class in range(length):
        class_indices = [index for index, cycle in enumerate(cycle_ids) if cycle % length == cycle_class]
        total_count = sum(counts[index] for index in class_indices)
        total_exposure = sum(exposures[index] for index in class_indices)
        rates.append(total_count / total_exposure if total_exposure else 0.0)
    log_likelihood = 0.0
    for cycle, exposure, count in zip(cycle_ids, exposures, counts, strict=True):
        mean = rates[cycle % length] * exposure
        if count:
            if mean <= 0.0:
                log_likelihood = -math.inf
                break
            log_likelihood += count * math.log(mean) - mean - math.lgamma(count + 1)
        else:
            log_likelihood -= mean
    parameter_count = length + 2
    bic = parameter_count * math.log(len(cycle_ids)) - 2.0 * log_likelihood
    return {
        "period_frames": period,
        "origin_residue_frames": origin,
        "higher_order_recurrence_length": length,
        "cycle_count": len(cycle_ids),
        "complete_cycle_count": sum(abs(value - 1.0) <= 1e-12 for value in exposures),
        "rates_by_cycle_class": [rounded(value) for value in rates],
        "log_likelihood": rounded(log_likelihood),
        "bic": rounded(bic),
    }


def occupancy_search(frames: np.ndarray, interval: list[int], scope: str) -> dict[str, Any]:
    scoped = scope_events(frames, scope)
    models = []
    insufficient = []
    for period in range(interval[0], interval[1] + 1):
        for origin in range(period):
            cycle_ids, exposures, counts, complete = cycle_inventory(scoped, period, origin)
            maximum_length = complete // 4
            if maximum_length < 1:
                insufficient.append(
                    {"period_frames": period, "origin_residue_frames": origin,
                     "reason": "FEWER_THAN_FOUR_COMPLETE_CYCLES"}
                )
                continue
            for length in range(1, maximum_length + 1):
                models.append(poisson_model(cycle_ids, exposures, counts, length, period, origin))
    if not models:
        return {"scope": scope, "status": "INSUFFICIENT_EVIDENCE", "tested_models": [],
                "rejected": insufficient, "selected": None, "nuisance_nonidentifiability": None}
    selected = min(
        models,
        key=lambda item: (
            item["bic"], item["higher_order_recurrence_length"],
            item["period_frames"], item["origin_residue_frames"],
        ),
    )
    tied = [
        item for item in models
        if item["bic"] == selected["bic"]
        and item["higher_order_recurrence_length"] == selected["higher_order_recurrence_length"]
    ]
    nuisance = [
        {"period_frames": item["period_frames"], "origin_residue_frames": item["origin_residue_frames"]}
        for item in tied
    ]
    return {
        "scope": scope,
        "status": "PRODUCED",
        "tested_models": models,
        "rejected": insufficient,
        "selected": selected,
        "nuisance_nonidentifiability": nuisance if len(nuisance) > 1 else [],
    }


def circular_summary(frames: np.ndarray, period: float, seed_material: str) -> dict[str, Any]:
    angles = 2.0 * math.pi * frames / period
    vector = np.mean(np.exp(1j * angles))
    center = float((np.angle(vector) / (2.0 * math.pi)) % 1.0)
    concentration = float(abs(vector))
    seed = int.from_bytes(hashlib.sha256(seed_material.encode()).digest()[:8], "big")
    rng = np.random.default_rng(seed)
    centers = []
    concentrations = []
    for _ in range(BOOTSTRAPS):
        sample = frames[rng.integers(0, len(frames), len(frames))]
        sample_vector = np.mean(np.exp(2j * math.pi * sample / period))
        sample_center = float((np.angle(sample_vector) / (2.0 * math.pi)) % 1.0)
        centers.append(center + ((sample_center - center + 0.5) % 1.0 - 0.5))
        concentrations.append(float(abs(sample_vector)))
    center_interval = np.percentile(centers, [2.5, 97.5]) % 1.0
    concentration_interval = np.percentile(concentrations, [2.5, 97.5])
    return {
        "period_frames": rounded(period),
        "circular_center": rounded(center),
        "phase_concentration_r": rounded(concentration),
        "center_95_interval": [rounded(value) for value in center_interval],
        "concentration_95_interval": [rounded(value) for value in concentration_interval],
        "bootstrap_seed": seed,
        "bootstrap_resamples": BOOTSTRAPS,
    }


def candidate_measurement(
    contributor: str, frames: np.ndarray, candidate: dict[str, Any], family: str,
) -> dict[str, Any]:
    interval = candidate["common_measurement_intersection_frames"]
    searches = {scope: occupancy_search(frames, interval, scope) for scope in ("FULL", "EARLY", "LATE")}
    lengths = [searches[scope]["selected"]["higher_order_recurrence_length"]
               if searches[scope]["selected"] else None for scope in ("FULL", "EARLY", "LATE")]
    persistent = None not in lengths and len(set(lengths)) == 1
    return {
        "family": family,
        "common_period_id": candidate["common_period_id"],
        "frozen_period_seconds": candidate["period_seconds"],
        "frozen_equal_source_estimate_frames": candidate["equal_source_estimate_frames"],
        "measurement_interval_frames": interval,
        "occupancy_searches": searches,
        "selected_lengths_full_early_late": lengths,
        "organization_persistence": "PERSISTENT" if persistent else "UNSTABLE_OR_UNRESOLVED",
        "phase_geometry": circular_summary(
            frames, candidate["equal_source_estimate_frames"],
            f"{EXPERIMENT_ID}:{contributor}:{candidate['common_period_id']}",
        ),
    }


def source_preference(measurements: list[dict[str, Any]]) -> str:
    short = [item for item in measurements if item["family"] == "SHORT"]
    if all(item["organization_persistence"] == "PERSISTENT"
           and item["selected_lengths_full_early_late"] == [1, 1, 1] for item in short):
        return "SHORT_FAMILY_PREFERRED"
    if all(item["organization_persistence"] == "PERSISTENT"
           and item["selected_lengths_full_early_late"] == [2, 2, 2] for item in short):
        return "LONG_FAMILY_PREFERRED"
    return "EQUIVALENT_OR_UNRESOLVED"


def pairwise_phase_agreement(source_results: dict[str, Any], candidate_ids: tuple[str, ...]) -> list[dict[str, Any]]:
    output = []
    for candidate_id in candidate_ids:
        source_items = {
            source: next(item for item in result["measurements"] if item["common_period_id"] == candidate_id)
            for source, result in source_results.items()
        }
        for left, right in itertools.combinations(source_items, 2):
            left_center = source_items[left]["phase_geometry"]["circular_center"]
            right_center = source_items[right]["phase_geometry"]["circular_center"]
            difference = (left_center - right_center + 0.5) % 1.0 - 0.5
            output.append(
                {"common_period_id": candidate_id, "left_source": left, "right_source": right,
                 "signed_circular_center_difference": rounded(difference)}
            )
    return output


def consensus(source_results: dict[str, Any]) -> str:
    votes = Counter(result["source_preference"] for result in source_results.values())
    short = votes["SHORT_FAMILY_PREFERRED"]
    long = votes["LONG_FAMILY_PREFERRED"]
    if short and long:
        return "SOURCE_DISAGREEMENT"
    if short >= 2:
        return "SHORT_FAMILY_PREFERRED"
    if long >= 2:
        return "LONG_FAMILY_PREFERRED"
    return "EQUIVALENT_HIERARCHICALLY_UNRESOLVED"


def execute() -> dict[str, Any]:
    if sha256(INPUT) != INPUT_SHA256 or sha256(PREREG) != PREREG_SHA256:
        raise RuntimeError("Frozen input or preregistration checksum mismatch")
    prior = json.loads(INPUT.read_text())
    common = {item["common_period_id"]: item for item in prior["common_period_candidates"]}
    if set(SHORT_IDS + LONG_IDS) != set(common):
        raise RuntimeError("Frozen candidate-family identity mismatch")
    source_results = {}
    for contributor, source in prior["source_results"].items():
        frames = np.asarray([item["frame_index"] for item in source["projected_events"]], dtype=int)
        measurements = [
            candidate_measurement(contributor, frames, common[candidate_id], family)
            for family, ids in (("SHORT", SHORT_IDS), ("LONG", LONG_IDS))
            for candidate_id in ids
        ]
        source_results[contributor] = {
            "eme_count": len(frames),
            "input_fingerprint": source["input_fingerprint"],
            "measurements": measurements,
            "source_preference": source_preference(measurements),
        }
    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": "BLIND_FROZEN",
        "epistemic_status": "SCIENTIFIC_INTERPRETATION_WITHOUT_MUSICAL_ROLE",
        "input_sha256": INPUT_SHA256,
        "preregistration_sha256": PREREG_SHA256,
        "candidate_families": {"SHORT": list(SHORT_IDS), "LONG": list(LONG_IDS)},
        "source_results": source_results,
        "cross_source_phase_agreement": pairwise_phase_agreement(source_results, SHORT_IDS + LONG_IDS),
        "blind_final_classification": consensus(source_results),
        "ground_truth_accessed": False,
        "declared_bpm_accessed": False,
        "declared_meter_accessed": False,
        "declared_timeline_accessed": False,
        "musical_role_assigned": False,
        "voice_status": "DEFERRED",
        "environment": {"python": sys.version, "platform": platform.platform(), "numpy": np.__version__},
    }
    result["scientific_fingerprint"] = fingerprint(result)
    return result


def main() -> None:
    first = execute()
    second = execute()
    first_bytes = canonical(first)
    if first_bytes != canonical(second):
        raise RuntimeError("Deterministic replay failed")
    (RUN_DIR / "blind_result.json").write_bytes(first_bytes + b"\n")
    freeze = {
        "experiment_id": EXPERIMENT_ID,
        "blind_result_sha256": hashlib.sha256(first_bytes + b"\n").hexdigest(),
        "scientific_fingerprint": first["scientific_fingerprint"],
        "deterministic_replay": True,
        "ground_truth_accessed": False,
        "blind_final_classification": first["blind_final_classification"],
        "source_preferences": {
            source: result["source_preference"] for source, result in first["source_results"].items()
        },
    }
    (RUN_DIR / "blind_freeze.json").write_bytes(canonical(freeze) + b"\n")


if __name__ == "__main__":
    main()
