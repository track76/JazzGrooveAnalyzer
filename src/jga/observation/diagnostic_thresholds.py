from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class DiagnosticThresholds:

    physical_offset_ms: float = 1.0

    metric_offset: float = 0.01

    internal_bpm: float = 0.10

    stability: float = 0.01
