"""
=========================================================
Jazz Groove Analyzer (JGA)

Analysis Log

Author:
    Angelo Tracanna
=========================================================
"""

from dataclasses import dataclass, field
from typing import Iterator

from jga.runtime.runtime_event import RuntimeEvent


@dataclass
class AnalysisLog:
    """
    Collects semantic runtime events emitted during
    pipeline execution.
    """

    entries: list[RuntimeEvent] = field(default_factory=list)

    def add(self, event: str | RuntimeEvent) -> None:
        """
        Accepts either a legacy string message or a
        RuntimeEvent instance.
        """

        if isinstance(event, RuntimeEvent):
            self.entries.append(event)
            return

        self.entries.append(
            RuntimeEvent(
                event_id="LEGACY",
                layer="UNKNOWN",
                component="UNKNOWN",
                message=event,
            )
        )

    def __iter__(self) -> Iterator[RuntimeEvent]:
        return iter(self.entries)
