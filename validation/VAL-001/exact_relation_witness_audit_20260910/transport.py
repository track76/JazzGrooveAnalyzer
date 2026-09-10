"""Byte transport only. No event, rational, witness, or outcome logic."""
import hashlib
import json
from pathlib import Path


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def verify_sha(path, expected):
    actual = sha(path)
    if actual != expected:
        raise ValueError('Authority hash mismatch: ' + str(path))
    return actual


def canonical(value):
    def convert(x):
        if isinstance(x, bool) or x is None or isinstance(x, str):
            return x
        if isinstance(x, int):
            return str(x)
        if isinstance(x, (list, tuple)):
            return [convert(v) for v in x]
        if isinstance(x, dict) and all(isinstance(k, str) for k in x):
            return {k: convert(v) for k, v in x.items()}
        raise TypeError('Noncanonical type: ' + type(x).__name__)
    return json.dumps(convert(value), sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


def parse(data):
    def object_pairs(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError('Duplicate JSON key')
            out[key] = value
        return out
    def forbidden(value):
        raise ValueError('Nonfinite JSON: ' + value)
    return json.loads(data, object_pairs_hook=object_pairs, parse_constant=forbidden)


def read(path):
    return parse(Path(path).read_bytes())


def rows(path):
    with Path(path).open('rb') as handle:
        for line in handle:
            yield parse(line)


def write(path, value):
    with Path(path).open('xb') as handle:
        handle.write(canonical(value) + b'\n')


def write_rows(path, values):
    with Path(path).open('xb') as handle:
        for value in values:
            handle.write(canonical(value) + b'\n')


def content_id(body):
    return hashlib.sha256(canonical(body)).hexdigest()


def files_index(directory, names):
    return {name: {'sha256': sha(Path(directory) / name),
                   'bytes': str((Path(directory) / name).stat().st_size)}
            for name in sorted(names)}
