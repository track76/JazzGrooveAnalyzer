"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    demucs_runner.py

Description:
    Runtime wrapper around the external Demucs backend.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from pathlib import Path
import subprocess


class DemucsRunner:
    """
    Executes Demucs separation backend.

    This class does not create JGA domain objects.
    It only manages backend execution and outputs.
    """

    def __init__(
        self,
        executor=None,
        executable="demucs",
    ):
        self.executor = executor or subprocess.run
        self.executable = executable

    def separate(
        self,
        input_file: Path,
        output_directory: Path,
        device: str = "mps",
    ) -> Path:
        """
        Execute Demucs and return output directory.
        """

        command = [
            self.executable,
            "-n",
            "htdemucs",
            "-d",
            device,
            "-o",
            str(output_directory),
            str(input_file),
        ]

        self.executor(
            command,
            check=True,
        )

        return (
            output_directory
            / "htdemucs"
            / input_file.stem
        )
