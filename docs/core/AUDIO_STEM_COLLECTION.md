# AudioStemCollection

## Purpose

`AudioStemCollection` is the logical input of the JGA Core.

It represents the complete set of audio stems produced by the Acquisition Layer and delivered to the Core.

The collection is independent from source separation algorithms and from every acquisition technology.

---

## Layer

Core

---

## Responsibilities

- contain AudioStem objects;
- preserve their ordering;
- provide uniform access to every stem;
- guarantee collection consistency.

---

## Non Responsibilities

- load audio files;
- perform source separation;
- execute DSP algorithms;
- perform musical interpretation.

---

## Relationships

Acquisition Layer

↓

AudioStemCollection

↓

Observation

↓

DSP

↓

Domain

↓

Analysis

---

## Invariants

- contains only `core.AudioStem`;
- never contains raw recordings;
- never depends on Domain entities;
- never depends on source separation implementations.