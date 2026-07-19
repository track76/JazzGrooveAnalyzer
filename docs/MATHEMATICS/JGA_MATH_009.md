# JGA-MATH-009

# Formal Mathematical Model of the Jazz Groove Analyzer

**Document ID:** JGA-MATH-009

**Version:** 2.1

**Status:** Official

**Project:** Jazz Groove Analyzer (JGA)

**Author:** Angelo Tracanna

---

# 1. Purpose

The purpose of this document is to define the formal mathematical model of the Jazz Groove Analyzer.

The model integrates every concept introduced throughout the Mathematical Foundations.

It represents the unique mathematical specification upon which every future computational implementation shall be based.

---

# 2. Mathematical Universe

## Definition 2.1

Let

𝕌

denote the mathematical universe of the Jazz Groove Analyzer.

Every mathematical entity belongs to 𝕌.

---

# 3. Fundamental Domains

The mathematical universe is partitioned into two domains.

Observation Domain

ℴ

Representation Domain

ℛ

such that

ℴ ⊂ 𝕌

ℛ ⊂ 𝕌

ℴ ∩ ℛ = ∅

and

𝕌 = ℴ ∪ ℛ

---

# 4. Fundamental Objects

The Observation Domain contains

𝒜

Audio Signal

𝒯

Transient

𝒪

Onset

𝒫𝒞

Pulse Candidate

The Representation Domain contains

ℰ

Elementary Metric Event

𝓒

Metric Cluster

𝒫

Pulse

ℐ

Internal Metric Timeline

---

# 5. Hierarchy

The abstraction hierarchy is defined by

𝒜

↓

𝒯

↓

𝒪

↓

𝒫𝒞

↓

ℰ

↓

𝓒

↓

𝒫

↓

ℐ

No mathematical object may bypass an intermediate abstraction level.

---

# 6. Transformations

Let

τ₁

be the transformation

𝒜 → 𝒯

τ₂

𝒯 → 𝒪

τ₃

𝒪 → 𝒫𝒞

τ₄

𝒫𝒞 → ℰ

τ₅

ℰ → 𝓒

τ₆

𝓒 → 𝒫

τ₇

𝒫 → ℐ

The complete mathematical model is therefore

τ₇ ∘ τ₆ ∘ τ₅ ∘ τ₄ ∘ τ₃ ∘ τ₂ ∘ τ₁

---

# 6.1 Transformation τ₇ — Internal Metric Timeline Reconstruction

Let

P = (p₁, p₂, …, pₙ)

be an ordered sequence of Pulse entities.

The transformation

τ₇(P) = ℐ

reconstructs the Internal Metric Timeline associated with the complete
Pulse sequence.

τ₇ operates on the sequence as a whole rather than on individual Pulse
entities.

The transformation satisfies the following mathematical properties:

- determinism;
- preservation of Pulse identity;
- preservation of chronological ordering;
- preservation of physical timestamps;
- preservation of temporal continuity.

No additional Pulse entities are created and no existing Pulse entities
are modified.

---

# 7. Formal Properties

The model satisfies the following properties.

• Uniqueness

• Identity

• Consistency

• Closure

• Hierarchy Preservation

• Semantic Preservation

• Implementation Independence

• Extensibility

---

## Representational Fidelity

Every mathematical transformation defined within the Jazz Groove Analyzer
is representational.

A transformation maps an object to a higher abstraction level without
altering the observed phenomenon.

Consequently, every transformation τ₁ … τ₇ preserves:

- object identity whenever applicable;
- physical timestamps;
- chronological ordering;
- observable information.

No mathematical transformation defined by the Jazz Groove Analyzer may:

- modify the observed phenomenon;
- generate artificial observations;
- perform temporal realignment;
- perform temporal quantization.

Every transformation changes only the representational domain while
preserving the observed musical behaviour.

---

# 8. Axioms

## Axiom 1

Every mathematical object possesses one unique formal definition.

---

## Axiom 2

Every mathematical object belongs to exactly one abstraction level.

---
