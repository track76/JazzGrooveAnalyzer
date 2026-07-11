from abc import ABC, abstractmethod


class MetricClusterBuilder(ABC):

    @abstractmethod
    def build(self, events):
        raise NotImplementedError