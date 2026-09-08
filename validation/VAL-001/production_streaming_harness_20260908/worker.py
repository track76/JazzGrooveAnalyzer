import time
START=time.perf_counter_ns()
import sys,json,resource,ctypes,importlib.util,hashlib,os
from pathlib import Path
from fractions import Fraction as Q
import flint
from streaming import canonical,digest,sha,array_rows,LRU,Writer
P=Path(__file__).parent;fixture,mode,where=sys.argv[1:];dest=Path(where);dest.mkdir(exist_ok=False)
freeze=json.loads((P/'source_freeze.json').read_bytes())
for n,h in freeze['files'].items():assert sha(P/n)==h
bp=P.parent/'certified_query_environment_20260907/binding.json';assert sha(bp)==freeze['binding_sha256']
b=json.loads(bp.read_bytes());fr=Path(flint.__file__).parent
assert sha(Path(sys.executable).resolve())==b['binding']['python']['binary_sha256']
for n,h in b['binding']['installed_binary_hashes'].items():assert sha(fr/n)==h
flint.ctx.prec=128;flint.ctx.threads=1
lib=ctypes.CDLL(str(fr/'.dylibs/libflint.24.0.dylib'));lib.flint_get_num_threads.restype=ctypes.c_int;assert lib.flint_get_num_threads()==1
pr=P.parent/'preregistrations/H-VAL001-PRODUCTION-STREAMING-HARNESS-01.md';assert sha(pr)==freeze['preregistration_sha256']
def load(name,path,expected):
 assert sha(path)==expected
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
ref=load('numeric_reference',P.parent/'certified_sparse_query_20260907/evaluator.py',freeze['numeric_sha256'])
module=load('cached_reference',P.parent/'cached_streaming_equivalence_20260908/optimized.py',freeze['optimized_sha256'])
engine=module.Optimized((sha(bp),128,freeze['optimized_sha256'],freeze['preregistration_sha256']),ref)
if mode=='production':engine.exp=LRU()
q=lambda v:Q(*map(int,v))
rat=lambda v:[str(v.numerator),str(v.denominator)]
upstream=Path(freeze['external_E_reference']);assert sha(upstream)==freeze['external_E_sha256']
def records():
 if fixture=='E':
  yield from array_rows(upstream)
 elif fixture=='C':
  pop={'population':'C','source':'synthetic-source:C','asset':'synthetic-construction:C','events':[
   {'id':'C.a','pulse_id':'C.a.pulse','fields':{'t':{'ratio':['0','1'],'bits':'0000000000000000','hex':'0x0.0p+0','json_token':'0.0'},'s':{'ratio':['1','1'],'bits':'3ff0000000000000','hex':'0x1.0000000000000p+0','json_token':'1.0'}}},
   {'id':'C.b','pulse_id':'C.b.pulse','fields':{'t':{'ratio':['1','1'],'bits':'3ff0000000000000','hex':'0x1.0000000000000p+0','json_token':'1.0'},'s':{'ratio':['1','2'],'bits':'3fe0000000000000','hex':'0x1.0000000000000p-1','json_token':'0.5'}}}], 'scope':['0','2'],'asset_bounds':['0','2']}
  w={'population':'C','u':rat(Q(0)),'L':rat(Q(2)),'center_ids':['C.a'],'scale_pairs':[],
   'membership':{'contained':['C.a','C.b'],'boundary':['C.b'],'positive':['C.a']},'requested':[rat(Q(-1)),rat(Q(1))],'asset_clipped':[rat(Q(0)),rat(Q(1))],'available':[rat(Q(0)),rat(Q(1))],
   'asset_unavailable':[{'ends':[rat(Q(-1)),rat(Q(0))],'closed':[True,False]}],'unavailable':[{'ends':[rat(Q(-1)),rat(Q(0))],'closed':[True,False]}],'asset_truncated':True,'scope_truncated':False}
  overlap={'generating_ids':['C.a','C.b'],'intersections':w['membership'],'pair_intersections':[]}
  for j in range(1,8194):
   t=Q(j,8192)
   yield {'query_id':['C',rat(Q(0)),rat(Q(2)),rat(t)],'input_provenance':pop,'window_provenance':w,
    'period_provenance':{'population':'C','T':rat(t),'f':rat(1/t),'origin':'CONTROLLED_NUMERICAL_PROBE','pairs':[],'pair_times':[],'construction_input_ids':['C.a','C.b'],'coincident_pairs':[]},
    'generation_evaluation_overlap':{'period':overlap,'scale':overlap},'scientific_status':'RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED'}
 else:
  # E was independently compared before S; only bounded templates are loaded.
  ep=dest.parent/'E'/'templates.json'
  templates=list(array_rows(ep));assert len(templates)==21
  for k in range(4080384):yield {'transport_ordinal':str(k),'template_index':str(k%21),'logical_record':templates[k%21]}

writer=Writer(dest) if mode=='production' else None
rf=(dest/'logical.jsonl').open('wb',buffering=65536) if mode=='reference' else None
# E templates are bounded auxiliary output for S; never a general result list.
tf=(dest/'templates.json').open('wb',buffering=65536) if fixture=='E' else None
if tf:tf.write(b'[')
hh=hashlib.sha256();count=0;current=None;high={'parsed':0,'hann':0,'amplitudes':0,'exp':0};windows=0;evalcalls=0
for record in records():
 if fixture!='S':
  pid,u,L,t=record['query_id'];uq,Lq,tq=map(q,(u,L,t));window=(pid,uq,Lq)
  if window!=current:
   current=window;windows+=1
   if mode=='production':engine.hann.clear();engine.amp.clear()
  pop=record['input_provenance'];measure=[{'id':e['id'],'t':str(q(e['fields']['t']['ratio'])),'s':str(q(e['fields']['s']['ratio']))} for e in pop['events']]
  numeric=engine.evaluate(pid,measure,{'u':str(uq),'L':str(Lq),'f':str(1/tq)});evalcalls+=1
  x,y=ref.bounds(numeric['real']),ref.bounds(numeric['imag']);numeric['zero_containment']=x[0]<=0<=x[1] and y[0]<=0<=y[1]
  record['numeric']=numeric
  for name,store in [('parsed',engine.parsed),('hann',engine.hann),('amplitudes',engine.amp),('exp',engine.exp)]:high[name]=max(high[name],len(store))
  if mode=='production':assert high['parsed']<=63 and high['hann']<=63 and high['amplitudes']<=63 and high['exp']<=4096
 payload=canonical(record);hh.update(payload+b'\n')
 if rf:rf.write(payload+b'\n')
 else:writer.row(record)
 if tf:
  if count:tf.write(b',')
  tf.write(payload)
 count+=1
if rf:rf.close()
if tf:tf.write(b']');tf.close()
if writer:writer.finish()
files={};sidecar_bytes=0;filecount=0;allocated=0;shard_bytes=0;canonical_count=0
for entry in os.scandir(dest):
 if not entry.is_file():continue
 st=entry.stat();filecount+=1;allocated+=st.st_blocks*512
 if entry.name.startswith('._'):sidecar_bytes+=st.st_size
 else:
  canonical_count+=1
  if entry.name.startswith('shard-'):shard_bytes+=st.st_size
  else:files[entry.name]=st.st_size
metrics={'fixture':fixture,'path':mode,'rows':str(count),'logical_fingerprint':hh.hexdigest(),'evaluator_calls':str(evalcalls),'arithmetic':{k:str(v) for k,v in engine.counts.items()},'cache_highwater':{k:str(v) for k,v in high.items()},'evictions':str(engine.exp.evictions if isinstance(engine.exp,LRU) else 0),'window_builds':str(windows),'buffered_result_records':'1','buffered_index_entries':'1' if writer else '0','templates':'21' if fixture=='S' else '0','canonical_files_bytes':{k:str(v) for k,v in files.items()},'canonical_bytes':str(sum(files.values())+shard_bytes),'canonical_file_count':str(canonical_count),'shard_bytes':str(shard_bytes),'shards':str(writer.nshards if writer else 0),'input_catalogue_rows':str(len(writer.inputs) if writer else 0),'period_catalogue_rows':str(len(writer.periods) if writer else 0),'max_compact_record_bytes':str(writer.maxrow if writer else 0)}
(dest/'metrics.json').write_bytes(canonical(metrics))
perf={'wall_ns':str(time.perf_counter_ns()-START),'peak_rss_bytes':str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),'filesystem_file_count_before_metrics':str(filecount),'sidecar_bytes':str(sidecar_bytes),'allocated_bytes':str(allocated),'precision':'128','threads':'1'}
(dest/'performance.json').write_bytes(canonical(perf));print(fixture,mode,count,flush=True)
