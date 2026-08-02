"""
Scientific Visualization Scene.
"""

from dataclasses import dataclass

from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)

from jga.visualization.visualization_annotation import (
    VisualizationAnnotation,
)


@dataclass(frozen=True)
class ScientificVisualizationScene:
    """
    Complete scientific visualization scene.
    """

    trajectories: tuple[
        VisualizationTrajectoryDescriptor,
        ...
    ] = ()

    annotations: tuple[
        VisualizationAnnotation,
        ...
    ] = ()

    def select(
        self,
        identifier: str,
    ) -> VisualizationTrajectoryDescriptor:
        """
        Returns the trajectory identified by
        the given identifier.
        """

        for trajectory in self.trajectories:

            if trajectory.identifier == identifier:
                return trajectory

        raise ValueError(
            f"Unknown trajectory: {identifier}"
        )

    def identifiers(
        self,
    ) -> tuple[str, ...]:
        """
        Returns all available trajectory identifiers.
        """

        return tuple(
            trajectory.identifier
            for trajectory in self.trajectories
        )

    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Returns whether the scene contains
        the requested trajectory.
        """

        return identifier in self.identifiers()

    def filter(
        self,
        *identifiers: str,
    ) -> "ScientificVisualizationScene":
        """
        Returns a new scene containing only
        the requested trajectories.
        """

        return ScientificVisualizationScene(
            trajectories=tuple(
                trajectory
                for trajectory in self.trajectories
                if trajectory.identifier in identifiers
            ),
            annotations=self.annotations,
        )

    def merge(
        self,
        other: "ScientificVisualizationScene",
    ) -> "ScientificVisualizationScene":
        """
        Returns a new scene containing the
        trajectories of both scenes.
        """

        return ScientificVisualizationScene(
            trajectories=(
                *self.trajectories,
                *other.trajectories,
            ),
            annotations=(
                *self.annotations,
                *other.annotations,
            ),
        )

    def difference(
        self,
        other: "ScientificVisualizationScene",
    ) -> "ScientificVisualizationScene":
        """
        Returns a new scene containing only
        trajectories not present in the
        other scene.
        """

        other_ids = set(
            other.identifiers()
        )

        return ScientificVisualizationScene(
            trajectories=tuple(
                trajectory
                for trajectory in self.trajectories
                if trajectory.identifier
                not in other_ids
            ),
            annotations=self.annotations,
        )

    def trajectory_count(
        self,
    ) -> int:
        """
        Returns the number of trajectories.
        """

        return len(
            self.trajectories
        )

    def total_points(
        self,
    ) -> int:
        """
        Returns the total number of visual
        points across all trajectories.
        """

        return sum(
            len(
                descriptor.trajectory.points
            )
            for descriptor in self.trajectories
        )

    def slice_time(
        self,
        start_time: float,
        end_time: float,
    ) -> "ScientificVisualizationScene":
        """
        Returns a new scene containing
        trajectories sliced by time window.
        """

        from jga.visualization.visualization_trajectory_descriptor import (
            VisualizationTrajectoryDescriptor,
        )

        return ScientificVisualizationScene(
            trajectories=tuple(
                VisualizationTrajectoryDescriptor(
                    identifier=descriptor.identifier,
                    trajectory=descriptor.trajectory.slice(
                        start_time,
                        end_time,
                    ),
                )
                for descriptor in self.trajectories
            ),
            annotations=tuple(
                annotation
                for annotation in self.annotations
                if start_time <= annotation.timestamp <= end_time
            ),
        )

    def slice(
        self,
        window,
    ) -> "ScientificVisualizationScene":
        """
        Returns a new scene filtered by a
        TemporalVisualizationWindow.
        """

        return ScientificVisualizationScene(
            trajectories=tuple(
                VisualizationTrajectoryDescriptor(
                    identifier=descriptor.identifier,
                    trajectory=descriptor.trajectory.slice(
                        window.start_time,
                        window.end_time,
                    ),
                )
                for descriptor in self.trajectories
            ),
            annotations=tuple(
                annotation
                for annotation in self.annotations
                if window.contains(annotation.timestamp)
            ),
        )

    def find_annotations(
        self,
        label: str,
    ) -> tuple:
        """
        Returns annotations matching the given label.
        """

        return tuple(
            annotation
            for annotation in self.annotations
            if annotation.label == label
        )

    def annotations_between(
        self,
        window,
    ) -> tuple:
        """
        Returns annotations contained
        inside the temporal window.
        """

        return tuple(
            annotation
            for annotation in self.annotations
            if window.contains(
                annotation.timestamp
            )
        )

    def annotation_for_reference(
        self,
        reference_id,
    ):
        """
        Returns the annotation associated with
        the given external reference id.
        """

        for annotation in self.annotations:

            if annotation.reference_id == reference_id:
                return annotation

        return None

    def annotation_for_reference_in_window(
        self,
        reference_id,
        window,
    ):
        """
        Returns the annotation associated with a reference id
        only if it belongs to the given temporal window.
        """

        for annotation in self.annotations:

            if (
                annotation.reference_id == reference_id
                and window.contains(
                    annotation.timestamp
                )
            ):
                return annotation

        return None

