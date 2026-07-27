from jga.reporting.compiler.analytical_score_compiler import (
    AnalyticalScoreCompiler,
)


def test_compile():

    compiler = AnalyticalScoreCompiler()

    score = compiler.compile(

        title="Test",

        artist="Unknown",

    )

    assert score.title == "Test"

    assert score.artist == "Unknown"

    assert score.bars == ()

