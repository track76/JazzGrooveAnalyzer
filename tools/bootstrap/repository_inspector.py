"""
Repository inspection utilities.

Copyright © 2026 Angelo Tracanna
"""

from __future__ import annotations

from dataclasses import dataclass
import subprocess


@dataclass(frozen=True)
class RepositorySnapshot:
    """Immutable snapshot of the current repository state."""

    branch: str
    commit: str
    commit_short: str
    working_tree_clean: bool
    status: str


class RepositoryInspector:
    """Collects information about the current Git repository."""

    def inspect(self) -> RepositorySnapshot:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            text=True,
        ).strip()

        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
        ).strip()

        commit_short = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            text=True,
        ).strip()

        status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            text=True,
        )

        return RepositorySnapshot(
            branch=branch,
            commit=commit,
            commit_short=commit_short,
            working_tree_clean=not bool(status.strip()),
            status=status,
        )
