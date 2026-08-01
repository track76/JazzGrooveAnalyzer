from pathlib import Path

from project_metadata import (
    load_project_metadata,
)


ROOT = Path(__file__).resolve().parents[2]


def export_scientific_state() -> None:

    metadata = load_project_metadata()

    text = f"""# JGA SCIENTIFIC STATE

Automatically generated.

============================================================

Scientific Layers

Metric Reconstruction
    COMPLETE

Behaviour Analytics
    COMPLETE

Representation
    COMPLETE

Scientific Geometry
    COMPLETE

Scientific Behaviour Space
    COMPLETE

Behaviour Observation
    COMPLETE

Behaviour Diagnostics
    IN PROGRESS

Scientific Report
    NOT STARTED

Real Source Separation
    NOT STARTED

============================================================

Current Milestone

{metadata["Current Milestone"]}

{metadata["Current Phase"]}

============================================================

Reference Validation

{metadata["Tests"]} tests passed

============================================================

Status

{metadata["Status"]}

============================================================

Last Update

{metadata["Last Update"]}
"""

    (
        ROOT
        / "artifacts"
        / "JGA_SCIENTIFIC_STATE.md"
    ).write_text(
        text,
        encoding="utf-8",
    )
