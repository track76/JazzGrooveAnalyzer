from __future__ import annotations

from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.instrument_classification import InstrumentClassification
from jga.source_understanding.instrument_classifier import InstrumentClassifier
from jga.source_understanding.instrument_family import InstrumentFamily
from jga.source_understanding.rules.classification_decision_maker import (
    ClassificationDecisionMaker,
)
from jga.source_understanding.rules.feature_range_rule import (
    FeatureRangeRule,
)
from jga.source_understanding.rules.long_duration_rule import (
    LongDurationRule,
)
from jga.source_understanding.rules.rule_engine import RuleEngine
from jga.source_understanding.rules.rule_set import RuleSet
from jga.source_understanding.feature_name import FeatureName


class ChordalClassifier(InstrumentClassifier):

    def __init__(self):
        self._rule_set = RuleSet(
            (
                FeatureRangeRule(
                    feature=FeatureName.SPECTRAL_CENTROID,
                    lower_bound=500.0,
                    upper_bound=1000.0,
                ),
                FeatureRangeRule(
                    feature=FeatureName.SPECTRAL_BANDWIDTH,
                    lower_bound=300.0,
                    upper_bound=800.0,
                ),
                FeatureRangeRule(
                    feature=FeatureName.SPECTRAL_ROLLOFF,
                    lower_bound=1000.0,
                    upper_bound=2500.0,
                ),
                LongDurationRule(1.0),
            )
        )

        self._engine = RuleEngine()
        self._decision_maker = ClassificationDecisionMaker()

    def classify(self, features: FeatureSet) -> InstrumentClassification:
        results = self._engine.evaluate(
            self._rule_set,
            features,
        )

        decision = self._decision_maker.decide(results)

        return InstrumentClassification(
            family=InstrumentFamily.CHORDAL,
            instrument=None,
            confidence=decision.confidence,
            classifier_name=self.__class__.__name__,
            classifier_version="0.1.0",
        )
