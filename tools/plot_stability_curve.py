"""
Plots the Stability Curve.
"""

from pathlib import Path

import matplotlib.pyplot as plt

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline


def main():

    import sys

    if len(sys.argv) != 2:
        print(
            "Usage:\n"
            "python tools/plot_stability_curve.py <audiofile>"
        )
        return 1

    pipeline = AnalysisPipeline()

    context = pipeline.analyze(sys.argv[1])

    curve = context.stability_curve

    if curve is None or len(curve) == 0:
        print("No Stability Curve.")
        return 1

    x = [p.time for p in curve]
    y = [p.score for p in curve]

    output = Path("output")
    output.mkdir(exist_ok=True)

    csv = output / "stability_curve.csv"

    with csv.open("w") as f:
        f.write("time,score\n")

        for point in curve:
            f.write(
                f"{point.time:.6f},"
                f"{point.score:.6f}\n"
            )

    plt.figure(figsize=(12, 4))
    plt.plot(x, y, marker="o")
    plt.axhline(0.75, linestyle="--")
    plt.xlabel("Time (s)")
    plt.ylabel("Stability")
    plt.grid(True)

    png = output / "stability_curve.png"
    plt.savefig(png)

    print(csv)
    print(png)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
