from pathlib import Path

from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.runtime.engines.analytical_groove_score_png_exporter_runner import (
    AnalyticalGrooveScorePngExporterRunner,
)


def test_m80_real_audio_analytical_score_png_export():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    destination = (
        "output/jga_analytical_groove_score_real_audio.png"
    )

    AnalyticalGrooveScorePngExporterRunner().export(
        context,
        destination,
    )

    assert Path(
        destination
    ).exists()
