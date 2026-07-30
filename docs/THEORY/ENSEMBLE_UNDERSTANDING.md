# Ensemble Understanding

## Purpose

The Ensemble Understanding layer assigns musical roles
to observed sources inside an ensemble.

Instrument classification answers:

"What sound source is observed?"

Ensemble understanding answers:

"What musical function does this source perform?"

---

# Principle

Instrument identity and musical role are separate concepts.

A source can have different musical functions depending
on the musical context.

---

# Input

The layer receives:

- ObservedSourceCollection
- InstrumentClassification results

---

# Output

The layer produces:

EnsembleProfile

containing:

- source role assignments
- ensemble relationships
- musical functions

---

# Scientific Principles

- observable information only
- deterministic interpretation
- no machine learning
- no hidden assumptions
- explainable decisions

---

# Initial Musical Roles

## Rhythmic Foundation

Sources contributing to temporal reference.

Examples:

- bass
- percussion


## Harmonic Support

Sources contributing harmonic structure.

Examples:

- piano
- guitar


## Melodic Source

Sources carrying melodic information.

Examples:

- voice
- wind instruments

---

# Separation Principle

Instrument classification and musical role inference
must remain independent layers.

