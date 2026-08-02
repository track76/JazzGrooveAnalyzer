import pytest

from jga.translation.semantic_bridge import SemanticBridge


def test_semantic_bridge_is_abstract():
    with pytest.raises(TypeError):
        SemanticBridge()
