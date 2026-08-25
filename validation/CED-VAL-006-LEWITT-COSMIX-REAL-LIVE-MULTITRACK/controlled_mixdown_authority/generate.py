#!/usr/bin/env python3
"""Measure or generate the exact CED-VAL-006 controlled integer-PCM mix."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import wave

import numpy as np


PCM24_MAX = (1 << 23) - 1


def digest(path: Path) -> str:
    value = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def decode_pcm24(path: Path, expected: dict) -> np.ndarray:
    if digest(path) != expected["sha256"]:
        raise RuntimeError(f"SOURCE_CHECKSUM_MISMATCH:{expected['filename']}")
    with wave.open(str(path), "rb") as source:
        facts = (
            source.getnchannels(), source.getsampwidth(), source.getframerate(),
            source.getnframes(), source.getcomptype(),
        )
        wanted = (
            expected["channels"], 3, expected["sample_rate_hz"],
            expected["frame_count"], "NONE",
        )
        if facts != wanted:
            raise RuntimeError(f"SOURCE_TECHNICAL_MISMATCH:{expected['filename']}")
        raw = source.readframes(source.getnframes())
    octets = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
    unsigned = (
        octets[:, 0].astype(np.int64)
        | (octets[:, 1].astype(np.int64) << 8)
        | (octets[:, 2].astype(np.int64) << 16)
    )
    signed = np.where(unsigned & (1 << 23), unsigned - (1 << 24), unsigned)
    return signed.reshape(expected["frame_count"], expected["channels"])


def exact_sum(manifest: dict, source_root: Path) -> np.ndarray:
    total = np.zeros((manifest["output_frame_count"], 2), dtype=np.int64)
    ordered = sorted(manifest["sources"], key=lambda item: item["filename"].encode())
    if ordered != manifest["sources"]:
        raise RuntimeError("SOURCE_MANIFEST_ORDER_MISMATCH")
    for source in ordered:
        decoded = decode_pcm24(source_root / source["filename"], source)
        frames = source["frame_count"]
        if source["channels"] == 1:
            total[:frames, 0] += decoded[:, 0]
            total[:frames, 1] += decoded[:, 0]
        elif source["channels"] == 2:
            total[:frames] += decoded
        else:
            raise RuntimeError(f"UNSUPPORTED_CHANNEL_COUNT:{source['filename']}")
    return total


def coefficient(peak: int) -> tuple[int, int]:
    return (PCM24_MAX, peak) if peak > PCM24_MAX else (1, 1)


def quantize(total: np.ndarray, numerator: int, denominator: int) -> np.ndarray:
    magnitude = np.abs(total)
    rounded = (magnitude * numerator + denominator // 2) // denominator
    encoded = np.where(total < 0, -rounded, rounded)
    if encoded.min() < -(1 << 23) or encoded.max() > PCM24_MAX:
        raise RuntimeError("OUTPUT_CLIPPING")
    return encoded.astype(np.int32)


def pcm24_bytes(samples: np.ndarray) -> bytes:
    unsigned = samples.astype(np.int64) & ((1 << 24) - 1)
    packed = np.empty((unsigned.size, 3), dtype=np.uint8)
    flat = unsigned.reshape(-1)
    packed[:, 0] = flat & 255
    packed[:, 1] = (flat >> 8) & 255
    packed[:, 2] = (flat >> 16) & 255
    return packed.tobytes()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("measure", "generate"))
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    total = exact_sum(manifest, args.source_root)
    peak = int(np.abs(total).max())
    numerator, denominator = coefficient(peak)
    measurement = {
        "global_gain_denominator": denominator,
        "global_gain_numerator": numerator,
        "global_gain_rational": f"{numerator}/{denominator}",
        "raw_summed_absolute_peak": peak,
    }
    if args.mode == "measure":
        print(json.dumps(measurement, sort_keys=True))
        return 0
    if args.plan is None or args.output is None:
        raise RuntimeError("GENERATE_REQUIRES_PLAN_AND_OUTPUT")
    plan = json.loads(args.plan.read_text())
    for key, value in measurement.items():
        if plan[key] != value:
            raise RuntimeError(f"FROZEN_MIX_PLAN_MISMATCH:{key}")
    samples = quantize(total, numerator, denominator)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("xb") as destination:
        with wave.open(destination, "wb") as output:
            output.setnchannels(2)
            output.setsampwidth(3)
            output.setframerate(48000)
            output.setnframes(manifest["output_frame_count"])
            output.writeframes(pcm24_bytes(samples))
    print(json.dumps({
        **measurement,
        "output_absolute_peak": int(np.abs(samples).max()),
        "output_frame_count": samples.shape[0],
        "output_sha256": digest(args.output),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
