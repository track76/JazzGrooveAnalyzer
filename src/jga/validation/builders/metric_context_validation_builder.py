"""
Metric Context Validation Builder.

Builds ValidationRecord objects from the observable
MetricContext representation.

No musical interpretation is introduced.
"""

from jga.core.metric_context import MetricContext
from jga.validation.models.validation_record import (
    ValidationRecord,
)


class MetricContextValidationBuilder:
    """
    Extracts observable ValidationRecord objects
    from a MetricContext.
    """

    def build(
        self,
        metric_context: MetricContext,
    ) -> tuple[ValidationRecord, ...]:

        if metric_context is None:
            raise ValueError(
                "MetricContext cannot be None."
            )

        records: list[ValidationRecord] = []

        for sequence in metric_context.source_pulse_sequences:

            for candidate in sequence.pulse_candidates:

                records.append(
                    ValidationRecord(
                        timestamp=candidate.time,
                        observation_type="PulseCandidate",
                        value=str(candidate.strength),
                        source=sequence.source.name,
                    )
                )

        return tuple(records)
