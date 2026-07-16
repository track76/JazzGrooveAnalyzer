from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]


def git(cmd):

    return subprocess.check_output(
        cmd,
        text=True,
    ).strip()


def generate_bootstrap():

    branch = git(
        ["git", "branch", "--show-current"]
    )

    commit = git(
        ["git", "rev-parse", "--short", "HEAD"]
    )

    text = f"""# Jazz Groove Analyzer

Branch: {branch}

Commit: {commit}

Repository is the source of truth.

Run

python tools/bootstrap.py

before every ChatGPT session.
"""

    (
        ROOT
        / "artifacts"
        / "JGA_BOOTSTRAP.md"
    ).write_text(
        text,
        encoding="utf-8",
    )
