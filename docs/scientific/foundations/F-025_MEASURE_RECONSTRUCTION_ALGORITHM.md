# F-025 — Measure Reconstruction Algorithm

## Purpose

A Reconstructed Measure is obtained by grouping an ordered sequence of
Beat References according to the reconstructed internal metric.

## Input

- Ordered Beat References
- Internal Time Signature
- Internal BPM

## Algorithm

1. Beat References are processed in chronological order.
2. Consecutive Beat References are grouped according to the current
   internal time signature.
3. Each complete group generates one Reconstructed Measure.
4. Every generated measure preserves traceability to the originating
   Beat References and Metric Clusters.

## Output

An ordered sequence of ReconstructedMeasure objects.

The reconstruction is deterministic and reproducible.

