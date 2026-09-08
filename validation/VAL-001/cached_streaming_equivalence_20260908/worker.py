import sys,time,resource,ctypes,importlib.util,inspect
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
import json,flint
from common import canonical,digest,sha,tagged,rational
from optimized import Optimized
start=time.perf_counter_ns();P=Path(__file__).parent
mode=sys.argv[1];dest=Path(sys.argv[2]);dest.mkdir(exist_ok=False)
freeze=json.loads((P/'source_freeze.json').read_bytes())
for name,h in freeze['files'].items():assert sha(P/name)==h
bp=P.parent/'certified_query_environment_20260907/binding.json';assert sha(bp)==freeze['binding_sha256']
binding=json.loads(bp.read_bytes());root=Path(flint.__file__).parent
assert sha(Path(sys.executable).resolve())==binding['binding']['python']['binary_sha256']
for n,h in binding['binding']['installed_binary_hashes'].items():assert sha(root/n)==h
flint.ctx.prec=128;flint.ctx.threads=1
lib=ctypes.CDLL(str(root/'.dylibs/libflint.24.0.dylib'));lib.flint_get_num_threads.restype=ctypes.c_int
assert lib.flint_get_num_threads()==1
rp=P.parent/'certified_sparse_query_20260907/evaluator.py';assert sha(rp)==freeze['naive_sha256']
spec=importlib.util.spec_from_file_location('frozen_reference',rp);ref=importlib.util.module_from_spec(spec);spec.loader.exec_module(ref)
namespace=(sha(bp),128,sha(rp),sha(P/'inputs.json'))
opt=Optimized(namespace,ref);counts={'exponentials':0,'hann':0,'amplitudes':0,'accumulations':0,'membership_builds':0}
# Trace actual executed reference lines; no reference-code mutation or extra queries.
lines,first=inspect.getsourcelines(ref.evaluate)
cosline=next(first+i for i,s in enumerate(lines) if 'w=(1+' in s)
termline=next(first+i for i,s in enumerate(lines) if 'z+=' in s)
def trace(frame,event,arg):
 if frame.f_code is ref.evaluate.__code__ and event=='line':
  if frame.f_lineno==cosline:counts['hann']+=1
  if frame.f_lineno==termline:
   for k in ('exponentials','amplitudes','accumulations'):counts[k]+=1
 return trace
inputs=json.loads((P/'inputs.json').read_bytes());inputrows=[];periodrows=[];windowrows=[];wc={};shards=[];buffer=[];naive=[];evaluating=0;writing=0;maxbuffer=0

def writefile(name,obj):
 global writing
 t=time.perf_counter_ns();(dest/name).write_bytes(canonical(obj));writing+=time.perf_counter_ns()-t

def flush():
 global buffer,maxbuffer
 if not buffer:return
 name=f'shard-{len(shards):06d}.json';writefile(name,buffer)
 shards.append({'name':name,'sha256':sha(dest/name),'rows':len(buffer),'first':buffer[0]['query_id'],'last':buffer[-1]['query_id']});buffer=[]

def pieces(w,a):
 out=[]
 if w[0]<a[0]:out.append({'ends':[w[0],a[0]],'closed':[True,False]})
 if a[1]<w[1]:out.append({'ends':[a[1],w[1]],'closed':[False,True]})
 return out

for pop in inputs:
 pid=pop['population'];ir=tagged(pop);inputrows.append(ir)
 measure=[{'id':e['id'],'t':str(rational(e['fields']['t']['ratio'])),'s':str(rational(e['fields']['s']['ratio']))} for e in pop['events']]
 times={e['id']:Q(e['t']) for e in measure};scope=list(map(Q,pop['scope']));asset=list(map(Q,pop['asset_bounds']))
 if pid=='P':
  pairs={}
  for i,j in combinations(sorted(times),2):
   d=abs(times[i]-times[j])
   if d:pairs.setdefault(d,[]).append([i,j])
  qs=[(u,L,t) for u in sorted(set(times.values())) for L in sorted({2*abs(v-u) for v in times.values() if v!=u}) for t in sorted(pairs)]
 else:pairs={Q(2):[]};qs=[(Q(1) if pid=='R' else Q(3,4),Q(2),Q(2))]
 pr={}
 for t,ps in pairs.items():
  body={'population':pid,'T':t,'f':1/t,'origin':'EVENT_DERIVED_POLICY' if pid=='P' else 'CONTROLLED_NUMERICAL_PROBE','pairs':ps,'pair_times':[[times[i],times[j]] for i,j in ps],
        'construction_input_ids':sorted(times) if pid!='P' else [],'coincident_pairs':[['P.b','P.e']] if pid=='P' else []}
  pr[t]=tagged(body);periodrows.append(pr[t])
 for u,L,t in qs:
  key=(namespace,pid,u,L,tuple(asset),tuple(scope))
  if mode=='naive' or key not in wc:
   counts['membership_builds']+=1
   w=[u-L/2,u+L/2];clip=[max(w[0],asset[0]),min(w[1],asset[1])];av=[max(clip[0],scope[0]),min(clip[1],scope[1])]
   contained=sorted(i for i,v in times.items() if av[0]<=v<=av[1]);boundary=sorted(i for i,v in times.items() if abs(v-u)==L/2);positive=sorted(set(contained)-set(boundary));centers=sorted(i for i,v in times.items() if v==u)
   wp=[[i,j] for i in centers for j in boundary] if pid=='P' else []
   body={'population':pid,'u':u,'L':L,'center_ids':centers,'scale_pairs':wp,'membership':{'contained':contained,'boundary':boundary,'positive':positive},'requested':w,'asset_clipped':clip,'available':av,'asset_unavailable':pieces(w,clip),'unavailable':pieces(w,av),'asset_truncated':w!=clip,'scope_truncated':av!=clip}
   row=tagged(body)
   if key not in wc:windowrows.append(row)
   wc[key]=row
  wr=wc[key];members=wr['body']['membership']
  def overlap(ps,extra):
   ids=sorted({i for pair in ps for i in pair}|set(extra))
   return {'generating_ids':ids,'intersections':{k:sorted(set(ids)&set(v)) for k,v in members.items()},'pair_intersections':[{'pair':pair,'intersections':{k:sorted(set(pair)&set(v)) for k,v in members.items()}} for pair in ps]}
  overlaps={'period':overlap(pr[t]['body']['pairs'],pr[t]['body']['construction_input_ids']),'scale':overlap(wr['body']['scale_pairs'],sorted(times) if pid!='P' else [])}
  q={'u':str(u),'L':str(L),'f':str(1/t)};clock=time.perf_counter_ns()
  if mode=='naive':
   sys.settrace(trace)
   try:numeric=ref.evaluate(measure,q)
   finally:sys.settrace(None)
  else:numeric=opt.evaluate(pid,measure,q)
  evaluating+=time.perf_counter_ns()-clock
  x,y=ref.bounds(numeric['real']),ref.bounds(numeric['imag']);numeric['zero_containment']=x[0]<=0<=x[1] and y[0]<=0<=y[1]
  logical={'query_id':[pid,u,L,t],'numeric':numeric,'scientific_status':'RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED','generation_evaluation_overlap':overlaps,
           'input_provenance':pop,'period_provenance':pr[t]['body'],'window_provenance':wr['body']}
  if mode=='naive':naive.append(logical)
  else:
   buffer.append({k:v for k,v in logical.items() if k not in ('input_provenance','period_provenance','window_provenance')}|{'input_ref':ir['id'],'period_ref':pr[t]['id'],'window_ref':wr['id']});maxbuffer=max(maxbuffer,len(buffer))
   if len(buffer)==4:flush()
if mode=='naive':writefile('logical.json',naive)
else:
 flush()
 for name,obj in [('inputs.json',inputrows),('periods.json',periodrows),('windows.json',windowrows)]:writefile(name,obj)
 writefile('index.json',{'shards':shards,'manifests':{n:sha(dest/n) for n in ('inputs.json','periods.json','windows.json')},'total':'21'})
 counts.update(opt.counts)
scientific_bytes=sum(f.stat().st_size for f in dest.iterdir() if f.is_file())
metrics={'counts':counts,'caches':{'parsed':len(opt.parsed),'exponentials':len(opt.exp),'hann':len(opt.hann),'amplitudes':len(opt.amp),'membership':len(wc) if mode!='naive' else 0},'max_buffered_rows':maxbuffer,'scientific_bytes':scientific_bytes}
writefile('mechanics.json',metrics)
perf={'wall_ns':str(time.perf_counter_ns()-start),'evaluation_ns':str(evaluating),'write_ns':str(writing),'peak_rss_bytes':str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),'naive_trace_instrumentation':mode=='naive','timing_limitation':'Naive line tracing overhead is included; no uninstrumented speedup claim.'}
(dest/'performance.json').write_bytes(canonical(perf))
