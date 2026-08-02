
from datetime import datetime
from uuid import uuid4

from jga.core.metric_context import MetricContext
from jga.domain.ensemble_analysis_result import (
    EnsembleAnalysisResult,
)
from jga.domain.metric_contributor import (
    MetricContributor,
)
from jga.domain.sound_source import (
    SoundSource,
)
from jga.runtime.analysis_context import (
    AnalysisContext,
)
from jga.translation.domain_reconstruction_input_builder import (
    DomainReconstructionInputBuilder,
)


def test_builder_creates_domain_reconstruction_input():

    source = SoundSource(
        id=uuid4(),
        name="bass",
        family="bass",
        description=None,
        created_at=datetime.now(),
    )

    contributor = MetricContributor(
        id=uuid4(),
        sound_source_id=source.id,
        musical_function_id=uuid4(),
        active=True,
        created_at=datetime.now(),
    )

    context = AnalysisContext(
        audio=None,
        ensemble_analysis_result=(
            EnsembleAnalysisResult(
                sound_sources=(source,),
                musical_functions=(),
                metric_contributors=(contributor,),
            )
        ),
        metric_context=MetricContext(
            source_pulse_sequences=(
                object(),
            ),
            periodicity_segments=(),
            metric_segments=(),
        ),
    )

    result = (
        DomainReconstructionInputBuilder()
        .build(context)
    )

    assert result.sound_sources == (source,)
    assert result.metric_contributors == (
        contributor,
    )
    assert result.metric_context is (
        context.metric_context
    )
