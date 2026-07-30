from __future__ import annotations

from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.instrument_classification import InstrumentClassification
from jga.source_understanding.instrument_classifier import InstrumentClassifier
from jga.source_understanding.instrument_family import InstrumentFamily
from jga.source_understanding.rules.classification_decision_maker import (
    ClassificationDecisionMaker,
)
from jga.source_understanding.rules.high_spectral_bandwidth_rule import (
    HighSpectralBandwidthRule,
)
from jga.source_understanding.rules.high_spectral_centroid_rule import (
    HighSpectralCentroidRule,
)
from jga.source_understanding.rules.high_spectral_rolloff_rule import (
    HighSpectralRolloffRule,
)
from jga.source_understanding.rules.long_duration_rule import (
    LongDurationRule,
)
from jga.source_understanding.rules.rule_engine import RuleEngine
from jga.source_understanding.rules.rule_set import RuleSet


class WindClassifier(InstrumentClassifier):
    def __init__(self):
        self._rule_set = RuleSet(
            (
                HighSpectralCentroidRule(500.0),
                HighSpectralBandwidthRule(300.0),
                HighSpectralRolloffRule(1000.0),
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
            family=InstrumentFamily.WIND,
            instrument=None,
            confidence=decision.confidence,
            classifier_name=self.__class__.__name__,
            classifier_version="0.1.0",
        )
