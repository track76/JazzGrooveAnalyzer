from jga.visualization.scientific_plot_metadata import (
    ScientificPlotMetadata,
)


def test_scientific_plot_metadata_is_valid():

    metadata = ScientificPlotMetadata(
        purpose="metric_analysis",
        domain="jazz_rhythm",
    )

    assert metadata.is_valid()
