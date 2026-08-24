"""Verify frozen EXEC-CEDVAL007-RENDERED-RESPONSE-20260824-210717."""
from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import tempfile

HERE = Path(__file__).resolve().parent
EXPECTED_COMBINED = "c915eb4a63b9f7e9a3650eef1ce28d52b6bc956da485ec3b5ae7451e87ab29a2"
EXPECTED_SOURCE = {
    "MARKER": "939a7bf7c0275e31563b51542007f80251e9275adad8116b5c83097acb91c08d",
    "DRUM": "9c251de148f71eaded8a549f646c19b68414a854a9adbc6704901aaa23d4f3cb",
}
SCIENTIFIC_FILES = (
    "input_manifest.json",
    "event_level_responses.json",
    "source_summary.json",
    "scientific_content.json",
    "result.json",
)


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    spec = importlib.util.spec_from_file_location("cedval007_response_execute", HERE / "execute.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory(prefix="cedval007-response-verify-") as directory:
        output = Path(directory)
        module.main(output)
        for name in SCIENTIFIC_FILES:
            if (output / name).read_bytes() != (HERE / name).read_bytes():
                raise RuntimeError(f"SCIENTIFIC_REPLAY_CONFLICT: {name}")
    scientific = json.loads((HERE / "scientific_content.json").read_text())
    if scientific["combined_response_measurement_fingerprint"] != EXPECTED_COMBINED:
        raise RuntimeError("COMBINED_FINGERPRINT_CONFLICT")
    for source, expected in EXPECTED_SOURCE.items():
        if scientific["sources"][source]["scientific_fingerprint"] != expected:
            raise RuntimeError(f"SOURCE_FINGERPRINT_CONFLICT: {source}")
    completion = json.loads((HERE / "completion_protocol.json").read_text())
    if completion["replay"]["result"] != "PASS_EXACT_TWO_COMPLETE_EXECUTIONS":
        raise RuntimeError("REPLAY_AUTHORITY_CONFLICT")
    manifest = json.loads((HERE / "artifact_manifest.json").read_text())
    for record in manifest["artifacts"]:
        if checksum(HERE / record["relative_path"]) != record["sha256"]:
            raise RuntimeError(f"ARTIFACT_CHECKSUM_CONFLICT: {record['relative_path']}")
    print(json.dumps({"execution_id": scientific["execution_id"], "combined_fingerprint": EXPECTED_COMBINED, "marker_fingerprint": EXPECTED_SOURCE["MARKER"], "drum_fingerprint": EXPECTED_SOURCE["DRUM"], "replay": "PASS_EXACT", "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
