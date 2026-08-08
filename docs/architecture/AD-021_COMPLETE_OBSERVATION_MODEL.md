# AD-021

Status

ACCEPTED

Title

Complete Observation Model

## Decision

Jazz Groove Analyzer analyzes the complete observable
musical signal.

No component of the pipeline may discard observations
according to an estimated analysis starting point.

Metric Stability is an observable descriptor of musical
behaviour.

Metric Stability shall never determine whether a musical
event belongs to the scientific observation.

## Consequences

AnalysisStartFilter is obsolete.

IntroDetector is no longer part of the analytical
decision process.

PulseCandidateBuilder extracts every observable pulse.

The complete recording becomes the scientific object
of observation.

## Validation

VAL-001

Validation Status

PASSED

Scientific Status

ACCEPTED

