from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.classification_rule import ClassificationRule
from jga.source_understanding.rules.rule_engine import RuleEngine
from jga.source_understanding.rules.rule_result import RuleResult
from jga.source_understanding.rules.rule_set import RuleSet


class DummyRule(ClassificationRule):
    def evaluate(self, features: FeatureSet) -> RuleResult:
        return RuleResult(
            satisfied=True,
            confidence=1.0,
        )


def test_rule_engine_evaluates_all_rules():
    engine = RuleEngine()

    features = FeatureSet()

    results = engine.evaluate(
        RuleSet(
            (
                DummyRule(),
                DummyRule(),
            )
        ),
        features,
    )

    assert len(results) == 2
    assert all(result.satisfied for result in results)
