from abc import ABC, abstractmethod


class OnsetDetector(ABC):

    @abstractmethod
    def detect(self, signal):
        raise NotImplementedError