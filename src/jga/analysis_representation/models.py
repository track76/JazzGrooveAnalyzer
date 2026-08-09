"""Concrete immutable analysis representation for schema revision 1."""

from dataclasses import dataclass

from jga.interfaces.validation import (
    AnalysisOutput,
    AnalysisSection,
    AnalysisTempo,
    AnalysisTimeSignature,
    ImmutableAnalysisRepresentation,
)


@dataclass(frozen=True, slots=True)
class FrozenAnalysisRepresentation(ImmutableAnalysisRepresentation):
    """Deeply immutable scientific result of one completed analysis."""

    analysis_execution_id: str
    audio_content_id: str
    audio_checksum: str
    source_revision: str
    pipeline_version: str
    schema_revision: str
    effective_configuration: tuple[tuple[str, str], ...]
    temporal_origin_seconds: float
    measurement_units: tuple[tuple[str, str], ...]
    output_completeness: tuple[tuple[str, str], ...]
    limitations: tuple[str, ...]
    content_fingerprint: str
    tempo: AnalysisOutput[AnalysisTempo]
    time_signature: AnalysisOutput[AnalysisTimeSignature]
    sections: AnalysisOutput[tuple[AnalysisSection, ...]]
    instrumentation: AnalysisOutput[tuple[str, ...]]

    def scientific_output(self, name: str) -> object:
        outputs = {
            "tempo": self.tempo,
            "time_signature": self.time_signature,
            "sections": self.sections,
            "instrumentation": self.instrumentation,
        }
        try:
            return outputs[name]
        except KeyError as error:
            raise KeyError(f"Unknown scientific output: {name}") from error
