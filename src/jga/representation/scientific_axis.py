"""
Scientific Axis.

Representation Layer semantic definition of one
scientific dimension.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScientificAxis:
    """
    Immutable definition of one scientific axis.

    An axis defines what a scientific coordinate means.
    It does not contain a measured value.
    """

    identifier: str

    name: str

    dimension: str

    unit: str

    description: str
