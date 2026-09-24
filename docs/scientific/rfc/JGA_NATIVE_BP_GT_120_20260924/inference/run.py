from pathlib import Path
import sys,os,json,csv,hashlib,datetime,inspect,importlib.metadata as md
W=Path(__file__).resolve().parent;O=W/'output';blocked=[]
def guard(event,args):
 if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  p=os.path.realpath(os.fsdecode(args[0]))
  if ('/JazzGrooveAnalyzer/' in p and not p.startswith(str(W)+os.sep)) or p.startswith('/Volumes/'):
   blocked.append(p);raise PermissionError('Inference input isolation: repository/external reference reads denied')
sys.addaudithook(guard)
import numpy as np
from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.inference import predict,Model
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=json.loads((W/'INPUT_AUDIO.json').read_text());assert len(inputs)==12
assert md.version('basic-pitch')=='0.4.0';modelpath=Path(ICASSP_2022_MODEL_PATH)
provenance={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'package_version':md.version('basic-pitch'),'runtime':md.version('coremltools'),'model':str(modelpath),'model_hashes':{str(f.relative_to(modelpath)):sha(f) for f in modelpath.rglob('*') if f.is_file()},'predict_signature':str(inspect.signature(predict)),'defaults_used':True,'input_manifest_sha256':sha(W/'INPUT_AUDIO.json'),'script_sha256':sha(Path(__file__)),'guard':'Python file-open audit hook blocks repository and /Volumes reads during this process; isolated opaque audio inputs only. This is not an OS-level sandbox.'}
(O/'MODEL_PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n');model=Model(modelpath)
allnotes=[]
for c in inputs:
 audio=Path(c['audio_path']);assert sha(audio)==c['audio_sha256'];clip=c['clip_id'];output,midi,notes=predict(audio,model)
 np.savez_compressed(O/f'{clip}_MODEL_OUTPUT.npz',**output);midi.write(str(O/f'{clip}.mid'))
 native=[]
 for k,n in enumerate(notes):
  start,end,pitch,amp,bends=n
  row={'clip_id':clip,'native_note_id':f'{clip}_N{k+1:03}','native_index':k,'onset_local_s':float(start),'offset_local_s':float(end),'duration_s':float(end-start),'midi_pitch':int(pitch),'amplitude':float(amp),'pitch_bends':np.asarray(bends).tolist() if bends is not None else None}
  native.append(row);allnotes.append(row)
 (O/f'{clip}_NATIVE_NOTES.json').write_text(json.dumps(native,indent=2)+'\n');print('CLIP COMPLETE',clip,len(notes),flush=True)
(O/'ALL_NATIVE_NOTES.json').write_text(json.dumps(allnotes,indent=2)+'\n')
with (O/'ALL_NATIVE_NOTES.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['clip_id','native_note_id','native_index','onset_local_s','offset_local_s','duration_s','midi_pitch','amplitude','pitch_bends']);w.writeheader();w.writerows([{**r,'pitch_bends':json.dumps(r['pitch_bends'])} for r in allnotes])
record={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'clips':12,'native_notes':len(allnotes),'GT_read':False,'blocked_read_attempts':blocked,'files':{f.name:sha(f) for f in O.iterdir() if f.is_file()}}
(O/'TRANSCRIPTION_COMPLETE.json').write_text(json.dumps(record,indent=2)+'\n');print('ALL INFERENCE SAVED AND HASHED',len(allnotes),flush=True)
