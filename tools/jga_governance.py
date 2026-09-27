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

def acquire(root,agent,task,token):
    registry=load(root,P+'AGENT_REGISTRY.json')
    a=next((a for a in registry['agents'] if a['agent_id']==agent),None)
    if not a or a['write_authority_status']!='AUTHORIZED_FOR_CURRENT_TASK' or a['current_task']!=task or a.get('current_mode') not in {'AUTHORIZED_WRITER','EXPERIMENTAL_ENGINEER'} or a.get('current_mode') not in a.get('allowed_modes',[]):
        raise ValueError('No current registered writer authorization')
    ledger=[json.loads(x) for x in (root/(P+'AGENT_WORK_LEDGER.jsonl')).read_text().splitlines() if x]
    records=[x for x in ledger if x['task_id']==task]
    if not records or not records[-1].get('write_paths'): raise ValueError('No registered write scope')
    payload={'agent':agent,'task':task,'token':token,'acquired_at':now(),'write_paths':records[-1]['write_paths'],'baseline':state(root)}
    lock=lock_path(root)
    fd=os.open(lock,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as f: json.dump(payload,f);f.flush();os.fsync(f.fileno())
    return {'status':'ACQUIRED','agent':agent,'task':task}

def lease(root,token,check=True):
    p=lock_path(root);d=json.loads(p.read_text())
    if d['token']!=token: raise ValueError('Writer token mismatch')
    if check and d['baseline']!=state(root): raise ValueError('STALE STATE — RESYNC REQUIRED; no automatic merge or baseline refresh')
    return d

def write(root,token,target,payload):
    d=lease(root,token)
    if target not in d['write_paths']: raise ValueError('Path outside PI-authorized task scope')
    safe(root,target)
    sys.path.insert(0,str(root/'tools'))
    import continuous_backup as backup
    if root.resolve()!=backup.ROOT.resolve(): raise ValueError('Backup authority/root mismatch')
    backup.atomic_write_and_backup(target,payload)
    after=state(root);before=d['baseline']
    a=dict(after['files']);b=dict(before['files']);a.pop(target,None);b.pop(target,None)
    if a!=b or any(after[k]!=before[k] for k in ['branch','head','index_sha256']):
        raise ValueError('Unexpected concurrent modification; stop for PI review')
    d['baseline']=after
    p=lock_path(root);tmp=p.with_suffix('.tmp')
    with tmp.open('w') as f:json.dump(d,f);f.flush();os.fsync(f.fileno())
    os.replace(tmp,p)
    return {'status':'WRITTEN_AND_BACKED_UP','path':target}

def release(root,token):
    d=lease(root,token);lock_path(root).unlink()  # only owner deletes its own verified lease
    return {'status':'RELEASED','task':d['task']}

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

def check(root):
    problems=[]
    cfg=load(root,P+'BOOTSTRAP_SOURCES.json')
    paths=cfg['recovery_links']+[x['path'] for x in cfg['sections']]
    registry=load(root,P+'AGENT_REGISTRY.json')
    rows=[json.loads(x) for x in (root/(P+'AGENT_WORK_LEDGER.jsonl')).read_text().splitlines() if x]
    decisions=[json.loads(x) for x in (root/(P+'PI_DECISION_LOG.jsonl')).read_text().splitlines() if x]
    ids={x['decision_id'] for x in decisions}
    for r in rows:
        paths+=r.get('artifact_paths',[])+r.get('input_authorities',[])
        if r['PI_authorization'] not in ids:problems.append({'issue':'UNKNOWN_PI_DECISION','task_id':r['task_id']})
    emb=load(root,P+'EMBARGO_REGISTRY.json')
    paths += [r['artifact'] for r in emb['embargoes']]
    for p in sorted(set(paths)):
        if not (root/p).exists():problems.append({'issue':'MISSING_REFERENCE','path':p})
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
    if (root/'JGA_BOOTSTRAP.md').read_text()!=render_bootstrap(root):problems.append({'issue':'BOOTSTRAP_STALE'})
    for a in registry['agents']:
        if a['current_mode'] not in a['allowed_modes']:problems.append({'issue':'AGENT_MODE_INVALID','agent':a['agent_id']})
    # Artifact identifiers mentioned in machine-readable ledgers must resolve.
    known={x['artifact_id'] for x in load(root,P+'EXTERNAL_ARTIFACT_MANIFEST.json')['artifacts']}
    for r in rows:
        for i in r.get('external_artifact_ids',[]):
            if i not in known:problems.append({'issue':'UNREGISTERED_EXTERNAL_ID','artifact_id':i})
    return {'status':'PASS' if not problems else 'FAIL','findings':problems,'scope':'registered references; historical files are not repaired automatically'}

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
    for c in ['check-writer','release','write']:
        p=sub.add_parser(c);p.add_argument('--token',required=True)
        if c=='write':p.add_argument('--target',required=True);p.add_argument('--payload',type=Path,required=True)
    p=sub.add_parser('secrets');p.add_argument('paths',nargs='+')
    args=ap.parse_args();root=args.root.resolve()
    try:
        if args.cmd=='check':result=check(root)
        elif args.cmd=='external':result=external_check(root,args.mode)
        elif args.cmd=='guard-staged':
            f=staged_guard(root);result={'status':'FAIL' if f else 'PASS','findings':f}
        elif args.cmd=='secrets':
            f=secrets(root,args.paths);result={'status':'FAIL' if f else 'PASS','findings':f}
        elif args.cmd=='acquire':result=acquire(root,args.agent,args.task,args.token)
        elif args.cmd=='release':result=release(root,args.token)
        elif args.cmd=='write':result=write(root,args.token,args.target,args.payload.read_bytes())
        else:lease(root,args.token);result={'status':'CURRENT'}
        print(json.dumps(result,indent=2));return 1 if result.get('status')=='FAIL' or result.get('findings') else 0
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as e:
        print(json.dumps({'status':'FAIL','reason':str(e)}));return 1
if __name__=='__main__':sys.exit(main())
