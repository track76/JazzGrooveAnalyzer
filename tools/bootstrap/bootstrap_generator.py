from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]


def git(cmd):
    return subprocess.check_output(
        cmd,
        text=True,
    ).strip()


CANONICAL_DOCUMENTS = [

    # Scientific Foundations

    "docs/scientific/JGA_SCIENTIFIC_MANIFESTO.md",
    "docs/scientific/JGA_OBSERVATION_MODEL.md",
    "docs/scientific/JGA_METRIC_CONTEXT.md",

    "docs/scientific/foundations/F-001_SCIENTIFIC_OBSERVATION.md",
    "docs/scientific/foundations/F-002_OBSERVABLE_MUSICAL_FACTS.md",
    "docs/scientific/foundations/F-003_OBSERVABLE_METRIC_CONTEXT.md",
    "docs/scientific/foundations/F-004_METRIC_PROJECTION.md",
    "docs/scientific/foundations/F-005_ENSEMBLE_BEHAVIOUR.md",
    "docs/scientific/foundations/F-006_HISTORICAL_COMPARISON.md",

    # Canonical Theory

    "docs/JGA_THEORETICAL_FRAMEWORK.md",
    "docs/JGA_PRINCIPLES.md",
    "docs/JGA_METRIC_STABILITY_MODEL.md",

    # Project

    "docs/JGA_PROJECT_STATE.md",
    "docs/JGA_DECISIONS.md",
]


def generate_bootstrap():

    branch = git(
        ["git", "branch", "--show-current"]
    )

    commit = git(
        ["git", "rev-parse", "--short", "HEAD"]
    )

    docs = "\n".join(
        f"- {document}"
        for document in CANONICAL_DOCUMENTS
    )

    text = f"""# Jazz Groove Analyzer

Branch: {branch}

Commit: {commit}

Repository is the source of truth.

Run

python tools/bootstrap.py

before every ChatGPT session.

------------------------------------------------------------

Canonical Documents

{docs}

------------------------------------------------------------

Development Workflow

Scientific Foundations
        ↓
Specifications
        ↓
Implementation
        ↓
Tests
        ↓
Validation

"""

    (
        ROOT
        / "artifacts"
        / "JGA_BOOTSTRAP.md"
    ).write_text(
        text,
        encoding="utf-8",
    )
