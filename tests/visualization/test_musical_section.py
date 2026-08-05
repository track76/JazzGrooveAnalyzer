from jga.visualization.musical_section import (
    MusicalSection,
)


def test_musical_section_can_be_created():

    section = MusicalSection(
        name="A1",
        first_measure=9,
        last_measure=40,
    )

    assert section.name == "A1"

    assert section.first_measure == 9

    assert section.last_measure == 40
