"""
Scientific Plot Metadata.

Semantic description of a scientific visualization.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScientificPlotMetadata:
    """
    Metadata describing scientific plot meaning.
    """

    purpose: str

    domain: str

    def is_valid(
        self,
    ) -> bool:
        """
        Checks metadata validity.
        """

        return bool(
            self.purpose
            and self.domain
        )
