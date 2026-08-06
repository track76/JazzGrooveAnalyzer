import pytest

from jga.validation.exporters.validation_exporter import ValidationExporter


def test_validation_exporter_is_abstract():
    with pytest.raises(TypeError):
        ValidationExporter()
