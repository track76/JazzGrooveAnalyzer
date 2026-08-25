#!/usr/bin/env python3
"""Deterministically verify the bounded v0.3.0-alpha release authority."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tomllib


ROOT = Path(__file__).resolve().parents[3]
RELEASE_DIR = Path(__file__).resolve().parent
AUTHORITY = RELEASE_DIR / "release_authority.json"
ACCEPTANCE = (
    ROOT
    / "validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK"
    / "acceptance_20260825_113950"
)
FAILED_ACCEPTANCE = ACCEPTANCE.parent / "acceptance_20260825_112627"
EXPECTED_RELEASE_FILES = {
    "docs/CHANGELOG.md",
    "docs/JGA_PROJECT_STATE.md",
    "docs/JGA_SCIENTIFIC_EVIDENCE_INDEX.md",
    "pyproject.toml",
    "validation/releases/JGA-v0.3.0-alpha/release_authority.json",
    "validation/releases/JGA-v0.3.0-alpha/verify.py",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def git(*args: str) -> str:
    return subprocess.run(
        ("git", *args), cwd=ROOT, check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout.strip()


def verify_manifest(directory: Path) -> dict:
    manifest = json.loads((directory / "artifact_manifest.json").read_text())
    for name, expected in manifest["artifacts"].items():
        actual = sha256((directory / name).read_bytes()).hexdigest()
        require(actual == expected, f"artifact checksum mismatch: {directory.name}/{name}")
    return manifest


def main() -> int:
    authority = json.loads(AUTHORITY.read_text())
    require(authority["release_tag"] == "v0.3.0-alpha", "release tag")
    require(authority["package_version"] == "0.3.0a0", "package version authority")
    package = tomllib.loads((ROOT / "pyproject.toml").read_text())
    require(package["project"]["version"] == "0.3.0a0", "pyproject version")
    require(git("rev-parse", "v0.2.0-alpha^{commit}") ==
            "08cc28c4f5f514ec7d1c04ae6e95367b4b251d17", "predecessor tag")
    for commit in (
        "39620901048053e4159faad78065a2703a586b5e",
        "c1990328a08976de21c5e712d6fce9a8cde9abe2",
        "97de373869a4577e216efc847b69f3ae22f453c1",
        "dfb143a7926582597133d918dde74fcac53402fa",
    ):
        git("cat-file", "-e", f"{commit}^{{commit}}")

    accepted = verify_manifest(ACCEPTANCE)
    require(accepted["status"] == "PASS_REAL_AUDIO_ACCEPTED", "acceptance status")
    require(accepted["acceptance_result_fingerprint"] ==
            authority["acceptance_authority"]["fingerprint"], "acceptance fingerprint")
    failed = verify_manifest(FAILED_ACCEPTANCE)
    require(failed["status"] == "FAIL_SCIENTIFIC_INTEGRATION_CONFLICT",
            "negative acceptance preservation")

    service = (ROOT / "src/jga/reporting/rhythm_section_timing_report_service.py").read_text()
    require('SCHEMA_ID = "JGA_RHYTHM_SECTION_TIMING_REPORT_V1"' in service,
            "schema id")
    require("SCHEMA_VERSION = 1" in service, "schema version")
    for claim in authority["claim_firewall"]:
        require(f'"{claim}"' in service, f"claim firewall: {claim}")

    index = (ROOT / authority["publication_evidence_index"]["path"]).read_text()
    require("First scientifically usable release traceability addendum" in index,
            "evidence index release link")
    require(authority["acceptance_authority"]["fingerprint"] in index,
            "evidence index acceptance fingerprint")
    state = (ROOT / "docs/JGA_PROJECT_STATE.md").read_text()
    require("Status: **PASS — v0.3.0-alpha**" in state, "project release state")

    base = "97de373869a4577e216efc847b69f3ae22f453c1"
    head = git("rev-parse", "HEAD")
    if head == base:
        changed = set(git("diff", "--cached", "--name-only").splitlines())
    else:
        changed = set(git("diff", "--name-only", f"{base}..{head}").splitlines())
    require(changed <= EXPECTED_RELEASE_FILES, f"out-of-scope release changes: {sorted(changed - EXPECTED_RELEASE_FILES)}")
    require(not any(path.startswith(("src/", "tests/", "tools/")) for path in changed),
            "scientific or production implementation changed")

    try:
        tag_commit = git("rev-parse", "v0.3.0-alpha^{commit}")
    except subprocess.CalledProcessError:
        tag_commit = "NOT_CREATED_PRECOMMIT"
    if tag_commit != "NOT_CREATED_PRECOMMIT":
        require(tag_commit == git("rev-parse", "HEAD"), "release tag target")

    print(json.dumps({
        "acceptance": "PASS",
        "historical_negative_evidence": "PASS",
        "implementation_scope": "PASS_REPORTING_CONTRACT_UNCHANGED",
        "release_tag_target": tag_commit,
        "release_version": authority["release_tag"],
        "status": "PASS",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"FAIL:{exc}", file=sys.stderr)
        raise SystemExit(1)
