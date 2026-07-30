from __future__ import annotations

from abc import ABC, abstractmethod

from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.rule_result import RuleResult


class ClassificationRule(ABC):
    """
    Base class for deterministic classification rules.
    """

    @abstractmethod
    def evaluate(self, features: FeatureSet) -> RuleResult:
        """
        Evaluates the rule.
        """
        raise NotImplementedError
