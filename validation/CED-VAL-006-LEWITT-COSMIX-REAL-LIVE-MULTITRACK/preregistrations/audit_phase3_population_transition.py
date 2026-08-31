#!/usr/bin/env python3
"""Frozen read-only Phase-3 population-transition audit."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import math
from pathlib import Path
import statistics

import numpy as np
import soundfile as sf

HERE = Path(__file__).resolve().parent
DATASET = HERE.parent
PHASE2 = DATASET / "bass_preservation_phase2_20260825_01/scoring_execution_1.json"
PHASE3 = DATASET / "bass_preservation_phase3_remediated_20260831_01/scoring_execution_1.json"
PROTOCOL = HERE / "PR-CEDVAL006-PHASE3-POPULATION-TRANSITION-AUDIT-01.json"
ORIGINAL_AUDIO = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/raw/BASS - DI.wav")
UNPROCESSED_AUDIO = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE2-01/M1_run_1/htdemucs_ft/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/bass.wav")
PROCESSED_AUDIO = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-PHASE3-DETERMINISTIC-WAV-SERIALIZATION-01/run_1/bass.wav")
EXPECTED_AUDIO = {
    "original": "c0a99f65158d12a69e062cc990e86631a0d29d7e83f30537d34eb301516855a9",
    "unprocessed": "a9949d98dd914de8a7aaa330b7a149340929c31b2665bc00d55eac8df230fe6b",
    "processed": "ac612091d963bcd5673b96cf5b906589decf8f0c7201599a5c0903bbf3cddc91",
}
THRESHOLD = 10.0 ** (-30.0 / 20.0)
WINDOW_SECONDS = 0.050
BANDS = ((20.0, 80.0), (80.0, 250.0), (250.0, 1000.0), (1000.0, 4000.0), (4000.0, None))


def canonical(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")


def digest(path):
    h = sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def quantile(values, probability):
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lo, hi = math.floor(position), math.ceil(position)
    return ordered[lo] if lo == hi else ordered[lo] + (ordered[hi] - ordered[lo]) * (position - lo)


def stats(values):
    values = [float(value) for value in values]
    if not values:
        return {key: None for key in ("count", "minimum", "q1", "median", "q3", "maximum", "mean", "population_sd")}
    return {"count": len(values), "minimum": min(values), "q1": quantile(values, .25), "median": quantile(values, .5), "q3": quantile(values, .75), "maximum": max(values), "mean": statistics.fmean(values), "population_sd": statistics.pstdev(values)}


def cliffs_delta(left, right):
    greater = less = 0
    for a in left:
        for b in right:
            greater += a > b
            less += a < b
    return (greater - less) / (len(left) * len(right)) if left and right else None


def seconds(record, key):
    return record[key]["seconds"]


def match_map(level2):
    return {item["original_eme_id"]: item for item in level2["matches"]}


def window_features(audio, rate, timestamp):
    length = round(WINDOW_SECONDS * rate)
    center = round(timestamp * rate)
    start = center - length // 2
    stop = start + length
    window = np.zeros((length, audio.shape[1]), dtype=np.float64)
    source_start, source_stop = max(0, start), min(len(audio), stop)
    window[source_start - start:source_stop - start] = audio[source_start:source_stop]
    absolute = np.abs(window)
    rms = float(np.sqrt(np.mean(window * window)))
    peak = float(np.max(absolute))
    mono = np.mean(window, axis=1)
    spectrum = np.abs(np.fft.rfft(mono * np.hanning(length))) ** 2
    frequencies = np.fft.rfftfreq(length, 1.0 / rate)
    audible = frequencies >= 20.0
    total = float(np.sum(spectrum[audible]))
    fractions = {}
    for low, high in BANDS:
        mask = frequencies >= low
        if high is not None:
            mask &= frequencies < high
        fractions[f"{int(low)}-{int(high) if high is not None else 'nyquist'}"] = float(np.sum(spectrum[mask]) / total) if total else 0.0
    return {
        "rms": rms,
        "rms_dbfs": 20.0 * math.log10(rms) if rms else None,
        "peak": peak,
        "peak_dbfs": 20.0 * math.log10(peak) if peak else None,
        "sample_fraction_below_threshold_nonzero": float(np.mean((absolute > 0.0) & (absolute < THRESHOLD))),
        "rms_below_threshold": 0.0 < rms < THRESHOLD,
        "peak_below_threshold": 0.0 < peak < THRESHOLD,
        "band_energy_fraction": fractions,
    }


def summarize_features(records):
    result = {}
    for asset in ("original", "unprocessed", "processed"):
        features = [record["features"][asset] for record in records]
        result[asset] = {
            "rms": stats([item["rms"] for item in features]),
            "rms_dbfs": stats([item["rms_dbfs"] for item in features if item["rms_dbfs"] is not None]),
            "peak": stats([item["peak"] for item in features]),
            "peak_dbfs": stats([item["peak_dbfs"] for item in features if item["peak_dbfs"] is not None]),
            "sample_fraction_below_threshold_nonzero": stats([item["sample_fraction_below_threshold_nonzero"] for item in features]),
            "rms_below_threshold_count": sum(item["rms_below_threshold"] for item in features),
            "peak_below_threshold_count": sum(item["peak_below_threshold"] for item in features),
            "band_energy_fraction": {band: stats([item["band_energy_fraction"][band] for item in features]) for band in features[0]["band_energy_fraction"]} if features else {},
        }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    phase2 = json.loads(PHASE2.read_text())["runs"]["M1_run_1"]["level_2"]["Double Bass"]
    phase3_runs = json.loads(PHASE3.read_text())["runs"]
    phase3 = phase3_runs["run_1"]["level_2"]["Double Bass"]
    assert phase3 == phase3_runs["run_2"]["level_2"]["Double Bass"]
    before, after = match_map(phase2), match_map(phase3)
    before_ids, after_ids = set(before), set(after)
    original_records = {item["original_eme_id"]: item for item in [*phase2["matches"], *phase2["original_only"]]}
    populations = {
        "A_MATCHED_BEFORE_AND_AFTER": sorted(before_ids & after_ids),
        "B_RECOVERED_AFTER_PROCESSING": sorted(after_ids - before_ids),
        "C_STILL_UNMATCHED_AFTER_PROCESSING": sorted(item["original_eme_id"] for item in phase3["original_only"]),
        "D_PROCESSED_ONLY": sorted(item["separated_eme_id"] for item in phase3["separated_only"]),
        "E_MATCH_IDENTITY_CHANGED": sorted(original_id for original_id in before_ids & after_ids if seconds(before[original_id], "separated_time") != seconds(after[original_id], "separated_time")),
    }
    audio_paths = {"original": ORIGINAL_AUDIO, "unprocessed": UNPROCESSED_AUDIO, "processed": PROCESSED_AUDIO}
    audios = {}
    audio_authority = {}
    for name, path in audio_paths.items():
        assert digest(path) == EXPECTED_AUDIO[name]
        data, rate = sf.read(path, dtype="float64", always_2d=True)
        audios[name] = (data, rate)
        audio_authority[name] = {"path": str(path), "sha256": EXPECTED_AUDIO[name], "sample_rate_hz": rate, "channels": data.shape[1], "frames": data.shape[0]}
    d_by_id = {item["separated_eme_id"]: item for item in phase3["separated_only"]}
    details = {}
    for population, identities in populations.items():
        records = []
        for identity in identities:
            if population == "D_PROCESSED_ONLY":
                anchor = seconds(d_by_id[identity], "separated_time")
                original_time = None
            else:
                source = after.get(identity) or before.get(identity) or original_records[identity]
                original_time = seconds(source, "original_time")
                anchor = original_time
            records.append({
                "identity": identity,
                "anchor_seconds": anchor,
                "original_timestamp_seconds": original_time,
                "unprocessed_timestamp_seconds": seconds(before[identity], "separated_time") if identity in before else None,
                "processed_timestamp_seconds": seconds(after[identity], "separated_time") if identity in after else (seconds(d_by_id[identity], "separated_time") if population == "D_PROCESSED_ONLY" else None),
                "unprocessed_signed_displacement_seconds": seconds(before[identity], "signed_displacement") if identity in before else None,
                "processed_signed_displacement_seconds": seconds(after[identity], "signed_displacement") if identity in after else None,
                "features": {name: window_features(*audios[name], anchor) for name in audios},
            })
        details[population] = records
    summaries = {}
    for population, records in details.items():
        summaries[population] = {
            "count": len(records),
            "original_timestamp_seconds": stats([item["original_timestamp_seconds"] for item in records if item["original_timestamp_seconds"] is not None]),
            "unprocessed_timestamp_seconds": stats([item["unprocessed_timestamp_seconds"] for item in records if item["unprocessed_timestamp_seconds"] is not None]),
            "processed_timestamp_seconds": stats([item["processed_timestamp_seconds"] for item in records if item["processed_timestamp_seconds"] is not None]),
            "unprocessed_signed_displacement_seconds": stats([item["unprocessed_signed_displacement_seconds"] for item in records if item["unprocessed_signed_displacement_seconds"] is not None]),
            "unprocessed_absolute_displacement_seconds": stats([abs(item["unprocessed_signed_displacement_seconds"]) for item in records if item["unprocessed_signed_displacement_seconds"] is not None]),
            "processed_signed_displacement_seconds": stats([item["processed_signed_displacement_seconds"] for item in records if item["processed_signed_displacement_seconds"] is not None]),
            "processed_absolute_displacement_seconds": stats([abs(item["processed_signed_displacement_seconds"]) for item in records if item["processed_signed_displacement_seconds"] is not None]),
            "audio": summarize_features(records),
        }
    recovered = details["B_RECOVERED_AFTER_PROCESSING"]
    processed_only = details["D_PROCESSED_ONLY"]
    spectral_test = {}
    qualifying = []
    for band in summaries["B_RECOVERED_AFTER_PROCESSING"]["audio"]["unprocessed"]["band_energy_fraction"]:
        b_before = [item["features"]["unprocessed"]["band_energy_fraction"][band] for item in recovered]
        d_before = [item["features"]["unprocessed"]["band_energy_fraction"][band] for item in processed_only]
        b_after = [item["features"]["processed"]["band_energy_fraction"][band] for item in recovered]
        d_after = [item["features"]["processed"]["band_energy_fraction"][band] for item in processed_only]
        before_difference = quantile(b_before, .5) - quantile(d_before, .5)
        after_difference = quantile(b_after, .5) - quantile(d_after, .5)
        delta = cliffs_delta(b_before, d_before)
        passes = abs(before_difference) >= .10 and abs(delta) >= .474 and before_difference * after_difference > 0
        spectral_test[band] = {"recovered_minus_processed_only_median_before": before_difference, "recovered_minus_processed_only_median_after": after_difference, "cliffs_delta_before": delta, "qualifies": passes}
        if passes:
            qualifying.append(band)
    eq_status = "YES" if qualifying else "NO"
    result = {
        "audit_id": "AUD-CEDVAL006-PHASE3-POPULATION-TRANSITION-01",
        "protocol_id": "PR-CEDVAL006-PHASE3-POPULATION-TRANSITION-AUDIT-01",
        "protocol_fingerprint": json.loads(PROTOCOL.read_text())["preregistration_fingerprint"],
        "phase3_run_authority": "RUN_1_AND_RUN_2_LEVEL_2_DOUBLE_BASS_BYTE_EQUIVALENT_SCIENTIFIC_CONTENT",
        "authorities": {"phase2_scoring_sha256": digest(PHASE2), "phase3_scoring_sha256": digest(PHASE3), "audio": audio_authority},
        "method": {"window_seconds": WINDOW_SECONDS, "window_anchor": "original EME timestamp for A/B/C/E; processed EME timestamp for D", "channel_amplitude_rule": "all channel samples", "spectral_channel_rule": "arithmetic-mean mono", "spectral_window": "Hann", "spectral_transform": "numpy rfft float64", "bands_hz": [[low, high] for low, high in BANDS], "threshold_linear": THRESHOLD, "low_level_representation_rule": "0 < unprocessed 50-ms local RMS < threshold", "eq_gate": "YES iff at least one fixed band has |recovered-minus-processed-only unprocessed median fraction| >= 0.10, |Cliff's delta| >= 0.474, and the median-difference direction agrees after processing; NO with adequate populations otherwise"},
        "population_summaries": summaries,
        "spectral_eq_hypothesis_test": {"status": eq_status, "qualifying_bands": qualifying, "by_band": spectral_test},
        "complete_population_records": details,
        "firewall": {"audio_modified": False, "demucs_rerun": False, "jga_rerun": False, "matching_changed": False, "detector_tuned": False, "eq_executed": False, "new_compressor": False, "production_code_changed": False, "historical_evidence_modified": False, "phase4_started": False},
    }
    result["audit_fingerprint"] = sha256(canonical(result)).hexdigest()
    args.output.write_bytes(canonical(result) + b"\n")
    print(result["audit_fingerprint"])


if __name__ == "__main__":
    main()
