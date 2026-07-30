from jga.source_understanding.instrument_family import InstrumentFamily


def test_instrument_family_contains_expected_values():
    expected = {
        "UNKNOWN",
        "PERCUSSION",
        "BASS",
        "CHORDAL",
        "WIND",
        "VOICE",
        "OTHER",
    }

    actual = {member.name for member in InstrumentFamily}

    assert actual == expected


def test_instrument_family_values_are_strings():
    for member in InstrumentFamily:
        assert isinstance(member.value, str)
