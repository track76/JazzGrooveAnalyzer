from jga.visualization.scientific_plot_layout import (
    ScientificPlotLayout,
)


def test_scientific_plot_layout_exists():

    layout = ScientificPlotLayout(
        title="Metric Timeline",
        x_axis="time",
        y_axis="metric_position",
    )

    assert layout.title == "Metric Timeline"

    assert layout.x_axis == "time"

    assert layout.y_axis == "metric_position"
