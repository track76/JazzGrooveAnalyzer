from .repository_inspector import RepositoryInspector


def check_git_status() -> None:
    """
    Warn if the repository is not in a clean state.

    Bootstrap generation continues even when the
    working tree contains uncommitted changes.
    """

    snapshot = RepositoryInspector().inspect()

    if snapshot.working_tree_clean:
        return

    print("\nRepository NOT READY\n")

    if snapshot.status:
        print(snapshot.status)

    print("\nWARNING: Continuing bootstrap generation...\n")
