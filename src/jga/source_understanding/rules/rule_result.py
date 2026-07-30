from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuleResult:
    """
    Result produced by a classification rule.
    """

    satisfied: bool
    confidence: float
