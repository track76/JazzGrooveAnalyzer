"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_cluster.py

Description:
    Represents a Metric Cluster recognized
    from consecutive stable Analysis Windows.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass, field

from jga.core.analysis_window import AnalysisWindow


@dataclass(slots=True)
class MetricCluster:
    """
    Represents a stable metric region of the
    musical performance.

    A Metric Cluster is composed of one or more
    consecutive Analysis Windows that share a
    coherent temporal behaviour.
    """

    start_time: float

    end_time: float

    mean_interval: float

    stability: float

    windows: list[AnalysisWindow] = field(default_factory=list)

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    @property
    def window_count(self) -> int:
        return len(self.windows)