from __future__ import annotations

from pathlib import Path


_METADATA_FILE = Path("docs/project/PROJECT_METADATA.md")


def load_project_metadata() -> dict[str, str]:
    """
    Loads the canonical JGA project metadata.

    The metadata file is the single source of truth for the
    current project status used by tooling.
    """

    metadata: dict[str, str] = {}

    for line in _METADATA_FILE.read_text(
        encoding="utf-8"
    ).splitlines():

        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        metadata[key.strip()] = value.strip()

    return metadata
