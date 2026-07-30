from dataclasses import dataclass

from jga.source_understanding.instrument_family import InstrumentFamily


@dataclass(frozen=True, slots=True)
class ClassificationDecision:
    """
    Result produced by the rule engine before creating an
    InstrumentClassification.
    """

    family: InstrumentFamily
    confidence: float
