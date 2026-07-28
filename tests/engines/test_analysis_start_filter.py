from jga.engines.analysis_start_filter import AnalysisStartFilter
from jga.runtime.analysis_context import AnalysisContext
from jga.core.pulse_candidate import PulseCandidate


def test_analysis_start_filter_removes_previous_candidates():

    context = AnalysisContext(audio=None)

    context.analysis_start_time = 10.0

    context.pulse_candidates = [
        PulseCandidate(time=5.0, strength=1.0),
        PulseCandidate(time=10.0, strength=1.0),
        PulseCandidate(time=12.0, strength=1.0),
    ]

    filter_engine = AnalysisStartFilter()

    result = filter_engine.process(context)

    assert len(result.pulse_candidates) == 2
    assert result.pulse_candidates[0].time == 10.0
    assert result.pulse_candidates[1].time == 12.0


def test_analysis_start_filter_is_neutral_at_zero():

    context = AnalysisContext(audio=None)

    context.analysis_start_time = 0.0

    context.pulse_candidates = [
        PulseCandidate(time=1.0, strength=1.0),
    ]

    filter_engine = AnalysisStartFilter()

    result = filter_engine.process(context)

    assert len(result.pulse_candidates) == 1
