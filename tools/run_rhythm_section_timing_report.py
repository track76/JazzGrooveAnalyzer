"""Create one canonical JGA Rhythm Section Timing Report JSON file."""

import argparse
from pathlib import Path
import sys

from jga.reporting.rhythm_section_timing_report import (
    AuthorizedSourceInput,
    RhythmSectionTimingReportError,
)
from jga.reporting.rhythm_section_timing_report_service import (
    RhythmSectionTimingReportService,
)


def _source(value: str) -> AuthorizedSourceInput:
    try:
        role, label, path = value.split("=", 2)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "source must be ROLE=LABEL=PATH"
        ) from exc
    if role not in {"TEMPORAL_REFERENCE", "ACCOMPANIMENT"}:
        raise argparse.ArgumentTypeError(
            "ROLE must be TEMPORAL_REFERENCE or ACCOMPANIMENT"
        )
    return AuthorizedSourceInput(Path(path), label, role)


def _checksum(value: str) -> tuple[str, str]:
    try:
        label, digest = value.split("=", 1)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "expected checksum must be LABEL=SHA256"
        ) from exc
    if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
        raise argparse.ArgumentTypeError("expected checksum must be lowercase SHA-256")
    return label, digest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a provenance-bound AD-040 JGA timing report.",
    )
    parser.add_argument(
        "--source",
        action="append",
        required=True,
        type=_source,
        help="repeat ROLE=LABEL=PATH; exactly one role must be TEMPORAL_REFERENCE",
    )
    parser.add_argument(
        "--expected-sha256",
        action="append",
        default=[],
        type=_checksum,
        help="repeat LABEL=SHA256; required checksum binding for every direct input",
    )
    parser.add_argument("--execution-id", required=True)
    parser.add_argument(
        "--source-identity", action="append", default=[],
        help="repeat LABEL=SOURCE_AUTHORITY_ID=SOURCE_INSTANCE_KEY; opaque caller-issued binding",
    )
    parser.add_argument("--provenance-id", required=True)
    parser.add_argument("--role-authority-id", required=True)
    parser.add_argument("--role-authority-fingerprint", required=True)
    parser.add_argument(
        "--calibration-applicability",
        required=True,
        choices=("APPLICABLE", "NOT_APPLICABLE", "UNESTABLISHED"),
    )
    parser.add_argument("--calibration-authority-id", required=True)
    parser.add_argument("--calibration-authority-fingerprint", required=True)
    parser.add_argument("--jga-revision", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    expected = dict(args.expected_sha256)
    if len(expected) != len(args.expected_sha256):
        print("ERROR:DUPLICATE_EXPECTED_CHECKSUM_LABEL", file=sys.stderr)
        return 2
    known_labels = {item.label for item in args.source}
    identities = {}
    for binding in args.source_identity:
        parts = binding.split("=", 2)
        if len(parts) != 3 or not all(parts) or parts[0] in identities or parts[0] not in known_labels:
            print("ERROR:INVALID_OR_DUPLICATE_SOURCE_IDENTITY_BINDING", file=sys.stderr)
            return 2
        identities[parts[0]] = parts[1:]
    if set(identities) != known_labels:
        print("ERROR:AD041_MISSING_DIRECT_INPUT_AUTHORITY", file=sys.stderr)
        return 2
    unknown = sorted(set(expected) - known_labels)
    if unknown:
        print(f"ERROR:CHECKSUM_LABEL_WITHOUT_SOURCE:{unknown[0]}", file=sys.stderr)
        return 2
    sources = tuple(
        AuthorizedSourceInput(
            path=item.path,
            label=item.label,
            role=item.role,
            expected_sha256=expected.get(item.label),
            source_authority_id=identities[item.label][0],
            source_instance_key=identities[item.label][1],
        )
        for item in args.source
    )
    try:
        report = RhythmSectionTimingReportService().build(
            sources,
            execution_id=args.execution_id,
            provenance_id=args.provenance_id,
            role_authority_id=args.role_authority_id,
            role_authority_fingerprint=args.role_authority_fingerprint,
            calibration_applicability=args.calibration_applicability,
            calibration_authority_id=args.calibration_authority_id,
            calibration_authority_fingerprint=(
                args.calibration_authority_fingerprint
            ),
            jga_revision=args.jga_revision,
        )
        report.write(args.output)
    except (RhythmSectionTimingReportError, OSError) as exc:
        print(f"ERROR:{exc}", file=sys.stderr)
        return 2
    print(f"schema={report.schema_id}")
    print(f"scientific_fingerprint={report.scientific_fingerprint}")
    print(f"output={args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
