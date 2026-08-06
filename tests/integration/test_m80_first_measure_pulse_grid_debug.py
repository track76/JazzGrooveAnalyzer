from jga.pipeline.default_analysis_pipeline import AnalysisPipeline


def test_m80_first_measure_pulse_grid_debug():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    measure = context.reconstructed_measures[0]

    print()
    print("==============================")
    print("FIRST MEASURE PULSE GRID")
    print("==============================")

    for beat in measure.beat_references[:16]:
        print(
            beat.index,
            beat.timestamp,
            beat.timestamp - measure.start_time_seconds,
        )
