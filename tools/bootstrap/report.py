from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def print_report():

    print()

    print("=" * 60)

    print("Artifacts generated")

    print()

    print(ROOT / "artifacts" / "JGA_BOOTSTRAP.md")

    print(ROOT / "artifacts" / "JGA_CONTEXT.zip")

    print(ROOT / "artifacts" / "JGA_REPOSITORY.zip")
    print(ROOT / "artifacts" / "JGA_ARCHITECTURE_MAP.md")

    print()

    print("READY FOR NEW CHAT")

    print("=" * 60)
