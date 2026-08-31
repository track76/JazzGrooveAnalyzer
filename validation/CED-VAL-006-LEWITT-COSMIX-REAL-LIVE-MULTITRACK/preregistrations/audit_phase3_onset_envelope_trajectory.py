#!/usr/bin/env python3
"""Frozen validation-only native onset-envelope trajectory audit."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
import math
from pathlib import Path
import statistics

import librosa
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from jga.audio.file_audio_source import FileAudioSource
from jga.engines.audio_preprocessor import AudioPreprocessor
from jga.runtime.analysis_context import AnalysisContext

DATASET = Path(__file__).resolve().parent.parent
PROTOCOL = Path(__file__).with_name("PR-CEDVAL006-PHASE3-ONSET-ENVELOPE-TRAJECTORY-AUDIT-01.json")
CAPTURE = DATASET / "phase3_detector_native_evidence_capture_20260831_01/capture_execution_1.json"
CELLS = DATASET / "phase3_cell_competition_audit_20260831_01/audit_execution_1.json"
INPUTS = {
    "unprocessed": Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE2-01/M1_run_1/htdemucs_ft/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/bass.wav"),
    "processed": Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-PHASE3-DETERMINISTIC-WAV-SERIALIZATION-01/run_1/bass.wav"),
}
EXPECTED = {
    CAPTURE: "9c39a729c7185e05a2db1125c38562365c603d43504d000405ed83d3dd836091",
    CELLS: "e82ba3df75e64111e4a1785758228d2e3657d86f306514d2c9df0ca96200f774",
    INPUTS["unprocessed"]: "a9949d98dd914de8a7aaa330b7a149340929c31b2665bc00d55eac8df230fe6b",
    INPUTS["processed"]: "ac612091d963bcd5673b96cf5b906589decf8f0c7201599a5c0903bbf3cddc91",
}
SR, HOP, RADIUS = 44100, 512, 8
PRE_MAX, POST_MAX, PRE_AVG, POST_AVG, WAIT, DELTA = 2, 1, 8, 9, 2, 0.07

def canonical(value): return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")
def digest(path):
    h = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""): h.update(block)
    return h.hexdigest()

def stats(values):
    values = sorted(float(x) for x in values)
    if not values: return {"count": 0, "minimum": None, "median": None, "maximum": None, "mean": None, "population_sd": None}
    return {"count": len(values), "minimum": values[0], "median": statistics.median(values), "maximum": values[-1], "mean": statistics.fmean(values), "population_sd": statistics.pstdev(values)}

def envelope(path):
    audio = FileAudioSource().load(str(path))
    context = AudioPreprocessor().process(AnalysisContext(audio=audio))
    raw = librosa.onset.onset_strength(y=context.processed_audio, sr=SR, hop_length=HOP)
    normalized = raw - np.min(raw)
    normalized /= np.max(normalized) + librosa.util.tiny(normalized)
    detected = librosa.onset.onset_detect(onset_envelope=raw, sr=SR, hop_length=HOP, units="frames")
    return raw, normalized, {int(x) for x in detected}

def frame_evidence(frame, raw, normalized, detected):
    lo, hi = max(0, frame - RADIUS), min(len(raw), frame + RADIUS + 1)
    frames = list(range(lo, hi))
    values = normalized[lo:hi]
    dominant = frames[int(np.argmax(values))]
    rank = 1 + sum(float(x) > float(normalized[frame]) for x in values)
    max_lo, max_hi = max(0, frame - PRE_MAX), min(len(raw), frame + POST_MAX)
    avg_lo, avg_hi = max(0, frame - PRE_AVG), min(len(raw), frame + POST_AVG)
    local_max = bool(normalized[frame] == np.max(normalized[max_lo:max_hi]))
    adaptive_mean = float(np.mean(normalized[avg_lo:avg_hi]))
    threshold = bool(normalized[frame] >= adaptive_mean + DELTA)
    prior = max((x for x in detected if x < frame), default=None)
    wait_clear = prior is None or frame - prior > WAIT
    eligible_pre_wait = local_max and threshold
    neighboring_eligible = [f for f in frames if bool(normalized[f] == np.max(normalized[max(0, f-PRE_MAX):min(len(raw), f+POST_MAX)])) and bool(normalized[f] >= float(np.mean(normalized[max(0, f-PRE_AVG):min(len(raw), f+POST_AVG)])) + DELTA)]
    return {
        "frame": frame, "sample_coordinate": frame * HOP,
        "raw_value": float(raw[frame]), "normalized_value": float(normalized[frame]),
        "local_maximum_raw_value": float(np.max(raw[lo:hi])),
        "dominant_local_peak_frame": dominant,
        "dominant_local_peak_distance_frames": dominant - frame,
        "dominant_local_peak_distance_seconds": (dominant - frame) * HOP / SR,
        "local_peak_rank": rank,
        "local_maximality_condition": local_max,
        "adaptive_mean_normalized": adaptive_mean,
        "adaptive_threshold_normalized": adaptive_mean + DELTA,
        "adaptive_threshold_margin": float(normalized[frame]) - adaptive_mean - DELTA,
        "adaptive_threshold_condition": threshold,
        "wait_condition_clear": wait_clear,
        "eligible_before_wait": eligible_pre_wait,
        "detected_candidate": frame in detected,
        "neighboring_eligible_peak_frames": neighboring_eligible,
        "window_frames": frames,
        "window_raw_values": [float(x) for x in raw[lo:hi]],
        "window_normalized_values": [float(x) for x in normalized[lo:hi]],
    }

def classify(before, after, transition, before_detected, after_detected):
    opposite = after_detected if transition == "DISAPPEARING" else before_detected
    reference = after if transition == "DISAPPEARING" else before
    other = before if transition == "DISAPPEARING" else after
    relocation = before["dominant_local_peak_frame"] != after["dominant_local_peak_frame"] and any(abs(x-reference["frame"]) <= RADIUS for x in opposite)
    if relocation: return "A_LOCAL_PEAK_RELOCATION"
    if before["local_maximality_condition"] != after["local_maximality_condition"]: return "C_LOCAL_MAXIMALITY_CHANGE"
    if before["adaptive_threshold_condition"] != after["adaptive_threshold_condition"]: return "D_ADAPTIVE_THRESHOLD_CHANGE"
    if before["eligible_before_wait"] and after["eligible_before_wait"] and before["wait_condition_clear"] != after["wait_condition_clear"]: return "B_WAIT_RANK_COMPETITION"
    if other["detected_candidate"] != reference["detected_candidate"]: return "E_OTHER_DETECTOR_NATIVE"
    return "F_UNRESOLVED"

def plot_example(record, path):
    fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=120)
    for condition, color in (("unprocessed", "#2457a6"), ("processed", "#c54b35")):
        ev = record[condition]
        offsets = [(x - record["frame"]) * HOP / SR * 1000 for x in ev["window_frames"]]
        ax.plot(offsets, ev["window_normalized_values"], marker="o", markersize=2.5, linewidth=1.2, label=condition, color=color)
        ax.axvline(ev["dominant_local_peak_distance_seconds"] * 1000, color=color, alpha=.25, linewidth=.8)
    ax.axvline(0, color="black", linestyle="--", linewidth=.8)
    ax.set(xlabel="Offset from authoritative coordinate (ms)", ylabel="Normalized onset envelope", title=f"{record['transition']} — {record['primary_mechanism']} — frame {record['frame']}")
    ax.legend(loc="best"); ax.grid(alpha=.2); fig.tight_layout()
    fig.savefig(path, metadata={"Software": "JGA deterministic validation", "Creation Time": "2026-08-31T00:00:00Z"})
    plt.close(fig)

def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--output-dir", type=Path, required=True); args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for path, expected in EXPECTED.items(): assert digest(path) == expected, path
    protocol = json.loads(PROTOCOL.read_text())
    capture, cell_audit = json.loads(CAPTURE.read_text()), json.loads(CELLS.read_text())
    raw_b, norm_b, det_b = envelope(INPUTS["unprocessed"])
    raw_a, norm_a, det_a = envelope(INPUTS["processed"])
    assert det_b == {x["frame_index"] for x in capture["candidate_evidence"]["unprocessed"]}
    assert det_a == {x["frame_index"] for x in capture["candidate_evidence"]["processed"]}
    labels = defaultdict(set)
    disappearing = {x["sample_coordinate"] for x in capture["disappearing_coordinates"]["records"]}
    emerging = {x["sample_coordinate"] for x in capture["newly_observable_coordinates"]["records"]}
    for x in capture["disappearing_coordinates"]["records"]: labels[x["sample_coordinate"]].update(("DISAPPEARING", x["population"]))
    for x in capture["newly_observable_coordinates"]["records"]: labels[x["sample_coordinate"]].update(("NEWLY_OBSERVABLE", x["population"]))
    for cell in cell_audit["complete_cell_records"]:
        if cell["population"] == "A_RETAINED" and not cell["E_changed_selection"] and cell["before_selected_coordinate"] == cell["after_selected_coordinate"]: labels[cell["before_selected_coordinate"]].add("RETAINED_UNCHANGED")
        if cell["population"] == "B_RECOVERED": labels[cell["after_selected_coordinate"]].add("B_GROSS_RECOVERY")
        if cell["population"] == "C2_LOST": labels[cell["before_selected_coordinate"]].add("C2_LOST")
        if cell["E_changed_selection"]:
            labels[cell["before_selected_coordinate"]].add("E_CHANGED_SELECTION_BEFORE")
            labels[cell["after_selected_coordinate"]].add("E_CHANGED_SELECTION_AFTER")
        if cell["after_candidate_count"] > 1:
            for item in cell["after_candidates"]: labels[item["producer_sample_coordinate"]].add("MULTI_CANDIDATE_CELL")
    records = []
    for coordinate in sorted(labels):
        frame = coordinate // HOP
        before, after = frame_evidence(frame, raw_b, norm_b, det_b), frame_evidence(frame, raw_a, norm_a, det_a)
        transition = "DISAPPEARING" if coordinate in disappearing else "NEWLY_OBSERVABLE" if coordinate in emerging else "RETAINED_OR_CONTEXT"
        mechanism = classify(before, after, transition, det_b, det_a) if transition != "RETAINED_OR_CONTEXT" else "NOT_APPLICABLE"
        records.append({"frame": frame, "sample_coordinate": coordinate, "labels": sorted(labels[coordinate]), "transition": transition, "primary_mechanism": mechanism, "dominant_peak_relocated": before["dominant_local_peak_frame"] != after["dominant_local_peak_frame"], "rank_change": after["local_peak_rank"] - before["local_peak_rank"], "unprocessed": before, "processed": after})
    transitions = [x for x in records if x["transition"] != "RETAINED_OR_CONTEXT"]
    by_transition = {}
    for transition in ("DISAPPEARING", "NEWLY_OBSERVABLE"):
        selected = [x for x in transitions if x["transition"] == transition]
        by_transition[transition] = {
            "count": len(selected), "primary_mechanisms": dict(sorted(Counter(x["primary_mechanism"] for x in selected).items())),
            "dominant_peak_relocated_count": sum(x["dominant_peak_relocated"] for x in selected),
            "local_maximality_gained_count": sum(not x["unprocessed"]["local_maximality_condition"] and x["processed"]["local_maximality_condition"] for x in selected),
            "local_maximality_lost_count": sum(x["unprocessed"]["local_maximality_condition"] and not x["processed"]["local_maximality_condition"] for x in selected),
            "threshold_gained_count": sum(not x["unprocessed"]["adaptive_threshold_condition"] and x["processed"]["adaptive_threshold_condition"] for x in selected),
            "threshold_lost_count": sum(x["unprocessed"]["adaptive_threshold_condition"] and not x["processed"]["adaptive_threshold_condition"] for x in selected),
            "rank_change": stats(x["rank_change"] for x in selected),
            "absolute_dominant_peak_shift_frames": stats(abs(x["processed"]["dominant_local_peak_frame"]-x["unprocessed"]["dominant_local_peak_frame"]) for x in selected),
        }
    subgroup = {}
    for label in ("B_GROSS_RECOVERY", "C2_LOST", "E_CHANGED_SELECTION_BEFORE", "E_CHANGED_SELECTION_AFTER", "MULTI_CANDIDATE_CELL", "RETAINED_UNCHANGED"):
        selected = [x for x in records if label in x["labels"]]
        subgroup[label] = {"coordinate_count": len(selected), "transition_counts": dict(sorted(Counter(x["transition"] for x in selected).items())), "primary_mechanisms": dict(sorted(Counter(x["primary_mechanism"] for x in selected if x["primary_mechanism"] != "NOT_APPLICABLE").items())), "rank_change": stats(x["rank_change"] for x in selected)}
    explained_names = {"A_LOCAL_PEAK_RELOCATION", "B_WAIT_RANK_COMPETITION", "C_LOCAL_MAXIMALITY_CHANGE", "D_ADAPTIVE_THRESHOLD_CHANGE", "E_OTHER_DETECTOR_NATIVE"}
    explained_rates = {key: sum(name in explained_names for name in value["primary_mechanisms"] for _ in range(value["primary_mechanisms"][name])) / value["count"] for key, value in by_transition.items()}
    combined = Counter(x["primary_mechanism"] for x in transitions)
    dominant_name, dominant_count = combined.most_common(1)[0]
    gate = protocol["prospective_principle_gate"]
    yes = all(rate >= gate["minimum_explained_fraction_each_transition"] for rate in explained_rates.values()) and dominant_count / len(transitions) >= gate["minimum_single_mechanism_fraction_combined"]
    no = all(rate < gate["no_maximum_explained_fraction_each_transition"] for rate in explained_rates.values())
    outcome = "YES" if yes else "NO" if no else "INDETERMINATE"
    plot_candidates = {}
    for key in sorted(set(x["primary_mechanism"] for x in transitions)):
        chosen = min((x for x in transitions if x["primary_mechanism"] == key), key=lambda x: x["sample_coordinate"], default=None)
        if chosen: plot_candidates[f"mechanism_{key}"] = chosen
    for label in ("B_GROSS_RECOVERY", "C2_LOST", "E_CHANGED_SELECTION_BEFORE", "E_CHANGED_SELECTION_AFTER"):
        chosen = min((x for x in records if label in x["labels"]), key=lambda x: x["sample_coordinate"], default=None)
        if chosen: plot_candidates[f"population_{label}"] = chosen
    plots = []
    used = set()
    for key, record in sorted(plot_candidates.items()):
        if record["sample_coordinate"] in used: continue
        used.add(record["sample_coordinate"])
        filename = f"diagnostic_{len(plots)+1:02d}_{key.lower()}.png"
        plot_example(record, args.output_dir / filename)
        plots.append({"filename": filename, "selection_class": key, "sample_coordinate": record["sample_coordinate"], "sha256": digest(args.output_dir / filename)})
    result = {"audit_id": protocol["audit_id"], "protocol_fingerprint": protocol["preregistration_fingerprint"], "authorities": {str(k): v for k,v in EXPECTED.items()}, "neighborhood": protocol["neighborhood"], "detector": protocol["detector"], "transition_results": by_transition, "subgroup_results": subgroup, "combined_primary_mechanisms": dict(sorted(combined.items())), "dominant_mechanism": {"name": dominant_name, "count": dominant_count, "fraction": dominant_count/len(transitions)}, "explained_fraction": explained_rates, "prospective_non_ground_truth_principle": outcome, "principle": protocol["prospective_principle_gate"]["principle_if_yes"] if outcome == "YES" else None, "diagnostic_plots": plots, "complete_coordinate_records": records, "firewall": protocol["firewall"]}
    result["audit_fingerprint"] = sha256(canonical(result)).hexdigest()
    (args.output_dir / "audit.json").write_bytes(canonical(result)+b"\n")
    print(result["audit_fingerprint"])

if __name__ == "__main__": main()
