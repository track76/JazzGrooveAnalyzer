#!/usr/bin/env python3
from hashlib import sha256
import json
from pathlib import Path
import struct
import soundfile as sf

HERE = Path(__file__).resolve().parent

def canonical(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")

def digest(path):
    h = sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def chunks(path):
    raw = Path(path).read_bytes()
    result, offset = [], 12
    while offset < len(raw):
        chunk_id = raw[offset:offset + 4].decode("ascii")
        size = struct.unpack("<I", raw[offset + 4:offset + 8])[0]
        result.append((chunk_id, size, raw[offset + 8:offset + 8 + size]))
        offset += 8 + size + size % 2
    return result

result = json.loads((HERE / "result.json").read_text())
expected = result.pop("result_fingerprint")
assert sha256(canonical(result)).hexdigest() == expected
result["result_fingerprint"] = expected
payloads = []
for run in result["runs"].values():
    path = Path(run["output_path"])
    assert digest(path) == run["whole_file_sha256"]
    audio, rate = sf.read(path, dtype="float32", always_2d=True)
    assert sha256(audio.tobytes(order="C")).hexdigest() == run["decoded_samples_sha256"]
    assert (rate, audio.shape) == (44100, (10944947, 2))
    inventory = chunks(path)
    assert [item[0] for item in inventory] == ["fmt ", "fact", "PAD ", "data"]
    assert [item[1] for item in inventory] == [16, 4, 24, 87559576]
    assert inventory[2][2] == bytes(24)
    payloads.append(path.read_bytes())
assert payloads[0] == payloads[1]
assert result["byte_identical_replay"]
assert not result["scientific_sample_population_changed"]
assert not result["phase3_transform_changed"]
assert not result["jga_changed"]
assert not result["production_code_changed"]
print(json.dumps({"byte_identical_replay": "YES", "result_fingerprint": expected, "status": "PASS"}, sort_keys=True))
