"""Repository loader for a data-defined scientific validation catalogue."""

from hashlib import sha256
import json
from pathlib import Path

from jga.validation_catalog.loaders.validation_catalog_loader import (
    ValidationCatalogLoader,
)
from jga.validation_catalog.models import (
    ValidationAsset,
    ValidationCatalog,
    ValidationCatalogProvenance,
    ValidationItem,
    ValidationItemMetadata,
    ValidationItemProvenance,
)


class RepositoryValidationCatalogLoader(ValidationCatalogLoader):
    """Verify and load the repository's immutable validation catalogue."""

    DEFAULT_CATALOGUE_PATH = Path("recordings/validation/catalog.json")

    def __init__(self, catalogue_path: Path | None = None) -> None:
        self.catalogue_path = catalogue_path or self.DEFAULT_CATALOGUE_PATH

    def load(self, repository_root: Path) -> ValidationCatalog:
        definition = json.loads(
            (repository_root / self.catalogue_path).read_text(encoding="utf-8")
        )
        items = tuple(
            self._load_item(repository_root, item)
            for item in definition["items"]
        )
        item_ids = tuple(item.validation_item_id for item in items)
        if len(set(item_ids)) != len(item_ids):
            raise ValueError("Validation Item identities must be unique.")

        provenance = definition["provenance"]
        return ValidationCatalog(
            catalogue_id=definition["catalogue_id"],
            provenance=ValidationCatalogProvenance(
                schema_version=provenance["schema_version"],
                catalogue_version=provenance["catalogue_version"],
            ),
            items=items,
        )

    def _load_item(
        self,
        repository_root: Path,
        definition: dict[str, object],
    ) -> ValidationItem:
        provenance = definition["provenance"]
        metadata = definition["metadata"]
        return ValidationItem(
            validation_item_id=definition["validation_item_id"],
            ground_truth_id=definition["ground_truth_id"],
            authoritative_musicxml=self._verified_asset(
                repository_root,
                definition["authoritative_musicxml"],
            ),
            mp3_recording=self._verified_asset(
                repository_root,
                definition["mp3_recording"],
            ),
            provenance=ValidationItemProvenance(
                schema_version=provenance["schema_version"],
                item_version=provenance["item_version"],
            ),
            metadata=ValidationItemMetadata(title=metadata["title"]),
        )

    @staticmethod
    def _verified_asset(
        repository_root: Path,
        definition: dict[str, str],
    ) -> ValidationAsset:
        repository_path = definition["repository_path"]
        expected_sha256 = definition["sha256"]
        checksum = sha256((repository_root / repository_path).read_bytes()).hexdigest()
        if checksum != expected_sha256:
            raise ValueError(
                f"Validation asset checksum mismatch: {repository_path}"
            )

        return ValidationAsset(
            repository_path=repository_path,
            sha256=checksum,
            repository_revision=definition["repository_revision"],
            licensing_status=definition["licensing_status"],
        )
