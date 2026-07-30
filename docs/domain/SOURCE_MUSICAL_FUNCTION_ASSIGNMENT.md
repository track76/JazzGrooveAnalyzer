# Source Musical Function Assignment

## Purpose

Represents the relationship between a SoundSource and a
MusicalFunction inside an ensemble context.

---

## Architectural Position

Layer:

Domain Layer

---

## Motivation

Instrument identity and musical function are different
concepts.

A SoundSource may perform different musical functions
depending on the musical context.

The relationship must therefore be explicitly represented.

---

## Model

SourceMusicalFunctionAssignment

Fields:

- id
- sound_source_id
- musical_function_id
- confidence
- rationale
- created_at

---

## Principles

- explicit relationship
- deterministic interpretation
- explainable assignment
- no implicit musical assumptions

---

## Relationship

SoundSource

↓

SourceMusicalFunctionAssignment

↓

MusicalFunction
