"""Operational infrastructure with no scientific responsibility."""

from .external_storage import (
    EXTERNAL_ROOT_ENVIRONMENT_VARIABLE,
    STANDARD_EXTERNAL_DIRECTORIES,
    ExternalStorage,
    ExternalStorageUnavailable,
)

__all__ = [
    "EXTERNAL_ROOT_ENVIRONMENT_VARIABLE",
    "STANDARD_EXTERNAL_DIRECTORIES",
    "ExternalStorage",
    "ExternalStorageUnavailable",
]
