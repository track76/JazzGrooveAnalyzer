"""Scientific Comparator boundary."""

from .comparator import ScientificComparator
from .errors import ComparatorBindingError, SchemaCompatibilityError
from .models import (
    ComparisonEvidenceState,
    ComparisonResult,
    InstrumentationComparisonEvidence,
    SectionComparisonEvidence,
    SectionCorrespondenceState,
    SectionsComparisonEvidence,
    TempoComparisonEvidence,
    TimeSignatureComparisonEvidence,
)

__all__ = [
    "ComparatorBindingError",
    "ComparisonEvidenceState",
    "ComparisonResult",
    "InstrumentationComparisonEvidence",
    "SchemaCompatibilityError",
    "ScientificComparator",
    "SectionComparisonEvidence",
    "SectionCorrespondenceState",
    "SectionsComparisonEvidence",
    "TempoComparisonEvidence",
    "TimeSignatureComparisonEvidence",
]
