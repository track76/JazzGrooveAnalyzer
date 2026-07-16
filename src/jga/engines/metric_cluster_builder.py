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

    Builds Metric Clusters by aggregating
    compatible Metric Segments.
    """

    def __init__(self):

        self.criteria = MetricClusterCriteria()

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        metric_segments = context.metric_segments or []
        clusters = []

        if not metric_segments:

            context.metric_clusters = clusters

            if context.report is not None:
                context.report.metric_clusters = clusters

            context.log.add("0 Metric Clusters detected.")

            return context

        start_time = metric_segments[0].periodicity.start_time
        end_time = metric_segments[0].periodicity.end_time
        mean_interval = metric_segments[0].periodicity.mean_interval
        stability = metric_segments[0].periodicity.stability
        count = 1

        for segment in metric_segments[1:]:

            interval_difference = (
                abs(segment.periodicity.mean_interval - mean_interval)
                / mean_interval
            )

            stability_difference = abs(
                segment.periodicity.stability - stability
            )

            compatible = (
                segment.periodicity.stability
                >= self.criteria.minimum_stability
                and stability >= self.criteria.minimum_stability
                and interval_difference
                <= self.criteria.interval_tolerance
                and stability_difference
                <= self.criteria.stability_tolerance
            )

            if compatible:

                end_time = segment.periodicity.end_time

                count += 1

                mean_interval = (
                    mean_interval * (count - 1)
                    + segment.periodicity.mean_interval
                ) / count

                stability = (
                    stability * (count - 1)
                    + segment.periodicity.stability
                ) / count

            else:

                clusters.append(
                    MetricCluster(
                        start_time=start_time,
                        end_time=end_time,
                        mean_interval=mean_interval,
                        stability=stability,
                        windows=[],
                    )
                )

                start_time = segment.periodicity.start_time
                end_time = segment.periodicity.end_time
                mean_interval = segment.periodicity.mean_interval
                stability = segment.periodicity.stability
                count = 1

        clusters.append(
            MetricCluster(
                start_time=start_time,
                end_time=end_time,
                mean_interval=mean_interval,
                stability=stability,
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