from jga.source_understanding.rules.rule_set import RuleSet


def test_rule_set_is_empty():
    rule_set = RuleSet(())

    assert len(rule_set.rules) == 0
