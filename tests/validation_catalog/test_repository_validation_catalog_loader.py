from dataclasses import FrozenInstanceError
import json
from pathlib import Path

import pytest

from jga.validation_catalog.loaders import RepositoryValidationCatalogLoader


REPOSITORY_ROOT = Path(".")


def test_loads_approved_catalogue_and_item_identities():
    catalogue = RepositoryValidationCatalogLoader().load(REPOSITORY_ROOT)

    assert catalogue.catalogue_id == "JGA-VALIDATION-CATALOG-v1"
    assert len(catalogue) == 1
    assert catalogue.item("VAL-001").validation_item_id == "VAL-001"
    assert catalogue.item("VAL-001").ground_truth_id == "GT-VAL-001-v1"


def test_preserves_catalogue_item_provenance_and_metadata():
    catalogue = RepositoryValidationCatalogLoader().load(REPOSITORY_ROOT)
    item = catalogue.item("VAL-001")

    assert catalogue.provenance.schema_version == "1"
    assert catalogue.provenance.catalogue_version == "1"
    assert item.provenance.schema_version == "1"
    assert item.provenance.item_version == "1"
    assert item.metadata.title == "THE COST OF LIVING"


def test_binds_approved_musicxml_asset_without_ground_truth_content():
    item = RepositoryValidationCatalogLoader().load(REPOSITORY_ROOT).item(
        "VAL-001"
    )
    asset = item.authoritative_musicxml

    assert asset.repository_path == (
        "recordings/validation/ground_truth/"
        "03 THE COST OF LIVING versione intro + 8 bar.musicxml"
    )
    assert asset.sha256 == (
        "809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778"
    )
    assert asset.repository_revision == (
        "c50abd435097b8f335a53b4146d9fa933764b15f"
    )
    assert asset.licensing_status == "not_specified"
    assert not hasattr(item, "ground_truth")


def test_binds_approved_mp3_asset_and_unspecified_licensing():
    item = RepositoryValidationCatalogLoader().load(REPOSITORY_ROOT).item(
        "VAL-001"
    )
    asset = item.mp3_recording

    assert asset.repository_path == (
        "recordings/validation/"
        "03 THE COST OF LIVING versione intro + 8 bar.mp3"
    )
    assert asset.sha256 == (
        "d358d1bca5144ea1dabee4d970fa5deabf81a209922481a77db0f01bd8bdbbbb"
    )
    assert asset.repository_revision == (
        "1b4ebfdcef25dc3e897b691d5149f52dce0d29fd"
    )
    assert asset.licensing_status == "not_specified"


def test_catalogue_is_deeply_immutable():
    catalogue = RepositoryValidationCatalogLoader().load(REPOSITORY_ROOT)
    item = catalogue.item("VAL-001")

    with pytest.raises(FrozenInstanceError):
        catalogue.catalogue_id = "changed"

    with pytest.raises(FrozenInstanceError):
        item.ground_truth_id = "changed"

    with pytest.raises(FrozenInstanceError):
        item.mp3_recording.licensing_status = "changed"


def test_catalogue_loading_is_deterministic():
    loader = RepositoryValidationCatalogLoader()

    assert loader.load(REPOSITORY_ROOT) == loader.load(REPOSITORY_ROOT)


def test_unknown_validation_item_is_rejected():
    catalogue = RepositoryValidationCatalogLoader().load(REPOSITORY_ROOT)

    with pytest.raises(KeyError):
        catalogue.item("VAL-999")


def test_asset_checksum_mismatch_is_rejected(tmp_path):
    loader = RepositoryValidationCatalogLoader()
    definition = json.loads(loader.DEFAULT_CATALOGUE_PATH.read_text())
    catalogue = tmp_path / loader.DEFAULT_CATALOGUE_PATH
    catalogue.parent.mkdir(parents=True)
    catalogue.write_text(json.dumps(definition))

    musicxml_path = definition["items"][0]["authoritative_musicxml"][
        "repository_path"
    ]
    musicxml = tmp_path / musicxml_path
    musicxml.parent.mkdir(parents=True)
    musicxml.write_bytes(b"not the approved MusicXML")

    with pytest.raises(ValueError, match="checksum mismatch"):
        loader.load(tmp_path)


def test_catalogue_items_are_loaded_from_repository_data(tmp_path):
    loader = RepositoryValidationCatalogLoader()
    definition = json.loads(loader.DEFAULT_CATALOGUE_PATH.read_text())
    original = definition["items"][0]
    additional = json.loads(json.dumps(original))
    additional["validation_item_id"] = "TEST-ITEM"
    additional["ground_truth_id"] = "TEST-GROUND-TRUTH"
    additional["metadata"]["title"] = "TEST ITEM"
    definition["items"].append(additional)

    catalogue_path = tmp_path / loader.DEFAULT_CATALOGUE_PATH
    catalogue_path.parent.mkdir(parents=True)
    catalogue_path.write_text(json.dumps(definition))
    for asset_name in ("authoritative_musicxml", "mp3_recording"):
        source = Path(original[asset_name]["repository_path"])
        destination = tmp_path / source
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())

    catalogue = loader.load(tmp_path)

    assert len(catalogue) == 2
    assert catalogue.item("TEST-ITEM").ground_truth_id == "TEST-GROUND-TRUTH"
    assert catalogue.item("TEST-ITEM").metadata.title == "TEST ITEM"
