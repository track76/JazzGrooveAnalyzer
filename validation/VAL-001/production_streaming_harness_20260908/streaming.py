"""Bounded byte streaming and operational cache lifetimes; no scientific formulas."""
import hashlib,json
from collections import OrderedDict
from fractions import Fraction

def enc(x):
 if isinstance(x,Fraction):return [str(x.numerator),str(x.denominator)]
 if isinstance(x,dict):return {k:enc(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [enc(v) for v in x]
 if isinstance(x,int) and not isinstance(x,bool):return str(x)
 return x
def canonical(x):return json.dumps(enc(x),sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  while b:=f.read(65536):h.update(b)
 return h.hexdigest()
def array_rows(path):
 # Incremental JSON array parser, retaining one object plus a fixed read buffer.
 decoder=json.JSONDecoder();buf='';ended=False
 with path.open('r',encoding='ascii',buffering=65536) as f:
  while True:
   if not buf:
    buf=f.read(65536)
    if not buf:break
   buf=buf.lstrip(' \r\n\t[,')
   if buf.startswith(']'):ended=True;break
   try:value,pos=decoder.raw_decode(buf)
   except json.JSONDecodeError:
    part=f.read(65536)
    if not part:raise
    buf+=part;continue
   yield value;buf=buf[pos:]
 assert ended
class LRU(OrderedDict):
 def __init__(self):super().__init__();self.evictions=0;self.high=0
 def __getitem__(self,k):v=super().__getitem__(k);self.move_to_end(k);return v
 def __setitem__(self,k,v):
  if k not in self and len(self)==4096:self.popitem(last=False);self.evictions+=1
  super().__setitem__(k,v);self.move_to_end(k);self.high=max(self.high,len(self))
class Writer:
 def __init__(self,path):
  self.path=path;self.index=(path/'index.json').open('wb',buffering=65536)
  self.windows=(path/'windows.jsonl').open('wb',buffering=65536)
  self.inputs={};self.periods={};self.window=None;self.total=0;self.nshards=0;self.rows=0;self.handle=None;self.maxrow=0
 def row(self,logical):
  stress='transport_ordinal' in logical;body=logical['logical_record'] if stress else logical
  compact={k:v for k,v in body.items() if k not in ('input_provenance','period_provenance','window_provenance')}
  for key,store in [('input',self.inputs),('period',self.periods)]:
   value=body[key+'_provenance'];h=digest(value)
   if h not in store:store[h]=value
   compact[key+'_ref']=h
  value=body['window_provenance'];h=digest(value)
  # repeated windows in S may recur: append on transition, content ID unchanged.
  if h!=self.window:self.windows.write(canonical({'id':h,'body':value})+b'\n');self.window=h
  compact['window_ref']=h
  if stress:compact={'transport_ordinal':logical['transport_ordinal'],'template_index':logical['template_index'],'logical_record':compact}
  identity=logical['transport_ordinal'] if stress else body['query_id']
  if self.handle is None:
   self.name=f'shard-{self.nshards:06d}.json';self.handle=(self.path/self.name).open('wb',buffering=65536);self.handle.write(b'[');self.hh=hashlib.sha256(b'[');self.first=identity
  b=canonical(compact);self.maxrow=max(self.maxrow,len(b))
  if self.rows:self.handle.write(b',');self.hh.update(b',')
  self.handle.write(b);self.hh.update(b);self.rows+=1;self.total+=1;self.last=identity
  if self.rows==4096:self.close_shard()
 def close_shard(self):
  if self.handle is None:return
  self.handle.write(b']');self.hh.update(b']');self.handle.close()
  self.index.write(canonical({'name':self.name,'sha256':self.hh.hexdigest(),'rows':self.rows,'first_id':self.first,'last_id':self.last})+b'\n')
  self.nshards+=1;self.rows=0;self.handle=None
 def finish(self):
  self.close_shard();self.index.close();self.windows.close()
  for name,store in [('inputs',self.inputs),('periods',self.periods)]:
   with (self.path/(name+'.json')).open('wb',buffering=65536) as f:
    f.write(b'[')
    for i,(h,body) in enumerate(store.items()):
     if i:f.write(b',')
     f.write(canonical({'id':h,'body':body}))
    f.write(b']')
  root={'schema':'JGA-STREAMING-INDEX-JSONL-V1','rows':self.total,'shards':self.nshards,'index_sha256':sha(self.path/'index.json'),'manifests':{n:sha(self.path/n) for n in ('inputs.json','periods.json','windows.jsonl')}}
  (self.path/'root.json').write_bytes(canonical(root))
