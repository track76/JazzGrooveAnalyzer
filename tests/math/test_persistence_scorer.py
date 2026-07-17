import numpy as np

from jga.math.persistence_scorer import PersistenceScorer


def test_empty_sequence_scores_zero():

    scorer = PersistenceScorer()

    assert scorer.compute(np.array([])) == 0.0


def test_short_sequence_scores_less_than_one():

    scorer = PersistenceScorer()

    score = scorer.compute(
        np.array([0.5, 0.5, 0.5, 0.5])
    )

    assert 0.0 < score < 1.0


def test_long_sequence_scores_one():

    scorer = PersistenceScorer()

    score = scorer.compute(
        np.ones(32)
    )

    assert score == 1.0
