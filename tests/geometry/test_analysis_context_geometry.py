from jga.runtime.analysis_context import AnalysisContext
from jga.geometry.scientific_geometric_plane import (
    ScientificGeometricPlane,
)


def test_analysis_context_accepts_scientific_geometric_plane():
    context = AnalysisContext(audio=None)

    plane = ScientificGeometricPlane(())

    context.scientific_geometric_plane = plane

    assert context.scientific_geometric_plane is plane
