from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]


def export_context():

    output = ROOT / "artifacts" / "JGA_CONTEXT"

    shutil.make_archive(
        str(output),
        "zip",
        ROOT / "docs",
    )
