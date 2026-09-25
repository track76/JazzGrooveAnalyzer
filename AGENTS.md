# Jazz Groove Analyzer — Agent Operating Guide

## 1. Purpose and Scope

This document defines the operational conduct of AI coding agents
contributing to JGA. It does not replace scientific, architectural or
implementation documentation.

## 2. Source Authority and Knowledge Hierarchy

The repository is the canonical source of truth. Follow the knowledge
hierarchy defined by the Development Constitution and the scientific
documentation. Reference canonical documents instead of duplicating
their content.

## 3. Session Startup Procedure

Before modifying a file:

1. Read this file.
2. Load root `JGA_BOOTSTRAP.md` as the sole current session recovery
   entry point.
3. Inspect the repository evidence relevant to the requested work.
4. Summarize the current state and any architectural ambiguities.
5. Obtain approval before making changes.

The bootstrap initializes a session; the repository remains canonical.
If they conflict, report the Evidence Conflict and stop until
clarification is provided.

## 4. Evidence Classification and Reporting

Classify each statement according to the JGA Knowledge Model. Do not
present an inference or assumption as an observed fact. Report
insufficient evidence and Evidence Conflicts; stop work that depends
on them until clarification is provided.

## 5. Scientific and Implementation Responsibilities

Do not introduce undocumented scientific concepts. Do not create
scientific or architectural decisions without human approval. Preserve
Ground Truth independence as defined by the Scientific Validation
Protocol.

## 6. Mandatory Development Workflow

Follow the Development Constitution: theory, architecture,
implementation, tests and validation. Do not bypass the documented
workflow.

## 7. Architectural Constraints

Preserve documented boundaries and dependency direction. Do not make
autonomous architectural changes. Refer to the architecture documents
and approved decisions when evaluating a change.

## 8. Ambiguities, Evidence Conflicts, and Stop Conditions

When requirements, scientific meaning, architectural ownership or
authoritative sources are unclear or incompatible, stop and request
clarification. Do not resolve the ambiguity autonomously.

## 9. Documentation and Repository Storage Policy

Treat scientific documentation and validation records according to the
Knowledge Model and Scientific Knowledge Record. Avoid duplication:
add references when existing documentation is sufficient. Preserve
generated artifacts through their documented workflows.

## 10. Required Deliverables

For approved work, provide modified files, scientific and
architectural rationale, applicable validation evidence,
cross-reference verification and unresolved inconsistencies.

## Governing References

- `docs/JGA_DEVELOPMENT_CONSTITUTION.md`
- `docs/scientific/README.md`
- `docs/scientific/JGA_SCIENTIFIC_MANIFESTO.md`
- `docs/scientific/foundations/JGA_KNOWLEDGE_MODEL.md`
- `docs/scientific/foundations/F-030_SCIENTIFIC_KNOWLEDGE_RECORD.md`
- `docs/scientific/JGA_OBSERVATION_MODEL.md`
- `docs/scientific/JGA_SCIENTIFIC_VALIDATION_PROTOCOL.md`
- `docs/JGA_ARCHITECTURE.md`
- `docs/architecture/CORE_DOMAIN_BOUNDARY.md`
- `docs/JGA_DECISIONS.md`
- `docs/JGA_PROJECT_STATE.md`
- `docs/TOOLCHAIN/DEVELOPER_TOOLCHAIN.md`

## Permanent continuous external backup gate

Before every writing workflow, read
`docs/project/CONTINUOUS_EXTERNAL_BACKUP_AUTHORITY.md` and run
`python3 tools/continuous_backup.py check`. After each relevant file is fully
closed and atomically installed, immediately copy/hash-verify it with
`python3 tools/continuous_backup.py files <repository-relative-path>` before
dependent work. Back up batch outputs incrementally and inventory after the batch.
Before commit run `python3 tools/continuous_backup.py staged`. Never delete mirror
orphans. If unavailable, report CONTINUOUS EXTERNAL BACKUP UNAVAILABLE and ask PI
about stopping versus explicit backup debt; never silently continue.
