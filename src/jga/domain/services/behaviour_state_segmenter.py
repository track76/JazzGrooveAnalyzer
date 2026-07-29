from __future__ import annotations

from abc import ABC, abstractmethod

from jga.domain.behaviour_state import BehaviourState
from jga.geometry.behaviour_trajectory import BehaviourTrajectory


class BehaviourStateSegmenter(ABC):
    """
    Segments one BehaviourTrajectory into an ordered
    sequence of BehaviourState objects.

    Implementations must satisfy the scientific
    specification defined in M8.
    """

    @abstractmethod
    def segment(
        self,
        trajectory: BehaviourTrajectory,
    ) -> tuple[BehaviourState, ...]:
        """
        Produce a complete BehaviourState segmentation.

        The returned states must

        - completely cover the trajectory
        - preserve ordering
        - contain no overlaps
        - contain no gaps
        """
        raise NotImplementedError
