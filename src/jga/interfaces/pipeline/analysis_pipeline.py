from abc import ABC, abstractmethod


class AnalysisPipeline(ABC):

    @abstractmethod
    def analyze(self, audio):
        raise NotImplementedError