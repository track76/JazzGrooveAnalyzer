from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]


def git(cmd):
    return subprocess.check_output(
        cmd,
        text=True,
    ).strip()


CANONICAL_DOCUMENTS = [

    # =====================================================
    # Scientific Documentation
    # =====================================================

    "docs/scientific/README.md",
    "docs/JGA_DEVELOPMENT_CONSTITUTION.md",
    "docs/scientific/JGA_SCIENTIFIC_MANIFESTO.md",
    "docs/scientific/JGA_OBSERVATION_MODEL.md",
    "docs/scientific/JGA_METRIC_CONTEXT.md",
    "docs/scientific/JGA_TAC_OBSERVATION_MODEL.md",
    "docs/scientific/JGA_TAC_DOMAIN_MAPPING.md",

    # =====================================================
    # Scientific Foundations
    # =====================================================

    "docs/scientific/foundations/F-001_SCIENTIFIC_OBSERVATION.md",
    "docs/scientific/foundations/F-002_OBSERVABLE_MUSICAL_FACTS.md",
    "docs/scientific/foundations/F-003_OBSERVABLE_METRIC_CONTEXT.md",
    "docs/scientific/foundations/F-004_METRIC_PROJECTION.md",
    "docs/scientific/foundations/F-005_ENSEMBLE_BEHAVIOUR.md",
    "docs/scientific/foundations/F-006_HISTORICAL_COMPARISON.md",

    # =====================================================
    # Canonical Theory
    # =====================================================

    "docs/JGA_THEORETICAL_FRAMEWORK.md",
    "docs/JGA_METHOD.md",
    "docs/JGA_PRINCIPLES.md",

    # =====================================================
    # Architecture
    # =====================================================

    "docs/JGA_ARCHITECTURE.md",
    "docs/architecture/CORE_DOMAIN_BOUNDARY.md",
    "docs/architecture/REPRESENTATION_TRANSLATION.md",

    # =====================================================
    # Domain
    # =====================================================

    "docs/JGA_DOMAIN_MODEL.md",
    "docs/domain/DOMAIN_MODEL_MAP.md",

    # =====================================================
    # Project
    # =====================================================

    "docs/JGA_DECISIONS.md",
    "docs/JGA_PROJECT_STATE.md",
]


def generate_bootstrap():

    branch = git(["git", "branch", "--show-current"])
    commit = git(["git", "rev-parse", "--short", "HEAD"])

    docs = "\n".join(f"- {d}" for d in CANONICAL_DOCUMENTS)

    text = f"""# Jazz Groove Analyzer (JGA)

Branch: {branch}

Commit: {commit}

Repository is the source of truth.

Run

python tools/bootstrap.py

before every ChatGPT session.

============================================================
Knowledge Hierarchy
============================================================

Scientific Theory
        ↓
Scientific Observation Model
        ↓
Architecture
        ↓
Domain Model
        ↓
Implementation

Theory precedes implementation.

============================================================
Development Constitution
============================================================

Always follow:

- docs/JGA_DEVELOPMENT_CONSTITUTION.md

The Development Constitution defines the
mandatory development methodology of JGA.

When implementation convenience conflicts
with the Constitution, the Constitution
always prevails.

============================================================
Canonical Documents
============================================================

{docs}

============================================================
Development Workflow
============================================================

Theory
        ↓
Architecture
        ↓
Implementation
        ↓
Tests
        ↓
Validation

============================================================
Current Project State
============================================================

Always refer to:

- docs/JGA_PROJECT_STATE.md

for the current implementation status.
"""

    (
        ROOT
        / "artifacts"
        / "JGA_BOOTSTRAP.md"
    ).write_text(
        text,
        encoding="utf-8",
    )
