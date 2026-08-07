import json
from pathlib import Path

from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)


def test_jga_val_001_report():

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/validation/03 THE COST OF LIVING versione intro + 8 bar.mp3"
    )

    report = {
        "dataset": "JGA-VAL-001",

        "experiment": {
            "mode": "blind",
            "separator": (
                "DummyMultiStemSeparator"
            ),
            "classifier": (
                "DummyInstrumentClassifier"
            ),
        },

        "audio": {
            "filename": context.audio.filename,
            "duration_seconds": context.audio.duration,
            "sample_rate": context.audio.sample_rate,
            "channels": context.audio.channels,
            "format": context.audio.format,
        },

        "ensemble_profile": (
            {
                "families": [
                    family.value
                    for family
                    in context.ensemble_profile.families
                ],
                "confidence": (
                    context.ensemble_profile.confidence
                ),
            }
            if context.ensemble_profile
            else None
        ),

        "observed_sources": [
            {
                "stem_id": source.stem_id,
                "classification": {
                    "family": (
                        source.classification.family.value
                    ),
                    "instrument": (
                        source.classification.instrument
                    ),
                    "confidence": (
                        source.classification.confidence
                    ),
                    "classifier": (
                        source.classification.classifier_name
                    ),
                    "version": (
                        source.classification.classifier_version
                    ),
                },
            }
            for source
            in context.observed_sources
        ]
        if context.observed_sources
        else [],

        "metric": {
            "beat_references": len(
                context.beat_references
            ),

            "metric_clusters": len(
                context.metric_clusters
            ),

            "measures": len(
                context.reconstructed_measures
            ),
        },

        "status": "baseline",
    }

    destination = Path(
        "artifacts/validation/JGA-VAL-001/baseline_report.json"
    )

    destination.write_text(
        json.dumps(
            report,
            indent=2,
            default=str,
        )
    )

    assert destination.exists()
