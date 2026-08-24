"""Verify the frozen CED-VAL-005 local visualization authority."""
from hashlib import sha256
import json
from pathlib import Path

RUN = Path("validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/local_visualizations_20260824_160657")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def checksum(path):
    digest = sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


result = json.loads((RUN / "result.json").read_text())
manifest = json.loads((RUN / "artifact_manifest.json").read_text())
for name, expected in manifest["artifacts"].items():
    assert checksum(RUN / name) == expected, name
for window in result["scientific_record"]["windows"]:
    basis = {key: value for key, value in window.items() if key != "scientific_content_fingerprint"}
    assert sha256(canonical(basis)).hexdigest() == window["scientific_content_fingerprint"]
    assert window["duration_sample_frames"] == 220500
    assert window["end_sample_frame_exclusive"] - window["start_sample_frame"] == 220500
    assert window["total_eme_count"] == window["drums_eme_count"] + window["double_bass_eme_count"]
    assert window["in_window_frozen_localization_count"] == window["double_bass_eme_count"]
    assert window["connectors_rendered_count"] + window["display_boundary_censoring_count"] == window["in_window_frozen_localization_count"]
basis = {
    "scientific_record": result["scientific_record"],
    "per_window_scientific_content_fingerprints": result["per_window_scientific_content_fingerprints"],
    "png_sha256": result["png_sha256"],
    "scientific_content_replay": result["scientific_content_replay"],
    "png_byte_replay": result["png_byte_replay"],
}
assert sha256(canonical(basis)).hexdigest() == result["aggregate_visualization_fingerprint"]
assert result["scientific_content_replay"] is True
assert result["png_byte_replay"] is True
assert result["scientific_record"]["firewalls"] == {
    "h02_used": False,
    "historical_authorities_changed": False,
    "jga_rerun": False,
    "musical_interpretation_performed": False,
    "production_code_changed": False,
    "raw_assets_changed": False,
    "strength_accessed": False,
}
print("PASS_FROZEN_FIVE_WINDOW_LOCAL_NEUTRAL_VISUALIZATIONS")
print(result["aggregate_visualization_fingerprint"])
