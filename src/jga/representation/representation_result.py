"""
Representation Result.
"""

from dataclasses import dataclass, field

from jga.representation.metric_landscape import (
    MetricLandscape,
)


@dataclass(frozen=True)
class RepresentationResult:
    """
    Final scientific representation produced
    by the representation pipeline.
    """

    metric_landscape: MetricLandscape | None = None

    metric_landscapes: dict[
        str,
        MetricLandscape,
    ] = field(
        default_factory=dict,
    )

    def __post_init__(
        self,
    ) -> None:

        if (
            not self.metric_landscapes
            and self.metric_landscape is not None
        ):

            object.__setattr__(
                self,
                "metric_landscapes",
                {
                    "ensemble": self.metric_landscape,
                },
            )

    def get_landscape(
        self,
        source_id: str,
    ) -> MetricLandscape:
        """
        Returns the metric landscape
        associated with a source.
        """

        return self.metric_landscapes[
            source_id
        ]
