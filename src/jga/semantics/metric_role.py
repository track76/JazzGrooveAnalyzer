"""
Metric Role.
"""

from enum import Enum


class MetricRole(Enum):
    """
    Scientific metric role.
    """

    UNKNOWN = "unknown"

    PULSE = "pulse"

    REFERENCE = "reference"

    DECORATION = "decoration"
