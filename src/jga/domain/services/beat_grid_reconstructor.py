"""
Beat Grid Reconstructor.

Builds a theoretical beat grid from beat seeds
and an estimated beat period.

M70.5
"""


class BeatGridReconstructor:
    """
    Initial deterministic implementation.

    Scientific model:

    grid[0] = first beat seed

    grid[n] = grid[0] + n × period
    """

    def reconstruct(
        self,
        seeds: tuple[float, ...],
        period: float,
    ) -> tuple[float, ...]:

        if not seeds:
            return ()

        ordered_seeds = tuple(
            sorted(
                set(seeds)
            )
        )

        origin = ordered_seeds[0]

        return tuple(
            origin + index * period
            for index in range(
                len(ordered_seeds)
            )
        )
