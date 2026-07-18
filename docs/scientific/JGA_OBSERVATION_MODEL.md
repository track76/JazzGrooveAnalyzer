# JGA Observation Model

Status: Draft

## Purpose

This document defines the scientific observation process adopted by the Jazz Groove Analyzer (JGA).

It specifies how observable musical evidence is progressively constructed before any semantic interpretation is performed.

The Observation Model represents the scientific bridge between the physical audio signal and the Domain Model.

---

## Scientific Scope

The Observation Model describes only observable phenomena.

It does not assign musical meaning.

It does not identify harmony.

It does not classify musical styles.

Its purpose is to transform physical observations into structured observable evidence.

---

# Observation Levels

The observation process is organized into progressive levels.

Each level produces the input for the following one.

---

## Level A0 — Ensemble Understanding

Level A0 identifies the beginning of the metrically stable musical performance.

Its objective is to determine when rhythmic analysis may legitimately start.

Typical responsibilities include:

- detecting non-metric introductions;
- identifying the beginning of ensemble interaction;
- identifying the stable metric regime;
- estimating the global meter (4/4, 3/4, 5/4, 12/8, etc.).

The output of Level A0 defines the temporal origin of the subsequent observation process.

---

## Level 1 — Observable Events

Level 1 extracts observable temporal events from the audio signal.

These events represent measurable temporal evidence without musical interpretation.

Observable events may include:

- onsets;
- transients;
- pulse candidates;
- temporal features.

---

## Level 2 — Observable Metric Context

Observable events become progressively organized into an Observable Metric Context.

At this stage the system begins to identify temporal organization without assigning semantic musical meaning.

The Metric Context emerges from the relationships among observable events.

---

## Level 3 — Metric Behaviour

Once the Metric Context has become sufficiently stable, the system may observe collective metric behaviour.

This level describes how rhythmic organization evolves over time.

Metric behaviour represents the final observable stage before semantic interpretation.

---

## Relationship with the Metric Context

The Observation Model progressively constructs the Observable Metric Context.

The Metric Context is therefore an emergent result of observation rather than an initial assumption.

---

## Relationship with TAC

The Temporal Alignment Context (TAC) organizes temporal relationships among observable events.

It provides the temporal evidence required before Domain entities may be constructed.

---

## Relationship with the Domain Model

The Domain Model consumes the observable evidence produced by the Observation Model.

The Observation Model never creates semantic entities.

The Domain Model never replaces scientific observation.

---

## Architectural Consequences

The Observation Model establishes the scientific boundary between physical observation and semantic interpretation.

Its outputs become the canonical inputs of the Translation Layer.
