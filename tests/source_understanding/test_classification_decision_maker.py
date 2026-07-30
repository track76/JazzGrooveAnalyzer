from jga.source_understanding.instrument_family import InstrumentFamily
from jga.source_understanding.rules.classification_decision_maker import (
    ClassificationDecisionMaker,
)
from jga.source_understanding.rules.rule_result import RuleResult


def test_no_satisfied_rules_produces_zero_confidence():
    decision = ClassificationDecisionMaker().decide(
        (
            RuleResult(satisfied=False, confidence=0.0),
            RuleResult(satisfied=False, confidence=0.0),
        )
    )

    assert decision.family is InstrumentFamily.UNKNOWN
    assert decision.confidence == 0.0


def test_one_satisfied_rule_out_of_two_produces_half_confidence():
    decision = ClassificationDecisionMaker().decide(
        (
            RuleResult(satisfied=True, confidence=1.0),
            RuleResult(satisfied=False, confidence=0.0),
        )
    )

    assert decision.family is InstrumentFamily.UNKNOWN
    assert decision.confidence == 0.5


def test_two_satisfied_rules_out_of_two_produce_full_confidence():
    decision = ClassificationDecisionMaker().decide(
        (
            RuleResult(satisfied=True, confidence=1.0),
            RuleResult(satisfied=True, confidence=1.0),
        )
    )

    assert decision.family is InstrumentFamily.UNKNOWN
    assert decision.confidence == 1.0


def test_one_satisfied_rule_out_of_three_produces_one_third_confidence():
    decision = ClassificationDecisionMaker().decide(
        (
            RuleResult(satisfied=True, confidence=1.0),
            RuleResult(satisfied=False, confidence=0.0),
            RuleResult(satisfied=False, confidence=0.0),
        )
    )

    assert decision.family is InstrumentFamily.UNKNOWN
    assert decision.confidence == 1 / 3
