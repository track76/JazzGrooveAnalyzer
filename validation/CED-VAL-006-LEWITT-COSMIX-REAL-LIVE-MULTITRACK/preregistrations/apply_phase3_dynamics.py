#!/usr/bin/env python3
"""Frozen Phase-3 transform; do not run before PI execution approval."""

import argparse
import numpy as np
import soundfile as sf

THRESHOLD = 10.0 ** (-30.0 / 20.0)

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()
x, rate = sf.read(args.input, dtype="float64", always_2d=True)
a = np.abs(x)
y = x.copy()
mask = (a > 0.0) & (a < THRESHOLD)
y[mask] = np.sign(x[mask]) * THRESHOLD * np.sqrt(a[mask] / THRESHOLD)
if np.max(np.abs(y)) > 1.0 or np.max(np.abs(y)) > np.max(a):
    raise RuntimeError("clipping/peak-preservation failure")
sf.write(args.output, y.astype(np.float32), rate, subtype="FLOAT")
