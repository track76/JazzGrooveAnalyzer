#!/usr/bin/env python3
from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

import mido

HERE = Path(__file__).resolve().parent

def canonical(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")

def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()

def verify(path, expected):
    actual = file_sha(path)
    if actual != expected:
        raise RuntimeError(f"checksum mismatch: {path}: {actual}")

def load_scorer(path):
    spec = importlib.util.spec_from_file_location("frozen_scorer", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("frozen scorer unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def midi_events(path):
    midi = mido.MidiFile(path)
    if midi.ticks_per_beat != 480:
        raise RuntimeError(f"unexpected ticks_per_beat {midi.ticks_per_beat}")
    tempos = [msg.tempo for track in midi.tracks for msg in track if msg.type == "set_tempo"]
    if any(tempo != 500000 for tempo in tempos):
        raise RuntimeError(f"unsupported tempo map {tempos}")
    total_notes = 0
    candidates = []
    for track_index, track in enumerate(midi.tracks):
        tick = 0
        program = 0
        track_name = None
        for message_index, msg in enumerate(track):
            tick += msg.time
            if msg.type == "track_name":
                track_name = msg.name
            elif msg.type == "program_change":
                program = msg.program
            elif msg.type == "note_on" and msg.velocity > 0:
                total_notes += 1
                if track_name == "Bass" and program == 33:
                    candidates.append({
                        "eme_id": f"YOURMT3-T{track_index}-M{message_index}",
                        "native_index": message_index,
                        "track_index": track_index,
                        "midi_note": msg.note,
                        "velocity": msg.velocity,
                        "absolute_tick": tick,
                        "time": Fraction(tick, 960),
                        "instrument_label": "ELECTRIC_BASS_LABEL"
                    })
    candidates.sort(key=lambda x: (x["time"], x["track_index"], x["native_index"]))
    return midi, total_notes, candidates, tempos

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    protocol = json.loads((HERE / "protocol.json").read_text())
    pcopy = dict(protocol); recorded_pf = pcopy.pop("protocol_fingerprint")
    calculated_pf = sha256(canonical(pcopy)).hexdigest()
    if recorded_pf != calculated_pf:
        raise RuntimeError(f"protocol fingerprint mismatch {recorded_pf} != {calculated_pf}")
    ca = protocol["candidate_authority"]; ra = protocol["reference_authority"]; ma = protocol["matching"]
    midi_path = Path(ca["midi_path"]); reference_path = Path(ra["path"]); scorer_path = Path(ma["scorer_path"])
    verify(midi_path, ca["midi_sha256"]); verify(reference_path, ra["sha256"]); verify(scorer_path, ma["scorer_sha256"])
    for authority in protocol["comparison_authorities"].values():
        verify(Path(authority["path"]), authority["sha256"])
    midi, total_notes, candidate, tempos = midi_events(midi_path)
    if total_notes != ca["expected_total_notes"] or len(candidate) != ca["expected_population_count"]:
        raise RuntimeError(f"candidate count invariant failed: total={total_notes} bass={len(candidate)}")
    scorer = load_scorer(scorer_path)
    reference = json.loads(reference_path.read_text())
    original = scorer.events(reference, ra["label"])
    if len(original) != ra["expected_eme_count"]:
        raise RuntimeError(f"reference count invariant failed: {len(original)}")
    assignment = scorer.assign(original, candidate)
    level1 = scorer.level1(original, candidate, Fraction(11912868, 48000))
    comp = json.loads(Path(protocol["comparison_authorities"]["complementarity"]["path"]).read_text())
    partition_key = {"A_BOTH":"BOTH", "B_DEMUCS_ONLY":"HTDEMUCS_FT_ONLY", "C_RX_ONLY":"RX_ONLY", "D_NEITHER":"NEITHER"}
    sets = {partition_key[k]: set(v["original_eme_ids"]) for k,v in comp["partition"].items()}
    expected = protocol["comparison_authorities"]["complementarity"]["expected_partition"]
    if {k:len(v) for k,v in sets.items()} != expected:
        raise RuntimeError("complementarity partition invariant failed")
    matched_ids = {m["original_eme_id"] for m in assignment["matches"]}
    partition_counts = {k:len(matched_ids & v) for k,v in sets.items()}
    neither = partition_counts["NEITHER"]
    union_count = protocol["comparison_authorities"]["complementarity"]["existing_union_count"] + neither
    demucs = json.loads(Path(protocol["comparison_authorities"]["htdemucs_ft"]["path"]).read_text())["runs"]["M1_run_1"]["level_2"]["Double Bass"]
    rx = json.loads(Path(protocol["comparison_authorities"]["rx11"]["path"]).read_text())["runs"]["run_1"]["level_2"]["Double Bass"]
    a = assignment["absolute_displacement_statistics"]
    if assignment["descriptive_f1"] >= demucs["descriptive_f1"] and assignment["descriptive_recall"] >= demucs["descriptive_recall"] and a["median"] <= demucs["absolute_displacement_statistics"]["median"] and a["rmse"] <= demucs["absolute_displacement_statistics"]["rmse"] and neither >= 22:
        classification = "CLEAR_IMPROVEMENT"
    elif neither >= 22 and a["median"] <= 0.050 and a["rmse"] <= 0.100:
        classification = "COMPLEMENTARY_BUT_INSUFFICIENT"
    elif assignment["descriptive_f1"] < demucs["descriptive_f1"] and assignment["descriptive_recall"] < demucs["descriptive_recall"] and a["median"] > demucs["absolute_displacement_statistics"]["median"] and a["rmse"] > demucs["absolute_displacement_statistics"]["rmse"] and neither < 22:
        classification = "WORSE_THAN_DEMUCS"
    else:
        classification = "NO_MATERIAL_UTILITY"
    result = {
        "benchmark_id": protocol["benchmark_id"], "protocol_fingerprint": recorded_pf,
        "candidate": {"midi_path": str(midi_path), "midi_sha256": file_sha(midi_path), "model": ca["model"], "checkpoint_sha256": ca["checkpoint_sha256"], "instrument_label": "ELECTRIC_BASS_LABEL", "total_midi_notes": total_notes, "bass_candidate_count": len(candidate), "ticks_per_beat": midi.ticks_per_beat, "tempo_messages": tempos},
        "level_1": level1,
        "level_2": assignment,
        "level_3": {"matched_original_partition_counts": partition_counts, "YOURMT3_RECOVERY_OF_NEITHER": {"numerator": neither, "denominator": 398, "rate": neither/398}, "retrospective_oracle_union": {"count": union_count, "denominator": 1055, "recall": union_count/1055, "production_selector_authorized": False}},
        "comparisons": {"htdemucs_ft": {k:demucs[k] for k in ("matched_count","original_only_count","separated_only_count","descriptive_precision","descriptive_recall","descriptive_f1","absolute_displacement_statistics")}, "rx11": {k:rx[k] for k in ("matched_count","original_only_count","separated_only_count","descriptive_precision","descriptive_recall","descriptive_f1","absolute_displacement_statistics")}},
        "instrument_label_conclusion": "Instrument classification FAILS for Double Bass: YourMT3 preserved label is ELECTRIC_BASS_LABEL. Temporal correspondence is evaluated independently and does not correct that class label.",
        "direct_bass_event_utility": classification,
        "timestamp_representation": {"native_model_lattice_seconds":0.01,"serialized_midi_onset":"exact absolute_tick/960 seconds","serialized_grid_seconds":1/960,"matching_offset_correction":"NONE"},
        "firewall": protocol["firewall"]
    }
    result["result_fingerprint"] = sha256(canonical(result)).hexdigest()
    args.output.write_bytes(canonical(result) + b"\n")
    print(result["result_fingerprint"])

if __name__ == "__main__":
    main()
