from pathlib import Path

from project_metadata import (
    load_project_metadata,
)


ROOT = Path(__file__).resolve().parents[2]


def export_session_context() -> None:

    metadata = load_project_metadata()

    text = f"""# Jazz Groove Analyzer (JGA)

Version

{metadata["Version"]}

Current Milestone

{metadata["Current Milestone"]}

Current Phase

{metadata["Current Phase"]}

Repository Status

{metadata["Status"]}

Main Branch

{metadata["Main Branch"]}

Python

{metadata["Python"]}

Tests

{metadata["Tests"]}

Last Update

{metadata["Last Update"]}

============================================================

Repository is the source of truth.

Read the Bootstrap package before continuing development.

Theory precedes implementation.
"""

    (
        ROOT
        / "artifacts"
        / "JGA_SESSION_CONTEXT.md"
    ).write_text(
        text,
        encoding="utf-8",
    )
