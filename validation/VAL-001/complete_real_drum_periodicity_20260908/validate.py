"""Streaming contract validator; never evaluates Fourier responses."""
import sys,json,hashlib,traceback
from common import *
run=sys.argv[1];assert run in ('run_1','run_2');out=P/('score_'+run[-1]+'.json');assert not out.exists()
checks=0;rows=0;accum=0;failures=[]
def ck(name,ok):
 global checks
 checks+=1
 if not ok:raise AssertionError(name)
def dy(v):
 ck('dyadic_shape',isinstance(v,list) and len(v)==2 and all(isinstance(x,str) for x in v))
 m,e=map(int,v);ck('normalized_dyadic',str(m)==v[0] and str(e)==v[1] and (m%2!=0 if m else e==0));return Q(m)*Q(2)**e
def ball(b):
 ck('ball_shape',set(b)=={'mid','rad'});m,r=dy(b['mid']),dy(b['rad']);ck('nonnegative_radius',r>=0);return m-r,m+r
def overlap(pairs,member):
 ids=sorted({i for p in pairs for i in p['ids']})
 return {'generating_ids':ids,'intersections':{k:sorted(set(ids)&set(v)) for k,v in member.items()},'pairs':[{'ids':p['ids'],'intersections':{k:sorted(set(p['ids'])&set(v)) for k,v in member.items()}} for p in pairs]}
try:
 inp,binding=setup();byid,times,groups,coincident,centers,pair=catalogues(inp);d=EXT/run/'production'
 metrics=json.loads((d/'metrics.json').read_bytes());root=json.loads((d/'root.json').read_bytes())
 ck('execution_complete',metrics['status']=='EXECUTION_COMPLETE_REQUIRES_VALIDATION' and metrics['queries']=='4080384')
 ck('root_contract',root['schema']=='JGA-STREAMING-INDEX-JSONL-V1' and root['rows']=='4080384' and root['shards']=='997')
 ck('root_canonical',canonical(root)==(d/'root.json').read_bytes());ck('root_metrics_hash',sha(d/'root.json')==metrics['root_sha256']);ck('index_hash',sha(d/'index.json')==root['index_sha256'])
 maps={}
 for name in ('inputs.json','periods.json'):
  ck('manifest_file_hash',sha(d/name)==root['manifests'][name]);maps[name]={}
  h=hashlib.sha256(b'[');n=0
  for r in array_rows(d/name):
   ck('manifest_content_id',digest(r['body'])==r['id'] and r['id'] not in maps[name]);maps[name][r['id']]=r['body']
   if n:h.update(b',')
   h.update(canonical(r));n+=1
  h.update(b']');ck('manifest_canonical',h.hexdigest()==root['manifests'][name])
 input_body=json.loads(canonical(provenance(inp)));ih=digest(input_body)
 ck('input_manifest',maps['inputs.json']=={ih:input_body})
 expected_periods={T:json.loads(canonical({'population':PID,'T':T,'f':1/T,'pairs':groups[T],'coincident_pairs':coincident})) for T in sorted(groups)}
 ck('complete_period_manifest',maps['periods.json']=={digest(v):v for v in expected_periods.values()})
 ck('window_file_hash',sha(d/'windows.jsonl')==root['manifests']['windows.jsonl'])
 scope=[q(inp['scope'][k]['ratio']) for k in ('start','end')]
 def windows():
  for u in sorted(set(times.values())):
   for L in sorted(set(2*abs(t-u) for t in times.values() if t!=u)):
    c=sorted(i for i,t in times.items() if t==u);b=sorted(i for i,t in times.items() if abs(t-u)==L/2)
    members={'contained':sorted(i for i,t in times.items() if abs(t-u)<=L/2),'boundary':b,'positive':sorted(i for i,t in times.items() if abs(t-u)<L/2)}
    requested=[u-L/2,u+L/2];available=[max(requested[0],scope[0]),min(requested[1],scope[1])];missing=[]
    if requested[0]<available[0]:missing.append({'ends':[requested[0],available[0]],'closed':[True,False]})
    if available[1]<requested[1]:missing.append({'ends':[available[1],requested[1]],'closed':[False,True]})
    ps=[pair(i,j) for i in c for j in b]
    w={'population':PID,'u':u,'L':L,'center_ids':c,'scale_pairs':ps,'membership':members,'requested':requested,'asset_clipped':available,'available':available,'asset_unavailable':missing,'unavailable':missing,'asset_truncated':available!=requested,'scope_truncated':False}
    yield u,L,w,overlap(ps,members)
 wi=iter(windows());period_list=sorted(groups);current=None;fingerprint=hashlib.sha256();window_count=0
 with (d/'windows.jsonl').open('rb',buffering=65536) as wf,(d/'index.json').open('rb',buffering=65536) as ix:
  for sn,line in enumerate(ix):
   ent=json.loads(line);ck('index_encoding',line==canonical(ent)+b'\n');ck('shard_name',ent['name']==f'shard-{sn:06d}.json')
   ck('shard_hash',sha(d/ent['name'])==ent['sha256']);ch=hashlib.sha256(b'[');local=0;first=None;last=None
   for compact in array_rows(d/ent['name']):
    if rows%1056==0:
     u,L,expected_window,scale_overlap=next(wi);wrline=wf.readline();wr=json.loads(wrline)
     expected_window=json.loads(canonical(expected_window));ck('window_geometry',wr['body']==expected_window and wr['id']==digest(expected_window));ck('window_canonical',wrline==canonical(wr)+b'\n');window_count+=1
     current=wr;members=expected_window['membership'];used=sorted(members['contained'],key=lambda i:(times[i],i))
    T=period_list[rows%1056];period=expected_periods[T]
    expected_id=json.loads(canonical([PID,u,L,T]));ck('complete_order',compact['query_id']==expected_id)
    ck('provenance_refs',compact['input_ref']==ih and compact['window_ref']==current['id'] and compact['period_ref']==digest(period))
    ck('overlap',compact['generation_evaluation_overlap']==json.loads(canonical({'period':overlap(groups[T],members),'scale':scale_overlap})))
    ck('status',compact['scientific_status']=='RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED')
    n=compact['numeric'];ck('numeric_fields',set(n)=={'real','imag','magnitude','phase_status','phase','contributing_ids','zero_containment'})
    x,y=ball(n['real']),ball(n['imag']);lo,hi=map(dy,n['magnitude']);ck('magnitude',0<=lo<=hi)
    zero=x[0]<=0<=x[1] and y[0]<=0<=y[1];branch=x[0]<0 and y[0]<=0<=y[1]
    ck('zero_containment',n['zero_containment']==zero)
    if zero:ck('zero_phase',n['phase_status']=='UNRESOLVED_ZERO_CONTAINMENT' and n['phase'] is None)
    elif branch:
     ck('branch_phase',n['phase_status']=='BRANCH_CUT_ENCLOSURE' and n['phase']['full_circle'] is True);ck('branch_bounds',dy(n['phase']['lower'])<0<dy(n['phase']['upper']))
    else:
     ck('resolved_phase',n['phase_status']=='RESOLVED_INTERVAL');ball(n['phase'])
    ck('ordered_contributors',n['contributing_ids']==used);accum+=len(used)
    expanded={k:v for k,v in compact.items() if k not in ('input_ref','period_ref','window_ref')};expanded.update(input_provenance=input_body,window_provenance=current['body'],period_provenance=period)
    fingerprint.update(canonical(expanded)+b'\n')
    if local:ch.update(b',')
    ch.update(canonical(compact));local+=1;rows+=1
    if first is None:first=compact['query_id']
    last=compact['query_id']
   ch.update(b']');ck('shard_canonical',ch.hexdigest()==ent['sha256']);ck('shard_population',local==min(4096,4080384-sn*4096) and ent['rows']==str(local));ck('shard_endpoints',first==ent['first_id'] and last==ent['last_id'])
   if (sn+1)%50==0:print(run,'validated',rows,flush=True)
  ck('no_extra_windows',wf.readline()==b'');ck('all_expected_windows',next(wi,None) is None)
 ck('population',rows==4080384 and accum==133195392 and window_count==3864 and sn==996)
 ck('logical_fingerprint',fingerprint.hexdigest()==metrics['logical_fingerprint']);ck('ordered_accumulation_count',metrics['arithmetic']['accumulations']==str(accum))
 ck('cache_bounds',all(int(metrics['cache_highwater'][k])<=v for k,v in [('parsed',63),('hann',63),('amp',63),('exp',4096)]))
 ck('buffers',metrics['buffered_result_records']==metrics['buffered_index_entries']=='1')
 result={'status':'PASS','checks_passed':checks,'checks_failed':0,'queries':rows,'accumulations':accum,'logical_fingerprint':fingerprint.hexdigest(),'root_sha256':sha(d/'root.json'),'metrics_sha256':sha(d/'metrics.json'),'implementation_binding_sha256':sha(P/'implementation_binding.json')}
except BaseException as exc:
 result={'status':'STOP_INCOMPLETE' if isinstance(exc,(OSError,KeyboardInterrupt,SystemExit)) else 'FAIL_CONTRACT','checks_passed':checks-1,'checks_failed':1,'queries_validated':rows,'exception':type(exc).__name__,'detail':str(exc)};traceback.print_exc()
out.write_bytes(canonical(result));print(result,flush=True);sys.exit(0 if result['status']=='PASS' else 1)
