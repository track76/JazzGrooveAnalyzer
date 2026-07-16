import subprocess
import sys


def check_git_status():

    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
    )

    if result.stdout.strip():

        print("\nRepository NOT READY\n")
        print(result.stdout)

        sys.exit(1)
