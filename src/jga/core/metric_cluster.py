"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_cluster.py

Description:
    Metric Cluster

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass, field

from jga.core.metric_position import MetricPosition
from jga.core.eme import EME


@dataclass
class MetricCluster:
    """
    Metric Cluster.

    A Metric Cluster is the collection of all
    Elementary Metric Events (EMEs) that belong
    to the same metric position.

    The cluster does NOT compute the Internal
    Reference Beat (BRI).

    It simply stores the EMEs that contribute
    to the collective timing of the ensemble.
    """

    metric_position: MetricPosition

    emes: list[EME] = field(default_factory=list)

    def add(self, eme: EME) -> None:
        """
        Adds an EME to the cluster.
        """

        self.emes.append(eme)

    @property
    def size(self) -> int:
        """
        Number of EMEs inside the cluster.
        """

        return len(self.emes)

    def __str__(self) -> str:

        return (
            f"{self.metric_position} | "
            f"EMEs: {self.size}"
        )