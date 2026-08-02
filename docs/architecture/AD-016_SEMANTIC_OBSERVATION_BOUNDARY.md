# AD-016 — Semantic Observation Boundary

Status: ACCEPTED

## Decision

The Source Understanding layer produces semantic observations.

The Domain layer remains the only layer allowed to instantiate:

- SoundSource
- MusicalFunction
- MetricContributor

No translator may directly construct Domain objects from
Source Understanding outputs.

Integration between the two layers must occur through an
explicit provider/bridge.

## Rationale

- preserves Domain independence
- preserves Source Understanding independence
- explicit transformations
- no duplicated responsibilities
