"""
=========================================================
Jazz Groove Analyzer (JGA)

Analytical Score Renderer

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from jga.reporting.compiler.analytical_score_compiler import (
    AnalyticalScoreCompiler,
)

from jga.reporting.renderers.ascii_renderer import (
    AnalyticalScoreAsciiRenderer,
)


def main():

    compiler = AnalyticalScoreCompiler()

    score = compiler.compile(

        title="Demo",

        artist="Unknown",

    )

    renderer = AnalyticalScoreAsciiRenderer()

    print(renderer.render(score))


if __name__ == "__main__":
    main()

