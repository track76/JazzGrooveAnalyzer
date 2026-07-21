from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from jga.domain.descriptor_set import DescriptorSet


@dataclass(frozen=True, slots=True)
class AnalyticalStructure:
    """
    Immutable analytical structure derived from Descriptor Algebra.

    This entity represents the output defined by M-100.

    It does not modify the originating DescriptorSet.

    No analytical operation is implemented here.
    Concrete mathematical structures will be introduced only
    after formal specification.
    """

    id: UUID = field(default_factory=uuid4)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    source_descriptor_set: DescriptorSet = field(
        default_factory=DescriptorSet
    )
