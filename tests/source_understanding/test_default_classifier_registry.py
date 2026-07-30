from jga.source_understanding.classifiers.default_classifier_registry import (
    DefaultClassifierRegistry,
)


def test_default_registry_contains_classifiers():

    registry = DefaultClassifierRegistry()

    assert len(registry._classifiers) >= 1
