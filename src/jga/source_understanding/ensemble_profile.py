from dataclasses import dataclass

from jga.source_understanding.instrument_family import InstrumentFamily


@dataclass(frozen=True, slots=True)
class EnsembleProfile:
    """
    High-level description of an observed ensemble.
    """

    families: tuple[InstrumentFamily, ...]
    confidence: float

    @property
    def size(self) -> int:
        return len(self.families)
