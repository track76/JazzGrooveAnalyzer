
from abc import ABC, abstractmethod

from jga.translation.domain_reconstruction_input import (
    DomainReconstructionInput,
)

from jga.translation.domain_reconstruction_result import (
    DomainReconstructionResult,
)


class DomainReconstructionBuilder(ABC):

    @abstractmethod
    def build(
        self,
        reconstruction_input: DomainReconstructionInput,
    ) -> DomainReconstructionResult:
        """
        Builds the reconstructed domain model from
        an explicit DomainReconstructionInput contract.
        """
        raise NotImplementedError
