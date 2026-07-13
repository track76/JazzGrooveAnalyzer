# Jazz Groove Analyzer — Bootstrap

> Bootstrap document for initializing a new development session.
>
> In future releases this document will be generated automatically by
> `tools/export_chat_context.py`.
>
> It is **not** the source of truth.
>
> If any information conflicts with the repository, **the repository always prevails**.

---

## Purpose

This document provides the minimum context required to continue the development of the Jazz Groove Analyzer (JGA) from the current project state.

When used together with **JGA_CONTEXT.zip**, it enables the project to resume from the current milestone without restating development rules or architectural decisions.

---

## Project

- **Project:** Jazz Groove Analyzer (JGA)
- **Repository:** Single source of truth.

---

## Development Rules

1. Verify the repository before proposing any modification.
2. Reason about architecture and layer responsibilities before implementation.
3. Design before implementation.
4. One atomic change at a time.
5. After every modification:
   - `git diff`
   - `pytest`
   - `git commit`
   - `git push`
6. Do not perform unnecessary refactoring.
7. Update documentation only when the architecture or the project status actually changes.

---

## Official Documentation

- `docs/JGA_PROJECT_STATE.md`
- `docs/JGA_ARCHITECTURE.md`
- `docs/JGA_THEORETICAL_FRAMEWORK.md`
- `docs/JGA_DOMAIN_MODEL.md`
- `docs/ROADMAP.md`
- `docs/CHANGELOG.md`

---

## Working Instructions

Continue development from the current milestone.

Do not reconsider architectural decisions that have already been approved and documented.

Always use the repository as the primary reference for every technical decision.

If documentation and code differ, **the repository always prevails**.

---

## Context

The accompanying **JGA_CONTEXT.zip** contains the project snapshot associated with this bootstrap.

Use this bootstrap together with **JGA_CONTEXT.zip** to initialize a new development session.
