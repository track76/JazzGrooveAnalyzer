"""
=========================================================
Jazz Groove Analyzer (JGA)

Tool:
    update_project_state.py

Description:
    Updates selected sections of JGA_PROJECT_STATE.md.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from pathlib import Path

PROJECT_STATE = Path("docs/JGA_PROJECT_STATE.md")


def replace(text: str, old: str, new: str) -> str:
    if old not in text:
        print(f"[WARNING] Pattern not found:\n{old}\n")
        return text
    return text.replace(old, new)


def main():

    text = PROJECT_STATE.read_text(encoding="utf-8")

    # -------- Version --------
    text = replace(
        text,
        "v0.2.0-alpha",
        "v0.2.0-alpha",
    )

    # -------- Milestone --------
    text = replace(
        text,
        "M3.1 — Core Integration",
        "M3.3 — Core Architecture Review",
    )

    # -------- Tests --------
    text = replace(
        text,
        "99 / 99 tests passing",
        "102 / 102 tests passing",
    )

    PROJECT_STATE.write_text(
        text,
        encoding="utf-8",
    )

    print("JGA_PROJECT_STATE.md updated.")


if __name__ == "__main__":
    main()
