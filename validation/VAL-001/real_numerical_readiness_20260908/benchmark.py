"""Synthetic resource probe only; imports immutable validated numerical/streaming paths."""
import sys,time,json,hashlib,struct,resource,ctypes,importlib.util,os
from pathlib import Path
from fractions import Fraction as Q
START=time.perf_counter_ns()
P=Path(__file__).resolve().parent;V=P.parent;H=V/'production_streaming_harness_20260908'
sys.path.insert(0,str(H))
from streaming import canonical,sha,LRU,Writer
import flint
freeze=json.loads((H/'source_freeze.json').read_bytes())
for n,h in freeze['files'].items():assert sha(H/n)==h
bp=V/'certified_query_environment_20260907/binding.json';assert sha(bp)==freeze['binding_sha256']
b=json.loads(bp.read_bytes());fr=Path(flint.__file__).parent
assert sha(Path(sys.executable).resolve())==b['binding']['python']['binary_sha256']
for n,h in b['binding']['installed_binary_hashes'].items():assert sha(fr/n)==h
flint.ctx.prec=128;flint.ctx.threads=1
lib=ctypes.CDLL(str(fr/'.dylibs/libflint.24.0.dylib'));lib.flint_get_num_threads.restype=ctypes.c_int;assert lib.flint_get_num_threads()==1
def load(name,path,h):
 assert sha(path)==h
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
ref=load('reference',V/'certified_sparse_query_20260907/evaluator.py',freeze['numeric_sha256'])
opt=load('optimized',V/'cached_streaming_equivalence_20260908/optimized.py',freeze['optimized_sha256'])
e=opt.Optimized((sha(bp),128,freeze['optimized_sha256'],freeze['preregistration_sha256']),ref);e.exp=LRU()
def field(x):
 token=json.dumps(x);y=float(token);assert struct.pack('>d',x)==struct.pack('>d',y)
 return {'json_token':token,'bits':struct.pack('>d',y).hex(),'hex':y.hex(),'ratio':[str(z) for z in y.as_integer_ratio()]}
def rat(x):return [str(x.numerator),str(x.denominator)]
events=[{'id':f'synthetic-observation-00000000-0000-0000-0000-{i:012d}','pulse_id':f'synthetic-pulse-00000000-0000-0000-0000-{i:012d}','fields':{'t':field(i/10),'s':field((i+1)/67)}} for i in range(63)]
ts=[Q(*map(int,x['fields']['t']['ratio'])) for x in events]
pop={'population':'SYNTHETIC_RESOURCE_63','source':'synthetic-source:resource-63','asset':'synthetic-construction:resource-63','events':events,'scope':['0','7'],'asset_bounds':['0','7']}
measure=[{'id':x['id'],'t':str(t),'s':str(Q(*map(int,x['fields']['s']['ratio'])))} for x,t in zip(events,ts)]
dest=Path(sys.argv[1]);dest.mkdir(exist_ok=False);w=Writer(dest)
start=time.perf_counter_ns();eval_ns=0;counts=[];rows=0;max_payload=0;high={k:0 for k in ('parsed','hann','amp','exp')};logical_bytes=0
for last in (31,62):
 L=2*ts[last];e.hann.clear();e.amp.clear()
 contained=[x['id'] for x,t in zip(events,ts) if t<=L/2];boundary=[events[last]['id']];positive=contained[:-1]
 membership={'contained':contained,'boundary':boundary,'positive':positive}
 win={'population':pop['population'],'u':['0','1'],'L':rat(L),'center_ids':[events[0]['id']],'scale_pairs':[[events[0]['id'],events[last]['id']]],'membership':membership,'requested':[rat(-L/2),rat(L/2)],'asset_clipped':[['0','1'],rat(L/2)],'available':[['0','1'],rat(L/2)],'asset_unavailable':[{'ends':[rat(-L/2),['0','1']],'closed':[True,False]}],'unavailable':[{'ends':[rat(-L/2),['0','1']],'closed':[True,False]}],'asset_truncated':True,'scope_truncated':False}
 before=dict(e.counts);section=time.perf_counter_ns()
 for j in range(1,1057):
  f=Q(j,1057);T=1/f
  q={'u':'0','L':str(L),'f':str(f)}
  tick=time.perf_counter_ns();numeric=e.evaluate(pop['population'],measure,q);eval_ns+=time.perf_counter_ns()-tick
  x,y=ref.bounds(numeric['real']),ref.bounds(numeric['imag']);numeric['zero_containment']=x[0]<=0<=x[1] and y[0]<=0<=y[1]
  overlap={'generating_ids':[z['id'] for z in events],'intersections':membership,'pair_intersections':[]}
  row={'query_id':[pop['population'],['0','1'],rat(L),rat(T)],'input_provenance':pop,'window_provenance':win,'period_provenance':{'population':pop['population'],'T':rat(T),'f':rat(f),'origin':'CONTROLLED_RESOURCE_PROBE','pairs':[],'pair_times':[],'construction_input_ids':[z['id'] for z in events],'coincident_pairs':[]},'generation_evaluation_overlap':{'period':overlap,'scale':overlap},'scientific_status':'RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED','numeric':numeric}
  payload=canonical(row);logical_bytes+=len(payload)+1;max_payload=max(max_payload,len(payload));w.row(row);rows+=1
  for k in high:high[k]=max(high[k],len(getattr(e,k)))
 counts.append({'terms':last+1,'queries':1056,'wall_ns':time.perf_counter_ns()-section,'arithmetic':{k:e.counts[k]-before[k] for k in before}})
w.finish();finish=time.perf_counter_ns();sizes={x.name:x.stat().st_size for x in dest.iterdir() if x.is_file() and not x.name.startswith('._')}
result={'synthetic_only':True,'events':63,'queries':rows,'sections':counts,'eval_ns':eval_ns,'work_wall_ns':finish-start,'startup_and_work_ns':finish-START,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'arithmetic':e.counts,'cache_highwater':high,'evictions':e.exp.evictions,'canonical_files_bytes':sizes,'canonical_bytes':sum(sizes.values()),'logical_bytes':logical_bytes,'max_logical_record_bytes':max_payload,'max_compact_record_bytes':w.maxrow,'shards':w.nshards,'free_external_bytes':os.statvfs(dest).f_bavail*os.statvfs(dest).f_frsize,'source_sha256':sha(Path(__file__)),'environment_binding_sha256':sha(bp),'external_output':str(dest),'scientific_inference':'NONE'}
(P/'measurement.json').write_bytes(canonical(result));print(json.dumps(result,sort_keys=True))
