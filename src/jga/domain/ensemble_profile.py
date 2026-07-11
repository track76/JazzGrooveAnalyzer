from dataclasses import dataclass
from typing import Sequence

from jga.domain.metric_contributor import MetricContributor
from jga.domain.musical_function import MusicalFunction
from jga.domain.sound_source import SoundSource


@dataclass(frozen=True, slots=True)
class EnsembleProfile:
    """
    Describes the musical state of the ensemble after Level A0 analysis.

    This object contains all contextual information required by the
    subsequent stages of the Jazz Groove Analyzer.
    """

    meter: str

    estimated_bpm: float

    pulse_start: float

    sound_sources: Sequence[SoundSource]

    musical_functions: Sequence[MusicalFunction]

    metric_contributors: Sequence[MetricContributor]

    confidence: float