"""
=========================================================
Jazz Groove Analyzer (JGA)

Analysis Log

Author:
    Angelo Tracanna
=========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class LogEntry:

    timestamp: datetime

    message: str


@dataclass
class AnalysisLog:

    entries: list[LogEntry] = field(default_factory=list)

    def add(self, message: str):

        self.entries.append(
            LogEntry(
                timestamp=datetime.now(),
                message=message
            )
        )

    def __iter__(self):
        return iter(self.entries)