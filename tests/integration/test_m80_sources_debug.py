from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m80_sources_debug():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    print()
    print("==============================")
    print("SOURCE DEBUG")
    print("==============================")

    if context.ensemble_analysis_result:

        print(
            "Sound sources:",
            len(
                context.ensemble_analysis_result.sound_sources
            )
        )

        for source in (
            context.ensemble_analysis_result.sound_sources
        ):
            print(
                source.name
            )

        print(
            "Metric contributors:",
            len(
                context.ensemble_analysis_result.metric_contributors
            )
        )

        for contributor in (
            context.ensemble_analysis_result.metric_contributors
        ):
            print(
                contributor
            )
