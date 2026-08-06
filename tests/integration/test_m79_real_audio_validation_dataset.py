from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m79_real_audio_validation_dataset():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    dataset = context.validation_dataset

    assert dataset is not None
    assert not dataset.is_empty

    print()
    print("==============================")
    print("M79 VALIDATION DATASET")
    print("==============================")
    print("Observations:", len(dataset))
    print()
