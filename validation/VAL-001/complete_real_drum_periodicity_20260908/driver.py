"""Complete lazy real-input integration; unchanged certified evaluator and Writer."""
import time,os,resource,sys,json,hashlib,traceback
START=time.perf_counter_ns()
from common import *
run=sys.argv[1];assert run in ('run_1','run_2');stage='PREFLIGHT';count=0;dest=EXT/run/'production'
status=P/(run+'_execution.json');assert not status.exists()
try:
 inp,binding=setup();byid,times,groups,coincident,centers,pair=catalogues(inp)
 required=(640 if run=='run_1' else 384)*2**30
 disk=os.statvfs(EXT.parent);free=disk.f_bavail*disk.f_frsize;assert free>=required,('capacity',free,required)
 assert not dest.parent.exists(),('existing_run',str(dest.parent))
 if run=='run_2':assert json.loads((P/'score_1.json').read_bytes())['status']=='PASS'
 dest.mkdir(parents=True,exist_ok=False)
 (dest/'preflight.json').write_bytes(canonical({'run':run,'free_bytes':free,'required_bytes':required,'mount_device':os.stat(dest).st_dev,'implementation_binding_sha256':sha(P/'implementation_binding.json')}))
 ref=load('bound_numeric',V/'certified_sparse_query_20260907/evaluator.py');opt=load('bound_optimized',V/'cached_streaming_equivalence_20260908/optimized.py')
 engine=opt.Optimized((sha(P/'implementation_binding.json'),128,inp['source_identity'],inp['asset_sha256']),ref);engine.exp=LRU()
 policy=load('bound_policy',V/'event_centered_query_policy_20260908/constructor.py')
 writer=Writer(dest);hh=hashlib.sha256();current=None;high={k:0 for k in ('parsed','hann','amp','exp')};windows=0
 input_body=provenance(inp);scope=[q(inp['scope'][k]['ratio']) for k in ('start','end')];asset=scope
 measure=[{'id':e['eme_id'],'t':str(q(e['timestamp']['ratio'])),'s':str(q(e['strength']['ratio']))} for e in inp['events']]
 periods={T:{'population':PID,'T':T,'f':1/T,'pairs':groups[T],'coincident_pairs':coincident} for T in sorted(groups)}
 stage='EXECUTION'
 for u in centers:
  centerids=sorted(i for i,t in times.items() if t==u)
  for L in sorted({2*abs(t-u) for t in times.values() if t!=u}):
   engine.hann.clear();engine.amp.clear();windows+=1
   boundary=sorted(i for i,t in times.items() if abs(t-u)==L/2);pairs=[pair(i,j) for i in centerids for j in boundary]
   requested=[u-L/2,u+L/2];clip=policy.intersection(requested,asset);available=policy.intersection(clip,scope)
   member={'contained':sorted(i for i,t in times.items() if available[0]<=t<=available[1]),'boundary':boundary,'positive':sorted(i for i,t in times.items() if abs(t-u)<L/2)}
   window={'population':PID,'u':u,'L':L,'center_ids':centerids,'scale_pairs':pairs,'membership':member,'requested':requested,'asset_clipped':clip,'available':available,'asset_unavailable':policy.missing(requested,clip),'unavailable':policy.missing(requested,available),'asset_truncated':clip!=requested,'scope_truncated':available!=clip}
   scale_overlap=policy.overlaps(pairs,member)
   for T in sorted(groups):
    numeric=engine.evaluate(PID,measure,{'u':str(u),'L':str(L),'f':str(1/T)})
    x,y=ref.bounds(numeric['real']),ref.bounds(numeric['imag']);numeric['zero_containment']=x[0]<=0<=x[1] and y[0]<=0<=y[1]
    record={'query_id':[PID,u,L,T],'input_provenance':input_body,'window_provenance':window,'period_provenance':periods[T],'generation_evaluation_overlap':{'period':policy.overlaps(groups[T],member),'scale':scale_overlap},'numeric':numeric,'scientific_status':'RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED'}
    payload=canonical(record);hh.update(payload+b'\n');writer.row(record);count+=1
    for k in high:high[k]=max(high[k],len(getattr(engine,k)))
    assert high['parsed']<=63 and high['hann']<=63 and high['amp']<=63 and high['exp']<=4096
    if count%4096==0:
     disk=os.statvfs(dest)
     if disk.f_bavail*disk.f_frsize<128*2**30:raise OSError('free storage below frozen 128 GiB reserve')
     if count%(4096*50)==0:print(run,'completed',count,flush=True)
 assert count==4080384 and engine.counts['accumulations']==133195392 and windows==3864
 writer.finish();assert writer.nshards==997
 files={};shard_bytes=0;allocated=0;sidecars=0;filecount=0
 for e in os.scandir(dest):
  if not e.is_file():continue
  st=e.stat();allocated+=st.st_blocks*512;filecount+=1
  if e.name.startswith('._'):sidecars+=st.st_size;continue
  if e.name=='preflight.json':continue
  if e.name.startswith('shard-'):shard_bytes+=st.st_size
  else:files[e.name]=st.st_size
 metrics={'status':'EXECUTION_COMPLETE_REQUIRES_VALIDATION','queries':count,'arithmetic':engine.counts,'cache_highwater':high,'evictions':engine.exp.evictions,'window_builds':windows,'logical_fingerprint':hh.hexdigest(),'root_sha256':sha(dest/'root.json'),'shards':writer.nshards,'shard_bytes':shard_bytes,'canonical_files_bytes':files,'canonical_bytes':shard_bytes+sum(files.values()),'max_compact_record_bytes':writer.maxrow,'buffered_result_records':1,'buffered_index_entries':1,'implementation_binding_sha256':sha(P/'implementation_binding.json')}
 (dest/'metrics.json').write_bytes(canonical(metrics))
 perf={'runtime_ns':time.perf_counter_ns()-START,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'allocated_bytes_before_metrics':allocated,'filesystem_files_before_metrics':filecount,'sidecar_bytes':sidecars,'external_path':str(dest),'free_bytes_before':free}
 (dest/'performance.json').write_bytes(canonical(perf));status.write_bytes(canonical({'status':'EXECUTION_COMPLETE','queries':count,'metrics_sha256':sha(dest/'metrics.json'),'performance':perf}));print(run,'EXECUTION_COMPLETE',count,flush=True)
except BaseException as exc:
 state='STOP_PREFLIGHT' if stage=='PREFLIGHT' else 'STOP_INCOMPLETE' if isinstance(exc,(OSError,KeyboardInterrupt,SystemExit)) else 'FAIL_CONTRACT'
 status.write_bytes(canonical({'status':state,'queries_completed':count,'exception':type(exc).__name__,'detail':str(exc),'stage':stage}));traceback.print_exc();sys.exit(1)
