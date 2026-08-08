# M81 — Ground Truth Model

Status:
WORK IN PROGRESS

---

## Purpose

This document specifies the canonical scientific
representation used as validation reference.

Ground Truth is NOT an analysis result.

Ground Truth is an independent observable musical
reference extracted from MusicXML.

---

## Scientific Principles

The Ground Truth model:

- is immutable;
- is independent from JGA;
- contains no inferred information;
- preserves only observable musical facts;
- is suitable for automatic comparison.

---

## Candidate Entities

GroundTruth

GroundTruthMeasure

GroundTruthBeat

GroundTruthEvent

GroundTruthTempo

GroundTruthTimeSignature

GroundTruthSection

GroundTruthBeat and GroundTruthEvent remain candidate
concepts and are not part of the mandatory M83 scope.

The canonical identity, authoritative source, minimum
quantities and normalization rules for the first Ground
Truth reference are defined by AD-028.


---

## Ground Truth Construction

Ground Truth is not the original score.

Ground Truth is a scientific representation
constructed from an authoritative source.

Examples of authoritative sources include:

- MusicXML
- MIDI
- Human annotated datasets

The source document remains immutable.

Ground Truth is the normalized scientific
representation used for validation.

Source
    ↓
Ground Truth Loader
    ↓
Ground Truth Model
    ↓
Validation Comparator

---

## Normalization

Different score formats may represent the same
musical information differently.

The Ground Truth layer normalizes these
differences into a canonical representation.

Normalization examples include:

- pickup measures
- tied notes
- implicit rests
- repeat notation
- multiple voices
- divisions conversion

The Validation Comparator never reads MusicXML
directly.

It always consumes the Ground Truth Model.


---

# Ground Truth Architecture

The Ground Truth Layer is composed of four
independent architectural components.

Authoritative Source
        │
        ▼
GroundTruthLoader
        │
        ▼
GroundTruthModel
        │
        ▼
GroundTruthComparator
        │
        ▼
ValidationReport

---

## Component Responsibilities

### Authoritative Source

Provides the original musical reference.

Examples:

- MusicXML
- MIDI
- Annotated datasets

---

### GroundTruthLoader

Responsible only for reading the source
and constructing the Ground Truth Model.

It performs no validation.

It performs no comparison.

---

### GroundTruthModel

Canonical immutable representation of
observable musical facts.

Independent from source format.

Independent from JGA.

---

### GroundTruthComparator

Receives:

- GroundTruthModel
- Immutable Analysis Representation

Produces only measurable differences.

It never performs reconstruction.

The Immutable Analysis Representation is defined by
AD-027. The comparator never consumes mutable runtime
state.

---

### ValidationReport

Scientific document describing:

- expected values
- observed values
- deviations
- accuracy
- conclusions


---

## Architectural Invariants

The following rules are mandatory.

1.

Ground Truth is immutable.

2.

Ground Truth never contains JGA Domain objects.

3.

Ground Truth never depends on the analysis pipeline.

4.

The Validation Comparator never modifies
Ground Truth.

5.

The Validation Comparator never modifies the
Immutable Analysis Representation.

6.

Validation always compares two immutable
representations.

7.

Scientific reports are reproducible from
the same inputs.

---

## Scientific Consequences

Validation becomes completely deterministic.

Different versions of JGA can therefore be
compared against the same Ground Truth.

This allows objective scientific evaluation
of every architectural evolution.
