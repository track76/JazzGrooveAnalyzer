from jga.core.stability_curve import StabilityCurve
from jga.core.stability_point import StabilityPoint


class MetricStabilityResolver:
    """
    Resolves the closest StabilityPoint
    to a temporal observation.
    """

    def resolve(
        self,
        timestamp: float,
        curve: StabilityCurve,
    ) -> StabilityPoint | None:

        if not curve.points:
            return None

        return min(
            curve.points,
            key=lambda point: abs(
                point.time - timestamp
            ),
        )
