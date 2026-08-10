"""Configurable storage locations for heavy operational artifacts."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Mapping


EXTERNAL_ROOT_ENVIRONMENT_VARIABLE = "JGA_EXTERNAL_ROOT"

STANDARD_EXTERNAL_DIRECTORIES = (
    "datasets",
    "recordings",
    "stems",
    "validation",
    "experiments",
    "renders",
    "reports",
    "temporary",
    "cache",
)


class ExternalStorageUnavailable(RuntimeError):
    """Raised before a heavy default write when external storage is unusable."""


@dataclass(frozen=True, slots=True)
class ExternalStorage:
    """Resolve standard heavy-artifact directories from one configured root."""

    root: Path

    @classmethod
    def from_environment(
        cls,
        environment: Mapping[str, str] | None = None,
    ) -> "ExternalStorage":
        values = os.environ if environment is None else environment
        configured = values.get(EXTERNAL_ROOT_ENVIRONMENT_VARIABLE, "").strip()
        if not configured:
            raise ExternalStorageUnavailable(
                "JGA_EXTERNAL_ROOT is not configured; heavy default writes "
                "are disabled. Set it to an existing writable external "
                "storage directory."
            )

        root = Path(configured).expanduser()
        if not root.is_absolute():
            raise ExternalStorageUnavailable(
                "JGA_EXTERNAL_ROOT must be an absolute path so storage "
                "identity does not depend on the current working directory."
            )
        if not root.exists():
            raise ExternalStorageUnavailable(
                f"JGA_EXTERNAL_ROOT does not exist: {root}. Heavy default "
                "writes were not started."
            )
        if not root.is_dir():
            raise ExternalStorageUnavailable(
                f"JGA_EXTERNAL_ROOT is not a directory: {root}. Heavy "
                "default writes were not started."
            )
        if not os.access(root, os.W_OK):
            raise ExternalStorageUnavailable(
                f"JGA_EXTERNAL_ROOT is not writable: {root}. Heavy default "
                "writes were not started."
            )
        return cls(root=root.resolve())

    def ensure_layout(self) -> tuple[Path, ...]:
        """Create and return the standard project-external directory layout."""

        directories = tuple(
            self.root / name for name in STANDARD_EXTERNAL_DIRECTORIES
        )
        for directory in directories:
            directory.mkdir(parents=False, exist_ok=True)
        return directories

    def directory(self, category: str, *parts: str) -> Path:
        """Return a path below one standard category, creating its parents."""

        if category not in STANDARD_EXTERNAL_DIRECTORIES:
            raise ValueError(f"Unknown external storage category: {category}")
        for part in parts:
            candidate = Path(part)
            if candidate.is_absolute() or ".." in candidate.parts:
                raise ValueError(
                    "External storage destinations must remain below their "
                    "declared category."
                )
        self.ensure_layout()
        destination = self.root / category
        if parts:
            destination = destination.joinpath(*parts)
            destination.mkdir(parents=True, exist_ok=True)
        return destination
