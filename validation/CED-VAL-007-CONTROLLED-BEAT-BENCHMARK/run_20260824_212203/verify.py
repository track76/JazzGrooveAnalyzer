"""Verify frozen EXEC-CEDVAL007-THREE-SYSTEM-BENCHMARK-20260824-212203."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile

BASE = Path("validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK")
RUN = BASE / "run_20260824_212203"
EXPECTED_COMBINED = "637c3898f9607f60cabbb43aeabd26383aacf216e475007e79ce07da5848d2a0"
EXPECTED_RAW_COMBINED = "0b5035e7f8e722c98dab6c8bc9c0fcbbe16c004f0369b9c8b621bcb748306026"
EXPECTED_SCORE = {"JGA": "38c618575dd569b0fde7a509574940fb56ad713acddebc93ea18f7f47a25a827", "LIBROSA": "ebd5c1619df87de4eed87b392abccbedde9a71291a1df81c5065a0003af7a9af", "ESSENTIA": "43f3b9ad787f6f2e91e26d6c99316e45545aa8e4fe4e34206656c70cbe5d7a10"}


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    raw_authority = json.loads((RUN / "raw_system_output_authority.json").read_text())
    if raw_authority["combined_raw_output_fingerprint"] != EXPECTED_RAW_COMBINED or sha256(canonical(raw_authority["basis"])).hexdigest() != EXPECTED_RAW_COMBINED:
        raise RuntimeError("RAW_COMBINED_FINGERPRINT_CONFLICT")
    scientific = json.loads((RUN / "scientific_content.json").read_text())
    if scientific["combined_benchmark_fingerprint"] != EXPECTED_COMBINED or sha256(canonical(scientific["combined_benchmark_fingerprint_basis"])).hexdigest() != EXPECTED_COMBINED:
        raise RuntimeError("COMBINED_FINGERPRINT_CONFLICT")
    for system, expected in EXPECTED_SCORE.items():
        if scientific["systems"][system]["scientific_fingerprint"] != expected:
            raise RuntimeError(f"SYSTEM_SCORE_FINGERPRINT_CONFLICT:{system}")
    with tempfile.TemporaryDirectory(prefix="cedval007-score-verify-") as directory:
        replay = Path(directory) / "score.json"
        subprocess.run([sys.executable, str(RUN / "score.py"), str(RUN), str(replay)], check=True, cwd=Path.cwd(), env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"})
        if replay.read_bytes() != (RUN / "scientific_content.json").read_bytes():
            raise RuntimeError("SCORING_REPLAY_CONFLICT")
    completion = json.loads((RUN / "completion_protocol.json").read_text())
    if completion["scoring_replay"] != "PASS_EXACT_TWO_INDEPENDENT_EXECUTIONS" or any(value != "PASS_EXACT_TWO_FRESH_PROCESSES" for value in completion["system_replay"].values()):
        raise RuntimeError("DETERMINISTIC_REPLAY_AUTHORITY_CONFLICT")
    manifest = json.loads((RUN / "artifact_manifest.json").read_text())
    for record in manifest["artifacts"]:
        if checksum(RUN / record["relative_path"]) != record["sha256"]:
            raise RuntimeError(f"ARTIFACT_CHECKSUM_CONFLICT:{record['relative_path']}")
    print(json.dumps({"execution_id": completion["execution_id"], "combined_benchmark_fingerprint": EXPECTED_COMBINED, "raw_output_fingerprint": EXPECTED_RAW_COMBINED, "scoring_replay": "PASS_EXACT", "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
