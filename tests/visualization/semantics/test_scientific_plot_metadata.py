from jga.visualization.scientific_plot_metadata import (
    ScientificPlotMetadata,
)


def test_scientific_plot_metadata_exists():

    metadata = ScientificPlotMetadata(
        purpose="metric_analysis",
        domain="jazz_rhythm",
    )

    assert metadata.purpose == "metric_analysis"

    assert metadata.domain == "jazz_rhythm"
