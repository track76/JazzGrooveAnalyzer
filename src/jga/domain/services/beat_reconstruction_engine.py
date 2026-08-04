"""
Beat Reconstruction Engine.

Reconstructs theoretical BeatReference objects
from observed ElementaryMetricEvents.

M70
"""

from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)
from jga.domain.services.beat_seed_estimator import (
    BeatSeedEstimator,
)
from jga.domain.services.beat_period_estimator import (
    BeatPeriodEstimator,
)
from jga.domain.services.beat_grid_reconstructor import (
    BeatGridReconstructor,
)


class BeatReconstructionEngine:
    """
    Initial reconstruction engine.

    Orchestrates beat reconstruction.
    """

    def __init__(self) -> None:
        self._seed_estimator = BeatSeedEstimator()
        self._period_estimator = BeatPeriodEstimator()
        self._grid_reconstructor = BeatGridReconstructor()

    def reconstruct(
        self,
        events: tuple[ElementaryMetricEvent, ...],
    ) -> tuple[BeatReference, ...]:

        if not events:
            return ()

        seeds = self._seed_estimator.estimate(
            events,
        )

        period = self._period_estimator.estimate(
            events,
        )

        grid = self._grid_reconstructor.reconstruct(
            seeds,
            period if period is not None else 0.0,
        )

        return tuple(
            BeatReference(
                id=uuid4(),
                index=index,
                timestamp=beat,
                created_at=datetime.now(),
            )
            for index, beat in enumerate(grid)
        )
