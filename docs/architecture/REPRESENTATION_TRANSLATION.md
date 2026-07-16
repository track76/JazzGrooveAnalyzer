# Representation Translation

Status: Draft

## Purpose

This document defines the contract between computational
representations produced by the Core and semantic
representations consumed by the Domain.

## Principles

The Core owns computational representations.

The Domain owns semantic representations.

No Domain object shall be directly created by DSP algorithms.

Every translation shall preserve the information required
to reconstruct the scientific model.

## Translation Boundary

AnalysisContext
        │
        ▼
Translation
        │
        ▼
Domain Services

## Future Work

The concrete translation mechanism will be introduced
during the Core–Domain integration phase.
