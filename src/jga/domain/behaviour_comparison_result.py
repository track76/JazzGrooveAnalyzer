from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class BehaviourComparisonResult:
    """
    Scientific comparison between two
    Behaviour Observation Frames.
    """

    physical_offset_match: bool

    metric_offset_match: bool

    internal_bpm_match: bool

    stability_match: bool

    @property
    def overall_match(self) -> bool:

        return (

            self.physical_offset_match

            and self.metric_offset_match

            and self.internal_bpm_match

            and self.stability_match

        )

