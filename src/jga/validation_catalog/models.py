"""Immutable models for the scientific validation catalogue."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationAsset:
    """Repository asset identity, integrity, provenance and licensing."""

    repository_path: str
    sha256: str
    repository_revision: str
    licensing_status: str


@dataclass(frozen=True, slots=True)
class ValidationItemProvenance:
    """Version provenance for one validation item."""

    schema_version: str
    item_version: str


@dataclass(frozen=True, slots=True)
class ValidationItemMetadata:
    """Minimum descriptive metadata for one validation item."""

    title: str


@dataclass(frozen=True, slots=True)
class ValidationItem:
    """Immutable binding of validation identities and catalogue assets."""

    validation_item_id: str
    ground_truth_id: str
    authoritative_musicxml: ValidationAsset
    mp3_recording: ValidationAsset
    provenance: ValidationItemProvenance
    metadata: ValidationItemMetadata


@dataclass(frozen=True, slots=True)
class ValidationCatalogProvenance:
    """Schema and catalogue version provenance."""

    schema_version: str
    catalogue_version: str


@dataclass(frozen=True, slots=True)
class ValidationCatalog:
    """Scientific catalogue of immutable Validation Items."""

    catalogue_id: str
    provenance: ValidationCatalogProvenance
    items: tuple[ValidationItem, ...]

    def __len__(self) -> int:
        return len(self.items)

    def item(self, validation_item_id: str) -> ValidationItem:
        """Return the uniquely identified validation item."""
        matches = tuple(
            item
            for item in self.items
            if item.validation_item_id == validation_item_id
        )
        if len(matches) != 1:
            raise KeyError(validation_item_id)
        return matches[0]
