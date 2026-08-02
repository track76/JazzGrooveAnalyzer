"""
Visualization State.

Represents the current exploration state
of a scientific visualization.

It does not contain scientific data.
"""

from __future__ import annotations

from dataclasses import dataclass

from jga.visualization.visualization_annotation import (
    VisualizationAnnotation,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)


@dataclass(frozen=True)
class VisualizationState:
    """
    Immutable visualization exploration state.
    """

    selected_sources: tuple[str, ...] = ()

    active_annotations: tuple[
        VisualizationAnnotation,
        ...
    ] = ()

    view_mode: str = "default"

    temporal_window: TemporalVisualizationWindow | None = None

    def __post_init__(self) -> None:

        if not self.view_mode:
            raise ValueError(
                "view_mode must not be empty."
            )
