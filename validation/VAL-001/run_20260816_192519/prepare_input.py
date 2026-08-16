"""Freeze timestamp-only AD-037 rhythm-section input; no Ground Truth access."""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "validation/VAL-001/run_20260816_182736/result.json.gz"
OUTPUT = Path(__file__).resolve().parent / "blind_input.json"
INCLUDED = ("Drums", "Double Bass", "Piano")


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


with gzip.open(SOURCE, "rt") as handle:
    source = json.load(handle)

populations = {}
for contributor in INCLUDED:
    source_events = source["contributors"][contributor]["events"]
    events = [
        {
            "eme_id": item["eme_id"],
            "absolute_timestamp_seconds": item["absolute_timestamp"],
            "contributor_id": item["contributor_id"],
            "sound_source_id": item["sound_source_id"],
            "supporting_pulse_candidate_ids": item["supporting_pulse_candidate_ids"],
            "observation_indices": item["observation_indices"],
            "observation_provenance_ids": item["observation_provenance_ids"],
            "source_asset_sha256": item["source_asset_sha256"],
        }
        for item in source_events
    ]
    population_fingerprint = hashlib.sha256(canonical(events)).hexdigest()
    populations[contributor] = {
        "eme_count": len(events),
        "input_fingerprint": population_fingerprint,
        "events": events,
    }

output = {
    "schema": "H-VAL001-RHYTHM-TEMPO-01-input/v1",
    "epistemic_status": "OBSERVATION_DERIVED_EME_EVIDENCE",
    "source_record_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "included_contributors": list(INCLUDED),
    "excluded_inputs": [
        "Tenor Sax", "Voice", "full mix", "symbolic score", "MusicXML",
        "MIDI", "declared BPM", "declared meter", "BeatReference timeline",
        "normalized phase", "Ground Truth", "Basic Pitch", "SOME",
    ],
    "sample_rate": 44100,
    "frame_length_samples": 512,
    "populations": populations,
}
OUTPUT.write_bytes(canonical(output) + b"\n")
