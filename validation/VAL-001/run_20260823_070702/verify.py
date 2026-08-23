"""Independent frozen-artifact verification for Calibration Zero."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


BASE = Path("validation/VAL-001/run_20260823_070702")
FRAME_SPACING = Fraction(512, 44100)
EXPECTED = {
    "Drums": (63, 63, 63, 0, 0),
    "Piano": (49, 49, 49, 0, 0),
    "Double Bass": (28, 27, 27, 1, 0),
    "Tenor Sax": (12, 16, 8, 0, 4),
}


def fraction(record: dict) -> Fraction:
    return Fraction(record["numerator"], record["denominator"])


def nearest_frame_offset(error: Fraction) -> int:
    ratio = error / FRAME_SPACING
    lower = ratio.numerator // ratio.denominator
    return min(
        (lower, lower + 1),
        key=lambda integer: (abs(ratio - integer), abs(integer), integer),
    )


def main() -> None:
    result = json.loads((BASE / "result.json").read_text())
    event_payload = json.loads((BASE / "event_level_results.json").read_text())
    valid_total = 0
    observed_total = 0
    recomputed_offsets = Counter()

    for source, expected in EXPECTED.items():
        correspondence = event_payload["correspondence_by_source"][source]
        summary = result["population_summary"][source]
        actual = (
            summary["symbolic_event_count"],
            summary["observed_eme_count"],
            summary["valid_correspondence_count"],
            summary["unmatched_symbolic_count"],
            summary["ambiguous_multiple_cell_count"],
        )
        assert actual == expected, (source, actual, expected)
        assert summary["unmatched_observed_count"] == 0
        assert summary["ambiguous_boundary_eme_count"] == 0
        assert len(correspondence["valid_records"]) == expected[2]
        valid_total += expected[2]
        observed_total += expected[1]

        for record in correspondence["valid_records"]:
            t_gt = fraction(record["t_gt_seconds"])
            t_jga = fraction(record["t_jga_seconds"])
            error = fraction(record["signed_error_seconds"])
            absolute = fraction(record["absolute_error_seconds"])
            residual = fraction(record["frame_residual_seconds"])
            offset = nearest_frame_offset(error)
            assert error == t_jga - t_gt
            assert absolute == abs(error)
            assert record["frame_offset"] == offset
            assert residual == error - offset * FRAME_SPACING
            assert record["correspondence_status"] == "VALID"
            assert record["supporting_pulse_candidate_ids"]
            assert record["source_asset_sha256"]
            recomputed_offsets[offset] += 1

    assert observed_total == 155
    assert valid_total == 147
    assert dict(sorted(recomputed_offsets.items())) == {
        int(key): value
        for key, value in result["frame_distributions"]["Overall"][
            "frame_offsets"
        ].items()
    }
    assert result["deterministic_replay"] is True
    assert result["raw_observations_modified"] is False
    assert result["correction_authorized"] is False
    assert result["declared_bpm_supplied_to_jga"] is False
    assert result["declared_meter_supplied_to_jga"] is False
    assert result["beat_reference_consumed_by_calibration"] is False

    scientific_content = {
        "experiment_id": result["experiment_id"],
        "authority_fingerprint": result["authority_fingerprint"],
        "correspondence": event_payload["correspondence_by_source"],
        "statistics": result["statistics"],
        "frame_distributions": result["frame_distributions"],
        "candidate_bias": result["candidate_bias"],
        "pairwise": result["pairwise_median_signed_error_difference_ms"],
        "bias_outcome": result["bias_evidence_outcome"],
        "measurement_structure_outcome": result["measurement_structure_outcome"],
        "quantization_structure_evidence": result[
            "quantization_structure_evidence"
        ],
    }
    fingerprint = sha256(
        json.dumps(scientific_content, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert fingerprint == result["scientific_fingerprint"]
    print("STATUS=PASS")
    print(f"OBSERVED_EME={observed_total}")
    print(f"VALID_CORRESPONDENCES={valid_total}")
    print(f"SCIENTIFIC_FINGERPRINT={fingerprint}")


if __name__ == "__main__":
    main()
