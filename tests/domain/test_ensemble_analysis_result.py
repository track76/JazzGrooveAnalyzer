from datetime import datetime
from uuid import uuid4

from jga.domain.ensemble_analysis_result import EnsembleAnalysisResult
from jga.domain.metric_contributor import MetricContributor
from jga.domain.musical_function import MusicalFunction
from jga.domain.sound_source import SoundSource


def test_create_ensemble_analysis_result():

    source = SoundSource(
        id=uuid4(),
        name="bass",
        family="strings",
        description=None,
        created_at=datetime.now(),
    )

    function = MusicalFunction(
        id=uuid4(),
        name="Walking Bass",
        description=None,
        is_metric=True,
        created_at=datetime.now(),
    )

    contributor = MetricContributor(
        id=uuid4(),
        sound_source_id=source.id,
        musical_function_id=function.id,
        active=True,
        created_at=datetime.now(),
    )

    result = EnsembleAnalysisResult(
        sound_sources=(source,),
        musical_functions=(function,),
        metric_contributors=(contributor,),
    )

    assert len(result.sound_sources) == 1
    assert len(result.musical_functions) == 1
    assert len(result.metric_contributors) == 1

    assert result.sound_sources[0] == source
    assert result.musical_functions[0] == function
    assert result.metric_contributors[0] == contributor