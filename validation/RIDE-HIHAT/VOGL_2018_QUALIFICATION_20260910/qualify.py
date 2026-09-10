"""One supplied CRNN_8 MDB evaluation; no training or parameter search."""
import collections
import collections.abc
import hashlib
import importlib.metadata
import json
import platform
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('/Volumes/SSD Track/JGA/experiments/RIDE-HIHAT-VOGL-2018')
PACKAGE = ROOT / 'package/madmom-0.16.dev0'
MDB = Path('/Volumes/SSD Track/JGA/datasets/RIDE-HIHAT-EXTERNAL/MDB-original-b29e2d63')
# Python 3.11 moved the abstract class; this does not modify model arithmetic.
collections.MutableSequence = collections.abc.MutableSequence
sys.path.insert(0, str(PACKAGE))
import numpy as np
from madmom.features.drums import CRNNDrumProcessor, DrumPeakPickingProcessor
from madmom.evaluation.onsets import onset_evaluation
from madmom.models import DRUMS_CRNN_8

SETTINGS = dict(model='CRNN_8', threshold=0.15, smooth=0, pre_avg=0.1,
                post_avg=0.01, pre_max=0.02, post_max=0.01, combine=0.02,
                delay=0, online=False, fps=100)
WINDOW = 0.025

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()

def write(path, obj):
    path.write_text(json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + '\n')

def matches(pred, ann):
    """Independent index traversal for subtype provenance; checked against supplier."""
    i = j = 0
    pairs, fp, fn = [], [], []
    while i < len(pred) and j < len(ann):
        d = pred[i] - ann[j]
        if abs(d) <= WINDOW:
            pairs.append((i, j)); i += 1; j += 1
        elif d < 0:
            fp.append(i); i += 1
        else:
            fn.append(j); j += 1
    fp.extend(range(i, len(pred))); fn.extend(range(j, len(ann)))
    official = onset_evaluation(pred, ann, window=WINDOW)
    assert (len(pairs), len(fp), len(fn)) == (len(official[0]), len(official[1]), len(official[3]))
    return pairs, fp, fn

def metrics(tp, fp, fn):
    return dict(tp=tp, fp=fp, fn=fn, gt=tp+fn, predictions=tp+fp,
                precision=tp/(tp+fp) if tp+fp else None,
                recall=tp/(tp+fn) if tp+fn else None,
                f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None)

def check():
    assert len(DRUMS_CRNN_8) == 5
    for pred, ann, expected in [([], [], (0,0,0)), ([1], [1,1], (1,0,1)),
            ([1,1], [1], (1,1,0)), ([0.025], [0], (1,0,0)),
            ([0.0250001], [0], (0,1,1)), ([1,2], [1,2], (2,0,0))]:
        result = matches(np.array(pred, dtype=float), np.array(ann, dtype=float))
        assert tuple(map(len, result)) == expected
    model = CRNNDrumProcessor(model='CRNN_8')
    # Synthetic silence tests the supplied audio-to-output chain, without MDB.
    act = model(np.zeros(44100, dtype=np.float32))
    assert act.ndim == 2 and act.shape[1] == 8 and np.isfinite(act).all()
    peaks = DrumPeakPickingProcessor(**SETTINGS)(act)
    assert peaks.size == 0 or (peaks.ndim == 2 and peaks.shape[1] == 2)
    print('SYNTHETIC_CHECK_OK', act.shape, flush=True)

def run():
    out = ROOT / 'execution'
    if out.exists():
        raise RuntimeError('Refusing to overwrite or repeat execution')
    admission = MDB / 'authority/admission_manifest.json'
    assert sha(admission) == '3c66085a119419d21d8268b8aac37f8bc16cb613c399af825d7b248c87d92421'
    manifest = json.loads(admission.read_text())
    for record in manifest['files']:
        p = MDB / record['path']
        assert p.stat().st_size == record['bytes'] and sha(p) == record['sha256'], p
    audio = sorted(MDB / r['path'] for r in manifest['files']
                   if '/audio/drum_only/' in r['path'] and r['path'].endswith('.wav'))
    assert len(audio) == 23
    assert len(DRUMS_CRNN_8) == 5
    # Freeze precedes any scientific prediction or annotation parsing.
    binding = dict(created_utc=datetime.now(timezone.utc).isoformat(), settings=SETTINGS,
        window_seconds=WINDOW, model='supplied five-member CRNN_8 ensemble',
        upstream_MDB_training_exposure=True, admission_sha256=sha(admission),
        archive_sha256=sha(ROOT / 'downloads/madmom-drums-dafx18.tar.gz'),
        protocol_sha256=sha(Path(__file__).with_name('PROTOCOL.md')), runner_sha256=sha(__file__),
        python=sys.version, platform=platform.platform(),
        dependencies={k:importlib.metadata.version(k) for k in ['numpy','scipy','Cython','setuptools','mido']},
        package_files={str(p.relative_to(PACKAGE)):sha(p) for p in sorted(PACKAGE.rglob('*'))
            if p.is_file() and not p.name.startswith('._') and
            p.suffix in ('.py','.pyx','.so','.pkl') and 'build' not in p.parts},
        weights={Path(p).name:sha(p) for p in DRUMS_CRNN_8},
        inputs={str(p.relative_to(MDB)):sha(p) for p in audio})
    out.mkdir()
    write(out / 'freeze.json', binding)
    print('FROZEN', sha(out / 'freeze.json'), flush=True)
    proc = CRNNDrumProcessor(model='CRNN_8')
    for p in audio:
        act = proc(str(p))
        assert act.ndim == 2 and act.shape[1] == 8 and np.isfinite(act).all()
        np.save(out / (p.stem + '.activations.npy'), act, allow_pickle=False)
        peaks = DrumPeakPickingProcessor(**SETTINGS)(act)
        write(out / (p.stem + '.predictions.json'), peaks.tolist())
        print('INFERRED', p.stem, flush=True)
    write(out / 'predictions_frozen.json', {p.name:sha(p) for p in sorted(out.glob('*.predictions.json'))})
    tracks = []
    for p in audio:
        annpath = MDB / 'original/MDB Drums/annotations/subclass' / (p.stem.removesuffix('_Drum') + '_subclass.txt')
        events = sorted((float(row.split()[0]), row.split()[1]) for row in annpath.read_text().splitlines() if row.strip())
        preds = np.array(json.loads((out / (p.stem + '.predictions.json')).read_text())).reshape(-1,2)
        track = dict(track=p.stem, scores={}, subtype_hits={}, ride_fp_coincidences={})
        for key, pitch, labels in [('Ride',51,{'RDC'}), ('HiHat',42,{'CHH','OHH','PHH'}),
                                    ('BroadBell_RDB_conditional',53,{'RDB'})]:
            a = [(t,l) for t,l in events if l in labels]
            d = np.sort(preds[preds[:,1] == pitch,0])
            pairs, fp, fn = matches(d, np.array([t for t,l in a]))
            track['scores'][key] = metrics(len(pairs),len(fp),len(fn))
            track['subtype_hits'][key] = {l:dict(gt=sum(x[1]==l for x in a),
                matched=sum(a[j][1]==l for i,j in pairs)) for l in sorted(labels)}
            if key == 'Ride':
                for i in fp:
                    labels_near = sorted({l for t,l in events if abs(t-d[i]) <= WINDOW})
                    category = '|'.join(labels_near) if labels_near else 'UNMATCHED'
                    track['ride_fp_coincidences'][category] = track['ride_fp_coincidences'].get(category,0)+1
        tracks.append(track)
    aggregate = {}
    for key in tracks[0]['scores']:
        aggregate[key] = metrics(*(sum(t['scores'][key][x] for t in tracks) for x in ['tp','fp','fn']))
    result = dict(aggregate=aggregate, tracks=tracks, upstream_MDB_training_exposure=True,
        independent_transfer_claim=False, freeze_sha256=sha(out/'freeze.json'))
    write(out/'result.json',result)
    write(out/'SHA256.json',{p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file()})
    print(json.dumps(aggregate,sort_keys=True),flush=True)

if __name__ == '__main__':
    if sys.argv[1:] == ['check']:
        check()
    elif sys.argv[1:] == ['run']:
        run()
    else:
        raise SystemExit('Use check or run')
