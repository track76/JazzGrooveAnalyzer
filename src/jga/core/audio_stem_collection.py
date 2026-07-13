"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    audio_stem_collection.py

Description:
    Immutable collection of AudioStem objects.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass
from typing import Iterator

from jga.core.audio_stem import AudioStem


@dataclass(frozen=True, slots=True)
class AudioStemCollection:
    """
    Logical input of the JGA Core.

    Represents the collection of audio stems produced by the
    Acquisition Layer.
    """

    stems: tuple[AudioStem, ...]

    def __iter__(self) -> Iterator[AudioStem]:
        return iter(self.stems)

    def __len__(self) -> int:
        return len(self.stems)

    def __getitem__(self, index: int) -> AudioStem:
        return self.stems[index]
