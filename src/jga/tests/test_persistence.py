"""
=========================================================
Jazz Groove Analyzer (JGA)

Test:
    Persistence Scorer

Author:
    Angelo Tracanna
=========================================================
"""

import numpy as np

from jga.math.persistence_scorer import PersistenceScorer


def main():

    scorer = PersistenceScorer()

    short = np.array([0.5, 0.5])

    print("Short sequence")
    print(scorer.compute(short))

    long = np.ones(24) * 0.5

    print("\nLong sequence")
    print(scorer.compute(long))


if __name__ == "__main__":
    main()