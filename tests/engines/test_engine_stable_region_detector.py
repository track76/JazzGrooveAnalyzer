from jga.core.stability_curve import StabilityCurve
from jga.core.stability_point import StabilityPoint
from jga.engines.stable_region_detector import StableRegionDetector


def test_detect_single_region():

    curve = StabilityCurve()

    curve.add(StabilityPoint(0.0, 0.20, 8))
    curve.add(StabilityPoint(1.0, 0.80, 8))
    curve.add(StabilityPoint(2.0, 0.81, 8))
    curve.add(StabilityPoint(3.0, 0.90, 8))
    curve.add(StabilityPoint(4.0, 0.40, 8))

    detector = StableRegionDetector()

    regions = detector.detect(curve)

    assert len(regions) == 1
    assert regions[0].start_time == 1.0
    assert regions[0].end_time == 3.0
    assert regions[0].size == 3
