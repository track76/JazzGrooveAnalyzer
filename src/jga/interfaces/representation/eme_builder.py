from abc import ABC, abstractmethod


class EMEBuilder(ABC):

    @abstractmethod
    def build(self, pulse_candidates):
        raise NotImplementedError