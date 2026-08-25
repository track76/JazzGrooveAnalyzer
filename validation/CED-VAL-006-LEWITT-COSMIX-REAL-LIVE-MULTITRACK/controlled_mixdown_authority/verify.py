#!/usr/bin/env python3
"""Verify PR-CEDVAL006-CONTROLLED-MIXDOWN-001 without regenerating audio."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import wave

import numpy as np


HERE = Path(__file__).resolve().parent
VALIDATION = HERE.parent
ROOT = VALIDATION.parents[1]
PARENT_MANIFEST = VALIDATION / "input_authority_manifest.json"
AUTHORITY = HERE / "controlled_mixdown_authority.json"
FILES = {
    "source_manifest.json": "7527e0577e782e968baa407e8c2ec6f12891b1a07acd959de86e0f56bbf362b1",
    "mix_plan.json": "3b0a7c2d933a4abb2c2b582bfeb1af90d2546defa98c97d500b2deb02d50fbf8",
    "generate.py": "d6fcd68f031fb9813e124073f28c58c6a2ab037e5517105132c9b24a1e5a03bb",
}


def digest(path: Path) -> str:
    value = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    authority = json.loads(AUTHORITY.read_text())
    expected_fingerprint = authority.pop("authority_fingerprint")
    computed = sha256(json.dumps(
        authority, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")).hexdigest()
    require(computed == expected_fingerprint, "authority fingerprint")
    for name, expected in FILES.items():
        require(digest(HERE / name) == expected, f"authority file checksum:{name}")

    source_manifest = json.loads((HERE / "source_manifest.json").read_text())
    parent = json.loads(PARENT_MANIFEST.read_text())
    parent_wavs = {
        item["filename"]: item for item in parent["scientifically_relevant_assets"]
        if item.get("file_type") == "WAV"
    }
    require(len(source_manifest["sources"]) == len(parent_wavs) == 15,
            "complete provider WAV population")
    for source in source_manifest["sources"]:
        original = parent_wavs[source["filename"]]
        require(source["inclusion_status"] == "INCLUDED", "source exclusion")
        require((source["sha256"], source["sample_rate_hz"], source["channels"],
                 source["frame_count"]) ==
                (original["sha256"], original["sample_rate_hz"],
                 original["channel_count"], original["frame_count_per_channel"]),
                f"source authority mismatch:{source['filename']}")

    output_record = authority["output_asset"]
    output = Path(output_record["absolute_operational_path"])
    require(digest(output) == output_record["sha256"], "output checksum")
    with wave.open(str(output), "rb") as wav:
        facts = (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(),
                 wav.getnframes(), wav.getcomptype())
        require(facts == (2, 3, 48000, 11912868, "NONE"), "output technical authority")
        peak = 0
        while True:
            raw = wav.readframes(65536)
            if not raw:
                break
            octets = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
            unsigned = (octets[:, 0].astype(np.int64)
                        | (octets[:, 1].astype(np.int64) << 8)
                        | (octets[:, 2].astype(np.int64) << 16))
            signed = np.where(unsigned & (1 << 23), unsigned - (1 << 24), unsigned)
            peak = max(peak, int(np.abs(signed).max()))
    require(peak == 8388607, "peak/clipping authority")
    require(output.stat().st_size == 71477252, "output byte size")
    require(authority["replay"]["classification"] == "BYTE_IDENTICAL_REPLAY",
            "replay authority")
    require(subprocess.run(
        ("git", "rev-parse", "v0.3.0-alpha^{commit}"), cwd=ROOT,
        check=True, text=True, stdout=subprocess.PIPE,
    ).stdout.strip() == "c7b9b65362303ff17c48897c4d26a518595fe9c5",
            "JGA release authority")
    print(json.dumps({
        "authority_fingerprint": expected_fingerprint,
        "authority_id": "PR-CEDVAL006-CONTROLLED-MIXDOWN-001",
        "output_sha256": output_record["sha256"],
        "raw_provider_assets_unchanged": True,
        "status": "PASS",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"FAIL:{exc}", file=sys.stderr)
        raise SystemExit(1)
