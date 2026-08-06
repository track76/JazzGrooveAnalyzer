"""
=========================================================
Jazz Groove Analyzer (JGA)

Validation Dataset Runner

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from jga.runtime.analysis_context import AnalysisContext

from jga.validation.builders.metric_context_validation_builder import (
    MetricContextValidationBuilder,
)
from jga.validation.factories.validation_dataset_factory import (
    ValidationDatasetFactory,
)
from jga.validation.models.validation_metadata import (
    ValidationMetadata,
)
from jga.validation.models.validation_source import (
    ValidationSource,
)


class ValidationDatasetRunner:
    """
    Orchestrates scientific validation dataset creation.

    The Runner contains no extraction logic.

    Observable evidence extraction is delegated to
    MetricContextValidationBuilder.
    """

    def __init__(self) -> None:

        self._builder = (
            MetricContextValidationBuilder()
        )

        self._factory = (
            ValidationDatasetFactory()
        )

    def run(
        self,
        context: AnalysisContext,
    ) -> None:

        if context.metric_context is None:
            return

        source = ValidationSource(
            recording_id=context.audio.filename,
            recording_name=context.audio.filename,
            performer="UNKNOWN",
        )

        metadata = ValidationMetadata(
            analysis_version="M79",
            sample_rate=context.audio.sample_rate,
            duration_seconds=context.audio.duration,
        )

        records = self._builder.build(
            context.metric_context,
        )

        context.validation_dataset = (
            self._factory.create(
                observations=records,
                source=source,
                metadata=metadata,
            )
        )
