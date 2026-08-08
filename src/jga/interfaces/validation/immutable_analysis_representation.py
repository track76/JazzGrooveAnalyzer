"""Immutable boundary between completed analysis and validation."""

from abc import ABC, abstractmethod


class ImmutableAnalysisRepresentation(ABC):
    """Scientific representation of one completed JGA analysis.

    Implementations must be deeply and transitively immutable. Values exposed
    through this contract must not reference ``AnalysisContext`` or any other
    mutable runtime state. Scientific outputs are limited to those required by
    the declared validation scope.
    """

    @property
    @abstractmethod
    def analysis_execution_id(self) -> str:
        """Unique identity of the completed analysis execution."""
        raise NotImplementedError

    @property
    @abstractmethod
    def audio_content_id(self) -> str:
        """Stable identity of the analyzed audio content."""
        raise NotImplementedError

    @property
    @abstractmethod
    def audio_checksum(self) -> str:
        """Integrity checksum of the analyzed audio content."""
        raise NotImplementedError

    @property
    @abstractmethod
    def source_revision(self) -> str:
        """Source revision that produced the scientific outputs."""
        raise NotImplementedError

    @property
    @abstractmethod
    def pipeline_version(self) -> str:
        """Version of the analysis pipeline."""
        raise NotImplementedError

    @property
    @abstractmethod
    def schema_revision(self) -> str:
        """Revision of this boundary contract's data schema."""
        raise NotImplementedError

    @property
    @abstractmethod
    def effective_configuration(self) -> tuple[tuple[str, str], ...]:
        """Complete, immutable effective analysis configuration."""
        raise NotImplementedError

    @property
    @abstractmethod
    def temporal_origin_seconds(self) -> float:
        """Temporal origin used to interpret included analysis values."""
        raise NotImplementedError

    @property
    @abstractmethod
    def measurement_units(self) -> tuple[tuple[str, str], ...]:
        """Units required to interpret included quantitative values."""
        raise NotImplementedError

    @property
    @abstractmethod
    def output_completeness(self) -> tuple[tuple[str, str], ...]:
        """Explicit completeness state of each scoped scientific output."""
        raise NotImplementedError

    @property
    @abstractmethod
    def limitations(self) -> tuple[str, ...]:
        """Scientific limitations affecting interpretation of the result."""
        raise NotImplementedError

    @property
    @abstractmethod
    def content_fingerprint(self) -> str:
        """Deterministic identity of the frozen scientific content."""
        raise NotImplementedError

    @abstractmethod
    def scientific_output(self, name: str) -> object:
        """Return one deeply immutable output in the declared scope."""
        raise NotImplementedError
