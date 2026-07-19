# Jazz Groove Analyzer (JGA)

# Domain Service Specification

# PulseSequenceValidator

## Purpose

The PulseSequenceValidator verifies that a sequence of Pulse entities
satisfies the structural preconditions required for metric reconstruction.

The validator performs validation only.

It never modifies, reorders or reconstructs the sequence.

## Responsibilities

- validate the input sequence;
- validate Pulse instances;
- validate chronological ordering;
- reject invalid sequences.

## Non-responsibilities

The validator never:

- reconstructs the Internal Metric Timeline;
- estimates tempo;
- infers metric structure;
- modifies Pulse entities.
