from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def print_report():

    artifacts = ROOT / "artifacts"

    print()
    print("=" * 60)
    print("Current recovery entry:", ROOT / "JGA_BOOTSTRAP.md")
    print("Additional export artifacts (not bootstrap authorities)")
    print()

    if artifacts.exists():

        for path in sorted(artifacts.iterdir()):

            if path.is_file() and path.name != "JGA_BOOTSTRAP.md":

                print(path)

    print()
    print("READY FOR NEW CHAT")
    print("=" * 60)

