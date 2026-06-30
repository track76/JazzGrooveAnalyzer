"""
=========================================================
Jazz Groove Analyzer (JGA)

Test:
    Analysis Report

Author:
    Angelo Tracanna
=========================================================
"""

import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from jga.pipeline.analysis_pipeline import AnalysisPipeline


def main():

    root = Tk()
    root.withdraw()

    filepath = askopenfilename(
        title="Select an audio file"
    )

    if not filepath:
        print("No file selected.")
        return

    pipeline = AnalysisPipeline()

    context = pipeline.analyze(filepath)

    report = context.report

    print("\n==========================================")
    print("        JAZZ GROOVE ANALYZER REPORT")
    print("==========================================")

    print(f"\nFile               : {report.filename}")
    print(f"Duration           : {report.duration:.2f} s")

    print("\nRHYTHMIC ANALYSIS")

    print(f"Rhythmic Events    : {report.pulse_candidates}")
    print(f"Time Intervals     : {report.pulse_intervals}")
    print(f"Analysis Windows   : {report.analysis_windows}")

    curve = report.stability_curve

    if curve is not None and len(curve) > 0:

        scores = np.array(
            [point.score for point in curve]
        )

        print("\nMETRIC STABILITY")

        print(f"Points             : {len(curve)}")
        print(f"Average            : {scores.mean():.3f}")
        print(f"Minimum            : {scores.min():.3f}")
        print(f"Maximum            : {scores.max():.3f}")

    else:

        print("\nNo Stability Curve available.")

    print("\n==========================================")

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()