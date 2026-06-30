"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    stability_summary.py

Description:
    Prints a summary of the Metric Stability analysis.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

import numpy as np

from jga.runtime.analysis_report import AnalysisReport


class StabilitySummary:
    """
    Prints a summary of the Metric Stability Curve.
    """

    def print(self, report: AnalysisReport):

        print("\n=========================================")
        print("      METRIC STABILITY SUMMARY")
        print("=========================================")

        print(f"\nFile                 : {report.filename}")
        print(f"Duration             : {report.duration:.2f} s")

        print(f"\nPulse Candidates     : {report.pulse_candidates}")
        print(f"Pulse Intervals      : {report.pulse_intervals}")
        print(f"Analysis Windows     : {report.analysis_windows}")

        curve = report.stability_curve

        if curve is None or len(curve) == 0:

            print("\nNo Stability Curve available.")
            return

        scores = np.array([point.score for point in curve])

        print("\nMetric Stability")

        print(f"Average              : {np.mean(scores):.3f}")
        print(f"Minimum              : {np.min(scores):.3f}")
        print(f"Maximum              : {np.max(scores):.3f}")

        print("\nFirst 10 Stability Values")

        for point in curve.points[:10]:
            print(f"{point.score:.3f}")

        print("\n=========================================")