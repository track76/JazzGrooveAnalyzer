from jga.representation.metric_landscape import (
    MetricLandscape,
)


def test_metric_landscape_reports_number_of_portraits():

    landscape = MetricLandscape(
        metric_cluster_portraits=(
            "a",
            "b",
            "c",
        ),
    )

    assert landscape.portrait_count == 3
