# Current recovery and review toolchain — 7 November 2026

Use root JGA_BOOTSTRAP.md (riferimento non distribuito in questa proiezione pubblica) together with the
persistent NEWCHAT handoff (riferimento non distribuito in questa proiezione pubblica). This is a local,
uncommitted documentary checkpoint; old checkpoints are preserved in their
original scientific/project records and in the verified pre-edit SSD snapshot.
Read the actual registry, current authority and access gates before execution.

## Environment

CPython 3.13.14; use the project's `.venv` for the documented technical checks.
The observed dependency snapshot and fresh-install limits are in the
review guide (riferimento non distribuito in questa proiezione pubblica). Core/review metadata
is declared in `pyproject.toml`; requirements.txt references that declaration.
Demucs/PyYAML and scientific campaign environments are not implicitly installed
or qualified. Do not use bootstrap's full workflow as a review smoke test.

## Recovery generation and writes

`tools/bootstrap/bootstrap_generator.py:render_bootstrap` is the canonical
deterministic renderer. This task installs its exact bytes via the existing
governed atomic writer and synchronous backup. Root bootstrap is not hand-edited;
there is no second current bootstrap. The full `tools/bootstrap.py` command also
runs tests/exports and is not authorized merely by session startup.

Use the common Git owner lease before every persistent mutation; serialize
registry/ledger, code/docs and external outputs. Verify the baseline and preserve
unrelated work. Use existing per-file copy/hash verification immediately after
each closed artifact, then the required inventory. Never delete mirror orphans.

## Resource and recovery qualifications

The 7 November personal recovery installed the four exact accounting payloads
and the hash-bound analytical-document read grant. Seven historical reservations
were charged in full, with actual CPU remaining UNKNOWN; preparation and recovery
reservations were also fully charged. A debit is not a measured whole-job CPU
duration and does not repair historical output nonconformance. The signed
accounting contract's original PROPOSED label is preserved as provenance; the
verified recovery receipt establishes the installed version's actual state.

The documentary task has zero scientific launches, detector runs, scoring,
training and WAV reads. Ordinary administration remains bounded by its signed
UTC-day limits and existing resource journal. Global backup has its separate
scheduled allowance; no restart replenishes reservations.

## Review and publication

See the review guide (riferimento non distribuito in questa proiezione pubblica) for the bounded
test command and the audit (riferimento non distribuito in questa proiezione pubblica) for release
exclusions and website/communications drafts. Pure technical tests are not a
scientific rerun. No commit, push, release, website deployment, email or external
contact follows from this checkpoint. An external exact-commit handoff remains
gated while these updates are uncommitted.
