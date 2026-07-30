from __future__ import annotations

from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.classification_rule import ClassificationRule
from jga.source_understanding.rules.comparison_operator import ComparisonOperator
from jga.source_understanding.rules.rule_result import RuleResult


class FeatureComparisonRule(ClassificationRule):
    """
    Generic comparison rule for a numerical feature.
    """

    def __init__(
        self,
        feature: FeatureName,
        operator: ComparisonOperator,
        threshold: float,
    ):
        self._feature = feature
        self._operator = operator
        self._threshold = threshold

    def evaluate(self, features: FeatureSet) -> RuleResult:
        value = features.get(self._feature)

        match self._operator:
            case ComparisonOperator.LESS:
                satisfied = value < self._threshold
            case ComparisonOperator.LESS_EQUAL:
                satisfied = value <= self._threshold
            case ComparisonOperator.GREATER:
                satisfied = value > self._threshold
            case ComparisonOperator.GREATER_EQUAL:
                satisfied = value >= self._threshold
            case _:
                raise ValueError(f"Unsupported operator: {self._operator}")

        return RuleResult(
            satisfied=satisfied,
            confidence=1.0 if satisfied else 0.0,
        )
