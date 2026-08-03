from jga.visualization.scientific_plot_layout import (
    ScientificPlotLayout,
)


def test_scientific_plot_layout_is_valid():

    layout = ScientificPlotLayout(
        title="Metric Timeline",
        x_axis="time",
        y_axis="metric_position",
    )

    assert layout.is_valid()
