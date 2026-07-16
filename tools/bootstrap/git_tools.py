import sys

from .repository_inspector import RepositoryInspector


def check_git_status() -> None:
    """Abort if the repository is not in a clean state."""

    snapshot = RepositoryInspector().inspect()

    if snapshot.working_tree_clean:
        return

    print("\nRepository NOT READY\n")

    if snapshot.status:
        print(snapshot.status)

    sys.exit(1)
