"""Construct the preregistered external-tracker mono authority; no GT access."""
from hashlib import sha256
import json, struct, sys, wave
from pathlib import Path
import numpy as np

source, array_path, manifest_path = map(Path, sys.argv[1:])
with wave.open(str(source), "rb") as wav:
    if (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getnframes(), wav.getcomptype()) != (2,3,44100,1463433,"NONE"):
        raise RuntimeError("PCM_AUTHORITY_CONFLICT")
    raw = wav.readframes(wav.getnframes())
b = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 2, 3)
u = b[:,:,0].astype(np.int64) | (b[:,:,1].astype(np.int64)<<8) | (b[:,:,2].astype(np.int64)<<16)
signed = np.where(u & 0x800000, u - 0x1000000, u)
mono = ((signed[:,0] + signed[:,1]) / (2 * 8388608)).astype(np.float32)
np.save(array_path, mono, allow_pickle=False)
record={"construction":"float32((int64(L)+int64(R))/(2*8388608))","dtype":str(mono.dtype),"shape":list(mono.shape),"c_order":bool(mono.flags.c_contiguous),"raw_bytes_sha256":sha256(mono.tobytes(order="C")).hexdigest(),"minimum_binary32_hex":struct.pack(">f",float(mono.min())).hex(),"maximum_binary32_hex":struct.pack(">f",float(mono.max())).hex(),"sample_rate_hz":44100,"sample_zero":"source sample zero","source_sha256":sha256(source.read_bytes()).hexdigest(),"normalized":False,"trimmed":False,"shifted":False,"resampled":False,"ground_truth_accessed":False,"numpy":np.__version__}
record["scientific_fingerprint"]=sha256(json.dumps(record,sort_keys=True,separators=(",",":")).encode()).hexdigest()
manifest_path.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
print(json.dumps(record,sort_keys=True))
