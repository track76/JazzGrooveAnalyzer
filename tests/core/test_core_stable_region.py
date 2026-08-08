from jga.core.stability_point import StabilityPoint
from jga.core.stable_region import StableRegion


def test_stable_region_properties():

    points = (
        StabilityPoint(
            time=1.0,
            score=0.8,
            window_size=8,
        ),
        StabilityPoint(
            time=2.0,
            score=0.9,
            window_size=8,
        ),
    )

    region = StableRegion(
        start_time=1.0,
        end_time=3.0,
        stability_points=points,
    )

    assert region.duration == 2.0
    assert region.size == 2
    assert abs(region.mean_score - 0.85) < 1e-9
