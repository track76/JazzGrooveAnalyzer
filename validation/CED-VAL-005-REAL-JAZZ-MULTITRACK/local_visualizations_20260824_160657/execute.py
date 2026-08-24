"""Render frozen CED-VAL-005 five-window neutral visualizations."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import shutil
import tempfile

BASE = Path("validation/CED-VAL-005-REAL-JAZZ-MULTITRACK")
SOURCE_RUN = BASE / "run_20260824_112305"
RUN = BASE / "local_visualizations_20260824_160657"
PREREG = BASE / "preregistrations/H-CEDVAL005-FIVE-WINDOW-LOCAL-NEUTRAL-VISUALIZATION-01.md"
CLARIFICATION = BASE / "preregistrations/CL-H-CEDVAL005-FIVE-WINDOW-COORDINATE-AUTHORITY-01.md"
STUDY_ID = "H-CEDVAL005-FIVE-WINDOW-LOCAL-NEUTRAL-VISUALIZATION-01"
CLARIFICATION_ID = "CL-H-CEDVAL005-FIVE-WINDOW-COORDINATE-AUTHORITY-01"
EXECUTION_ID = "EXEC-CEDVAL005-LOCAL-VISUALIZATION-20260824-160657"
SOURCE_EXECUTION_ID = "EXEC-CEDVAL005-REAL-AUDIO-20260824-112305"
SOURCE_FINGERPRINT = "074d84768f508e6ceee9c9225c34e9ea881ce50d88e0d5f930525b92e87bd9d6"
SR, HOP, SCOPE = 44100, 512, 10068072
WINDOWS = (
    ("W1", 0, 1006807, 896557, 1117057),
    ("W2", 1, 3020421, 2910171, 3130671),
    ("W3", 2, 5034036, 4923786, 5144286),
    ("W4", 3, 7047650, 6937400, 7157900),
    ("W5", 4, 9061264, 8951014, 9171514),
)
INPUT_HASHES = {
    "elementary_metric_events.json": "81e45700196b7f712237da5ac6bbb32324a3f782bb66022e2427b08d9e342f2d",
    "drum_relative_localizations.json": "cf4a8b3c00bd4ee5b102867b554ce76fda79b0c8ea8e4d0e652f8e4950228b03",
    "rhythm_section_timing_profile.json": "e8f2f7061b80265c04518f43eddb3aaf6a9931e044b33ff3a33333370150f312",
}
AUTHORITY_HASHES = {
    str(PREREG): "83beb4287dfa2224b8e4dcb72a94cfc5dd87f38dfe7ecb91c98986610f9f31c7",
    str(CLARIFICATION): "42b41897e1c7e4123a0783a71debbe65138f2efb680a1c6534fbcb5217bd5e8c",
}


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def verify_and_load() -> tuple[dict, list[dict], dict]:
    for name, expected in INPUT_HASHES.items():
        if checksum(SOURCE_RUN / name) != expected:
            raise RuntimeError(f"FROZEN_INPUT_CONFLICT: {name}")
    for name, expected in AUTHORITY_HASHES.items():
        if checksum(Path(name)) != expected:
            raise RuntimeError(f"AUTHORITY_CONFLICT: {name}")
    manifest = json.loads((SOURCE_RUN / "artifact_manifest.json").read_text())
    if manifest["execution_id"] != SOURCE_EXECUTION_ID or manifest["scientific_fingerprint"] != SOURCE_FINGERPRINT:
        raise RuntimeError("SOURCE_EXECUTION_AUTHORITY_CONFLICT")
    events = json.loads((SOURCE_RUN / "elementary_metric_events.json").read_text())
    localizations = json.loads((SOURCE_RUN / "drum_relative_localizations.json").read_text())
    profile = json.loads((SOURCE_RUN / "rhythm_section_timing_profile.json").read_text())
    for source_records in events.values():
        for event in source_records:
            sample = event["producer_sample_coordinate"]
            if sample != HOP * event["producer_frame"]:
                raise RuntimeError(f"PRODUCER_COORDINATE_CONFLICT: {event['eme_id']}")
            timestamp = sample / SR
            if timestamp != event["timestamp_seconds"] or timestamp.hex() != event["timestamp_hex"]:
                raise RuntimeError(f"TIMESTAMP_COORDINATE_CONFLICT: {event['eme_id']}")
    for _, _, _, start, end in WINDOWS:
        if not (0 <= start < end <= SCOPE and end - start == 220500):
            raise RuntimeError("WINDOW_AUTHORITY_CONFLICT")
    return events, localizations, profile


def build_content(events: dict, localizations: list[dict], profile: dict) -> dict:
    localization_by_target = {item["target_eme_id"]: item for item in localizations}
    windows = []
    for window_id, stratum, center, start, end in WINDOWS:
        drums = [item for item in events["Drums"] if start <= item["producer_sample_coordinate"] < end]
        bass = [item for item in events["Double Bass"] if start <= item["producer_sample_coordinate"] < end]
        drum_ids = {item["eme_id"] for item in drums}
        included_localizations = []
        connectors = []
        censored = []
        ties = []
        for event in bass:
            localization = localization_by_target.get(event["eme_id"])
            if localization is None:
                raise RuntimeError(f"FROZEN_LOCALIZATION_MISSING: {event['eme_id']}")
            included_localizations.append(localization)
            if localization["nearest_selection_status"] == "EQUAL_DISTANCE_TIE":
                ties.append(localization["localization_id"])
            reference = localization["nearest_drum_reference"]
            if reference is None:
                raise RuntimeError(f"FROZEN_NEAREST_REFERENCE_MISSING: {event['eme_id']}")
            decision = {
                "localization_id": localization["localization_id"],
                "bass_eme_id": event["eme_id"],
                "drum_eme_id": reference["eme_id"],
                "bass_timestamp_seconds": event["timestamp_seconds"],
                "drum_timestamp_seconds": reference["timestamp_seconds"],
            }
            if reference["eme_id"] in drum_ids:
                connectors.append(decision)
            else:
                censored.append(decision)
        record = {
            "window_id": window_id,
            "stratum_index": stratum,
            "center_sample_frame": center,
            "center_time_seconds": center / SR,
            "start_sample_frame": start,
            "end_sample_frame_exclusive": end,
            "start_time_seconds": start / SR,
            "end_time_seconds_exclusive": end / SR,
            "duration_sample_frames": end - start,
            "duration_seconds": (end - start) / SR,
            "drums_eme_count": len(drums),
            "double_bass_eme_count": len(bass),
            "total_eme_count": len(drums) + len(bass),
            "in_window_frozen_localization_count": len(included_localizations),
            "connectors_rendered_count": len(connectors),
            "display_boundary_censoring_count": len(censored),
            "nearest_tie_count": len(ties),
            "included_drums_eme_ids": [item["eme_id"] for item in drums],
            "included_double_bass_eme_ids": [item["eme_id"] for item in bass],
            "included_localization_ids": [item["localization_id"] for item in included_localizations],
            "nearest_tie_localization_ids": ties,
            "connectors": connectors,
            "display_boundary_censoring": censored,
            "drums_events": drums,
            "double_bass_events": bass,
            "source_execution_id": SOURCE_EXECUTION_ID,
            "source_scientific_fingerprint": SOURCE_FINGERPRINT,
            "profile_id": profile["profile_id"],
            "correspondence_status": "GEOMETRIC_ONLY",
            "acquisition_authority_status": "ACQUISITION_AUTHORITY_PARTIAL",
        }
        fingerprint_basis = {
            key: value for key, value in record.items()
            if key not in {"scientific_content_fingerprint", "drums_events", "double_bass_events"}
        }
        record["scientific_content_fingerprint"] = sha256(canonical(fingerprint_basis)).hexdigest()
        windows.append(record)
    return {
        "schema": "JGA-CEDVAL005-LOCAL-NEUTRAL-VISUALIZATION/v1",
        "study_id": STUDY_ID,
        "clarification_id": CLARIFICATION_ID,
        "execution_id": EXECUTION_ID,
        "source_execution_id": SOURCE_EXECUTION_ID,
        "source_scientific_fingerprint": SOURCE_FINGERPRINT,
        "membership_coordinate": "producer_sample_coordinate",
        "membership_rule": "start_sample_frame <= producer_sample_coordinate < end_sample_frame",
        "frame_lattice": {"hop_samples": HOP, "sample_rate_hz": SR, "seconds": HOP / SR},
        "windows": windows,
        "acquisition_authority_status": "ACQUISITION_AUTHORITY_PARTIAL",
        "correspondence_status": "GEOMETRIC_ONLY",
        "firewalls": {
            "jga_rerun": False,
            "h02_used": False,
            "strength_accessed": False,
            "musical_interpretation_performed": False,
            "raw_assets_changed": False,
            "historical_authorities_changed": False,
            "production_code_changed": False,
        },
    }


def render(content: dict, directory: Path) -> dict[str, str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    directory.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for item in content["windows"]:
        fig, ax = plt.subplots(figsize=(14, 4.5), constrained_layout=True)
        for event in item["drums_events"]:
            ax.scatter(event["timestamp_seconds"], 1.0, s=22, marker="|", linewidths=1.2, color="#242424", zorder=3)
        for event in item["double_bass_events"]:
            ax.scatter(event["timestamp_seconds"], 0.0, s=22, marker="|", linewidths=1.2, color="#1769aa", zorder=3)
        for connector in item["connectors"]:
            ax.plot(
                [connector["bass_timestamp_seconds"], connector["drum_timestamp_seconds"]],
                [0.0, 1.0], color="#8d99a6", alpha=0.42, linewidth=0.65, zorder=1,
            )
        ax.set_xlim(item["start_time_seconds"], item["end_time_seconds_exclusive"])
        ax.set_ylim(-0.45, 1.45)
        ax.set_yticks([0.0, 1.0], ["Double Bass", "Drums"])
        ax.set_xlabel("Absolute distributed-file time (seconds)")
        ax.set_title(
            f"CED-VAL-005 {item['window_id']} — OBSERVATIONAL / FRAME-RESOLVED\n"
            "GEOMETRIC_ONLY — 512-sample JGA frame lattice"
        )
        ax.grid(axis="x", color="#dddddd", linewidth=0.45)
        ax.text(
            0.995, 0.02, "Not physical-onset Ground Truth", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=8, color="#555555",
        )
        path = directory / f"cedval005_{item['window_id'].lower()}_observational.png"
        fig.savefig(path, dpi=180, metadata={"Software": "JGA frozen scientific visualization"})
        plt.close(fig)
        hashes[item["window_id"]] = checksum(path)
    return hashes


def main() -> None:
    events, localizations, profile = verify_and_load()
    first_content = build_content(events, localizations, profile)
    second_content = build_content(events, localizations, profile)
    content_replay = canonical(first_content) == canonical(second_content)
    if not content_replay:
        raise RuntimeError("SCIENTIFIC_CONTENT_REPLAY_FAILURE")
    with tempfile.TemporaryDirectory(prefix="jga-cedval005-local-pass1-") as tmp1, tempfile.TemporaryDirectory(prefix="jga-cedval005-local-pass2-") as tmp2:
        first_hashes = render(first_content, Path(tmp1))
        second_hashes = render(second_content, Path(tmp2))
        png_replay = first_hashes == second_hashes
        if not png_replay:
            raise RuntimeError("PNG_BYTE_REPLAY_FAILURE")
        for window_id, _, _, _, _ in WINDOWS:
            filename = f"cedval005_{window_id.lower()}_observational.png"
            shutil.copyfile(Path(tmp1) / filename, RUN / filename)
    compact_windows = []
    for item in first_content["windows"]:
        compact_windows.append({key: value for key, value in item.items() if key not in {"drums_events", "double_bass_events"}})
    scientific_record = {**first_content, "windows": compact_windows}
    png_hashes = {window_id: checksum(RUN / f"cedval005_{window_id.lower()}_observational.png") for window_id, *_ in WINDOWS}
    aggregate_basis = {
        "scientific_record": scientific_record,
        "per_window_scientific_content_fingerprints": {
            item["window_id"]: item["scientific_content_fingerprint"] for item in compact_windows
        },
        "png_sha256": png_hashes,
        "scientific_content_replay": content_replay,
        "png_byte_replay": png_replay,
    }
    aggregate_fingerprint = sha256(canonical(aggregate_basis)).hexdigest()
    result = {
        "status": "PASS_FROZEN_FIVE_WINDOW_LOCAL_NEUTRAL_VISUALIZATIONS",
        **aggregate_basis,
        "aggregate_visualization_fingerprint": aggregate_fingerprint,
        "artifact_paths": [str(RUN / f"cedval005_{window_id.lower()}_observational.png") for window_id, *_ in WINDOWS],
    }
    write_json(RUN / "scientific_content.json", scientific_record)
    write_json(RUN / "result.json", result)
    write_json(RUN / "input_manifest.json", {
        "study_id": STUDY_ID,
        "clarification_id": CLARIFICATION_ID,
        "execution_id": EXECUTION_ID,
        "source_execution_id": SOURCE_EXECUTION_ID,
        "source_scientific_fingerprint": SOURCE_FINGERPRINT,
        "input_checksums": INPUT_HASHES,
        "authority_checksums": AUTHORITY_HASHES,
        "authority_gate": "PASS",
    })
    write_json(RUN / "completion_protocol.json", {
        "status": result["status"],
        "scientific_content_replay": "PASS_EXACT_TWO_COMPLETE_EXECUTIONS",
        "png_byte_replay": "PASS_BYTE_IDENTICAL_TWO_COMPLETE_EXECUTIONS",
        "aggregate_visualization_fingerprint": aggregate_fingerprint,
        "jga_rerun": False,
        "h02_used": False,
        "strength_accessed": False,
        "musical_interpretation_performed": False,
        "production_code_changed": False,
    })
    report = [
        f"# {STUDY_ID} Frozen Visualization Result",
        "",
        f"Execution: `{EXECUTION_ID}`",
        "",
        f"Aggregate visualization fingerprint: `{aggregate_fingerprint}`.",
        "",
        "Status: **PASS_FROZEN_FIVE_WINDOW_LOCAL_NEUTRAL_VISUALIZATIONS**",
        "",
        "Five unchanged systematic windows were rendered from frozen EME and AD-038 records using `producer_sample_coordinate` membership. Scientific-content and PNG-byte replay both passed across two complete executions.",
        "",
        "Acquisition authority remains `ACQUISITION_AUTHORITY_PARTIAL`; correspondence remains `GEOMETRIC_ONLY`. The figures are observational and frame-resolved, not physical-onset or musical-interpretation authority.",
    ]
    (RUN / "report.md").write_text("\n".join(report) + "\n")
    artifacts = [
        "execute.py", "verify.py", "input_manifest.json", "scientific_content.json", "result.json",
        "completion_protocol.json", "report.md",
        *[f"cedval005_{window_id.lower()}_observational.png" for window_id, *_ in WINDOWS],
    ]
    write_json(RUN / "artifact_manifest.json", {
        "study_id": STUDY_ID,
        "execution_id": EXECUTION_ID,
        "aggregate_visualization_fingerprint": aggregate_fingerprint,
        "artifacts": {name: checksum(RUN / name) for name in artifacts},
    })
    print(json.dumps({
        "status": result["status"],
        "execution_id": EXECUTION_ID,
        "windows": [{
            "window_id": item["window_id"],
            "bounds": [item["start_sample_frame"], item["end_sample_frame_exclusive"]],
            "counts": [item["drums_eme_count"], item["double_bass_eme_count"], item["total_eme_count"]],
            "localizations": item["in_window_frozen_localization_count"],
            "connectors": item["connectors_rendered_count"],
            "censoring": item["display_boundary_censoring_count"],
            "ties": item["nearest_tie_count"],
            "fingerprint": item["scientific_content_fingerprint"],
            "png_sha256": png_hashes[item["window_id"]],
        } for item in compact_windows],
        "aggregate_visualization_fingerprint": aggregate_fingerprint,
        "scientific_content_replay": content_replay,
        "png_byte_replay": png_replay,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
