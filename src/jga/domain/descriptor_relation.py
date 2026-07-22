from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor


@dataclass(frozen=True, slots=True)
class DescriptorRelation:
    """
    Immutable mathematical relationship between BehaviourDescriptor
    objects.

    DescriptorRelation belongs to Behaviour Analytics.

    It represents a mathematical relation without introducing
    musical interpretation.

    Input
    -----
    BehaviourDescriptor*

    Output
    ------
    DescriptorRelation

    Preserved Invariants
    --------------------
    - immutability
    - provenance
    - descriptor identity
    """

    id: UUID = field(default_factory=uuid4)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    descriptors: tuple[BehaviourDescriptor, ...] = ()

