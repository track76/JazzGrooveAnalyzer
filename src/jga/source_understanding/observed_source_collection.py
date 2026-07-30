from collections.abc import Iterator, Sequence

from jga.source_understanding.observed_source import ObservedSource


class ObservedSourceCollection(Sequence[ObservedSource]):
    """
    Immutable collection of observed sound sources.
    """

    def __init__(self, sources: tuple[ObservedSource, ...]):
        self._sources = sources

    def __len__(self) -> int:
        return len(self._sources)

    def __getitem__(self, index):
        return self._sources[index]

    def __iter__(self) -> Iterator[ObservedSource]:
        return iter(self._sources)
