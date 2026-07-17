import numpy as np

from jga.math.stability_scorer import StabilityScorer


def test_regular_intervals_score_one():

    scorer = StabilityScorer()

    score = scorer.compute(
        np.array([0.5, 0.5, 0.5, 0.5])
    )

    assert score == 1.0


def test_irregular_intervals_score_less_than_one():

    scorer = StabilityScorer()

    score = scorer.compute(
        np.array([0.5, 0.7, 0.4, 0.8])
    )

    assert 0.0 < score < 1.0


def test_empty_sequence_scores_zero():

    scorer = StabilityScorer()

    assert scorer.compute(np.array([])) == 0.0
