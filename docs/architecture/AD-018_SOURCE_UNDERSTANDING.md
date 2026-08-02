# AD-018 — Source Understanding Boundary

Status: ACCEPTED

## Problem

The Source Understanding layer produces semantic observations
derived from the audio signal.

These observations must become available to the Domain layer
without introducing coupling between the two subsystems.

## Decision

The Source Understanding layer SHALL terminate with an
ObservedSourceCollection.

ObservedSourceCollection SHALL NOT enter the Domain layer.

Integration between Source Understanding and Domain SHALL occur
through an explicit Boundary Translation component
(Semantic Bridge).

The Semantic Bridge is responsible for translating semantic
observations into Domain entities.

The Domain layer remains completely independent from the
Source Understanding implementation.

## Architecture

AudioStemCollection
        │
        ▼
Source Understanding
        │
        ▼
ObservedSourceCollection
        │
        ▼
Semantic Bridge
        │
        ▼
tuple[SoundSource]
        │
        ▼
Domain Services

## Consequences

- explicit architectural boundary
- explicit translation step
- no dependency from Domain to Source Understanding
- no dependency from Source Understanding to Domain
- full traceability of semantic translations
