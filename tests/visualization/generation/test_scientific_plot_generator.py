from jga.visualization.scientific_plot_generator import (
    ScientificPlotGenerator,
)


def test_scientific_plot_generator_exists():

    generator = ScientificPlotGenerator()

    assert generator is not None
