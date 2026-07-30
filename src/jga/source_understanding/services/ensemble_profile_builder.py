from jga.source_understanding.ensemble_profile import EnsembleProfile
from jga.source_understanding.observed_source_collection import (
    ObservedSourceCollection,
)


class EnsembleProfileBuilder:
    """
    Builds an EnsembleProfile from observed sources.
    """

    def build(
        self,
        observed: ObservedSourceCollection,
    ) -> EnsembleProfile:

        families = tuple(
            source.classification.family
            for source in observed
        )

        if not families:
            confidence = 0.0
        else:
            confidence = (
                sum(
                    source.classification.confidence
                    for source in observed
                )
                / len(observed)
            )

        return EnsembleProfile(
            families=families,
            confidence=confidence,
        )
