from jga.domain.stable_region_detection_result import (
    StableRegionDetectionResult,
)


def test_stable_region_detection_result_creation():

    result = StableRegionDetectionResult(
        events=(),
        evidences=(),
    )

    assert result.events == ()
    assert result.evidences == ()
