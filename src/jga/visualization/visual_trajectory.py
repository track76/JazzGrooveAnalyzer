"""
Visual Trajectory.
"""

from dataclasses import dataclass

from jga.visualization.visual_point import (
    VisualPoint,
)


@dataclass(frozen=True)
class VisualTrajectory:
    """
    Scientific visual trajectory.
    """

    points: tuple[
        VisualPoint,
        ...
    ] = ()

    def is_empty(
        self,
    ) -> bool:
        """
        Returns whether the trajectory
        contains no points.
        """

        return not self.points

    def first_point(
        self,
    ) -> VisualPoint:
        """
        Returns the first visual point.
        """

        if self.is_empty():
            raise ValueError(
                "Empty trajectory."
            )

        return self.points[0]

    def last_point(
        self,
    ) -> VisualPoint:
        """
        Returns the last visual point.
        """

        if self.is_empty():
            raise ValueError(
                "Empty trajectory."
            )

        return self.points[-1]

    def start_time(
        self,
    ) -> float:
        """
        Returns the first timestamp.
        """

        return self.first_point().time

    def end_time(
        self,
    ) -> float:
        """
        Returns the last timestamp.
        """

        return self.last_point().time

    def duration(
        self,
    ) -> float:
        """
        Returns the temporal duration.
        """

        return (
            self.end_time()
            - self.start_time()
        )

    def point_count(
        self,
    ) -> int:
        """
        Returns the number of visual points.
        """

        return len(
            self.points
        )

    def slice(
        self,
        start_time: float,
        end_time: float,
    ) -> "VisualTrajectory":
        """
        Returns a temporal slice
        of the trajectory.
        """

        return VisualTrajectory(
            points=tuple(
                point
                for point in self.points
                if (
                    start_time
                    <= point.time
                    <= end_time
                )
            ),
        )
