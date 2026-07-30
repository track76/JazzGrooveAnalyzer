from __future__ import annotations

from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.classification_rule import ClassificationRule
from jga.source_understanding.rules.rule_result import RuleResult


class FeatureRangeRule(ClassificationRule):
    """
    Generic range comparison rule for numerical features.
    """

    def __init__(
        self,
        feature: FeatureName,
        lower_bound: float,
        upper_bound: float,
    ):
        self._feature = feature
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound

    def evaluate(self, features: FeatureSet) -> RuleResult:
        value = features.get(self._feature)

        satisfied = (
            self._lower_bound <= value <= self._upper_bound
        )

        return RuleResult(
            satisfied=satisfied,
            confidence=1.0 if satisfied else 0.0,
        )
