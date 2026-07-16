from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]


def export_repository():

    output = ROOT / "artifacts" / "JGA_REPOSITORY.zip"

    subprocess.run(
        [
            "git",
            "archive",
            "--format=zip",
            f"--output={output}",
            "HEAD",
        ],
        check=True,
    )
