"""Explicit Comparator binding and schema errors."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BindingFailure:
    binding: str
    expected: str
    observed: str


@dataclass(frozen=True, slots=True)
class SchemaCompatibilityFailure:
    boundary: str
    accepted_versions: tuple[str, ...]
    observed_version: str


class ComparatorBindingError(Exception):
    """Raised before evidence production when scientific identities do not bind."""

    def __init__(
        self,
        comparison_execution_id: str,
        protocol_id: str,
        schema_version: str,
        failures: tuple[BindingFailure, ...],
    ) -> None:
        super().__init__("Comparator input binding failed.")
        self.comparison_execution_id = comparison_execution_id
        self.protocol_id = protocol_id
        self.schema_version = schema_version
        self.failures = failures


class SchemaCompatibilityError(Exception):
    """Raised before evidence production for an unsupported boundary schema."""

    def __init__(
        self,
        comparison_execution_id: str,
        protocol_id: str,
        schema_version: str,
        failures: tuple[SchemaCompatibilityFailure, ...],
    ) -> None:
        super().__init__("Comparator input schema is incompatible.")
        self.comparison_execution_id = comparison_execution_id
        self.protocol_id = protocol_id
        self.schema_version = schema_version
        self.failures = failures
