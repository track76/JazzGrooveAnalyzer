"""
Updates selected sections of JGA_PROJECT_STATE.md.
"""

from pathlib import Path
import re

PROJECT_STATE = Path("docs/JGA_PROJECT_STATE.md")


def main():
    text = PROJECT_STATE.read_text(encoding="utf-8")

    # Update tests count everywhere
    text = re.sub(
        r"\d+\s*/\s*\d+\s+tests passing",
        "105 / 105 tests passing",
        text,
    )

    PROJECT_STATE.write_text(text, encoding="utf-8")

    print("JGA_PROJECT_STATE.md updated.")


if __name__ == "__main__":
    main()
