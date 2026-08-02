from pathlib import Path

from jga.separation.demucs_runner import (
    DemucsRunner,
)


def test_demucs_runner_builds_expected_command():

    calls = []

    def fake_executor(command, check):
        calls.append(
            {
                "command": command,
                "check": check,
            }
        )

    runner = DemucsRunner(
        executor=fake_executor,
        executable="/fake/bin/demucs",
    )

    result = runner.separate(
        input_file=Path("test_audio.mp3"),
        output_directory=Path("output"),
    )

    assert len(calls) == 1

    assert calls[0]["command"] == [
        "/fake/bin/demucs",
        "-n",
        "htdemucs",
        "-d",
        "mps",
        "-o",
        "output",
        "test_audio.mp3",
    ]

    assert calls[0]["check"] is True

    assert result == (
        Path("output")
        / "htdemucs"
        / "test_audio"
    )
