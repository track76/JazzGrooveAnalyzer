from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from jga.domain.analytical_structure import AnalyticalStructure
from jga.domain.descriptor_set import DescriptorSet

from jga.domain.behaviour_diagnostic_result import (
    BehaviourDiagnosticResult,
)


@dataclass(frozen=True, slots=True)
class BehaviourAnalyticsResult:
    """
    Immutable result produced by Behaviour Analytics.
    """

    id: UUID = field(default_factory=uuid4)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    descriptor_set: DescriptorSet = field(
        default_factory=lambda: DescriptorSet(
            descriptors=(),
        )
    )

    analytical_structure: AnalyticalStructure | None = None

    behaviour_diagnostic_result: (
        BehaviourDiagnosticResult | None
    ) = None
