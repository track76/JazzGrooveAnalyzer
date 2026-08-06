"""
Validation Exporter interface.
"""

from abc import ABC, abstractmethod

from jga.validation.validation_dataset import ValidationDataset


class ValidationExporter(ABC):
    """
    Exports a ValidationDataset.

    Exporters must not perform semantic interpretation.
    """

    @abstractmethod
    def export(self, dataset: ValidationDataset, destination: str) -> None:
        """
        Export the validation dataset.
        """
        raise NotImplementedError
