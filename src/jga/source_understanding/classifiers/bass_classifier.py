from __future__ import annotations

from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.instrument_classification import InstrumentClassification
from jga.source_understanding.instrument_classifier import InstrumentClassifier
from jga.source_understanding.instrument_family import InstrumentFamily
from jga.source_understanding.rules.classification_decision_maker import (
    ClassificationDecisionMaker,
)
from jga.source_understanding.rules.low_spectral_centroid_rule import (
    LowSpectralCentroidRule,
)
from jga.source_understanding.rules.low_spectral_rolloff_rule import (
    LowSpectralRolloffRule,
)
from jga.source_understanding.rules.rule_engine import RuleEngine
from jga.source_understanding.rules.rule_set import RuleSet


class BassClassifier(InstrumentClassifier):
    def __init__(self):
        self._rule_set = RuleSet(
            (
                LowSpectralCentroidRule(
                    threshold=300.0,
                ),
                LowSpectralRolloffRule(
                    threshold=400.0,
                ),
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
            family=InstrumentFamily.BASS,
            instrument=None,
            confidence=decision.confidence,
            classifier_name=self.__class__.__name__,
            classifier_version="0.1.0",
        )
