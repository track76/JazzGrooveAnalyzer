from abc import ABC, abstractmethod


class PulseBuilder(ABC):

    @abstractmethod
    def build(self, clusters):
        raise NotImplementedError