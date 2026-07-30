from __future__ import annotations

from jga.source_understanding.instrument_family import InstrumentFamily
from jga.source_understanding.rules.classification_decision import (
    ClassificationDecision,
)
from jga.source_understanding.rules.rule_result import RuleResult


class ClassificationDecisionMaker:
    """
    Converts rule results into a classification decision.
    """

    def decide(
        self,
        results: tuple[RuleResult, ...],
    ) -> ClassificationDecision:
        if not results:
            return ClassificationDecision(
                family=InstrumentFamily.UNKNOWN,
                confidence=0.0,
            )

        confidence = sum(
            result.confidence
            for result in results
            if result.satisfied
        ) / len(results)

        return ClassificationDecision(
            family=InstrumentFamily.UNKNOWN,
            confidence=confidence,
        )
