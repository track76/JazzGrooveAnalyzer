"""
=========================================================
Jazz Groove Analyzer (JGA)

Test:
    Periodicity Scorer

Author:
    Angelo Tracanna
=========================================================
"""

import numpy as np

from jga.math.regularity_scorer import RegularityScorer

def main():

    scorer = RegularityScorer()

    perfect = np.array([
        0.50,
        0.50,
        0.50,
        0.50,
        0.50
    ])

    score = scorer.compute(perfect)

    print("\nPerfect sequence")
    print(score)

    irregular = np.array([
        0.31,
        0.72,
        0.41,
        0.68,
        0.27
    ])

    score = scorer.compute(irregular)

    print("\nIrregular sequence")
    print(score)


if __name__ == "__main__":
    main()