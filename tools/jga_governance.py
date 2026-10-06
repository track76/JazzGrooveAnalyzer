#!/usr/bin/env python3
"""JGA governance checks and cooperative single-writer gate; never scientific analysis."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
P = 'docs/project/'
HEAVY = {'.wav','.mp3','.m4a','.flac','.aiff','.aif','.ogg','.mp4','.pt','.pth','.onnx','.h5','.hdf5','.ckpt','.npy','.npz','.parquet','.zip','.tar','.gz','.safetensors'}
MAX_GIT_BYTES = 10 * 1024 * 1024  # governance routing limit, not a scientific threshold
SKIP = {'.venv','venv','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','.ipynb_checkpoints'}

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(root,*args): return subprocess.check_output(['git','-C',str(root),*args])
def load(root,name): return json.loads((root/name).read_text())
def sha(p):
    if p.is_symlink(): return hashlib.sha256(os.readlink(p).encode()).hexdigest()
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def safe(root,name):
    rel=Path(name)
    if rel.is_absolute() or '..' in rel.parts or not rel.parts or rel.parts[0]=='.git': raise ValueError('Unsafe repository payload path')
    p=root/rel
    if any(x.is_symlink() for x in [p,*p.parents] if x.is_relative_to(root)): raise ValueError('Symlink payload/parent prohibited')
    if not p.resolve().is_relative_to(root.resolve()): raise ValueError('Outside repository')
    return p

def state(root):
    raw=git(root,'ls-files','--cached','--others','--exclude-standard','-z')
    names=set(os.fsdecode(x) for x in raw.split(b'\0') if x)
    # Include ignored payloads too: Git ignore is not permission to hide concurrent scientific writes.
    for directory, dirs, files_here in os.walk(root,followlinks=False):
        dirs[:]=[d for d in dirs if d not in SKIP and d!='.git' and not (Path(directory)/d).is_symlink()]
        for f in files_here:
            if f=='.DS_Store' or f.startswith('._') or f.endswith(('.pyc','.pyo','.tmp','.lock')):continue
            names.add(str((Path(directory)/f).relative_to(root)))
    files={}
    for name in sorted(names):
        p=root/name
        if any(x in SKIP for x in Path(name).parts): continue
        if p.exists() or p.is_symlink():
            s=p.lstat();files[name]=[s.st_size,s.st_mtime_ns,s.st_mode,sha(p) if s.st_size<=262144 or p.is_symlink() else None]
        else: files[name]=None
    return {'branch':git(root,'branch','--show-current').decode().strip(),'head':git(root,'rev-parse','HEAD').decode().strip(),
            'index_sha256':hashlib.sha256(git(root,'ls-files','--stage','-z')).hexdigest(),'files':files}

def lock_path(root):
    common=Path(git(root,'rev-parse','--git-common-dir').decode().strip())
    if not common.is_absolute(): common=root/common
    return common.resolve()/'jga-writer.lock'

def decision_for(root,task,agent,decision_id):
    rows=[json.loads(x) for x in (root/(P+'PI_DECISION_LOG.jsonl')).read_text().splitlines() if x.strip()]
    found=[x for x in rows if x.get('decision_id')==decision_id]
    if len(found)!=1: raise ValueError('Missing or ambiguous PI linkage')
    d=found[0]
    if d.get('task_id')!=task: raise ValueError('PI decision wrong task')
    if d.get('agent_id',agent)!=agent: raise ValueError('PI decision wrong agent')
    if d.get('decision',d.get('status')) not in {'AUTHORIZED_FOR_CURRENT_TASK','APPROVED'}: raise ValueError('PI decision not authorized')
    return d

def external_path(root,name):
    p=Path(name)
    if not p.is_absolute() or '..' in p.parts or p.resolve().is_relative_to(root.resolve()): raise ValueError('External path must be absolute and outside repository')
    if any(x.is_symlink() for x in [p,*p.parents]): raise ValueError('External symlink prohibited')
    return p

def in_external_scope(path,roots,paths):
    p=Path(path)
    return str(p) in paths or any(p.is_relative_to(Path(x)) for x in roots)

def external_state(paths):
    result={}
    for name in paths:
        p=Path(name)
        if p.exists():
            if not p.is_file():raise ValueError('Registered external output path must be a file')
            s=p.stat();result[name]=[s.st_size,s.st_mtime_ns,sha(p)]
        else:result[name]=None
    return result

def validate_phase(decision,task,phase,freezes=None):
    # Optional phases never confer another task or reveal authorization.
    if decision.get('task_id')!=task: raise ValueError('No automatic cross-task chaining')
    if phase not in decision.get('phases',[]): raise ValueError('Phase not PI-authorized')
    if phase=='HUMAN_UNSEAL':
        required={'method','parameters','population','evaluation','machine_output'}
        if not freezes or any(not re.fullmatch(r'[0-9a-f]{64}',freezes.get(k,'')) for k in required):raise ValueError('Independent freeze gates required before Human release')
    return {'task_id':task,'phase':phase,'status':'GATE_VALIDATED'}

def validate_blind_view(root,task,agent,view,decision=None):
    # Coordinator may inspect canonical logs; restricted workers supply only
    # their permitted, coordinator-verified PI decision record.
    d=decision if decision is not None else decision_for(root,task,agent,view.get('PI_decision'))
    if d.get('decision_id')!=view.get('PI_decision') or d.get('task_id')!=task or d.get('agent_id',agent)!=agent or d.get('decision',d.get('status')) not in {'APPROVED','AUTHORIZED_FOR_CURRENT_TASK'}:raise ValueError('Restricted PI authorization mismatch')
    if d.get('blind_worker_startup')!=view:raise ValueError('Explicit PI-bound restricted view required; worker cannot skip recovery silently')
    required={'task_id','agent_id','PI_decision','coordinator_recovery_record','allowed_files','denied_paths','release_condition'}
    if not required.issubset(view) or view['task_id']!=task or view['agent_id']!=agent or view['release_condition']!='INDEPENDENT_MACHINE_OUTPUT_FREEZE':raise ValueError('Incomplete blind-worker binding')
    if not view['denied_paths'] or not view['allowed_files']:raise ValueError('Explicit allowlist and denylist required')
    rec=view['coordinator_recovery_record'];p=Path(rec['path'])
    if not p.is_absolute() or sha(p)!=rec['sha256']:raise ValueError('Coordinator recovery record hash mismatch')
    for x in view['allowed_files']:
        p=Path(x['path'])
        if not p.is_absolute() or any(x.is_symlink() for x in [p,*p.parents]) or any(p.resolve().is_relative_to(Path(q).resolve()) for q in view['denied_paths']):raise ValueError('Protected target path denied')
        if sha(p)!=x['sha256']:raise ValueError('Permitted authority hash mismatch')
    return view

def blind_access(root,task,agent,view,path,decision=None):
    if decision is None:raise ValueError('Restricted worker requires permitted PI record; canonical recovery logs must not be opened implicitly')
    validate_blind_view(root,task,agent,view,decision)
    p=Path(path).resolve()
    if any(p.is_relative_to(Path(q).resolve()) for q in view['denied_paths']):raise ValueError('Protected target path denied before release')
    if str(p) not in {str(Path(x['path']).resolve()) for x in view['allowed_files']}:raise ValueError('Path outside permitted authority view')
    return p

def acquire(root,agent,task,token):
    registry=load(root,P+'AGENT_REGISTRY.json')
    a=next((a for a in registry['agents'] if a['agent_id']==agent),None)
    if not a or a['write_authority_status']!='AUTHORIZED_FOR_CURRENT_TASK' or a['current_task']!=task or a.get('current_mode') not in {'AUTHORIZED_WRITER','EXPERIMENTAL_ENGINEER'} or a.get('current_mode') not in a.get('allowed_modes',[]):
        raise ValueError('No current registered writer authorization')
    ledger=[json.loads(x) for x in (root/(P+'AGENT_WORK_LEDGER.jsonl')).read_text().splitlines() if x]
    records=[x for x in ledger if x['task_id']==task]
    if not records or not any(records[-1].get(k) for k in ['write_paths','external_write_roots','external_write_paths']): raise ValueError('No registered write scope')
    r=dict(records[-1]);r.setdefault('write_paths',[])
    decision_id=r.get('PI_decision',r.get('PI_authorization'))
    if not decision_id or a.get('PI_decision',decision_id)!=decision_id:raise ValueError('Missing PI linkage')
    decision=decision_for(root,task,agent,decision_id)
    if r.get('agent_id',agent)!=agent:raise ValueError('Ledger wrong agent')
    permitted=decision.get('write_paths',decision.get('repository_write_paths',[]))
    if not set(r['write_paths']).issubset(permitted) or not set(r['write_paths']).issubset(a.get('write_paths',r['write_paths'])):raise ValueError('PI-linked repository scope mismatch')
    for name in r['write_paths']:safe(root,name)
    roots=[str(external_path(root,x)) for x in r.get('external_write_roots',[])]
    paths=[str(external_path(root,x)) for x in r.get('external_write_paths',[])]
    authorized_roots=[str(external_path(root,x)) for x in decision.get('external_write_roots',[])]
    authorized_paths=[str(external_path(root,x)) for x in decision.get('external_write_paths',[])]
    if any(not in_external_scope(x,authorized_roots,authorized_paths) for x in roots+paths):raise ValueError('PI-linked external scope mismatch')
    if roots!=[str(Path(x)) for x in a.get('external_write_roots',roots)] or paths!=a.get('external_write_paths',paths):raise ValueError('Agent external scope mismatch')
    payload={'agent':agent,'task':task,'PI_decision':decision_id,'token':token,'acquired_at':now(),'write_paths':r['write_paths'],'external_write_roots':roots,'external_write_paths':paths,'external_baseline':external_state(paths),'baseline':state(root)}
    lock=lock_path(root)
    fd=os.open(lock,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as f: json.dump(payload,f);f.flush();os.fsync(f.fileno())
    return {'status':'ACQUIRED','agent':agent,'task':task}

def lease(root,token,check=True):
    p=lock_path(root);d=json.loads(p.read_text())
    if d['token']!=token: raise ValueError('Writer token mismatch')
    if check and external_state(list(d.get('external_baseline',{})))!=d.get('external_baseline',{}):raise ValueError('STALE EXTERNAL STATE — RESYNC REQUIRED')
    if check and d['baseline']!=state(root): raise ValueError('STALE STATE — RESYNC REQUIRED; no automatic merge or baseline refresh')
    return d

def write(root,token,target,payload):
    d=lease(root,token)
    if target not in d['write_paths']: raise ValueError('Path outside PI-authorized task scope')
    safe(root,target)
    sys.path.insert(0,str(root/'tools'))
    import continuous_backup as backup
    if root.resolve()!=backup.ROOT.resolve(): raise ValueError('Backup authority/root mismatch')
    verification=backup.atomic_write_and_backup(target,payload)
    after=state(root);before=d['baseline']
    a=dict(after['files']);b=dict(before['files']);a.pop(target,None);b.pop(target,None)
    if a!=b or any(after[k]!=before[k] for k in ['branch','head','index_sha256']):
        raise ValueError('Unexpected concurrent modification; stop for PI review')
    d['baseline']=after
    p=lock_path(root);tmp=p.with_suffix('.tmp')
    with tmp.open('w') as f:json.dump(d,f);f.flush();os.fsync(f.fileno())
    os.replace(tmp,p)
    return {'status':'WRITTEN_BACKUP_DEBT' if isinstance(verification,dict) and verification.get('status')=='BACKUP_DEBT_PI_AUTHORIZED' else 'WRITTEN_AND_BACKED_UP','path':target}

def write_external(root,token,target,payload,provenance):
    """Create bounded persistent output plus independently verified provenance sidecar.
    Cooperative adapter, not OS access control; no recursive acquisition inventory.
    Existing files are never overwritten by this creation adapter.
    """
    d=lease(root,token);p=external_path(root,target);record=Path(str(p)+'.provenance.json')
    for x in (p,record):
        if not in_external_scope(x,d.get('external_write_roots',[]),d.get('external_write_paths',[])):raise ValueError('Unregistered external write rejected')
        if x.exists():raise ValueError('Existing external artifact preserved; overwrite prohibited')
    if not all(provenance.get(k) for k in ['artifact_id','source_provenance','authority_classification']):raise ValueError('External output provenance required')
    sys.path.insert(0,str(root/'tools'));import continuous_backup as backup
    if root.resolve()!=backup.ROOT.resolve():raise ValueError('Backup authority/root mismatch')
    if backup.preflight()['status']!='BACKUP_VERIFIED':raise ValueError('Persistent scientific output requires verified backup')
    evidence={'task_id':d['task'],'agent_id':d['agent'],'PI_decision':d['PI_decision'],**provenance,'path':str(p),'size_bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest()}
    # Reserved identity cannot be replaced by caller-provided provenance.
    evidence.update(task_id=d['task'],agent_id=d['agent'],PI_decision=d['PI_decision'])
    for dest,data in [(p,payload),(record,(json.dumps(evidence,indent=2)+'\n').encode())]:
        lease(root,token)
        backup.atomic_external_write_and_backup(dest,data)
        expected=hashlib.sha256(data).hexdigest()
        if sha(dest)!=expected:raise ValueError('External output verification failed')
        d['external_baseline'][str(dest)]=external_state([str(dest)])[str(dest)]
        lock=lock_path(root);tmp=lock.with_suffix('.tmp');tmp.write_text(json.dumps(d));os.replace(tmp,lock)
    return {'status':'WRITTEN_AND_BACKED_UP','manifest':str(record),**evidence}

def release(root,token):
    d=lease(root,token);lock_path(root).unlink()  # only owner deletes its own verified lease
    return {'status':'RELEASED','task':d['task']}

def resync(root,token,justification):
    """Owner-initiated baseline resync. Requires the lock owner and token, and
    refuses any divergence outside the lease's own registered write_paths, so a
    concurrent writer can never be silently absorbed."""
    if not justification.strip():raise ValueError('A resync justification is required')
    p=lock_path(root);d=json.loads(p.read_text())
    if d['token']!=token:raise ValueError('Writer token mismatch')
    before=d['baseline'];after=state(root)
    a=dict(after['files']);b=dict(before['files'])
    diverging=sorted(k for k in set(a)|set(b) if a.get(k)!=b.get(k))
    outside=[k for k in diverging if k not in d['write_paths']]
    if outside:raise ValueError('Refusing resync: divergence outside authorized write_paths: %s'%outside)
    if any(after[k]!=before[k] for k in ['branch','head','index_sha256']):
        raise ValueError('Refusing resync: branch, HEAD or index changed since the lease was acquired')
    d['baseline']=after
    d['resyncs']=d.get('resyncs',[])+[{'resynced_at':now(),'justification':justification.strip(),
        'diverging_paths':diverging,'branch':after['branch'],'head':after['head'],'index_sha256':after['index_sha256']}]
    tmp=p.with_suffix('.tmp')
    with tmp.open('w') as f:json.dump(d,f);f.flush();os.fsync(f.fileno())
    os.replace(tmp,p)
    return {'status':'RESYNCED','task':d['task'],'absorbed_paths':diverging,
            'branch':after['branch'],'head':after['head'],'justification':justification.strip()}

def staged_guard(root):
    errors=[]
    for item in git(root,'diff','--cached','--name-only','--diff-filter=ACMRT','-z').split(b'\0'):
        if not item: continue
        name=os.fsdecode(item);size=int(git(root,'cat-file','-s',':'+name))
        if size>MAX_GIT_BYTES or Path(name).suffix.lower() in HEAVY:
            errors.append({'path':name,'issue':'HEAVY_STAGED_BLOB','bytes':size})
        mode=git(root,'ls-files','--stage','--',name).decode().split()[0]
        if mode=='120000': errors.append({'path':name,'issue':'STAGED_SYMLINK_REQUIRES_PI_REVIEW'})
    return errors

def external_check(root,mode):
    manifest=load(root,P+'EXTERNAL_ARTIFACT_MANIFEST.json');findings=[];verified=0
    for a in manifest['artifacts']:
        p=Path(a['canonical_external_path']);b=Path(a['backup_destination']) if a.get('backup_destination') else None
        if not p.exists():findings.append({'artifact_id':a['artifact_id'],'issue':'SOURCE_MISSING'});continue
        if a.get('size_bytes') is not None and p.stat().st_size!=a['size_bytes']:
            findings.append({'artifact_id':a['artifact_id'],'issue':'SOURCE_SIZE_MISMATCH'})
        need_hash=mode=='full' or (mode=='incremental' and (not a.get('verified_mtime_ns') or p.stat().st_mtime_ns!=a['verified_mtime_ns']))
        backup_changed = b is not None and b.exists() and b.stat().st_mtime_ns != a.get('backup_verified_mtime_ns')
        if need_hash:
            if not a.get('sha256'):findings.append({'artifact_id':a['artifact_id'],'issue':'HASH_UNREGISTERED'})
            elif sha(p)!=a['sha256']:findings.append({'artifact_id':a['artifact_id'],'issue':'SOURCE_HASH_MISMATCH'})
        if mode != 'metadata' and (need_hash or backup_changed) and b and b.exists() and a.get('sha256') and sha(b)!=a['sha256']:
            findings.append({'artifact_id':a['artifact_id'],'issue':'BACKUP_HASH_MISMATCH'})
        if a['backup_class']!='TEMPORARY_NO_BACKUP' and (b is None or not b.exists()):
            findings.append({'artifact_id':a['artifact_id'],'issue':'REQUIRED_BACKUP_MISSING'})
        if not a.get('source_provenance'):findings.append({'artifact_id':a['artifact_id'],'issue':'PROVENANCE_MISSING'})
        if a.get('source_provenance') and not (root/a['source_provenance']).exists():
            findings.append({'artifact_id':a['artifact_id'],'issue':'PROVENANCE_REFERENCE_MISSING'})
        verified+=1
    return {'mode':mode,'checked':verified,'findings':findings,'scope':manifest['coverage_scope'],
            'note':'metadata is existence/size only; incremental unchanged bytes rely on recorded verification, not a new full hash claim'}

def handoff_git_current(root,text,s):
    if s['branch'] not in text: return False
    if s['head'] in text: return True  # explicitly observed preparation HEAD
    if '$Format:%H$' not in text: return False
    path=P+'JGA_CHAT_HANDOFF.md'
    try:
        committed=git(root,'show','HEAD:'+path).decode()
        touched=git(root,'log','-1','--format=%H','--',path).decode().strip()
        attrs=git(root,'check-attr','export-subst','--',path).decode().strip()
        return committed==text and touched==s['head'] and attrs.endswith(': set')
    except subprocess.CalledProcessError: return False

def row_digest(row):
    return hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def historical_resolutions(rows,decisions):
    """PI-acknowledged append-only dispositions; originals remain visible."""
    byid={d['decision_id']:d for d in decisions};resolved={};warnings=[];errors=[]
    for i,c in enumerate(rows):
        if c.get('event')!='HISTORICAL_GOVERNANCE_CORRECTION':continue
        try:
            pi=byid[c['PI_authorization']]
            if pi.get('decision',pi.get('status')) not in {'APPROVED','AUTHORIZED_FOR_CURRENT_TASK'} or not pi.get('historical_reconciliation_authorized') or not pi.get('historical_qualification_acceptance'):raise ValueError('PI historical disposition not authorized')
            n=c['original_record_number']-1
            if n<0 or n>=i:raise ValueError('Correction must reference earlier immutable event')
            original=rows[n]
            if row_digest(original)!=c['original_record_sha256'] or original['task_id']!=c['original_task_id']:raise ValueError('Historical event identity mismatch')
            if original['task_id']==pi['task_id']:raise ValueError('Current task cannot receive historical exception')
            if not c.get('source_provenance') or not c.get('preservation_requirement') or c.get('scientific_bytes_shown_invalid') is not False:raise ValueError('Incomplete correction provenance')
            kind=c['resolution_kind'];key=(n,kind,c.get('missing_path'))
            if key in resolved or (kind in {'CORRECTIVE_PI_LINKAGE','HISTORICAL_AUTHORIZATION_UNRESOLVED'} and any(k[0]==n and k[1] in {'CORRECTIVE_PI_LINKAGE','HISTORICAL_AUTHORIZATION_UNRESOLVED'} for k in resolved)):raise ValueError('Conflicting or duplicate correction')
            if kind=='CORRECTIVE_PI_LINKAGE':
                d=byid[c['verified_existing_PI_decision']]
                if d.get('task_id')!=original['task_id']:raise ValueError('Correction PI task mismatch')
                if original.get('pi_authorization') and original['pi_authorization']!=d['decision_id']:raise ValueError('Conflicting original PI linkage')
            elif kind=='HISTORICAL_AUTHORIZATION_UNRESOLVED':
                missing=c['missing_decision_id']
                if missing!=original.get('PI_authorization') or missing in byid:raise ValueError('Unresolved authorization identity mismatch')
            elif kind=='HISTORICAL_REFERENCE_RESOLUTION':
                if c['missing_path'] not in original.get('artifact_paths',[])+original.get('input_authorities',[]):raise ValueError('Reference not in original event')
                if c['reference_status'] not in {'NEVER_PRODUCED','SUPERSEDED','MOVED/PRESERVED_ELSEWHERE','HISTORICALLY_MISSING','UNKNOWN'}:raise ValueError('Invalid historical reference disposition')
            else:raise ValueError('Unknown correction kind')
            resolved[key]=c
            warnings.append({'issue':kind,'original_record_number':n+1,'original_task_id':original['task_id'],'qualification':'RESOLVED_FOR_CURRENT_CONSISTENCY_WITH_QUALIFICATION','historically_authorized':False if kind=='HISTORICAL_AUTHORIZATION_UNRESOLVED' else None,'missing_path':c.get('missing_path'),'reference_status':c.get('reference_status'),'PI_acknowledgement':pi['decision_id']})
        except (KeyError,ValueError,TypeError) as e:errors.append({'issue':'INVALID_HISTORICAL_CORRECTION','record_number':i+1,'reason':str(e)})
    return resolved,warnings,errors

def validate_legacy_mapping(ids,artifacts,prefix):
    expected=[prefix+str(i).zfill(3) for i in range(1,len(artifacts)+1)]
    names=[a['name'] for a in artifacts]
    if not artifacts or ids!=expected or len(names)!=len(set(names)) or names!=sorted(names):raise ValueError('Invalid external positional mapping')
    for a in artifacts:
        if Path(a['path']).name!=Path(a['name']).name or not re.fullmatch('[0-9a-f]{64}',a['sha256']) or a['bytes']<0:raise ValueError('Invalid external artifact metadata')
    return list(zip(ids,artifacts))

def save_lease(root,d):
    p=lock_path(root);tmp=p.with_suffix('.tmp')
    with tmp.open('w') as f:json.dump(d,f);f.flush();os.fsync(f.fileno())
    os.replace(tmp,p)

def publication_context(root,token):
    d=lease(root,token);pi=decision_for(root,d['task'],d['agent'],d['PI_decision']);p=pi.get('publication',{})
    if p.get('commit') is not True or p.get('push') is not True or p.get('branch')!=d['baseline']['branch'] or not p.get('remote'):raise ValueError('PI publication scope required')
    if not set(d['write_paths']).issubset(pi.get('write_paths',[])):raise ValueError('Publication PI path scope mismatch')
    return d,pi

def reviewed_manifest(root,token,paths):
    d,pi=publication_context(root,token)
    if not paths or len(paths)!=len(set(paths)) or not set(paths).issubset(d['write_paths']):raise ValueError('Reviewed path scope mismatch')
    if git(root,'diff','--cached','--name-only','-z'):raise ValueError('Unexpected pre-staged files')
    entries=[]
    for name in sorted(paths):
        p=safe(root,name)
        if not p.is_file():raise ValueError('Unexpected deletion or non-file')
        exists=bool(git(root,'ls-files','--error-unmatch','--',name).strip()) if name in git(root,'ls-files','-z').decode().split('\0') else False
        entries.append({'path':name,'operation':'M' if exists else 'A','sha256':sha(p),'size_bytes':p.stat().st_size})
    return {'task_id':d['task'],'agent_id':d['agent'],'PI_decision':d['PI_decision'],'branch':d['baseline']['branch'],'parent':d['baseline']['head'],'initial_index_sha256':d['baseline']['index_sha256'],'entries':entries}

def validate_review(root,d,review):
    if any(review.get(k)!=d[v] for k,v in [('task_id','task'),('agent_id','agent'),('PI_decision','PI_decision')]):raise ValueError('Reviewed owner/task/PI mismatch')
    if review.get('branch')!=d['baseline']['branch'] or review.get('parent')!=d['baseline']['head']:raise ValueError('Unexpected parent or branch')
    entries=review.get('entries',[]);paths=[x['path'] for x in entries]
    if not paths or len(paths)!=len(set(paths)) or not set(paths).issubset(d['write_paths']):raise ValueError('Reviewed path scope mismatch')
    for x in entries:
        p=safe(root,x['path'])
        if x['operation'] not in {'A','M'} or not p.is_file():raise ValueError('Unexpected deletion')
        if sha(p)!=x['sha256'] or p.stat().st_size!=x['size_bytes']:raise ValueError('Reviewed bytes changed')


def verify_index(root,review):
    paths=[x['path'] for x in review['entries']]
    changed=[os.fsdecode(x) for x in git(root,'diff','--cached','--name-only','-z').split(b'\0') if x]
    if sorted(changed)!=sorted(paths):raise ValueError('Partial staging or unexpected staged scope')
    for x in review['entries']:
        op=git(root,'diff','--cached','--name-status','--',x['path']).decode().split('\t')[0]
        blob=git(root,'show',':'+x['path'])
        if op!=x['operation'] or hashlib.sha256(blob).hexdigest()!=x['sha256']:raise ValueError('Staged operation/blob mismatch')
    return git(root,'write-tree').decode().strip()


def publication_stage(root,token,review):
    d,pi=publication_context(root,token);validate_review(root,d,review)
    if git(root,'diff','--cached','--name-only','-z'):raise ValueError('Unexpected pre-staged files')
    if review['initial_index_sha256']!=d['baseline']['index_sha256']:raise ValueError('Initial index mismatch')
    before=d['baseline'];git(root,'add','--',*[x['path'] for x in review['entries']]);tree=verify_index(root,review);after=state(root)
    if after['files']!=before['files'] or any(after[k]!=before[k] for k in ['branch','head']):raise ValueError('Concurrent worktree change while staging')
    d['baseline']=after;d['publication']={'phase':'GOVERNED_STAGE','review':review,'review_sha256':row_digest(review),'tree':tree,'initial_state':before,'remote':pi['publication']['remote'],'remote_url':git(root,'remote','get-url','--push',pi['publication']['remote']).decode().strip()};save_lease(root,d)
    return {'status':'GOVERNED_STAGE','tree':tree,'paths':len(review['entries'])}


def publication_guards(root,review):
    import ast
    paths=[x['path'] for x in review['entries']]
    if staged_guard(root) or secrets(root,paths):raise ValueError('Publication staged/secret guard failed')
    for name in paths:
        body=git(root,'show',':'+name)
        if name.endswith('.py'):ast.parse(body,filename=name)
        elif name.endswith('.json'):json.loads(body)
        elif name.endswith('.jsonl'):
            for line in body.splitlines():
                if line.strip():json.loads(line)
    result=check(root)
    if result['status']!='PASS':raise ValueError('Governance/bootstrap/handoff consistency failed')
    cmd=['python3','-B',str(root/'tools/continuous_backup.py'),'staged']
    proc=subprocess.run(cmd,cwd=root,capture_output=True,text=True)
    if proc.returncode:raise ValueError('Backup/debt publication gate failed: '+proc.stdout+proc.stderr)
    backup=json.loads(proc.stdout)
    if backup.get('status') not in {'PASS','BACKUP_VERIFIED','BACKUP_DEBT_PI_AUTHORIZED'}:raise ValueError('Backup state blocked')
    return {'governance':result,'backup':backup}


def publication_verify(root,token,validation_path):
    d,pi=publication_context(root,token);pub=d.get('publication',{});review=pub['review'];validate_review(root,d,review)
    tree=verify_index(root,review)
    if tree!=pub['tree']:raise ValueError('Reviewed tree mismatch')
    v=json.loads(safe(root,validation_path).read_text())
    if validation_path not in {x['path'] for x in review['entries']} or v.get('test_exit_code')!=0 or not v.get('publication_tests_passed'):raise ValueError('Reviewed passing test receipt required')
    gates=publication_guards(root,review);pub.update(phase='VERIFY_STAGED_SCOPE',validation_path=validation_path,gates=gates);save_lease(root,d)
    return {'status':'VERIFY_STAGED_SCOPE','backup_state':gates['backup']['status']}


def publication_commit(root,token,message):
    d,pi=publication_context(root,token);pub=d['publication'];review=pub['review']
    if pub['phase']!='VERIFY_STAGED_SCOPE':raise ValueError('Verified staged gate required')
    validate_review(root,d,review)
    if verify_index(root,review)!=pub['tree']:raise ValueError('Verified staged tree changed')
    before=d['baseline'];git(root,'commit','-m',message);after=state(root);head=after['head']
    parents=git(root,'show','-s','--format=%P',head).decode().split()
    paths=git(root,'diff-tree','--no-commit-id','--name-only','-r','-z',head).split(b'\0');paths=sorted(os.fsdecode(x) for x in paths if x)
    if parents!=[review['parent']] or after['branch']!=before['branch'] or git(root,'rev-parse',head+'^{tree}').decode().strip()!=pub['tree'] or paths!=sorted(x['path'] for x in review['entries']) or after['files']!=before['files']:raise ValueError('Unexpected parent/branch/tree or hook-induced change; STOP')
    for x in review['entries']:
        if hashlib.sha256(git(root,'show',head+':'+x['path'])).hexdigest()!=x['sha256']:raise ValueError('Committed blob mismatch')
    if git(root,'diff','--cached','--name-only','-z'):raise ValueError('Unexpected index after commit')
    d['baseline']=after;pub.update(phase='VERIFY_COMMIT',commit=head);save_lease(root,d)
    return {'status':'VERIFY_COMMIT','commit':head}


def publication_push(root,token):
    d,pi=publication_context(root,token);pub=d['publication']
    if pub['phase'] not in {'VERIFY_COMMIT','PUSH_FAILED','REMOTE_MISMATCH'}:raise ValueError('Verified commit required')
    head=pub['commit'];branch=d['baseline']['branch'];remote=pub['remote']
    if git(root,'remote','get-url','--push',remote).decode().strip()!=pub['remote_url']:raise ValueError('Authorized remote changed')
    try:git(root,'push',remote,head+':refs/heads/'+branch)
    except subprocess.CalledProcessError:
        pub['phase']='PUSH_FAILED';save_lease(root,d);raise ValueError('Push failed; PUBLICATION NOT VERIFIED')
    rows=git(root,'ls-remote','--heads',remote,'refs/heads/'+branch).decode().strip().split()
    if not rows or rows[0]!=head:
        pub['phase']='REMOTE_MISMATCH';save_lease(root,d);raise ValueError('Remote mismatch; PUBLICATION NOT VERIFIED')
    if state(root)!=d['baseline']:raise ValueError('Concurrent worktree change during push')
    pub.update(phase='VERIFY_REMOTE_HEAD',remote_head=head,verified_at=now());save_lease(root,d)
    return {'status':'VERIFY_REMOTE_HEAD','commit':head,'remote_head':head,'backup_state':pub['gates']['backup']['status']}


def check(root):
    problems=[];notices=[]
    cfg=load(root,P+'BOOTSTRAP_SOURCES.json')
    paths=cfg['recovery_links']+[x['path'] for x in cfg['sections']]
    registry=load(root,P+'AGENT_REGISTRY.json')
    rows=[json.loads(x) for x in (root/(P+'AGENT_WORK_LEDGER.jsonl')).read_text().splitlines() if x]
    decisions=[json.loads(x) for x in (root/(P+'PI_DECISION_LOG.jsonl')).read_text().splitlines() if x]
    ids={x['decision_id'] for x in decisions}
    resolved,warnings,correction_errors=historical_resolutions(rows,decisions)
    notices.extend(warnings);problems.extend(correction_errors)
    missing_origins={}
    for n,r in enumerate(rows):
        refs=r.get('artifact_paths',[])+r.get('input_authorities',[])
        paths+=refs
        for ref in refs:missing_origins.setdefault(ref,[]).append(n)
        if r.get('PI_authorization',r.get('PI_decision')) not in ids and not any((n,k,None) in resolved for k in ['CORRECTIVE_PI_LINKAGE','HISTORICAL_AUTHORIZATION_UNRESOLVED']):problems.append({'issue':'UNKNOWN_PI_DECISION','task_id':r['task_id']})
    emb=load(root,P+'EMBARGO_REGISTRY.json')
    paths += [r['artifact'] for r in emb['embargoes']]
    for p in sorted(set(paths)):
        if not (root/p).exists():
            origins=missing_origins.get(p,[])
            current_reference=p in cfg['recovery_links'] or any(x['path']==p for x in cfg['sections']) or any(x['artifact']==p for x in emb['embargoes'])
            if current_reference or not origins or not all((n,'HISTORICAL_REFERENCE_RESOLUTION',p) in resolved for n in origins):problems.append({'issue':'MISSING_REFERENCE','path':p})
    for f in [P+'JGA_CHAT_HANDOFF.md',P+'MULTI_AGENT_COORDINATION_STATE.md','docs/JGA_PROJECT_STATE.md','docs/JGA_SCIENTIFIC_STATE.md']:
        t=(root/f).read_text()
        for target in re.findall(r'\]\(([^)]+)\)',t):
            if target.startswith(('http:','https:','#','mailto:')):continue
            if not (root/f).parent.joinpath(target.split('#')[0]).exists():problems.append({'issue':'MISSING_DOCUMENT_LINK','file':f,'target':target})
    handoff=(root/(P+'JGA_CHAT_HANDOFF.md')).read_text()
    s=state(root)
    if not handoff_git_current(root,handoff,s):problems.append({'issue':'HANDOFF_STALE_GIT'})
    sys.path.insert(0,str(root))
    from tools.bootstrap.bootstrap_generator import render_bootstrap
    if (root/'JGA_BOOTSTRAP.md').read_text()!=render_bootstrap(root):
        if cfg.get('production_generation_status','').startswith('DEFERRED') and cfg.get('PI_decision') in ids:
            notices.append({'issue':'BOOTSTRAP_GENERATION_DEFERRED','PI_decision':cfg['PI_decision'],'publication_ready':False})
        else:problems.append({'issue':'BOOTSTRAP_STALE'})
    for a in registry['agents']:
        if a['current_mode'] not in a['allowed_modes']:problems.append({'issue':'AGENT_MODE_INVALID','agent':a['agent_id']})
    # Artifact identifiers mentioned in machine-readable ledgers must resolve.
    known={x['artifact_id'] for x in load(root,P+'EXTERNAL_ARTIFACT_MANIFEST.json')['artifacts']}
    for r in rows:
        for i in r.get('external_artifact_ids',[]):
            if i not in known:problems.append({'issue':'UNREGISTERED_EXTERNAL_ID','artifact_id':i})
    return {'status':'PASS' if not problems else 'FAIL','findings':problems,'notices':notices,'historical_qualifications':warnings,'consistency_classification':'CURRENT_ERROR' if problems else ('PASS_WITH_HISTORICAL_QUALIFICATIONS' if warnings else 'PASS'),'scope':'registered references; immutable historical originals preserved'}

def secrets(root,paths):
    findings=[]
    pattern=re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:gh[pousr]_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16}|sk-[A-Za-z0-9_-]{24,})')
    for name in paths:
        p=safe(root,name)
        if p.is_file() and p.stat().st_size<2*1024*1024 and pattern.search(p.read_text(errors='replace')):
            findings.append({'path':name,'issue':'POSSIBLE_SECRET_REDACTED'})
    return findings

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=ROOT)
    sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('check');sub.add_parser('guard-staged')
    e=sub.add_parser('external');e.add_argument('--mode',choices=['metadata','incremental','full'],default='metadata')
    a=sub.add_parser('acquire');a.add_argument('--agent',required=True);a.add_argument('--task',required=True);a.add_argument('--token',required=True)
    for c in ['check-writer','release','resync','write']:
        p=sub.add_parser(c);p.add_argument('--token',required=True)
        if c=='write':p.add_argument('--target',required=True);p.add_argument('--payload',type=Path,required=True)
        if c=='resync':p.add_argument('--justification',required=True)
    e=sub.add_parser('write-external');e.add_argument('--token',required=True);e.add_argument('--target',required=True);e.add_argument('--payload',type=Path,required=True);e.add_argument('--provenance',type=Path,required=True)
    p=sub.add_parser('secrets');p.add_argument('paths',nargs='+')
    for name in ['publication-stage','publication-verify','publication-commit','publication-push']:
        p=sub.add_parser(name);p.add_argument('--token',required=True)
        if name=='publication-stage':p.add_argument('--review',type=Path,required=True)
        if name=='publication-verify':p.add_argument('--validation-path',required=True)
        if name=='publication-commit':p.add_argument('--message',required=True)
    args=ap.parse_args();root=args.root.resolve()
    try:
        if args.cmd=='check':result=check(root)
        elif args.cmd=='external':result=external_check(root,args.mode)
        elif args.cmd=='guard-staged':
            f=staged_guard(root);result={'status':'FAIL' if f else 'PASS','findings':f}
        elif args.cmd=='secrets':
            f=secrets(root,args.paths);result={'status':'FAIL' if f else 'PASS','findings':f}
        elif args.cmd=='publication-stage':result=publication_stage(root,args.token,json.loads(args.review.read_text()))
        elif args.cmd=='publication-verify':result=publication_verify(root,args.token,args.validation_path)
        elif args.cmd=='publication-commit':result=publication_commit(root,args.token,args.message)
        elif args.cmd=='publication-push':result=publication_push(root,args.token)
        elif args.cmd=='acquire':result=acquire(root,args.agent,args.task,args.token)
        elif args.cmd=='write-external':result=write_external(root,args.token,args.target,args.payload.read_bytes(),json.loads(args.provenance.read_text()))
        elif args.cmd=='release':result=release(root,args.token)
        elif args.cmd=='resync':result=resync(root,args.token,args.justification)
        elif args.cmd=='write':result=write(root,args.token,args.target,args.payload.read_bytes())
        else:lease(root,args.token);result={'status':'CURRENT'}
        print(json.dumps(result,indent=2));return 1 if result.get('status')=='FAIL' or result.get('findings') else 0
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as e:
        print(json.dumps({'status':'FAIL','reason':str(e)}));return 1
if __name__=='__main__':sys.exit(main())
