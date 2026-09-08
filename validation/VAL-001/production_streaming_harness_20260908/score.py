"""Streaming comparison; no evaluator/cache imports."""
import json,sys,hashlib
from pathlib import Path
from fractions import Fraction as Q
from streaming import canonical,digest,sha,array_rows
run=Path(sys.argv[1]);fixture=sys.argv[2];out=Path(sys.argv[3]);r=run/'reference'/fixture;p=run/'production'/fixture
checks=0;failures=[]
def ck(name,ok):
 global checks
 checks+=1
 if not ok:failures.append(name);raise ValueError(name)
try:
 rm=json.loads((r/'metrics.json').read_bytes());pm=json.loads((p/'metrics.json').read_bytes());root=json.loads((p/'root.json').read_bytes())
 n={'E':21,'C':8193,'S':4080384}[fixture];shards=(n+4095)//4096
 ck('counts',rm['rows']==pm['rows']==root['rows']==str(n) and root['shards']==str(shards))
 ck('index_hash',sha(p/'index.json')==root['index_sha256'])
 maps={}
 for name in ('inputs.json','periods.json'):
  ck(name+':manifest_hash',sha(p/name)==root['manifests'][name]);maps[name]={}
  for row in array_rows(p/name):
   ck(name+':content_hash',digest(row['body'])==row['id']);ck(name+':unique',row['id'] not in maps[name]);maps[name][row['id']]=row['body']
 ck('window_hash',sha(p/'windows.jsonl')==root['manifests']['windows.jsonl'])
 fingerprint=hashlib.sha256();count=0;current_id=None;window=None
 with (r/'logical.jsonl').open('rb',buffering=65536) as rf,(p/'windows.jsonl').open('rb',buffering=65536) as wf,(p/'index.json').open('rb',buffering=65536) as ix:
  for sn,line in enumerate(ix):
   ent=json.loads(line);ck('index_canonical',line==canonical(ent)+b'\n');ck('shard_name',ent['name']==f'shard-{sn:06d}.json');ck('shard_hash',sha(p/ent['name'])==ent['sha256'])
   local=0;first=None;last=None
   for compact in array_rows(p/ent['name']):
    stress=fixture=='S';body=compact['logical_record'] if stress else compact
    wid=body['window_ref']
    if wid!=current_id:
     wr=json.loads(wf.readline());ck('window_id',wr['id']==wid and digest(wr['body'])==wid);current_id=wid;window=wr['body']
    expanded={k:v for k,v in body.items() if k not in ('input_ref','period_ref','window_ref')}
    expanded.update(input_provenance=maps['inputs.json'][body['input_ref']],period_provenance=maps['periods.json'][body['period_ref']],window_provenance=window)
    if stress:
     ck('stress_order',compact['transport_ordinal']==str(count) and compact['template_index']==str(count%21))
     expanded={'transport_ordinal':compact['transport_ordinal'],'template_index':compact['template_index'],'logical_record':expanded}
    payload=canonical(expanded)+b'\n';expected=rf.readline();ck('exact_logical_record',payload==expected);fingerprint.update(payload)
    if fixture=='C':
     ck('C_membership',window['membership']=={'contained':['C.a','C.b'],'boundary':['C.b'],'positive':['C.a']})
     ck('C_scope',window['requested']==[['-1','1'],['1','1']] and window['available']==[['0','1'],['1','1']])
     ck('C_order',expanded['query_id']==['C',['0','1'],['2','1'],[str(Q(count+1,8192).numerator),str(Q(count+1,8192).denominator)]])
    if fixture=='E':
     qid=expanded['query_id'];pid=qid[0]
     if pid=='Z':ck('E_zero',expanded['numeric']['phase_status']=='UNRESOLVED_ZERO_CONTAINMENT')
     if pid=='R':ck('E_branch',expanded['numeric']['phase_status']=='BRANCH_CUT_ENCLOSURE')
     if pid=='P':
      table={(0,2):('abe','be','a'),(0,6):('abec','c','abe'),(1,2):('abe','a','be'),(1,4):('abec','c','abe'),(3,4):('bec','be','c'),(3,6):('abec','a','bec')}
      u,L=(int(qid[j][0]) for j in (1,2));wanted={k:sorted('P.'+i for i in v) for k,v in zip(('contained','boundary','positive'),table[u,L])};ck('E_membership',window['membership']==wanted)
    identity=compact['transport_ordinal'] if stress else compact['query_id']
    if first is None:first=identity
    last=identity;local+=1;count+=1
   ck('shard_rows',local==min(4096,n-sn*4096) and ent['rows']==str(local));ck('shard_endpoints',ent['first_id']==first and ent['last_id']==last)
  ck('no_extra_reference',rf.readline()==b'');ck('no_extra_windows',wf.readline()==b'')
 ck('all_records',count==n);ck('fingerprints',fingerprint.hexdigest()==rm['logical_fingerprint']==pm['logical_fingerprint'])
 ck('cache_bounds',all(int(pm['cache_highwater'][k])<=lim for k,lim in [('parsed',63),('hann',63),('amplitudes',63),('exp',4096)]))
 ck('buffer_contract',pm['buffered_result_records']=='1' and pm['buffered_index_entries']=='1')
 expectedcalls=0 if fixture=='S' else n;ck('evaluation_population',rm['evaluator_calls']==pm['evaluator_calls']==str(expectedcalls))
 ck('accumulation_population',rm['arithmetic']['accumulations']==pm['arithmetic']['accumulations']==str(0 if fixture=='S' else 68 if fixture=='E' else 16386))
 if fixture=='C':ck('eviction_exercised',int(pm['evictions'])>0)
except Exception as e:
 if not failures:failures.append(type(e).__name__+':'+str(e))
result={'status':'FAIL' if failures else 'PASS','checks_passed':str(checks-len(failures)),'checks_failed':str(len(failures)),'failures':failures,'fixture':fixture,'reference_metrics_sha256':sha(r/'metrics.json'),'production_metrics_sha256':sha(p/'metrics.json'),'root_sha256':sha(p/'root.json')}
out.write_bytes(canonical(result));print(result,flush=True);sys.exit(1 if failures else 0)
