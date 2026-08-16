# JGA Scientific Research Constitution

Status: LOCKED

## Purpose and Authority

This Constitution is the highest authority governing the scientific mission,
research direction, scientific scope and scientific evolution of Jazz Groove
Analyzer (JGA).

It consolidates and protects the philosophy already established by the
Scientific Manifesto, Knowledge Model, Scientific Knowledge Record,
Observation Model, scientific Foundations and Scientific Validation Protocol.
It introduces no new scientific theory and predetermines no experimental
outcome.

The Development Constitution remains the mandatory authority for development
methodology and execution. Where scientific direction is concerned, it is
subordinate to this Constitution.

## Scientific Mission

JGA exists to develop a scientifically reproducible methodology for observing,
describing, analysing and comparing musical timing behaviour from audio
evidence.

Software supports this mission. Software development is not itself the
scientific objective.

## Governing Principles

### Research drives implementation

Implementation may proceed only when required to obtain scientifically
relevant evidence that the existing repository cannot obtain. Every proposed
implementation shall answer:

> What scientific evidence cannot be obtained with the current repository?

Without a clear answer, implementation is not justified.

### Observation before interpretation

Observation shall not assign musical meaning unsupported by evidence.
Observation, Translation and Domain responsibilities remain separated under
the Observation Model and approved architecture. Higher-level interpretation
shall not retroactively redefine lower-level observation.

### Evidence before representation

A permanent representation requires prior evidence that its subject exists,
is observable, is reproducible and directly serves the JGA mission. Potential
usefulness alone is insufficient.

### Architecture is a scientific constraint

The approved architecture is an intentional scientific boundary. Research
shall first use existing capabilities. Architecture shall not expand to
accommodate possibilities; change requires explicit scientific necessity and
the approval required by repository governance.

### Scientific minimalism and effectiveness

Research shall take the shortest scientifically valid path to evidence about
musical timing. The preferred sequence is:

Smaller experiment

→ Evidence

→ Scientific conclusion

→ Implementation only if indispensable

Additional abstraction, representation, tooling or experimental dimensions
are justified only when they materially increase scientific value.

When a scientifically simpler path exists that produces equivalent evidence,
the simpler path shall always be preferred.

### No scientific or architectural drift

JGA studies musical timing. Detector, onset-detection, DSP, audio-engineering,
algorithm-optimisation, tooling and software-architecture research may proceed
only when strictly necessary to answer a scientific question directly serving
that mission. The observation tool shall not become an independent research
objective.

Before approving a direction, ask:

> Are we studying musical timing, or are we beginning to study the observation
> tool itself?

If the tool has become the primary objective, stop and reconsider the
direction.

### Evidence hierarchy

Scientific reasoning shall preserve this progression:

Observed Fact

→ Derived Evidence

→ Scientific Interpretation

→ Musical Interpretation

Each level remains traceable to and distinguishable from the levels below it.
This progression does not replace the contributor evidence classifications of
the Knowledge Model or the Observation–Translation–Domain boundaries.

### Falsifiability, determinism and reproducibility

An experiment shall permit outcomes capable of contradicting its working
hypothesis. A design capable only of confirmation is insufficient.

Scientific claims shall rely on reproducible evidence under declared
conditions. Deterministic replay and provenance remain fundamental wherever
applicable. Ground Truth independence remains governed by SVP-001.

### Repository authority

The repository is the authoritative source of project knowledge. Repository
evidence supersedes conversational or AI memory, assumptions, undocumented
decisions and historical recollection. Evidence conflicts and uncertainty are
handled under the Knowledge Model; they shall not be resolved silently.

### Operational independence

External storage, caches, notifications, bootstrap-generation mechanics,
temporary files and local-machine configuration are operational concerns, not
scientific knowledge. They shall support research without altering scientific
meaning. Canonical assets, provenance and storage remain governed by existing
repository authority.

### Long-term scientific value

A scientific objective should materially improve at least one of:

- scientific evidence;
- reproducibility;
- methodological clarity;
- experimental validity;
- historical comparability;
- publication readiness; or
- the ability to analyse musical timing.

Objectives that primarily increase software complexity shall normally be
rejected.

## Mission Alignment Gate

Before a new scientific objective proceeds, its record shall state:

```text
Scientific Question:

Direct Contribution to JGA Mission:

Missing Scientific Evidence:

Why Existing Evidence Is Insufficient:

Smallest Experiment Capable of Obtaining the Missing Evidence:

Architectural Impact: None / Minimal / Required

Complexity Introduced:
```

If direct mission alignment cannot be demonstrated, the objective shall not
proceed.

An autonomous Scientific Research Lead may rank justified directions only by:

1. direct contribution to the JGA scientific mission;
2. missing scientific evidence;
3. experimental value;
4. simplicity;
5. minimal architectural impact; and
6. long-term scientific value.

Scientific curiosity alone is insufficient justification.

## Stop Rule

When evidence is insufficient, prefer a smaller experiment.

When interpretation is uncertain, gather evidence.

When architecture appears insufficient, first demonstrate scientifically that
the missing capability is indispensable.

Never expand architecture merely because expansion is possible.

## Governing Relationships

- The Scientific Manifesto states the philosophy protected here.
- The Knowledge Model classifies project evidence and governs uncertainty.
- F-030 preserves scientific records and provenance.
- F-031 and F-032 govern their established scientific subjects.
- The Observation Model governs construction of observable evidence.
- SVP-001 governs validation and Ground Truth independence.
- Approved architecture governs scientific boundaries and dependency direction.
- The Development Constitution governs development methodology and execution.

## Modification Policy

This Constitution is LOCKED. Modification requires explicit Principal
Investigator approval and a traceable repository decision.
