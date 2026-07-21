from tests.support.domain_objects import (
    make_behaviour_observation,
    make_internal_metric_timeline,
    make_pulse,
    make_metric_cluster,
    make_beat_reference,
    make_elementary_metric_event,
)


def test_make_elementary_metric_event():
    assert make_elementary_metric_event() is not None


def test_make_beat_reference():
    assert make_beat_reference().index == 0


def test_make_metric_cluster():
    assert make_metric_cluster().size == 1


def test_make_pulse():
    assert make_pulse().index == 0


def test_make_internal_metric_timeline():
    timeline = make_internal_metric_timeline()

    assert timeline.pulse_count == 1


def test_make_behaviour_observation():
    observation = make_behaviour_observation()

    assert observation.first_pulse.index == 0
    assert observation.last_pulse.index == 0
