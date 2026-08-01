
from pathlib import Path

from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m27_real_audio_evidence_summary():

    audio = Path(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    assert audio.exists()

    result = AnalysisPipeline().analyze(
        str(audio)
    )

    print()
    print("==============================")
    print("M27 REAL AUDIO EVIDENCE")
    print("==============================")

    diagnostic = (
        result.behaviour_diagnostic_result
    )

    assert diagnostic is not None

    evidence = (
        diagnostic.scientific_evidence
    )

    print(
        "Scientific evidence count:",
        len(evidence.evidences)
    )

    for item in evidence.evidences:
        print(
            item.name,
            "=",
            item.value,
        )

    report = result.scientific_report

    print(
        "Scientific report:",
        report is not None,
    )

