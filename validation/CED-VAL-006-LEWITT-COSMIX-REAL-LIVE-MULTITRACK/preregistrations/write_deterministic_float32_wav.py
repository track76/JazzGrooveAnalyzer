#!/usr/bin/env python3
"""Serialize an already-frozen float32 sample population deterministically."""

import argparse
from hashlib import sha256
from pathlib import Path

import soundfile as sf

SFC_SET_ADD_PEAK_CHUNK = 0x1050
SF_FALSE = 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--expected-decoded-sha256", required=True)
    args = parser.parse_args()

    samples, rate = sf.read(args.input, dtype="float32", always_2d=True)
    decoded_sha256 = sha256(samples.tobytes(order="C")).hexdigest()
    if decoded_sha256 != args.expected_decoded_sha256:
        raise RuntimeError("decoded-sample authority failure")
    if rate != 44100 or samples.shape != (10944947, 2):
        raise RuntimeError("technical audio authority failure")

    with sf.SoundFile(
        args.output,
        mode="w",
        samplerate=44100,
        channels=2,
        format="WAV",
        subtype="FLOAT",
    ) as output:
        result = sf._snd.sf_command(
            output._file, SFC_SET_ADD_PEAK_CHUNK, sf._ffi.NULL, SF_FALSE
        )
        if result != 0:
            raise RuntimeError("PEAK-chunk suppression command failed")
        output.write(samples)

    replay, replay_rate = sf.read(args.output, dtype="float32", always_2d=True)
    if replay_rate != rate or sha256(replay.tobytes(order="C")).hexdigest() != decoded_sha256:
        raise RuntimeError("serialized decoded-sample equivalence failure")
    print(decoded_sha256)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
