import inspect

from jga.domain.services.behaviour_state_segmenter import (
    BehaviourStateSegmenter,
)


def test_segmenter_is_abstract():

    assert inspect.isabstract(BehaviourStateSegmenter)


def test_segment_method_exists():

    assert hasattr(
        BehaviourStateSegmenter,
        "segment",
    )
