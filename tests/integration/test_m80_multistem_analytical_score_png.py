import pytest

from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)

from jga.runtime.engines.analytical_groove_score_png_exporter_runner import (
    AnalyticalGrooveScorePngExporterRunner,
)


def test_m80_multistem_analytical_score_png_export():

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    destination = (
        "output/jga_analytical_groove_score_multistem.png"
    )

    with pytest.raises(ValueError, match="No measures available"):
        AnalyticalGrooveScorePngExporterRunner().export(
            context,
            destination,
        )
