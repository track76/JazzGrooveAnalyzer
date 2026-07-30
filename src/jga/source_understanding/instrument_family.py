from enum import Enum


class InstrumentFamily(str, Enum):
    """
    High-level classification of musical sound sources.

    Families are intentionally broad and independent from the
    specific instrument recognition algorithm.
    """

    UNKNOWN = "unknown"
    PERCUSSION = "percussion"
    BASS = "bass"
    CHORDAL = "chordal"
    WIND = "wind"
    VOICE = "voice"
    OTHER = "other"
