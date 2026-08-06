from pathlib import Path

from jga.runtime.engines.analytical_groove_score_png_exporter_runner import (
    AnalyticalGrooveScorePngExporterRunner,
)


def test_png_exporter_runner_exists():

    runner = (
        AnalyticalGrooveScorePngExporterRunner()
    )

    assert runner is not None
