"""Independent verification of frozen pairwise Calibration Zero results."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


BASE = Path("validation/VAL-001/run_20260823_095617")
FRAME = Fraction(512, 44100)
EXPECTED = {
    "Piano": (36, 36, 13, 0, 0),
    "Double Bass": (19, 18, 9, 0, 1),
    "Tenor Sax": (9, 5, 3, 0, 4),
}


def frac(record: dict) -> Fraction:
    return Fraction(record["numerator"], record["denominator"])


def nearest_frame(error: Fraction) -> int:
    ratio = error / FRAME
    lower = ratio.numerator // ratio.denominator
    return min((lower, lower + 1), key=lambda k: (abs(ratio-k), abs(k), k))


def main() -> None:
    pair = json.loads((BASE / "symbolic_pair_authority.json").read_text())
    events = json.loads((BASE / "event_pair_results.json").read_text())
    result = json.loads((BASE / "result.json").read_text())
    assert pair["authority_status"] == "FROZEN"
    assert pair["jga_timestamps_accessed"] is False
    all_offsets = Counter()
    for source, expected in EXPECTED.items():
        analysis = result["analyses"][source]
        actual = (
            analysis["symbolic_pair_count"], analysis["valid_jga_pair_count"],
            analysis["unmatched_symbolic_pair_count"],
            analysis["ambiguous_symbolic_pair_count"],
            analysis["unresolved_jga_pair_count"],
        )
        assert actual == expected, (source, actual, expected)
        for record in events["records_by_source"][source]:
            if record["jga_pair_status"] != "VALID_JGA_PAIR":
                continue
            source_gt = frac(record["source_t_gt_seconds"])
            drum_gt = frac(record["drum_t_gt_seconds"])
            source_jga = frac(record["source_t_jga_seconds"])
            drum_jga = frac(record["drum_t_jga_seconds"])
            delta_gt = frac(record["delta_gt_seconds"])
            delta_jga = frac(record["delta_jga_seconds"])
            error = frac(record["signed_e_pair_seconds"])
            absolute = frac(record["absolute_e_pair_seconds"])
            residual = frac(record["frame_residual_seconds"])
            assert delta_gt == source_gt - drum_gt
            assert delta_jga == source_jga - drum_jga
            assert error == delta_jga - delta_gt
            assert absolute == abs(error)
            offset = nearest_frame(error)
            assert record["frame_offset"] == offset
            assert residual == error - offset * FRAME
            all_offsets[offset] += 1
    assert dict(sorted(all_offsets.items())) == {
        int(key): value for key, value in result["frame_offsets"].items()
    }
    scientific_content = {
        "experiment_id": result["experiment_id"],
        "symbolic_pair_authority_fingerprint": result["symbolic_pair_authority_fingerprint"],
        "records_by_source": events["records_by_source"],
        "analyses": result["analyses"],
        "overall_classification": result["overall_classification"],
        "common_absolute_bias_cancellation": result["common_absolute_bias_cancellation"],
        "frame_offsets": result["frame_offsets"],
        "frame_residual_ms": result["frame_residual_ms"],
    }
    fingerprint = sha256(
        json.dumps(scientific_content, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert fingerprint == result["scientific_fingerprint"]
    assert result["deterministic_replay"] is True
    assert result["bootstrap_status"] == "PASS"
    assert result["raw_observations_modified"] is False
    assert result["correction_authorized"] is False
    assert result["geometric_nearest_drum_matching_used"] is False
    assert result["correspondence_tolerance_used"] is False
    print("STATUS=PASS")
    print(f"VALID_PAIRS={sum(item[1] for item in EXPECTED.values())}")
    print(f"SCIENTIFIC_FINGERPRINT={fingerprint}")


if __name__ == "__main__":
    main()
