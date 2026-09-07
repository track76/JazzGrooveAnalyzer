"""Isolated pinned backend. Model loading is offline; native Demucs DSP is reused."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import sys


def digest(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    authority_path, checksum, cache, input_file, output = sys.argv[1:]
    if digest(authority_path) != checksum:
        raise ValueError('Authority checksum mismatch')
    authority = json.loads(Path(authority_path).read_text())
    expected = authority['environment']
    if platform.python_version() != expected['python']:
        raise ValueError('Python environment mismatch')
    for name in ['demucs', 'torch', 'torchaudio', 'safetensors', 'huggingface_hub']:
        if importlib.metadata.version(name) != expected[name]:
            raise ValueError('Environment mismatch: '+name)
    for key, value in expected['thread_environment'].items():
        if os.environ.get(key) != value:
            raise ValueError('Thread configuration mismatch')
    model = authority['model']
    for item in [model['manifest'], *model['checkpoints']]:
        if digest(Path(cache)/item['file']) != item['sha256']:
            raise ValueError('Model artifact mismatch')
    import yaml
    import demucs.api
    from demucs.apply import BagOfModels
    from demucs.hf import load_safetensors_model
    from demucs.api import Separator, save_audio
    bag = yaml.safe_load((Path(cache)/model['manifest']['file']).read_text())
    models = [load_safetensors_model(Path(cache)/(sig+'.safetensors')) for sig in bag['models']]
    frozen = BagOfModels(models, bag.get('weights'), bag.get('segment'))
    frozen.eval()
    if list(frozen.sources) != model['taxonomy']:
        raise ValueError('Model output contract mismatch')
    # Same native loader functions as the HF backend, pinned to verified bytes.
    def get_model(name, repo=None):
        if name != model['name'] or repo is not None:
            raise ValueError('Unapproved model request')
        return frozen
    demucs.api.get_model = get_model
    contract = authority['execution_contract']
    if (contract['common_arguments'] != ['-d','cpu','--shifts','0','--overlap','0.25','-j','0','--float32']
        or not contract['split'] or contract['segment_override'] is not None
        or contract['clip_mode'] != 'rescale'):
        raise ValueError('Unsupported frozen configuration')
    separator = Separator(model=model['name'], device='cpu', shifts=0,
        overlap=0.25, jobs=0, split=True, segment=None, progress=False)
    _, separated = separator.separate_audio_file(Path(input_file))
    Path(output).mkdir(parents=True, exist_ok=False)
    for key, signal in separated.items():
        save_audio(signal, str(Path(output)/(key+'.wav')), samplerate=separator.samplerate,
            bitrate=320, preset=2, clip='rescale', as_float=True, bits_per_sample=16)


if __name__ == '__main__':
    main()
