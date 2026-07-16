"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_cluster_builder.py

Description:
    Builds Metric Clusters from Metric Segments.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.core.metric_cluster import MetricCluster
from jga.core.metric_cluster_criteria import MetricClusterCriteria
from jga.runtime.analysis_context import AnalysisContext


class MetricClusterBuilder:
    """
    JGA-172

    Builds Metric Clusters.
    """

    def __init__(self):

        self.criteria = MetricClusterCriteria()

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

         clusters = []

         metric_segments = context.metric_segments or []

         for segment in metric_segments:

             clusters.append(
                 MetricCluster(
                 start_time=segment.periodicity.start_time,
                 end_time=segment.periodicity.end_time,
                 mean_interval=segment.periodicity.mean_interval,
                 stability=segment.periodicity.stability,
                 windows=[],
                 )
             )

         context.metric_clusters = clusters

         if context.report is not None:
             context.report.metric_clusters = clusters

         context.log.add(
             f"{len(clusters)} Metric Clusters detected."
         )

         return context
