"""Completed Analysis to Immutable Analysis Representation boundary."""

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path

from jga.analysis_representation.models import FrozenAnalysisRepresentation
from jga.interfaces.validation import AnalysisOutput, AnalysisOutputState
from jga.runtime.analysis_context import AnalysisContext


_SCOPED_OUTPUTS = (
    "instrumentation",
    "sections",
    "tempo",
    "time_signature",
)

_LIMITATIONS = (
    "instrumentation: canonical validation-facing categories are not produced",
    "sections: canonical section boundaries are not produced",
    "tempo: validation-facing tempo is not scientifically produced",
    "time_signature: validation-facing time signature is not scientifically produced",
)


@dataclass(frozen=True, slots=True)
class MaterializationProvenance:
    """Stable caller-owned provenance for one completed analysis."""

    analysis_execution_id: str
    audio_content_id: str
    source_revision: str
    pipeline_version: str
    effective_configuration: tuple[tuple[str, str], ...] = ()
    temporal_origin_seconds: float = 0.0


class CompletedAnalysisMaterializer:
    """Freezes approved outputs without exposing mutable runtime state."""

    SCHEMA_REVISION = "1"

    def materialize(
        self,
        completed_analysis: AnalysisContext,
        provenance: MaterializationProvenance,
    ) -> FrozenAnalysisRepresentation:
        audio_checksum = self._checksum(completed_analysis.audio.path)
        outputs = {
            name: AnalysisOutput(AnalysisOutputState.NOT_PRODUCED)
            for name in _SCOPED_OUTPUTS
        }
        output_completeness = tuple(
            (name, outputs[name].state.value) for name in _SCOPED_OUTPUTS
        )
        measurement_units = (
            ("sections.start_full_measure", "full_measure"),
            ("sections.measure_count", "full_measure"),
            ("tempo", "beats_per_minute"),
            ("temporal_origin", "seconds"),
            ("time_signature", "beats/beat_type"),
        )
        effective_configuration = tuple(sorted(provenance.effective_configuration))

        fingerprint_payload = {
            "audio_checksum": audio_checksum,
            "effective_configuration": effective_configuration,
            "limitations": _LIMITATIONS,
            "measurement_units": measurement_units,
            "outputs": output_completeness,
            "pipeline_version": provenance.pipeline_version,
            "schema_revision": self.SCHEMA_REVISION,
            "source_revision": provenance.source_revision,
            "temporal_origin_seconds": provenance.temporal_origin_seconds,
        }
        content_fingerprint = sha256(
            json.dumps(
                fingerprint_payload,
                ensure_ascii=True,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()

        return FrozenAnalysisRepresentation(
            analysis_execution_id=provenance.analysis_execution_id,
            audio_content_id=provenance.audio_content_id,
            audio_checksum=audio_checksum,
            source_revision=provenance.source_revision,
            pipeline_version=provenance.pipeline_version,
            schema_revision=self.SCHEMA_REVISION,
            effective_configuration=effective_configuration,
            temporal_origin_seconds=provenance.temporal_origin_seconds,
            measurement_units=measurement_units,
            output_completeness=output_completeness,
            limitations=_LIMITATIONS,
            content_fingerprint=content_fingerprint,
            tempo=outputs["tempo"],
            time_signature=outputs["time_signature"],
            sections=outputs["sections"],
            instrumentation=outputs["instrumentation"],
        )

    @staticmethod
    def _checksum(path: Path) -> str:
        digest = sha256()
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
