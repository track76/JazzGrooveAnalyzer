# AD-026 — Bootstrap Architecture

Status

LOCKED

Date

2026-08-01

---

# Purpose

The Bootstrap subsystem is the official mechanism for transferring the
architectural and scientific state of the Jazz Groove Analyzer (JGA)
to a new development session.

Its purpose is not to back up the repository, but to reconstruct the
minimum complete context required to continue development without
losing architectural consistency.

The Bootstrap is therefore considered an integral part of the JGA
development workflow.

---

# Motivation

The JGA project evolves over long periods and spans multiple
development sessions.

Because conversational context is limited, the project requires a
deterministic mechanism capable of reconstructing the current
architectural state from the repository itself.

The Bootstrap subsystem generates a coherent set of derived documents
that summarize the current repository state while preserving the
repository as the unique source of truth.


---

# Bootstrap Principles

## BP-001 — Single Source of Truth

Every mutable project metadata shall have exactly one canonical source.

Generated documents shall never become independent sources of project
information.

---

## BP-002 — Separation of Responsibilities

Each Bootstrap document shall have exactly one responsibility.

No generated document shall duplicate the purpose of another generated
document.

---

## BP-003 — Source Documents

Source documents are maintained manually and represent the permanent
knowledge of the project.

They shall never be generated automatically.

---

## BP-004 — Generated Documents

Generated documents are deterministic artifacts produced exclusively
from source documents and repository inspection.

They shall never contain manually maintained information.

---

## BP-005 — Deterministic Generation

Running the Bootstrap Generator multiple times without repository
changes shall always produce identical artifacts.

---

## BP-006 — Repository First

The repository is the authoritative representation of the project.

The Bootstrap summarizes the repository but never replaces it.


---

# Bootstrap Architecture

The Bootstrap subsystem is composed of two categories of documents:

1. Source Documents

2. Generated Artifacts

Only Source Documents constitute the permanent knowledge of the project.

Generated Artifacts are disposable representations derived from the
current repository state.

No Generated Artifact shall become a source document.

---

# Source Documents

The following documents constitute the canonical knowledge of the
project.

PROJECT_METADATA.md

Maintains the canonical project metadata.

Examples:

- version

- current milestone

- current phase

- branch

- tests

- last update

---

JGA_PROJECT_STATE.md

Maintains the project roadmap, milestone descriptions,
implementation status and historical evolution.

---

JGA_DECISIONS.md

Maintains the chronological list of Architectural Decisions.

---

Architecture Documents

Describe the permanent architectural structure of the project.

---

Scientific Foundations

Describe the scientific model independently from the software
implementation.

---

Repository

The repository remains the authoritative representation of the
implemented system.

---

# Generated Artifacts

Generated Artifacts are reconstructed automatically from Source
Documents and repository inspection.

They contain no unique knowledge.

Current Bootstrap artifacts include:

JGA_BOOTSTRAP.md

artifacts/JGA_SESSION_CONTEXT.md

JGA_PIPELINE_STATE.md

JGA_RUNTIME_STATE.md

JGA_SCIENTIFIC_STATE.md

JGA_ARCHITECTURE_MAP.md

JGA_CONTEXT.zip

JGA_REPOSITORY.zip


---

# Export Contracts

Each Bootstrap exporter is responsible for producing exactly one
Generated Artifact.

Every exporter shall explicitly define:

- input documents

- repository information used

- output artifact

- forbidden responsibilities

No exporter shall generate information owned by another exporter.

---

## Project State Exporter

Input

PROJECT_METADATA.md

JGA_PROJECT_STATE.md

Output

JGA_PROJECT_STATE.md

Responsibility

Updates dynamic project metadata while preserving manually maintained
project documentation.

Forbidden

Generating scientific summaries.

Generating runtime information.

Generating session context.

---

## Scientific State Exporter

Input

PROJECT_METADATA.md

Repository inspection

Pipeline inspection

Output

JGA_SCIENTIFIC_STATE.md

Responsibility

Summarizes the current scientific implementation state.

Forbidden

Maintaining roadmap information.

Maintaining historical documentation.

---

## Runtime State Exporter

Input

Repository inspection

Pipeline inspection

Output

JGA_RUNTIME_STATE.md

Responsibility

Describes the current Runtime architecture.

Forbidden

Maintaining scientific roadmap information.

---

## Pipeline State Exporter

Input

Pipeline inspection

Output

JGA_PIPELINE_STATE.md

Responsibility

Describes the ordered execution pipeline.

Forbidden

Maintaining implementation status.

Maintaining milestone information.

---

## Session Context Exporter

Input

PROJECT_METADATA.md

Generated Artifacts

Output

artifacts/JGA_SESSION_CONTEXT.md

Responsibility

Produces the minimum operational context required to continue
development in a new session.

Forbidden

Duplicating complete project documentation.

---

## Bootstrap Generator

Input

All Generated Artifacts

Repository inspection

Output

JGA_BOOTSTRAP.md

JGA_CONTEXT.zip

JGA_REPOSITORY.zip

Responsibility

Packages the Bootstrap artifacts required to transfer the project to a
new development session.

Forbidden

Generating scientific information.

Generating architectural documentation.


---

# Dependency Graph

The Bootstrap subsystem shall respect the following dependency graph.

Source Documents

↓

Repository Inspection

↓

Bootstrap Exporters

↓

Generated Artifacts

↓

Bootstrap Package

↓

New Development Session

Dependencies shall always flow in this direction.

Generated Artifacts shall never become inputs of Source Documents.

---

# Bootstrap Workflow

The official Bootstrap workflow is defined as follows.

Developer updates the repository.

↓

Developer executes the complete validation suite.

↓

Developer commits and pushes the repository.

↓

Bootstrap Generator inspects the repository.

↓

Bootstrap Exporters generate all derived artifacts.

↓

Bootstrap Package is produced.

↓

A new development session starts from the generated Bootstrap.

The Bootstrap shall always represent the exact state of the repository
at the time of generation.

---

# Architectural Rules

AR-001

PROJECT_METADATA.md is the unique source of mutable project metadata.

---

AR-002

Every Generated Artifact shall be reproducible from Source Documents
and repository inspection.

---

AR-003

Generated Artifacts shall never contain unique project knowledge.

---

AR-004

Every exporter owns exactly one artifact.

---

AR-005

Bootstrap generation shall be deterministic.

Running the Bootstrap Generator multiple times without repository
changes shall always produce identical artifacts.

---

AR-006

The Bootstrap subsystem shall never modify Source Documents except when
explicitly designed to synchronize mutable metadata.

---

AR-007

A new development session shall be reconstructable exclusively from the
generated Bootstrap package together with the repository.

---

# Consequences

The Bootstrap subsystem becomes an official architectural component of
the Jazz Groove Analyzer.

Project knowledge is separated from generated representations.

Repository consistency is improved through the elimination of duplicated
metadata.

The Bootstrap becomes deterministic, reproducible and suitable for
long-term scientific development.


---


# Future Extensions

The Bootstrap architecture intentionally separates permanent project
knowledge from generated representations.

This design allows future extensions without modifying the fundamental
architecture.

Examples include:

- automatic Bootstrap validation

- repository consistency verification

- artifact integrity verification

- automatic test statistics

- repository quality metrics

- benchmark summaries

- scientific coverage reports

- documentation consistency verification

Such extensions shall remain additional Bootstrap Exporters and shall
respect the architectural principles defined by this decision.

---

# Architectural Invariants

The following invariants shall always hold.

AI-001

Every project information has exactly one owner.

---

AI-002

Every generated artifact is reproducible.

---

AI-003

No generated artifact becomes a source document.

---

AI-004

Bootstrap generation never modifies repository knowledge.

---

AI-005

Removing any generated artifact never removes project knowledge.



# Decision

The Bootstrap subsystem is adopted as an official architectural
component of the Jazz Groove Analyzer.

All future Bootstrap developments shall conform to the principles,
contracts and responsibilities defined by this Architectural Decision.

Status

LOCKED


---
