from __future__ import annotations

from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.rule_result import RuleResult
from jga.source_understanding.rules.rule_set import RuleSet


class RuleEngine:
    """
    Evaluates a RuleSet against a FeatureSet.
    """

    def evaluate(
        self,
        rule_set: RuleSet,
        features: FeatureSet,
    ) -> tuple[RuleResult, ...]:
        return tuple(
            rule.evaluate(features)
            for rule in rule_set.rules
        )
