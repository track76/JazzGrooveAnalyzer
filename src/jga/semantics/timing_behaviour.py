"""
Timing Behaviour.
"""

from enum import Enum


class TimingBehaviour(Enum):
    """
    Scientific timing behaviour.
    """

    UNKNOWN = "unknown"

    ANTICIPATING = "anticipating"

    CENTERED = "centered"

    DELAYING = "delaying"

    VARIABLE = "variable"
