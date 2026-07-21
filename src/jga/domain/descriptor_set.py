from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor


@dataclass(frozen=True, slots=True)
class DescriptorSet:
    """
    Immutable mathematical set of BehaviourDescriptor objects.

    This entity represents the formal input of Behaviour Analytics.

    The class only guarantees representation integrity.
    Analytical operations belong to Behaviour Analytics services.
    """

    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    descriptors: tuple[BehaviourDescriptor, ...] = ()

    @property
    def size(self) -> int:
        return len(self.descriptors)

    def __iter__(self):
        return iter(self.descriptors)
