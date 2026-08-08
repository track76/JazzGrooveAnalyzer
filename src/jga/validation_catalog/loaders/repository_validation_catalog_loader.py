"""Repository loader for JGA-VALIDATION-CATALOG-v1."""

from hashlib import sha256
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
    """Verifies and loads the approved immutable validation catalogue."""

    CATALOGUE_ID = "JGA-VALIDATION-CATALOG-v1"
    CATALOGUE_SCHEMA_VERSION = "1"
    CATALOGUE_VERSION = "1"

    VALIDATION_ITEM_ID = "VAL-001"
    VALIDATION_ITEM_SCHEMA_VERSION = "1"
    VALIDATION_ITEM_VERSION = "1"
    GROUND_TRUTH_ID = "GT-VAL-001-v1"

    MUSICXML_PATH = (
        "recordings/validation/ground_truth/"
        "03 THE COST OF LIVING versione intro + 8 bar.musicxml"
    )
    MUSICXML_SHA256 = (
        "809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778"
    )
    MUSICXML_REPOSITORY_REVISION = (
        "c50abd435097b8f335a53b4146d9fa933764b15f"
    )

    MP3_PATH = (
        "recordings/validation/"
        "03 THE COST OF LIVING versione intro + 8 bar.mp3"
    )
    MP3_SHA256 = (
        "d358d1bca5144ea1dabee4d970fa5deabf81a209922481a77db0f01bd8bdbbbb"
    )
    MP3_REPOSITORY_REVISION = (
        "1b4ebfdcef25dc3e897b691d5149f52dce0d29fd"
    )

    LICENSING_STATUS = "not_specified"

    def load(self, repository_root: Path) -> ValidationCatalog:
        musicxml = self._verified_asset(
            repository_root=repository_root,
            repository_path=self.MUSICXML_PATH,
            expected_sha256=self.MUSICXML_SHA256,
            repository_revision=self.MUSICXML_REPOSITORY_REVISION,
        )
        mp3 = self._verified_asset(
            repository_root=repository_root,
            repository_path=self.MP3_PATH,
            expected_sha256=self.MP3_SHA256,
            repository_revision=self.MP3_REPOSITORY_REVISION,
        )

        item = ValidationItem(
            validation_item_id=self.VALIDATION_ITEM_ID,
            ground_truth_id=self.GROUND_TRUTH_ID,
            authoritative_musicxml=musicxml,
            mp3_recording=mp3,
            provenance=ValidationItemProvenance(
                schema_version=self.VALIDATION_ITEM_SCHEMA_VERSION,
                item_version=self.VALIDATION_ITEM_VERSION,
            ),
            metadata=ValidationItemMetadata(
                title="THE COST OF LIVING",
            ),
        )

        return ValidationCatalog(
            catalogue_id=self.CATALOGUE_ID,
            provenance=ValidationCatalogProvenance(
                schema_version=self.CATALOGUE_SCHEMA_VERSION,
                catalogue_version=self.CATALOGUE_VERSION,
            ),
            items=(item,),
        )

    def _verified_asset(
        self,
        repository_root: Path,
        repository_path: str,
        expected_sha256: str,
        repository_revision: str,
    ) -> ValidationAsset:
        asset_path = repository_root / repository_path
        checksum = sha256(asset_path.read_bytes()).hexdigest()
        if checksum != expected_sha256:
            raise ValueError(
                f"Validation asset checksum mismatch: {repository_path}"
            )

        return ValidationAsset(
            repository_path=repository_path,
            sha256=checksum,
            repository_revision=repository_revision,
            licensing_status=self.LICENSING_STATUS,
        )
