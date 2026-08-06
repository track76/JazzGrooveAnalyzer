"""
Contribution Type.
"""

from enum import Enum


class ContributionType(Enum):
    """
    Scientific contribution to the metric framework.
    """

    UNKNOWN = "unknown"

    PRIMARY = "primary"

    SECONDARY = "secondary"

    SUPPORTING = "supporting"
