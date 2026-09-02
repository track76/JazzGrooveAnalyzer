#!/usr/bin/env python3
"""Frozen CED-VAL-010 known-source spectro-temporal characterization."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.stats import mannwhitneyu


HERE = Path(__file__).resolve().parent
PROTOCOL = json.loads((HERE / "protocol.json").read_text())
ROOT = Path(PROTOCOL["dataset"]["root"])
SR = 44_100
FRAME = 2_048
HOP = 256
NFFT = 4_096
BLOCK = 44_100
SCOPE = 9_160_573
PRE = 8_820
POST = 35_280
FREQ_ALL = np.fft.rfftfreq(NFFT, 1.0 / SR)
KEEP = FREQ_ALL <= 8_000.0
FREQ = FREQ_ALL[KEEP].astype("<f8")
WINDOW = np.hanning(FRAME + 1)[:-1].astype(np.float64)
FAMILIES = {
    "attack": ["log_power_rise_db", "attack_time_to_peak_seconds", "attack_spectral_flatness", "attack_high_low_log_ratio_db"],
    "centroid": ["attack_centroid_hz", "centroid_change_hz"],
    "bandwidth": ["attack_bandwidth_hz", "bandwidth_change_hz"],
    "flux": [f"{b}_{x}" for b in ("low", "mid", "high") for x in ("attack_flux", "flux_persistence")],
    "slope": ["attack_slope", "slope_change"],
    "harmonic": ["harmonic_decay_db_per_second", "harmonic_persistence"],
    "f0": ["f0_availability_fraction", "f0_continuity_cents"],
}
ENDPOINTS = [x for values in FAMILIES.values() for x in values]


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def write_json(path: Path, value: object) -> None:
    path.write_bytes(canonical_bytes(value))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_source(label: str) -> np.ndarray:
    authority = PROTOCOL["dataset"]["input_authorities"][label]
    path = ROOT / authority["file"]
    actual = sha256_file(path)
    if actual != authority["sha256"]:
        raise RuntimeError(f"checksum mismatch for {label}: {actual}")
    audio, rate = sf.read(path, dtype="float64", always_2d=True)
    if rate != SR or len(audio) != authority["frames"]:
        raise RuntimeError(f"format mismatch for {label}")
    return audio[:SCOPE].mean(axis=1, dtype=np.float64)


def representation(audio: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    starts = np.arange(0, len(audio) - FRAME + 1, HOP, dtype=np.int64)
    power = np.empty((len(starts), int(KEEP.sum())), dtype="<f8")
    for first in range(0, len(starts), 512):
        batch_starts = starts[first:first + 512]
        frames = np.stack([audio[s:s + FRAME] for s in batch_starts])
        spectrum = np.fft.rfft(frames * WINDOW, n=NFFT, axis=1)
        power[first:first + len(batch_starts)] = (spectrum.real[:, KEEP] ** 2 + spectrum.imag[:, KEEP] ** 2)
    return starts, FREQ.copy(), power


def scientific_representation_fingerprint(label: str, starts: np.ndarray, freq: np.ndarray, power: np.ndarray) -> str:
    h = hashlib.sha256()
    h.update(canonical_bytes({"label": label, "frame": FRAME, "hop": HOP, "nfft": NFFT, "scope": SCOPE}))
    for name, array in (("frame_starts", starts.astype("<i8", copy=False)), ("frequency_hz", freq), ("power", power)):
        h.update(name.encode() + b"\0")
        h.update(str(array.shape).encode() + b"\0")
        h.update(array.tobytes(order="C"))
    return h.hexdigest()


def flux(power: np.ndarray) -> np.ndarray:
    bins = (FREQ >= 20.0) & (FREQ <= 8_000.0)
    out = np.zeros(len(power), dtype=np.float64)
    out[1:] = np.maximum(power[1:, bins] - power[:-1, bins], 0.0).sum(axis=1)
    return out


def construct_episodes(audios: dict[str, np.ndarray], starts: dict[str, np.ndarray], fluxes: dict[str, np.ndarray], labels: list[str]) -> dict[str, list[dict]]:
    result = {label: [] for label in labels}
    full_blocks = SCOPE // BLOCK
    for block_id in range(full_blocks):
        lo, hi = block_id * BLOCK, (block_id + 1) * BLOCK
        if not all(np.any(audios[label][lo:hi] != 0.0) for label in labels):
            continue
        candidates = {}
        for label in labels:
            valid = np.flatnonzero((starts[label] >= lo) & (starts[label] < hi) & (starts[label] >= PRE) & (starts[label] + POST + FRAME <= SCOPE))
            if len(valid) == 0:
                break
            local = fluxes[label][valid]
            candidates[label] = int(valid[int(np.argmax(local))])
        if len(candidates) != len(labels):
            continue
        for label, anchor_i in candidates.items():
            anchor = int(starts[label][anchor_i])
            selected = np.flatnonzero((starts[label] >= anchor - PRE) & (starts[label] <= anchor + POST))
            result[label].append({
                "block_id": block_id,
                "block_start_sample": lo,
                "block_end_sample_exclusive": hi,
                "anchor_frame_index": anchor_i,
                "anchor_start_sample": anchor,
                "anchor_flux": float(fluxes[label][anchor_i]),
                "first_selected_frame_index": int(selected[0]),
                "last_selected_frame_index": int(selected[-1]),
                "selected_frame_count": int(len(selected)),
            })
    return result


def interval(relative_seconds: np.ndarray, lo: float, hi: float) -> np.ndarray:
    return (relative_seconds >= lo) & (relative_seconds < hi)


def frame_f0(audio: np.ndarray, frame_starts: np.ndarray) -> np.ndarray:
    frames = np.stack([audio[int(s):int(s) + FRAME] for s in frame_starts])
    frames = frames - frames.mean(axis=1, keepdims=True)
    energy = np.square(frames)
    nonzero = energy.sum(axis=1) > 0.0
    transformed = np.fft.rfft(frames, n=2 * FRAME, axis=1)
    ac = np.fft.irfft(np.square(np.abs(transformed)), n=2 * FRAME, axis=1)[:, :FRAME]
    prefix = np.concatenate([np.zeros((len(frames), 1)), np.cumsum(energy, axis=1)], axis=1)
    min_lag = int(math.ceil(SR / 1046.5))
    max_lag = int(math.floor(SR / 41.2))
    lags = np.arange(min_lag, max_lag + 1)
    left_energy = prefix[:, FRAME - lags]
    right_energy = prefix[:, FRAME:FRAME + 1] - prefix[:, lags]
    denom = np.sqrt(left_energy * right_energy)
    score = np.divide(ac[:, lags], denom, out=np.full_like(ac[:, lags], -np.inf), where=denom > 0.0)
    best = lags[np.argmax(score, axis=1)]
    f0 = SR / best.astype(np.float64)
    f0[~nonzero] = np.nan
    return f0


def measurements(label: str, audio: np.ndarray, starts: np.ndarray, power: np.ndarray, episodes: list[dict], epsilon: float) -> list[dict]:
    use = (FREQ >= 20.0) & (FREQ <= 8_000.0)
    slope_use = (FREQ >= 80.0) & (FREQ <= 8_000.0)
    freq = FREQ[use]
    log_freq = np.log10(FREQ[slope_use])
    centered_log_freq = log_freq - log_freq.mean()
    slope_denom = np.square(centered_log_freq).sum()
    bands = {"low": (20.0, 250.0), "mid": (250.0, 2000.0), "high": (2000.0, 8000.0)}
    rows = []
    for episode in episodes:
        ids = np.arange(episode["first_selected_frame_index"], episode["last_selected_frame_index"] + 1)
        local_power = power[ids]
        relative = (starts[ids] - episode["anchor_start_sample"]) / SR
        pre = interval(relative, -0.200, -0.025)
        attack = interval(relative, 0.000, 0.075)
        late = interval(relative, 0.250, 0.750)
        scoped = local_power[:, use]
        total = scoped.sum(axis=1)
        centroid = np.divide((scoped * freq).sum(axis=1), total, out=np.full(len(ids), np.nan), where=total > 0)
        bandwidth = np.sqrt(np.divide((scoped * np.square(freq[None, :] - centroid[:, None])).sum(axis=1), total, out=np.full(len(ids), np.nan), where=total > 0))
        positive = scoped > 0
        flatness = np.exp(np.log(scoped + epsilon).mean(axis=1)) / (scoped.mean(axis=1) + epsilon)
        logp = np.log10(local_power[:, slope_use] + epsilon)
        slopes = ((logp - logp.mean(axis=1, keepdims=True)) * centered_log_freq).sum(axis=1) / slope_denom
        peak_attack_index = np.flatnonzero(attack)[int(np.argmax(total[attack]))]
        row = {
            "source": label,
            "block_id": episode["block_id"],
            "log_power_rise_db": float(10 * np.log10((total[peak_attack_index] + epsilon) / (np.median(total[pre]) + epsilon))),
            "attack_time_to_peak_seconds": float(relative[peak_attack_index]),
            "attack_spectral_flatness": float(np.median(flatness[attack])),
            "attack_high_low_log_ratio_db": float(10 * np.log10((np.median(local_power[attack][:, (FREQ >= 2000) & (FREQ <= 8000)].sum(axis=1)) + epsilon) / (np.median(local_power[attack][:, (FREQ >= 20) & (FREQ < 250)].sum(axis=1)) + epsilon))),
            "attack_centroid_hz": float(np.nanmedian(centroid[attack])),
            "centroid_change_hz": float(np.nanmedian(centroid[late]) - np.nanmedian(centroid[attack])),
            "attack_bandwidth_hz": float(np.nanmedian(bandwidth[attack])),
            "bandwidth_change_hz": float(np.nanmedian(bandwidth[late]) - np.nanmedian(bandwidth[attack])),
            "attack_slope": float(np.median(slopes[attack])),
            "slope_change": float(np.median(slopes[late]) - np.median(slopes[attack])),
        }
        for band, (lo, hi) in bands.items():
            mask = (FREQ >= lo) & (FREQ < hi if hi < 8000 else FREQ <= hi)
            band_power = local_power[:, mask].sum(axis=1)
            band_flux = np.zeros(len(ids))
            band_flux[1:] = np.maximum(local_power[1:, mask] - local_power[:-1, mask], 0.0).sum(axis=1)
            normalized = band_flux / (np.concatenate(([band_power[0]], band_power[:-1])) + epsilon)
            row[f"{band}_attack_flux"] = float(np.max(normalized[attack]))
            row[f"{band}_flux_persistence"] = float((np.median(normalized[late]) + epsilon) / (np.median(normalized[attack]) + epsilon))
        f0 = frame_f0(audio, starts[ids])
        partial_sum = np.zeros(len(ids))
        partial_tracks = []
        for harmonic in range(1, 7):
            target = f0 * harmonic
            available = np.isfinite(target) & (target <= 8000.0)
            values = np.full(len(ids), np.nan)
            values[available] = np.array([np.interp(target[i], FREQ, local_power[i]) for i in np.flatnonzero(available)])
            partial_sum += np.nan_to_num(values)
            partial_tracks.append(values)
        partial_count = np.sum(np.isfinite(np.stack(partial_tracks)), axis=0)
        f0_available = np.isfinite(f0) & (partial_count >= 2)
        consecutive = f0_available[1:] & f0_available[:-1]
        continuity = np.median(np.abs(1200 * np.log2(f0[1:][consecutive] / f0[:-1][consecutive]))) if np.any(consecutive) else None
        decay_slopes = []
        decay_scope = (relative >= 0.0) & (relative < 0.750)
        for track in partial_tracks:
            valid = decay_scope & np.isfinite(track)
            if valid.sum() >= 2:
                decay_slopes.append(float(np.polyfit(relative[valid], 10 * np.log10(track[valid] + epsilon), 1)[0]))
        row["harmonic_decay_db_per_second"] = float(np.median(decay_slopes)) if decay_slopes else None
        row["harmonic_persistence"] = float((np.median(partial_sum[late]) + epsilon) / (np.median(partial_sum[attack]) + epsilon))
        row["f0_availability_fraction"] = float(f0_available.sum() / max(1, np.count_nonzero(total > 0)))
        row["f0_continuity_cents"] = float(continuity) if continuity is not None else None
        rows.append(row)
    return rows


def cliff_delta(a: np.ndarray, b: np.ndarray) -> float:
    u = mannwhitneyu(a, b, alternative="two-sided", method="asymptotic").statistic
    return float(2.0 * u / (len(a) * len(b)) - 1.0)


def summarize(rows: dict[str, list[dict]], first: str, second: str) -> dict:
    output = {}
    for ordinal, endpoint in enumerate(ENDPOINTS):
        arrays = {}
        distributions = {}
        for label in (first, second):
            values = np.array([row[endpoint] for row in rows[label] if row[endpoint] is not None and np.isfinite(row[endpoint])], dtype=np.float64)
            arrays[label] = values
            q = np.quantile(values, [0, .25, .5, .75, 1], method="linear") if len(values) else [None] * 5
            distributions[label] = {"available": len(values), "unavailable": len(rows[label]) - len(values), "minimum": q[0], "q1_linear": q[1], "median": q[2], "q3_linear": q[3], "maximum": q[4]}
        a, b = arrays[first], arrays[second]
        delta = cliff_delta(a, b)
        rng = np.random.Generator(np.random.PCG64(20260902 + ordinal))
        boot = np.empty(2000)
        for i in range(2000):
            boot[i] = cliff_delta(a[rng.integers(0, len(a), len(a))], b[rng.integers(0, len(b), len(b))])
        test = mannwhitneyu(a, b, alternative="two-sided", method="asymptotic")
        output[endpoint] = {
            "family": next(family for family, endpoints in FAMILIES.items() if endpoint in endpoints),
            "distributions": distributions,
            "cliffs_delta": delta,
            "rank_auc": (delta + 1.0) / 2.0,
            "cliffs_delta_bootstrap_95_ci": [float(np.quantile(boot, .025)), float(np.quantile(boot, .975))],
            "mann_whitney_u": float(test.statistic),
            "mann_whitney_two_sided_p": float(test.pvalue) if np.isfinite(test.pvalue) else None,
            "mann_whitney_unavailable_reason": None if np.isfinite(test.pvalue) else "SCIPY_ASYMPTOTIC_P_UNDEFINED_FOR_CONSTANT_COMBINED_POPULATION",
        }
    return output


def classify(summary: dict, row_count: dict[str, int]) -> tuple[str, list[str]]:
    unavailable_bad = 0
    for endpoint in ENDPOINTS:
        if any(summary[endpoint]["distributions"][label]["available"] < .8 * row_count[label] for label in ("BassDI", "Piano")):
            unavailable_bad += 1
    if unavailable_bad > len(ENDPOINTS) / 2:
        return "TIMBRAL_SOURCE_STRUCTURE_INDETERMINATE", []
    qualifying = []
    for family, endpoints in FAMILIES.items():
        for endpoint in endpoints:
            item = summary[endpoint]
            lo, hi = item["cliffs_delta_bootstrap_95_ci"]
            if abs(item["cliffs_delta"]) >= .147 and (lo > 0 or hi < 0):
                qualifying.append(family)
                break
    qualifying = sorted(set(qualifying))
    transient = "attack" in qualifying
    trajectory_or_decay = any(x in qualifying for x in ("centroid", "bandwidth", "flux", "slope", "harmonic", "f0"))
    if len(qualifying) >= 5 and transient and trajectory_or_decay:
        return "DISTINCT_TIMBRAL_STRUCTURE_OBSERVED", qualifying
    if len(qualifying) >= 2:
        return "PARTIAL_TIMBRAL_STRUCTURE_OBSERVED", qualifying
    return "TIMBRAL_SOURCE_STRUCTURE_INDETERMINATE", qualifying


def acquire(label: str, out: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray, str]:
    audio = load_source(label)
    starts, freq, power = representation(audio)
    fingerprint = scientific_representation_fingerprint(label, starts, freq, power)
    np.savez(out / f"{label.lower()}_representation.npz", frame_starts=starts.astype("<i8"), frequency_hz=freq, power=power)
    return audio, starts, power, fingerprint


def primary(out: Path) -> None:
    labels = ["BassDI", "Piano"]
    acquired = {label: acquire(label, out) for label in labels}
    audios = {label: acquired[label][0] for label in labels}
    starts = {label: acquired[label][1] for label in labels}
    powers = {label: acquired[label][2] for label in labels}
    fingerprints = {label: acquired[label][3] for label in labels}
    fluxes = {label: flux(powers[label]) for label in labels}
    episodes = construct_episodes(audios, starts, fluxes, labels)
    write_json(out / "primary_episodes.json", {"protocol_id": PROTOCOL["protocol_id"], "sources": episodes})
    rows = {}
    epsilons = {}
    for label in labels:
        positive = powers[label][powers[label] > 0]
        epsilons[label] = max(np.finfo(np.float64).tiny, float(np.median(positive)) * 1e-12)
        rows[label] = measurements(label, audios[label], starts[label], powers[label], episodes[label], epsilons[label])
    write_json(out / "primary_measurements.json", {"protocol_id": PROTOCOL["protocol_id"], "rows": rows})
    summary = summarize(rows, "BassDI", "Piano")
    classification, qualifying = classify(summary, {label: len(rows[label]) for label in labels})
    result = {
        "protocol_id": PROTOCOL["protocol_id"],
        "protocol_fingerprint": PROTOCOL["protocol_fingerprint"],
        "population_counts": {label: len(rows[label]) for label in labels},
        "representation_fingerprints": fingerprints,
        "epsilons": epsilons,
        "comparison_orientation": "BassDI_minus_Piano",
        "endpoints": summary,
        "qualifying_dimension_families": qualifying,
        "classification": classification,
        "firewall": "Known-source bounded observational structure only; no classifier, detector, threshold, physical onset, mixture attribution, causal mechanism, or human-equivalence claim.",
    }
    result["result_fingerprint"] = hashlib.sha256(canonical_bytes(result)).hexdigest()
    write_json(out / "primary_result.json", result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("primary",), default="primary")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    primary(args.output)


if __name__ == "__main__":
    main()
