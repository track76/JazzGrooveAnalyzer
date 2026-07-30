from __future__ import annotations

from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.classification_rule import ClassificationRule
from jga.source_understanding.rules.comparison_operator import ComparisonOperator
from jga.source_understanding.rules.feature_comparison_rule import (
    FeatureComparisonRule,
)
from jga.source_understanding.rules.rule_result import RuleResult


class HighSpectralRolloffRule(ClassificationRule):
    """
    Compatibility wrapper around FeatureComparisonRule.
    """

    def __init__(self, threshold: float):
        self._rule = FeatureComparisonRule(
            feature=FeatureName.SPECTRAL_ROLLOFF,
            operator=ComparisonOperator.GREATER_EQUAL,
            threshold=threshold,
        )

    def evaluate(self, features: FeatureSet) -> RuleResult:
        return self._rule.evaluate(features)
