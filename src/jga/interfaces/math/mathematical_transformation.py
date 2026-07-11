from abc import ABC, abstractmethod


class MathematicalTransformation(ABC):

    @abstractmethod
    def transform(self, obj):
        raise NotImplementedError