from abc import ABC, abstractmethod


class TransientDetector(ABC):

    @abstractmethod
    def detect(self, signal):
        raise NotImplementedError