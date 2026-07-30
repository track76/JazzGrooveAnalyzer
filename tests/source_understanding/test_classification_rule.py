from typing import get_type_hints

from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.classification_rule import ClassificationRule
from jga.source_understanding.rules.rule_result import RuleResult


def test_classification_rule_contract():
    hints = get_type_hints(ClassificationRule.evaluate)

    assert hints["features"] is FeatureSet
    assert hints["return"] is RuleResult
