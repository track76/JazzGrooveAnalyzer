from abc import ABC, abstractmethod


class PulseCandidateBuilder(ABC):

    @abstractmethod
    def build(self, onsets):
        raise NotImplementedError