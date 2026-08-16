from datetime import datetime
from decimal import Decimal
from uuid import uuid4

import numpy as np

from jga.core.audio_file import AudioFile
from jga.domain.beat_reference import BeatReference
from jga.domain.declared_metric_reference import (
    DeclaredMetricReference,
    MetricReferenceProvenance,
)
from jga.runtime.analysis_context import AnalysisContext
from jga.runtime.engines.reconstructed_measure_runner import (
    ReconstructedMeasureRunner,
)


def declared_reference() -> DeclaredMetricReference:
    return DeclaredMetricReference(
        beats_per_minute=Decimal("78"),
        beat_unit="quarter",
        provenance=MetricReferenceProvenance(
            source_id="GT-VAL-001-v1",
            source_kind="authoritative controlled-source context",
            source_sha256=(
                "809a6ef276c4c3b9042c71d40a71763d"
                "cbf90d47e654e784af371eb53d073778"
            ),
            temporal_scope="complete controlled performance",
        ),
    )


def context_with_beats() -> AnalysisContext:
    context = AnalysisContext(
        audio=AudioFile(
            path="controlled.wav",
            raw_audio=np.zeros(1),
            sample_rate=44100,
            duration=0.0,
            channels=1,
            format="wav",
        )
    )
    context.beat_references = tuple(
        BeatReference(
            id=uuid4(),
            index=index,
            timestamp=index * (60.0 / 78.0),
            created_at=datetime.now(),
        )
        for index in range(16)
    )
    return context


def test_absent_metric_reference_does_not_silently_build_at_120_bpm():
    context = context_with_beats()

    ReconstructedMeasureRunner().run(context)

    assert context.reconstructed_measures == ()


def test_declared_metric_reference_is_preserved_by_reconstructed_measure():
    context = context_with_beats()
    context.declared_metric_reference = declared_reference()

    ReconstructedMeasureRunner().run(context)

    assert len(context.reconstructed_measures) == 1
    measure = context.reconstructed_measures[0]
    assert measure.internal_bpm == 78.0
    assert measure.declared_metric_reference is context.declared_metric_reference
