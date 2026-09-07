"""
=========================================================
Jazz Groove Analyzer (JGA)

Module:
    Audio Loader

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from pathlib import Path
from hashlib import sha256
import json
from uuid import NAMESPACE_URL, uuid5

import librosa

from tkinter import Tk
from tkinter.filedialog import askopenfilename

from jga.core.audio_file import AudioFile


SUPPORTED_FORMATS = {
    ".wav",
    ".mp3",
    ".flac",
    ".aif",
    ".aiff",
    ".m4a",
}


class FileAudioSource:
    """
    Carica una registrazione audio e crea
    l'oggetto AudioFile utilizzato dal JGA.
    """

    def load(
        self, filepath: str, *, source_authority_id: str | None = None,
        source_instance_key: str | None = None,
        expected_sha256: str | None = None,
    ) -> AudioFile:

        identity = {}
        if source_authority_id is not None or source_instance_key is not None:
            if any(not isinstance(value, str) or not value.strip()
                   for value in (source_authority_id, source_instance_key)):
                raise ValueError("AD041_MISSING_DIRECT_INPUT_AUTHORITY")
            if (not isinstance(expected_sha256, str) or len(expected_sha256) != 64
                    or any(c not in "0123456789abcdef" for c in expected_sha256)):
                raise ValueError("AD041_MISSING_ASSET_BINDING")
            rule = "jga-direct-input-source-identity/v1"
            identity = dict(
                source_identity=uuid5(NAMESPACE_URL, json.dumps({
                    "rule": rule, "source_authority_id": source_authority_id,
                    "source_instance_key": source_instance_key,
                }, sort_keys=True, separators=(",", ":"))),
                source_authority_id=source_authority_id,
                source_instance_key=source_instance_key,
                source_identity_rule=rule,
            )

        path = Path(filepath)

        if not path.exists():
            raise FileNotFoundError(
                f"\nFile non trovato:\n{filepath}"
            )

        if path.suffix.lower() not in SUPPORTED_FORMATS:
            raise ValueError(
                f"\nFormato non supportato: {path.suffix}"
            )

        with path.open("rb") as stream:
            digest = sha256()
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        asset_sha256 = digest.hexdigest()
        if expected_sha256 is not None and expected_sha256 != asset_sha256:
            raise ValueError("AD041_ASSET_BINDING_MISMATCH")

        raw_audio, sample_rate = librosa.load(
            path,
            sr=None,
            mono=False
        )

        if raw_audio.ndim == 1:
            channels = 1
            duration = len(raw_audio) / sample_rate
        else:
            channels = raw_audio.shape[0]
            duration = raw_audio.shape[1] / sample_rate

        return AudioFile(
            path=path,
            raw_audio=raw_audio,
            sample_rate=sample_rate,
            duration=duration,
            channels=channels,
            format=path.suffix.lower().replace(".", ""),
            asset_sha256=asset_sha256,
            **identity,
        )


def main():

    print(">>> MAIN AVVIATO <<<")

    print("\n==========================================")
    print("      Jazz Groove Analyzer (JGA)")
    print("==========================================\n")

    root = Tk()
    root.withdraw()

    filepath = askopenfilename(
        title="Seleziona una registrazione audio",
        filetypes=[
            (
                "Audio",
                "*.wav *.mp3 *.flac *.aif *.aiff *.m4a"
            ),
            ("Tutti i file", "*.*")
        ]
    )

    if not filepath:
        print("Nessun file selezionato.")
        return

    loader = FileAudioSource()

    audio = loader.load(filepath)

    print("\n========== AUDIO FILE ==========")
    print(f"Nome file   : {audio.filename}")
    print(f"Formato     : {audio.format}")
    print(f"Canali      : {audio.channels}")
    print(f"Sample Rate : {audio.sample_rate} Hz")
    print(f"Durata      : {audio.duration:.2f} s")
    print("================================")


if __name__ == "__main__":
    main()
