from pathlib import Path

import pytest

from jga.operational.external_storage import (
    EXTERNAL_ROOT_ENVIRONMENT_VARIABLE,
    STANDARD_EXTERNAL_DIRECTORIES,
    ExternalStorage,
    ExternalStorageUnavailable,
)


def test_requires_configured_external_root() -> None:
    with pytest.raises(
        ExternalStorageUnavailable,
        match="heavy default writes are disabled",
    ):
        ExternalStorage.from_environment({})


def test_rejects_relative_root() -> None:
    with pytest.raises(
        ExternalStorageUnavailable,
        match="must be an absolute path",
    ):
        ExternalStorage.from_environment(
            {EXTERNAL_ROOT_ENVIRONMENT_VARIABLE: "relative/storage"}
        )


def test_rejects_missing_root(tmp_path: Path) -> None:
    missing = tmp_path / "not-mounted"
    with pytest.raises(
        ExternalStorageUnavailable,
        match="does not exist",
    ):
        ExternalStorage.from_environment(
            {EXTERNAL_ROOT_ENVIRONMENT_VARIABLE: str(missing)}
        )
    assert not missing.exists()


def test_rejects_non_directory_root(tmp_path: Path) -> None:
    file_path = tmp_path / "external-file"
    file_path.write_text("not a directory", encoding="utf-8")
    with pytest.raises(
        ExternalStorageUnavailable,
        match="is not a directory",
    ):
        ExternalStorage.from_environment(
            {EXTERNAL_ROOT_ENVIRONMENT_VARIABLE: str(file_path)}
        )


def test_creates_complete_standard_layout(tmp_path: Path) -> None:
    storage = ExternalStorage.from_environment(
        {EXTERNAL_ROOT_ENVIRONMENT_VARIABLE: str(tmp_path)}
    )

    directories = storage.ensure_layout()

    assert directories == tuple(
        tmp_path / name for name in STANDARD_EXTERNAL_DIRECTORIES
    )
    assert all(directory.is_dir() for directory in directories)


def test_resolves_nested_category_directory(tmp_path: Path) -> None:
    storage = ExternalStorage.from_environment(
        {EXTERNAL_ROOT_ENVIRONMENT_VARIABLE: str(tmp_path)}
    )

    result = storage.directory("experiments", "H-TEST", "run_001")

    assert result == tmp_path / "experiments" / "H-TEST" / "run_001"
    assert result.is_dir()


def test_rejects_unknown_category(tmp_path: Path) -> None:
    storage = ExternalStorage.from_environment(
        {EXTERNAL_ROOT_ENVIRONMENT_VARIABLE: str(tmp_path)}
    )
    with pytest.raises(ValueError, match="Unknown external storage category"):
        storage.directory("unknown")


@pytest.mark.parametrize("part", ("../escape", "/absolute"))
def test_destination_cannot_escape_category(tmp_path: Path, part: str) -> None:
    storage = ExternalStorage.from_environment(
        {EXTERNAL_ROOT_ENVIRONMENT_VARIABLE: str(tmp_path)}
    )

    with pytest.raises(ValueError, match="remain below"):
        storage.directory("reports", part)
