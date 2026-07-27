from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from jga.geometry.geometric_point import GeometricPoint


@dataclass(frozen=True)
class BehaviourTrajectory:
    """
    Chronological sequence of GeometricPoints.

    A BehaviourTrajectory belongs to the Geometry layer because it represents
    the evolution of a geometric projection rather than an observable musical
    fact.
    """

    points: list[GeometricPoint] = field(default_factory=list)

    @property
    def point_count(self) -> int:
        return len(self.points)

    @property
    def is_empty(self) -> bool:
        return len(self.points) == 0

    @property
    def first_point(self) -> GeometricPoint | None:
        return None if self.is_empty else self.points[0]

    @property
    def last_point(self) -> GeometricPoint | None:
        return None if self.is_empty else self.points[-1]

    def __iter__(self) -> Iterator[GeometricPoint]:
        return iter(self.points)

