from jga.visualization.analytical_score import (
    AnalyticalScore,
)
from jga.visualization.analytical_score_builder import (
    AnalyticalScoreBuilder,
)

from jga.runtime.analysis_context import (
    AnalysisContext,
)

from jga.domain.reconstructed_measure import (
    ReconstructedMeasure,
)

from jga.domain.sound_source import (
    SoundSource,
)

from jga.domain.metric_contributor import (
    MetricContributor,
)

from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)

from jga.domain.ensemble_analysis_result import (
    EnsembleAnalysisResult,
)

from jga.domain.metric_cluster import (
    MetricCluster,
)

from jga.domain.metric_contributor import (
    MetricContributor,
)

from jga.domain.sound_source import (
    SoundSource,
)

from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)

from jga.domain.ensemble_analysis_result import (
    EnsembleAnalysisResult,
)

from jga.domain.beat_reference import (
    BeatReference,
)

from jga.representation.metric_point import (
    MetricPoint,
)

from jga.representation.metric_trajectory import (
    MetricTrajectory,
)

from jga.representation.metric_landscape import (
    MetricLandscape,
)

from jga.representation.representation_result import (
    RepresentationResult,
)

from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)

from jga.representation.standard_axes import (
    METRIC_TEMPORAL_DISPLACEMENT_AXIS,
)

from uuid import uuid4
from datetime import datetime




def create_context():

    beat = BeatReference(
        id=uuid4(),
        index=0,
        timestamp=0.0,
        created_at=datetime.now(),
    )

    measure = ReconstructedMeasure(
        number=1,
        time_signature="4/4",
        internal_bpm=124.0,
        start_time_seconds=0.0,
        end_time_seconds=2.0,
        beat_references=(beat,),
        metric_clusters=(),
    )

    source = SoundSource(
        id=uuid4(),
        name="Double Bass",
        family="Strings",
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

    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=contributor.id,
        timestamp=0.010,
        confidence=1.0,
        created_at=datetime.now(),
    )

    cluster = MetricCluster(
        id=uuid4(),
        beat_reference=beat,
        events=(event,),
        created_at=datetime.now(),
    )

    analysis_result = EnsembleAnalysisResult(
        sound_sources=(source,),
        musical_functions=(),
        metric_contributors=(contributor,),
    )

    metric_point = MetricPoint(
        event=event,
        coordinate=ScientificCoordinate(
            axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
            value=10.0,
        ),
    )

    representation_result = RepresentationResult(
        metric_landscape=MetricLandscape(
            metric_trajectory=MetricTrajectory(
                metric_points=(metric_point,),
            ),
        ),
    )

    return AnalysisContext(
        audio=None,
        ensemble_analysis_result=analysis_result,
        metric_clusters=(cluster,),
        reconstructed_measures=(measure,),
        representation_result=representation_result,
    )



def test_builder_can_be_instantiated():
    assert AnalyticalScoreBuilder() is not None


def test_builder_exposes_build_method():

    builder = AnalyticalScoreBuilder()

    assert callable(builder.build)


def test_build_returns_analytical_score():

    builder = AnalyticalScoreBuilder()

    score = builder.build(
        create_context()
    )

    assert isinstance(
        score,
        AnalyticalScore,
    )


def test_analytical_score_contains_recording_information():

    score = AnalyticalScoreBuilder().build(
        create_context()
    )

    assert score.recording_title == ""
    assert score.time_signature == "NOT_PRODUCED"
    assert score.meter_origin is None
    assert score.average_bpm == 124.0


def test_builder_creates_instrument_lanes():

    score = AnalyticalScoreBuilder().build(
        create_context()
    )

    assert len(score.instrument_lanes) == 1

    assert score.instrument_lanes[0].name == "Double Bass"

    assert len(
        score.instrument_lanes[0].metric_events
    ) == 1



def test_builder_maps_metric_events_to_instrument_lanes():

    score = AnalyticalScoreBuilder().build(
        create_context()
    )

    assert len(score.instrument_lanes) == 1
