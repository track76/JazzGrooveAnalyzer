import numpy as np

from jga.core.audio_stem import AudioStem
from jga.core.audio_stem_collection import AudioStemCollection


def create_stem(name: str) -> AudioStem:
    return AudioStem(
        name=name,
        signal=np.zeros(1024),
        sample_rate=44100,
    )


def test_collection_contains_stems():
    collection = AudioStemCollection(
        (
            create_stem("Bass"),
            create_stem("Drums"),
        )
    )

    assert len(collection) == 2


def test_collection_is_iterable():
    collection = AudioStemCollection(
        (
            create_stem("Bass"),
            create_stem("Drums"),
        )
    )

    names = [stem.name for stem in collection]

    assert names == ["Bass", "Drums"]


def test_collection_supports_indexing():
    collection = AudioStemCollection(
        (
            create_stem("Bass"),
            create_stem("Drums"),
        )
    )

    assert collection[0].name == "Bass"
    assert collection[1].name == "Drums"
