from jga.representation.projection import ScientificProjectionEngine


def test_engine_is_instantiable():
    engine = ScientificProjectionEngine()
    assert engine is not None


def test_engine_exposes_project_method():
    engine = ScientificProjectionEngine()
    assert callable(engine.project)
