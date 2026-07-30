from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DescriptorSet:
    """
    Immutable collection of behaviour descriptors.
    """

    descriptors: tuple[object, ...]

    @property
    def size(self) -> int:
        return len(self.descriptors)

    def __iter__(self):
        return iter(self.descriptors)

    def __len__(self) -> int:
        return len(self.descriptors)
