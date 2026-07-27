from jga.geometry.resolvers import (
    MetricStabilityResolver,
)

from jga.core.stability_curve import (
    StabilityCurve,
)

from jga.core.stability_point import (
    StabilityPoint,
)


def test_resolver_returns_closest_stability_point():

    curve = StabilityCurve(
        points=[
            StabilityPoint(
                time=1.0,
                score=0.8,
                window_size=10,
            ),
            StabilityPoint(
                time=2.0,
                score=0.9,
                window_size=10,
            ),
        ]
    )

    resolver = MetricStabilityResolver()

    point = resolver.resolve(
        1.8,
        curve,
    )

    assert point.score == 0.9
