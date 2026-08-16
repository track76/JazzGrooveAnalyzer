"""Epistemic origin of scientific values crossing JGA boundaries."""

from enum import Enum


class ScientificValueOrigin(str, Enum):
    """Keep measured, supplied and reconstructed knowledge distinct."""

    OBSERVED = "OBSERVED"
    DECLARED = "DECLARED"
    INFERRED = "INFERRED"
