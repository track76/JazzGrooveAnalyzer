from decimal import Decimal

from jga.interfaces.validation import (
    AnalysisOutput,
    AnalysisOutputState,
    AnalysisSection,
    AnalysisTempo,
    AnalysisTimeSignature,
    ImmutableAnalysisRepresentation,
)


MP3_SHA256 = "d358d1bca5144ea1dabee4d970fa5deabf81a209922481a77db0f01bd8bdbbbb"


class FakeImmutableAnalysis(ImmutableAnalysisRepresentation):
    def __init__(
        self,
        *,
        schema_revision: str = "1",
        audio_checksum: str = MP3_SHA256,
        tempo: AnalysisOutput[AnalysisTempo] | None = None,
        time_signature: AnalysisOutput[AnalysisTimeSignature] | None = None,
        sections: AnalysisOutput[tuple[AnalysisSection, ...]] | None = None,
        instrumentation: AnalysisOutput[tuple[str, ...]] | None = None,
    ) -> None:
        self._schema_revision = schema_revision
        self._audio_checksum = audio_checksum
        self._tempo = tempo or AnalysisOutput(
            AnalysisOutputState.PRESENT,
            AnalysisTempo(Decimal("80"), "quarter"),
        )
        self._time_signature = time_signature or AnalysisOutput(
            AnalysisOutputState.PRESENT,
            AnalysisTimeSignature(4, 4),
        )
        self._sections = sections or AnalysisOutput(
            AnalysisOutputState.PRESENT,
            (
                AnalysisSection("Intro", 1, 4),
                AnalysisSection("A", 5, 8),
            ),
        )
        self._instrumentation = instrumentation or AnalysisOutput(
            AnalysisOutputState.PRESENT,
            ("Voice", "Saxophone", "Piano", "Double Bass", "Drum Set"),
        )

    @property
    def analysis_execution_id(self) -> str:
        return "ANALYSIS-EXECUTION-001"

    @property
    def audio_content_id(self) -> str:
        return "VAL-001-MP3"

    @property
    def audio_checksum(self) -> str:
        return self._audio_checksum

    @property
    def source_revision(self) -> str:
        return "SOURCE-REVISION-001"

    @property
    def pipeline_version(self) -> str:
        return "PIPELINE-001"

    @property
    def schema_revision(self) -> str:
        return self._schema_revision

    @property
    def effective_configuration(self) -> tuple[tuple[str, str], ...]:
        return ()

    @property
    def temporal_origin_seconds(self) -> float:
        return 0.0

    @property
    def measurement_units(self) -> tuple[tuple[str, str], ...]:
        return (("tempo", "beats_per_minute"),)

    @property
    def output_completeness(self) -> tuple[tuple[str, str], ...]:
        return (
            ("tempo", self._tempo.state.value),
            ("time_signature", self._time_signature.state.value),
            ("sections", self._sections.state.value),
            ("instrumentation", self._instrumentation.state.value),
        )

    @property
    def limitations(self) -> tuple[str, ...]:
        return ()

    @property
    def content_fingerprint(self) -> str:
        return "ANALYSIS-CONTENT-001"

    @property
    def tempo(self) -> AnalysisOutput[AnalysisTempo]:
        return self._tempo

    @property
    def time_signature(self) -> AnalysisOutput[AnalysisTimeSignature]:
        return self._time_signature

    @property
    def sections(self) -> AnalysisOutput[tuple[AnalysisSection, ...]]:
        return self._sections

    @property
    def instrumentation(self) -> AnalysisOutput[tuple[str, ...]]:
        return self._instrumentation

    def scientific_output(self, name: str) -> object:
        return {
            "tempo": self.tempo,
            "time_signature": self.time_signature,
            "sections": self.sections,
            "instrumentation": self.instrumentation,
        }[name]
