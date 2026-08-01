"""
Updates selected sections of JGA_PROJECT_STATE.md.
"""

from pathlib import Path
import re

from project_metadata import (
    load_project_metadata,
)

PROJECT_STATE = Path("docs/JGA_PROJECT_STATE.md")


def main() -> None:

    metadata = load_project_metadata()

    text = PROJECT_STATE.read_text(
        encoding="utf-8",
    )

    tests = metadata["Tests"]

    text = re.sub(
        r"\d+\s*/\s*\d+\s+tests passing",
        f"{tests} / {tests} tests passing",
        text,
    )

    PROJECT_STATE.write_text(
        text,
        encoding="utf-8",
    )

    print("JGA_PROJECT_STATE.md updated.")


if __name__ == "__main__":
    main()
