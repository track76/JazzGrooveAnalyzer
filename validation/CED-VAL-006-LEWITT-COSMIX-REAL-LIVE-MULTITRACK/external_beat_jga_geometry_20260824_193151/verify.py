"""Verify frozen CED-VAL-006 external-beat/JGA geometry authority."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile

RUN = Path(__file__).resolve().parent


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    manifest = json.loads((RUN / "artifact_manifest.json").read_text())
    for name, expected in manifest["artifacts"].items():
        observed = checksum(RUN / name)
        if observed != expected:
            raise RuntimeError(f"ARTIFACT_CHECKSUM_CONFLICT: {name}")
    result = json.loads((RUN / "result.json").read_text())
    content = json.loads((RUN / "scientific_content.json").read_text())
    if result["combined_comparison_fingerprint"] != content["combined_comparison_fingerprint"]:
        raise RuntimeError("SCIENTIFIC_FINGERPRINT_CONFLICT")
    if set(content["analyses"]) != {"Essentia", "librosa"}:
        raise RuntimeError("TRACKER_POPULATION_CONFLICT")
    if content["algorithmic_dependency_caveat"] != {
        "epistemic_effect": "LIBROSA_ALIGNMENT_CANNOT_INDEPENDENTLY_VALIDATE_JGA",
        "essentia_more_algorithmically_independent_comparator": True,
        "frozen_equal_start_seconds": 26.528,
        "geometry_rule_changed_by_dependency": False,
        "librosa_and_jga_frontend_fully_independent": False,
    }:
        raise RuntimeError("ALGORITHMIC_DEPENDENCY_CAVEAT_CONFLICT")
    for tracker, expected_count in (("Essentia", 527), ("librosa", 466)):
        analysis = content["analyses"][tracker]
        summary = analysis["summary"]
        bins = summary["frame_lattice_descriptive_counts"]
        disjoint = bins["disjoint_audit_bins"]
        if summary["external_beat_count"] != expected_count or summary["localized_count"] != expected_count:
            raise RuntimeError(f"COUNT_CONFLICT:{tracker}")
        if sum(disjoint.values()) != expected_count:
            raise RuntimeError(f"FRAME_BIN_PARTITION_CONFLICT:{tracker}")
        if len(analysis["cases"]) != expected_count:
            raise RuntimeError(f"CASE_POPULATION_CONFLICT:{tracker}")
    if any(result["firewalls"].values()):
        raise RuntimeError("FIREWALL_CONFLICT")
    with tempfile.TemporaryDirectory(prefix="jga-geometry-verify-") as directory:
        replay = Path(directory) / "replay.json"
        subprocess.run([sys.executable, str(RUN / "execute.py"), "derive", str(replay)], check=True)
        if replay.read_bytes() != (RUN / "scientific_content.json").read_bytes():
            raise RuntimeError("DETERMINISTIC_REPLAY_FAILURE")
    print(json.dumps({
        "status": "PASS",
        "artifact_checksums": "PASS",
        "scientific_fingerprint": result["combined_comparison_fingerprint"],
        "deterministic_replay": "PASS_EXACT_FROZEN_CONTENT",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
