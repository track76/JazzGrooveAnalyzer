from dataclasses import dataclass

from jga.domain.metric_contributor import MetricContributor
from jga.domain.musical_function import MusicalFunction
from jga.domain.sound_source import SoundSource
from jga.domain.source_musical_function_assignment import (
    SourceMusicalFunctionAssignment,
)


@dataclass(frozen=True, slots=True)
class EnsembleAnalysisResult:
    """
    Output of the Level A0 ensemble analysis pipeline.

    Contains both legacy separated collections and the
    explicit source/function relationship model.
    """

    sound_sources: tuple[SoundSource, ...]

    musical_functions: tuple[MusicalFunction, ...]

    metric_contributors: tuple[MetricContributor, ...]

    source_function_assignments: tuple[
        SourceMusicalFunctionAssignment,
        ...,
    ] = ()
