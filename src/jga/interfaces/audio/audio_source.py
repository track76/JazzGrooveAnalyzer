from abc import ABC, abstractmethod


class AudioSource(ABC):
    """Abstract audio source."""

    @abstractmethod
    def load(self, path: str):
        """Load an audio source."""
        raise NotImplementedError