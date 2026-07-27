from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def print_report():

    artifacts = ROOT / "artifacts"

    print()
    print("=" * 60)
    print("Artifacts generated")
    print()

    if artifacts.exists():

        for path in sorted(artifacts.iterdir()):

            if path.is_file():

                print(path)

    print()
    print("READY FOR NEW CHAT")
    print("=" * 60)

