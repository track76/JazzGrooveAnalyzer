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

import librosa

from tkinter import Tk
from tkinter.filedialog import askopenfilename

from src.jga.core.audio_file import AudioFile


SUPPORTED_FORMATS = {
    ".wav",
    ".mp3",
    ".flac",
    ".aif",
    ".aiff",
    ".m4a",
}


class AudioLoader:
    """
    Carica una registrazione audio e crea
    l'oggetto AudioFile utilizzato dal JGA.
    """

    def load(self, filepath: str) -> AudioFile:

        path = Path(filepath)

        if not path.exists():
            raise FileNotFoundError(
                f"\nFile non trovato:\n{filepath}"
            )

        if path.suffix.lower() not in SUPPORTED_FORMATS:
            raise ValueError(
                f"\nFormato non supportato: {path.suffix}"
            )

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
            format=path.suffix.lower().replace(".", "")
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

    loader = AudioLoader()

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