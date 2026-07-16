from abc import ABC, abstractmethod

from jga.runtime.analysis_context import AnalysisContext


class DomainInputBuilder(ABC):

    @abstractmethod
    def build(
        self,
        context: AnalysisContext,
    ):
        """
        Builds the canonical Domain input from the
        AnalysisContext.
        """
        raise NotImplementedError
