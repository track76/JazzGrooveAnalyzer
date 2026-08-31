#!/usr/bin/env python3
"""Frozen validation-only Phase-3 detector-native evidence capture."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path
import statistics

import librosa

from jga.audio.file_audio_source import FileAudioSource
from jga.engines.audio_preprocessor import AudioPreprocessor
from jga.engines.source_pulse_candidate_builder import SourcePulseCandidateBuilder
from jga.runtime.analysis_context import AnalysisContext
from jga.separation.null_separator import NullSeparator


DATASET = Path(__file__).resolve().parent.parent
PROTOCOL = Path(__file__).with_name("PR-CEDVAL006-PHASE3-DETECTOR-NATIVE-EVIDENCE-CAPTURE-01.json")
CELL_AUDIT = DATASET / "phase3_cell_competition_audit_20260831_01/audit_execution_1.json"
PHASE2_REPORT = DATASET / "bass_preservation_phase2_20260825_01/canonical_report_M1_run_1.json"
PHASE3_REPORT = DATASET / "bass_preservation_phase3_remediated_20260831_01/canonical_report_run_1.json"
INPUTS = {
    "unprocessed": Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE2-01/M1_run_1/htdemucs_ft/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/bass.wav"),
    "processed": Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-PHASE3-DETERMINISTIC-WAV-SERIALIZATION-01/run_1/bass.wav"),
}
EXPECTED = {
    CELL_AUDIT: "e82ba3df75e64111e4a1785758228d2e3657d86f306514d2c9df0ca96200f774",
    PHASE2_REPORT: "ac6a92c05c953cd25e911da9df5bc09fbaf86872ed70b2d39e301380a0508f17",
    PHASE3_REPORT: "744b53a3cfeb30c1650892f27845f2a5e0d6d54dc92ab1075f03316f0c2cc542",
    INPUTS["unprocessed"]: "a9949d98dd914de8a7aaa330b7a149340929c31b2665bc00d55eac8df230fe6b",
    INPUTS["processed"]: "ac612091d963bcd5673b96cf5b906589decf8f0c7201599a5c0903bbf3cddc91",
}
HOP = 512
SR = 44100


def canonical(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")


def digest(path):
    h = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def summary(values):
    values = sorted(float(v) for v in values)
    if not values:
        return {k: None for k in ("count", "minimum", "q1_linear", "median", "q3_linear", "maximum", "mean", "population_sd")}
    def quantile(q):
        position = (len(values) - 1) * q
        lo, hi = math.floor(position), math.ceil(position)
        return values[lo] if lo == hi else values[lo] * (hi - position) + values[hi] * (position - lo)
    return {"count": len(values), "minimum": values[0], "q1_linear": quantile(.25), "median": statistics.median(values), "q3_linear": quantile(.75), "maximum": values[-1], "mean": statistics.fmean(values), "population_sd": statistics.pstdev(values)}


def cliff_delta(left, right):
    if not left or not right:
        return None
    wins = losses = 0
    for a in left:
        for b in right:
            wins += a > b
            losses += a < b
    return (wins - losses) / (len(left) * len(right))


def canonical_candidates(report_path):
    report = json.loads(report_path.read_text())
    authority = next(x for x in report["source_authorities"] if x["label"] == "Double Bass")
    observations = {x["pulse_candidate_id"]: x for x in report["observations"]["Double Bass"]}
    result = []
    for eme in report["elementary_metric_events"]:
        if eme["source_asset_sha256"] != authority["sha256"]:
            continue
        observation = observations[eme["supporting_pulse_candidate_ids"][0]]
        result.append({"eme_id": eme["eme_id"], **observation})
    return sorted(result, key=lambda x: (x["producer_sample_coordinate"], x["observation_index"]))


def capture(path, expected_report):
    audio = FileAudioSource().load(str(path))
    context = AnalysisContext(audio=audio)
    context = AudioPreprocessor().process(context)
    context = NullSeparator().process(context)
    context = SourcePulseCandidateBuilder().process(context)
    official = context.source_pulse_sequences[0].pulse_candidates
    signal = context.audio_stems[0].signal
    frames = librosa.onset.onset_detect(y=signal, sr=SR, units="frames")
    envelope = librosa.onset.onset_strength(y=signal, sr=SR)
    times = librosa.frames_to_time(frames, sr=SR)
    assert len(official) == len(frames) == len(expected_report)
    records = []
    for index, (candidate, frame, time, frozen) in enumerate(zip(official, frames, times, expected_report)):
        frame = int(frame)
        sample = frame * HOP
        strength = float(envelope[frame])
        assert candidate.time == float(time)
        assert candidate.strength == strength
        assert frozen["observation_index"] == index
        assert frozen["producer_frame"] == frame
        assert frozen["producer_sample_coordinate"] == sample
        assert frozen["timestamp_seconds"] == candidate.time
        records.append({
            "observation_index": index,
            "canonical_eme_id": frozen["eme_id"],
            "canonical_pulse_candidate_id": frozen["pulse_candidate_id"],
            "onset_timestamp_seconds": candidate.time,
            "onset_timestamp_hex": candidate.time.hex(),
            "frame_index": frame,
            "sample_coordinate": sample,
            "native_onset_strength": strength,
            "native_onset_strength_hex": strength.hex(),
            "native_confidence": float(candidate.confidence),
        })
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    for path, expected in EXPECTED.items():
        assert digest(path) == expected, path
    protocol = json.loads(PROTOCOL.read_text())
    before = capture(INPUTS["unprocessed"], canonical_candidates(PHASE2_REPORT))
    after = capture(INPUTS["processed"], canonical_candidates(PHASE3_REPORT))
    before_by_coord = {x["sample_coordinate"]: x for x in before}
    after_by_coord = {x["sample_coordinate"]: x for x in after}
    audit = json.loads(CELL_AUDIT.read_text())
    cells = audit["complete_cell_records"]

    groups = {name: [] for name in ("A_UNCHANGED", "B", "C1", "C2", "D", "E")}
    disappearing, newly_observable, multi = [], [], []
    d_ids = {x["processed_eme_id"] for x in audit["D_candidate_records"]}
    for cell in cells:
        pop = cell["population"]
        is_e = cell["E_changed_selection"]
        old = [{**x, **before_by_coord[x["producer_sample_coordinate"]]} for x in cell["before_candidates"]]
        new = [{**x, **after_by_coord[x["producer_sample_coordinate"]]} for x in cell["after_candidates"]]
        old_selected = next((x for x in old if x["selected"]), None)
        new_selected = next((x for x in new if x["selected"]), None)
        label = "B" if pop == "B_RECOVERED" else "C1" if pop == "C1_NEVER_MATCHED" else "C2" if pop == "C2_LOST" else "E" if is_e else "A_UNCHANGED"
        groups[label].append({
            "original_eme_id": cell["original_eme_id"],
            "before_selected_strength": old_selected["native_onset_strength"] if old_selected else None,
            "after_selected_strength": new_selected["native_onset_strength"] if new_selected else None,
            "before_candidate_strengths": [x["native_onset_strength"] for x in old],
            "after_candidate_strengths": [x["native_onset_strength"] for x in new],
        })
        disappearing.extend({"population": label, **x} for x in old if x["producer_sample_coordinate"] not in {y["producer_sample_coordinate"] for y in new})
        newly_observable.extend({"population": label, **x} for x in new if x["producer_sample_coordinate"] not in {y["producer_sample_coordinate"] for y in old})
        if len(new) > 1:
            selected_strength = new_selected["native_onset_strength"]
            other = [x["native_onset_strength"] for x in new if not x["selected"]]
            multi.append({"population": label, "candidate_count": len(new), "selected_strength": selected_strength, "maximum_other_strength": max(other), "selected_is_unique_strength_maximum": selected_strength > max(other)})

    d_after = [x for x in after if x["canonical_eme_id"] in d_ids]
    groups["D"] = [{"processed_eme_id": x["canonical_eme_id"], "after_selected_strength": x["native_onset_strength"]} for x in d_after]
    characterization = {}
    for label, records in groups.items():
        characterization[label] = {
            "population_count": len(records),
            "before_selected_strength": summary([x["before_selected_strength"] for x in records if x.get("before_selected_strength") is not None]),
            "after_selected_strength": summary([x["after_selected_strength"] for x in records if x.get("after_selected_strength") is not None]),
            "paired_same_coordinate_strength_change": summary([
                after_by_coord[cell["after_selected_coordinate"]]["native_onset_strength"] - before_by_coord[cell["before_selected_coordinate"]]["native_onset_strength"]
                for cell in cells if ((label == "A_UNCHANGED" and cell["population"] == "A_RETAINED" and not cell["E_changed_selection"]) or (label == "E" and cell["E_changed_selection"])) and cell["before_selected_coordinate"] == cell["after_selected_coordinate"]
            ]),
        }
    b_strength = [x["after_selected_strength"] for x in groups["B"]]
    d_strength = [x["after_selected_strength"] for x in groups["D"]]
    delta = cliff_delta(b_strength, d_strength)
    unique_rate = sum(x["selected_is_unique_strength_maximum"] for x in multi) / len(multi) if multi else None
    gate = protocol["prospective_discriminator_gate"]
    yes = ((delta is not None and abs(delta) >= gate["large_absolute_cliffs_delta"]) or (unique_rate is not None and unique_rate >= gate["unique_maximum_alignment_rate"]))
    no = ((delta is not None and abs(delta) < gate["negligible_absolute_cliffs_delta"]) and (unique_rate is not None and unique_rate <= .5))
    status = "YES" if yes else "NO" if no else "INDETERMINATE"
    result = {
        "study_id": protocol["study_id"],
        "protocol_fingerprint": protocol["preregistration_fingerprint"],
        "input_authorities": {label: {"path": str(path), "sha256": EXPECTED[path]} for label, path in INPUTS.items()},
        "detector": protocol["detector"],
        "candidate_counts": {"unprocessed": len(before), "processed": len(after)},
        "native_evidence_captured": protocol["native_evidence"],
        "candidate_evidence": {"unprocessed": before, "processed": after},
        "population_strength_characterization": characterization,
        "disappearing_coordinates": {"count": len(disappearing), "strength": summary(x["native_onset_strength"] for x in disappearing), "records": disappearing},
        "newly_observable_coordinates": {"count": len(newly_observable), "strength": summary(x["native_onset_strength"] for x in newly_observable), "records": newly_observable},
        "multi_candidate_relationships": {"cell_count": len(multi), "selected_unique_strength_maximum_count": sum(x["selected_is_unique_strength_maximum"] for x in multi), "selected_unique_strength_maximum_rate": unique_rate, "records": multi},
        "descriptive_discriminator_evidence": {"B_vs_D_cliffs_delta": delta, "gate": gate},
        "prospective_non_ground_truth_discriminator": status,
        "firewall": protocol["firewall"],
    }
    result["study_fingerprint"] = sha256(canonical(result)).hexdigest()
    args.output.write_bytes(canonical(result) + b"\n")
    print(result["study_fingerprint"])


if __name__ == "__main__":
    main()
