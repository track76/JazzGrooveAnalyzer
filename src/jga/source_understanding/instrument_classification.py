from dataclasses import dataclass

from jga.source_understanding.instrument_family import InstrumentFamily


@dataclass(frozen=True, slots=True)
class InstrumentClassification:
    """
    Result produced by an instrument classifier.

    The classification is separated from SoundSource so that
    different classifiers can produce independent observations.
    """

    family: InstrumentFamily
    instrument: str | None
    confidence: float
    classifier_name: str
    classifier_version: str
