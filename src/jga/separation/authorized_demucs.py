"""Explicit, checksum-bound Demucs execution and AD-041 output provenance."""
import json
import os
from pathlib import Path
import subprocess
from uuid import NAMESPACE_URL, uuid5

import librosa

from jga.core.audio_file import AudioFile
from jga.core.audio_stem import AudioStem

RULE = "jga-separated-source-identity/v1"


def file_sha256(path):
    with Path(path).open("rb") as stream:
        return __import__('hashlib').file_digest(stream, "sha256").hexdigest()


def separated_identity(parent, authority, key):
    from uuid import UUID
    value = {"rule": RULE, "parent_source_identity": str(UUID(str(parent))),
             "separator_authority_id": authority, "output_source_key": key}
    if not authority or not key:
        raise ValueError("Missing separated identity authority")
    return uuid5(NAMESPACE_URL, json.dumps(value, sort_keys=True, separators=(",", ":")))


class AuthorizedDemucsRunner:
    """Run the frozen backend in its own environment; retain every original WAV."""

    def __init__(self, authority_path, authority_sha256, python, model_cache, *, resume_checksums=None):
        self.authority_path = Path(authority_path).resolve()
        if file_sha256(self.authority_path) != authority_sha256:
            raise ValueError("Separator authority checksum mismatch")
        self.authority_sha256 = authority_sha256
        self.authority = json.loads(self.authority_path.read_text())
        self.python = str(python)
        self.model_cache = Path(model_cache)
        self.resume_checksums = resume_checksums

    def separate(self, audio, output_directory):
        if audio.source_identity_rule != "jga-direct-input-source-identity/v1":
            raise ValueError("AD041 requires an authorized parent")
        if file_sha256(audio.path) != audio.asset_sha256:
            raise ValueError("Parent asset changed")
        output_directory = Path(output_directory).resolve()
        if self.resume_checksums is not None:
            expected_keys = set(self.authority['model']['taxonomy'])
            if set(self.resume_checksums) != expected_keys:
                raise ValueError('Incomplete resume asset authority')
            for key, checksum in self.resume_checksums.items():
                if file_sha256(output_directory/(key+'.wav')) != checksum:
                    raise ValueError('Resume output checksum mismatch')
        else:
            if output_directory.exists():
                raise FileExistsError(output_directory)
            env = dict(os.environ)
            env.update(self.authority["environment"]["thread_environment"])
            env.update({"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"})
            subprocess.run([
                self.python, str(Path(__file__).with_name("demucs_authorized_backend.py")),
                str(self.authority_path), self.authority_sha256, str(self.model_cache),
                str(audio.path), str(output_directory),
            ], env=env, check=True)
        expected = self.authority["model"]["taxonomy"]
        if {p.name for p in output_directory.glob('*.wav') if not p.name.startswith('._')} != {k+'.wav' for k in expected}:
            raise ValueError("Separator output contract mismatch")
        stems = []
        for key in expected:
            path = output_directory / (key + '.wav')
            digest = file_sha256(path)
            signal, sr = librosa.load(path, sr=None, mono=False)
            if sr != 44100 or signal.ndim != 2 or signal.shape[0] != 2:
                raise ValueError("Unexpected native separated audio representation")
            identity = separated_identity(audio.source_identity,
                self.authority['separator_authority_id'], key)
            lineage = {
                'parent_source_identity': str(audio.source_identity),
                'parent_source_authority_id': audio.source_authority_id,
                'parent_source_instance_key': audio.source_instance_key,
                'parent_asset_sha256': audio.asset_sha256,
                'separator_authority_id': self.authority['separator_authority_id'],
                'separator_authority_sha256': self.authority_sha256,
                'output_source_key': key, 'output_asset_sha256': digest,
                'source_identity_rule': RULE,
            }
            stems.append(AudioStem(key, signal, sr, source='DemucsSeparator',
                id=identity, source_identity_rule=RULE, asset_sha256=digest,
                asset_path=str(path), transformation_provenance=lineage))
        return tuple(stems)


def output_audio(stem):
    """Retain source/asset authority when entering the per-file preparation path."""
    if stem.source_identity_rule != RULE or not stem.asset_path:
        raise ValueError('Unbound separated output')
    return AudioFile(Path(stem.asset_path), stem.signal, stem.sample_rate,
        stem.signal.shape[-1] / stem.sample_rate, stem.signal.shape[0], 'wav',
        source_identity=stem.id, source_identity_rule=RULE,
        asset_sha256=stem.asset_sha256,
        transformation_provenance=dict(stem.transformation_provenance))
