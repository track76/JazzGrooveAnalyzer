from pathlib import Path
import shutil


def export_runtime_state():

    artifacts = Path("artifacts")
    artifacts.mkdir(exist_ok=True)

    source = Path("docs/JGA_RUNTIME_STATE.md")

    if source.exists():

        shutil.copy(
            source,
            artifacts / "JGA_RUNTIME_STATE.md",
        )
