import pytest

from jga.translation.tau8_translator import Tau8Translator


def test_tau8_translator_can_be_instantiated():

    translator = Tau8Translator()

    assert translator is not None


def test_tau8_requires_implementation():

    translator = Tau8Translator()

    with pytest.raises(NotImplementedError):
        translator.translate(None)
