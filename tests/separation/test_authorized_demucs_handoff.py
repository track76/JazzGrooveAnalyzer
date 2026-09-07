from hashlib import sha256
from pathlib import Path

import librosa
import numpy as np
import pytest

from jga.core.audio_file import AudioFile
from jga.engines.audio_preprocessor import AudioPreprocessor
from jga.engines.source_pulse_candidate_builder import SourcePulseCandidateBuilder
from jga.runtime.analysis_context import AnalysisContext
from jga.separation.null_separator import NullSeparator
from jga.separation.authorized_demucs import separated_identity, RULE


def test_preparation_matches_historical_rule_and_detector(monkeypatch):
    signal = np.zeros((2, 44100), dtype=np.float32)
    for frame in [5000, 15000, 30000]:
        signal[0, frame:frame+40] = 0.8
        signal[1, frame:frame+40] = 0.2
    signal[1, 15000:15040] = 0.6  # Distinguish averaging from either-channel selection.
    historical = np.mean(signal, axis=0)
    historical /= np.max(np.abs(historical))
    assert not np.array_equal(historical, signal[0] / np.max(np.abs(signal[0])))
    assert not np.array_equal(historical, signal[1] / np.max(np.abs(signal[1])))
    identity = separated_identity('05ec5862-d97c-5b49-833c-5949bc3fd950', 'authority', 'drums')
    def context():
        return AnalysisContext(audio=AudioFile(Path('synthetic.wav'), signal.copy(),
            44100, 1.0, 2, 'wav', source_identity=identity, source_identity_rule=RULE,
            asset_sha256='a'*64, transformation_provenance={'output_source_key':'drums'}))
    a, b = context(), context()
    AudioPreprocessor().process(a)
    AudioPreprocessor().process(b)
    assert np.array_equal(a.processed_audio, historical)
    assert a.processed_audio.tobytes() == b.processed_audio.tobytes()
    assert np.array_equal(np.flatnonzero(a.processed_audio), np.flatnonzero(signal[0]))
    assert np.array_equal(signal, a.audio.raw_audio)
    prep = a.audio.transformation_provenance['detector_preparation']
    assert prep == b.audio.transformation_provenance['detector_preparation']
    assert prep['input_separated_wav_sha256'] == 'a'*64
    assert prep['source_identity'] == str(identity)
    assert prep['input_frame_count'] == prep['output_frame_count'] == 44100
    assert prep['prepared_signal_sha256'] == sha256(historical.astype('<f4').tobytes()).hexdigest()
    expected = librosa.onset.onset_detect(y=historical, sr=44100, units='frames')
    original = librosa.onset.onset_detect
    calls = []
    def observe(**kwargs):
        calls.append(set(kwargs))
        return original(**kwargs)
    monkeypatch.setattr(librosa.onset, 'onset_detect', observe)
    NullSeparator().process(a)
    SourcePulseCandidateBuilder().process(a)
    assert calls == [{'y', 'sr', 'units'}]
    actual = [c.time for c in a.source_pulse_sequences[0].pulse_candidates]
    assert actual == list(librosa.frames_to_time(expected, sr=44100))
    assert a.audio_stems.stems[0].id == identity


def test_source_identity_uses_only_authoritative_tuple():
    parent = '05ec5862-d97c-5b49-833c-5949bc3fd950'
    keys = ['drums', 'bass', 'other', 'vocals', 'guitar', 'piano']
    ids = [separated_identity(parent, 'authority', key) for key in keys]
    assert len(set(ids)) == 6
    assert ids == [separated_identity(parent, 'authority', key) for key in keys]
    assert separated_identity(parent, 'different-authority', 'drums') != ids[0]
    with pytest.raises(ValueError):
        separated_identity(parent, '', 'drums')


def test_resume_requires_all_assets_and_ignores_appledouble(tmp_path):
    import json
    import soundfile as sf
    from jga.separation.authorized_demucs import AuthorizedDemucsRunner, file_sha256
    output = tmp_path/'outputs'
    output.mkdir()
    keys = ['drums', 'bass', 'other', 'vocals', 'guitar', 'piano']
    authority = tmp_path/'authority.json'
    authority.write_text(json.dumps({'separator_authority_id':'test-authority',
        'model':{'taxonomy':keys}}))
    hashes = {}
    for key in keys:
        path = output/(key+'.wav')
        sf.write(path, np.zeros((2048,2),dtype=np.float32),44100,subtype='FLOAT')
        hashes[key] = file_sha256(path)
        (output/('._'+key+'.wav')).write_bytes(b'metadata, not audio')
    parent_path = tmp_path/'parent.wav'
    sf.write(parent_path,np.zeros((2048,2),dtype=np.float32),48000)
    parent = AudioFile(parent_path,np.zeros((2,2048)),48000,2048/48000,2,'wav',
        source_identity_rule='jga-direct-input-source-identity/v1',
        asset_sha256=file_sha256(parent_path))
    runner=AuthorizedDemucsRunner(authority,file_sha256(authority),'unused',tmp_path,
        resume_checksums=hashes)
    stems=runner.separate(parent,output)
    assert len(stems)==6 and len({s.id for s in stems})==6
    assert {s.name:s.asset_sha256 for s in stems}==hashes
    hashes['bass']='0'*64
    with pytest.raises(ValueError,match='Resume output checksum mismatch'):
        runner.separate(parent,output)
