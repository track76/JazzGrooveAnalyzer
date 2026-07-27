from pathlib import Path
import shutil


def export_scientific_state():

    artifacts = Path("artifacts")
    artifacts.mkdir(exist_ok=True)

    source = Path("docs/JGA_SCIENTIFIC_STATE.md")

    if source.exists():

        shutil.copy(
            source,
            artifacts / "JGA_SCIENTIFIC_STATE.md",
        )
