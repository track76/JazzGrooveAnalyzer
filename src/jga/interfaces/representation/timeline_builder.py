from abc import ABC, abstractmethod


class TimelineBuilder(ABC):

    @abstractmethod
    def build(self, pulses):
        raise NotImplementedError