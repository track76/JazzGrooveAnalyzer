from abc import ABC, abstractmethod


class SignalRepresentation(ABC):

    @abstractmethod
    def represent(self, audio):
        raise NotImplementedError