"""
Beat Projection Engine.

Projects an observed event onto the reconstructed
beat grid.

M71.1
"""


class BeatProjectionEngine:
    """
    Projects an observed event onto the
    nearest reconstructed beat.
    """

    def project(
        self,
        event_timestamp: float,
        beat_grid: tuple[float, ...],
    ) -> float | None:

        if not beat_grid:
            return None

        return min(
            beat_grid,
            key=lambda beat: abs(
                event_timestamp - beat
            ),
        )
