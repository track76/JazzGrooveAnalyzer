import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def export_context():

    shutil.make_archive(
        "JGA_CONTEXT",
        "zip",
        ROOT / "docs",
    )
