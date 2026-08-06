"""
Validation Record.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationRecord:
    """
    Single observational record exported during scientific validation.
    """

    timestamp: float
    observation_type: str
    value: str
    source: str
