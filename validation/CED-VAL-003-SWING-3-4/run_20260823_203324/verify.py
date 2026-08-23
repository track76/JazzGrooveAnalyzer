"""Independent arithmetic, lineage, cardinality and fingerprint verification."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


BASE = Path("validation/CED-VAL-003-SWING-3-4/run_20260823_203324")
FRAME = Fraction(512, 44100)


def frac(record: dict) -> Fraction:
    return Fraction(record["numerator"], record["denominator"])


def nearest_frame(error: Fraction) -> int:
    ratio = error / FRAME
    lower = ratio.numerator // ratio.denominator
    return min((lower, lower + 1), key=lambda value: (abs(ratio - value), abs(value), value))


def main() -> None:
    authority = json.loads((BASE / "calibration_symbolic_events.json").read_text())
    pair_authority = json.loads((BASE / "symbolic_pair_authority.json").read_text())
    events = json.loads((BASE / "event_level_results.json").read_text())
    pairs = json.loads((BASE / "event_pair_results.json").read_text())
    result = json.loads((BASE / "result.json").read_text())
    expected = {"Drums": (155, 155, 47, 54, 0, 54, 0), "Double Bass": (100, 100, 96, 2, 0, 2, 0), "Piano": (57, 50, 50, 7, 0, 0, 0)}
    observed_ids = set()
    recomputed_offsets = Counter()
    valid_total = 0
    for source, counts in expected.items():
        payload = events["correspondence_by_source"][source]
        actual = tuple(payload[key] for key in ("symbolic_event_count", "observed_eme_count", "valid_correspondence_count", "unmatched_symbolic_count", "unmatched_observed_count", "ambiguous_multiple_cell_count", "ambiguous_boundary_eme_count"))
        assert actual == counts, (source, actual, counts)
        valid_total += counts[2]
        for record in payload["valid_records"]:
            t_gt, t_jga = frac(record["t_gt_seconds"]), frac(record["t_jga_seconds"])
            error = frac(record["signed_error_seconds"])
            assert error == t_jga - t_gt
            assert frac(record["absolute_error_seconds"]) == abs(error)
            offset = nearest_frame(error)
            assert record["frame_offset"] == offset
            assert frac(record["frame_residual_seconds"]) == error - offset * FRAME
            assert record["supporting_pulse_candidate_ids"] and record["source_asset_sha256"]
            assert record["eme_id"] not in observed_ids
            observed_ids.add(record["eme_id"])
            recomputed_offsets[offset] += 1
        for cell in payload["event_results"]:
            for candidate in cell.get("candidate_emes", []):
                assert candidate["eme_id"] not in observed_ids
                observed_ids.add(candidate["eme_id"])
        for record in payload["boundary_results"] + payload["unmatched_observed"]:
            assert record["eme_id"] not in observed_ids
            observed_ids.add(record["eme_id"])
    assert len(observed_ids) == 305
    assert valid_total == 193
    assert dict(sorted(recomputed_offsets.items())) == {int(key): value for key, value in result["frame_distributions"]["Overall"]["frame_offsets"].items()}
    pair_valid = 0
    for source, records in pairs["pairs_by_source"].items():
        for record in records:
            if record["jga_pair_status"] != "VALID_JGA_PAIR":
                continue
            pair_valid += 1
            delta_gt = frac(record["delta_gt_seconds"])
            delta_jga = frac(record["delta_jga_seconds"])
            error = frac(record["signed_e_pair_seconds"])
            assert delta_gt == frac(record["source_t_gt_seconds"]) - frac(record["drum_t_gt_seconds"])
            assert delta_jga == frac(record["source_t_jga_seconds"]) - frac(record["drum_t_jga_seconds"])
            assert error == delta_jga - delta_gt
            assert frac(record["absolute_e_pair_seconds"]) == abs(error)
            offset = nearest_frame(error)
            assert record["frame_offset"] == offset
            assert frac(record["frame_residual_seconds"]) == error - offset * FRAME
            assert record["source_lineage"]["supporting_pulse_candidate_ids"]
            assert record["drum_lineage"]["supporting_pulse_candidate_ids"]
    assert pair_valid == 44
    scientific = {"experiment_id": result["experiment_id"], "dataset_fingerprint": result["dataset_fingerprint"], "symbolic_authority_fingerprint": authority["scientific_fingerprint"], "pair_authority_fingerprint": pair_authority["scientific_fingerprint"], "correspondence": events["correspondence_by_source"], "pairs": pairs["pairs_by_source"], "statistics": result["statistics"], "temporal": result["temporal_partitions"], "frames": result["frame_distributions"], "bias": result["candidate_bias"], "absolute_outcome": result["absolute_bias_outcome"], "pair_summaries": result["pairwise"], "measurement_outcome": result["measurement_structure_outcome"]}
    fingerprint = sha256(json.dumps(scientific, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert fingerprint == result["scientific_fingerprint"]
    assert result["deterministic_replay"] is True
    assert result["raw_observations_modified"] is False
    assert result["correction_authorized"] is False
    assert result["h02_executed"] is False
    print(f"STATUS=PASS\nOBSERVED_EME={len(observed_ids)}\nVALID_CORRESPONDENCES={valid_total}\nVALID_PAIRS={pair_valid}\nSCIENTIFIC_FINGERPRINT={fingerprint}")


if __name__ == "__main__":
    main()
