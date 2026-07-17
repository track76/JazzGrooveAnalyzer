import numpy as np

from jga.math.regularity_scorer import RegularityScorer


def test_perfectly_regular_sequence_scores_one():

    scorer = RegularityScorer()

    score = scorer.compute(
        np.array([0.5, 0.5, 0.5, 0.5])
    )

    assert score == 1.0


def test_irregular_sequence_scores_less_than_one():

    scorer = RegularityScorer()

    score = scorer.compute(
        np.array([0.5, 0.7, 0.4, 0.8])
    )

    assert 0.0 < score < 1.0


def test_empty_sequence_scores_zero():

    scorer = RegularityScorer()

    score = scorer.compute(np.array([]))

    assert score == 0.0
