"""PI-authorized completed-file backup; never delete mirror payloads.
Call check before work, files after EACH completed write, all after a batch,
staged before commit. This is a synchronous workflow gate, not a watcher.
"""
from pathlib import Path
import argparse, datetime, fcntl, hashlib, json, os, shutil, subprocess, sys, tempfile, time
ROOT = Path('/Users/StarTrack/Development/JazzGrooveAnalyzer')
# Historical destination is provenance only, never an implicit active target.
VOLUME = BACKUP_ROOT = MIRROR = None
CONFIGURATION = 'docs/project/BACKUP_CONFIGURATION.json'
SKIP_DIRS = {'.venv','venv','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','.ipynb_checkpoints'}
SKIP_NAMES = {'.DS_Store'}

def digest(p):
    if p.is_symlink():
        b=os.readlink(p).encode(); return hashlib.sha256(b).hexdigest(),len(b),'symlink'
    with p.open('rb') as f: h=hashlib.file_digest(f,'sha256').hexdigest()
    return h,p.stat().st_size,'file'

def excluded(rel):
    cfg=ROOT/CONFIGURATION
    if cfg.is_file():
        c=json.loads(cfg.read_text())
        if any(rel.is_relative_to(Path(x)) or Path(x).is_relative_to(rel) for x in c.get('scientific_evidence_paths',[])):return False
        if c.get('disposable_profiles') and profile_classification(rel)=='DISPOSABLE_REPRODUCIBLE':return True
    return any(x in SKIP_DIRS for x in rel.parts) or rel.name in SKIP_NAMES or rel.name.startswith('._') or rel.suffix in {'.pyc','.pyo','.lock'} or rel.name.endswith('.tmp')

def configuration():
    p=ROOT/CONFIGURATION
    if not p.is_file():raise RuntimeError('BACKUP_BLOCKED: explicit PI-authorized configuration required')
    c=json.loads(p.read_text())
    rows=[json.loads(x) for x in (ROOT/'docs/project/PI_DECISION_LOG.jsonl').read_text().splitlines() if x.strip()]
    matches=[x for x in rows if x.get('decision_id')==c.get('PI_decision')]
    if len(matches)!=1 or matches[0].get('task_id')!=c.get('task_id'):raise RuntimeError('BACKUP_BLOCKED: missing PI linkage')
    d=matches[0]
    if d.get('decision',d.get('status')) not in {'AUTHORIZED_FOR_CURRENT_TASK','APPROVED'}:raise RuntimeError('BACKUP_BLOCKED: PI decision not approved')
    if c['state']=='BACKUP_DEBT_PI_AUTHORIZED':
        debt=d.get('backup_debt')
        fields=['scope','reason','permitted_work','prohibited_work','settlement_condition']
        if not isinstance(debt,dict) or any(not c.get(k) or c[k]!=debt.get(k) for k in fields):raise RuntimeError('BACKUP_BLOCKED: incomplete or unlinked backup debt')
    elif c['state']=='BACKUP_VERIFIED':
        destination=c.get('backup_destination')
        if not destination or destination!=d.get('backup_destination'):raise RuntimeError('BACKUP_BLOCKED: target not explicitly PI authorized')
        target=Path(destination)
        if not target.is_absolute() or '..' in target.parts or any(target.is_relative_to(Path(x)) for x in c.get('prohibited_write_roots',[])):raise RuntimeError('BACKUP_BLOCKED: prohibited target')
        if any(x.is_symlink() for x in [target,*target.parents]):raise RuntimeError('BACKUP_BLOCKED: symlink target')
    else:raise RuntimeError('BACKUP_BLOCKED')
    return c

def publication_debt_authorization(paths=()):
    """Exact PI-linked checkpoint exception; never backup certification."""
    c=configuration()
    rows=[json.loads(x) for x in (ROOT/'docs/project/PI_DECISION_LOG.jsonl').read_text().splitlines() if x.strip()]
    d=next(x for x in rows if x.get('decision_id')==c['PI_decision'])
    if c['state']!='BACKUP_DEBT_PI_AUTHORIZED' or c.get('publication_under_backup_debt') is not True or d.get('publication_under_backup_debt') is not True:
        raise RuntimeError('Publication blocked while backup debt is open')
    if any(str(safe_relative(p)) not in c['scope'] or str(safe_relative(p)) not in d.get('write_paths',[]) for p in paths):
        raise RuntimeError('Publication outside exact PI-authorized checkpoint scope')
    return {'status':'BACKUP_DEBT_PI_AUTHORIZED','PI_decision':c['PI_decision'],'task_id':c['task_id'],'publication_exception':True,'backup_verified':False,'external_write_roots':d.get('external_write_roots',[])}

def preflight():
    global VOLUME,BACKUP_ROOT,MIRROR
    c=configuration()
    if c['state']=='BACKUP_DEBT_PI_AUTHORIZED':
        VOLUME=BACKUP_ROOT=MIRROR=None
        return {'status':'BACKUP_DEBT_PI_AUTHORIZED','PI_decision':c['PI_decision'],'scope':c['scope'],'settlement_condition':c['settlement_condition']}
    BACKUP_ROOT=Path(c['backup_destination']);VOLUME=BACKUP_ROOT.parent;MIRROR=BACKUP_ROOT/'JazzGrooveAnalyzer_CURRENT'
    if not VOLUME.is_mount() or not BACKUP_ROOT.is_dir() or BACKUP_ROOT.stat().st_dev == ROOT.stat().st_dev:
        raise RuntimeError('BACKUP_BLOCKED: CONTINUOUS EXTERNAL BACKUP UNAVAILABLE')
    with tempfile.TemporaryFile(dir=BACKUP_ROOT) as f:
        f.write(b'JGA preflight');f.flush();os.fsync(f.fileno())
    if MIRROR.is_symlink():raise RuntimeError('Mirror must not be a symlink')
    MIRROR.mkdir(exist_ok=True)
    return {'status':'BACKUP_VERIFIED','backup_destination':str(BACKUP_ROOT)}

def profile_classification(rel):
    c=configuration();p=Path(rel)
    if any(p.is_relative_to(Path(x)) for x in c.get('scientific_evidence_paths',[])):return 'SCIENTIFIC_EVIDENCE'
    for x in c.get('disposable_profiles',[]):
        if p.is_relative_to(Path(x['path'])):
            if x.get('classification')!='DISPOSABLE_REPRODUCIBLE' or not x.get('inspection_record') or not x.get('PI_decision'):raise ValueError('Profile exclusion requires explicit inspected authorization')
            rows=[json.loads(y) for y in (ROOT/'docs/project/PI_DECISION_LOG.jsonl').read_text().splitlines() if y.strip()]
            if not any(y.get('decision_id')==x['PI_decision'] and x in y.get('disposable_profiles',[]) for y in rows):raise ValueError('Unlinked disposable profile exclusion')
            return 'DISPOSABLE_REPRODUCIBLE'
    return 'PRESERVE'

def git_head():
    return subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()

def safe_relative(value):
    p=Path(value)
    if p.is_absolute(): p=p.relative_to(ROOT)
    if '..' in p.parts or not p.parts or p == Path('.') or p.name == 'BACKUP_LOG.jsonl': raise ValueError('Unsafe/reserved path')
    # Never traverse source or destination symlink directories.
    for root in (ROOT,MIRROR):
        if root is None:continue
        for parent in p.parents:
            if (root/parent).is_symlink(): raise ValueError('Symlink parent: '+str(root/parent))
    return p

def backup_file(rel):
    status=preflight();rel=safe_relative(rel)
    if status['status']=='BACKUP_DEBT_PI_AUTHORIZED':
        if str(rel) not in status['scope']:raise ValueError('Outside PI-authorized backup-debt scope')
        h,size,kind=digest(ROOT/rel)
        return {**status,'path':str(rel),'sha256':h,'size':size,'type':kind,'operation':'LOCAL_ONLY_NOT_BACKED_UP'}
    if profile_classification(rel)=='DISPOSABLE_REPRODUCIBLE':raise ValueError('Explicit disposable profile excluded')
    if excluded(rel): raise ValueError('Disposable path excluded: '+str(rel))
    src=ROOT/rel; dst=MIRROR/rel
    before=src.lstat(); h,size,kind=digest(src)
    if (before.st_size,before.st_mtime_ns,before.st_ino)!=(src.lstat().st_size,src.lstat().st_mtime_ns,src.lstat().st_ino): raise RuntimeError('Source changing: '+str(rel))
    exists=dst.exists() or dst.is_symlink()
    if exists and digest(dst)==(h,size,kind): return {'path':str(rel),'sha256':h,'size':size,'type':kind,'operation':'UNCHANGED_VERIFIED'}
    dst.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.jga-copy-',dir=dst.parent); os.close(fd); tmp=Path(name)
    try:
        if kind=='symlink': tmp.unlink(); tmp.symlink_to(os.readlink(src))
        else:
            with src.open('rb') as i,tmp.open('wb') as o:
                shutil.copyfileobj(i,o,8*1024*1024);o.flush();os.fsync(o.fileno())
            shutil.copystat(src,tmp)
        after=src.lstat()
        if (before.st_size,before.st_mtime_ns,before.st_ino)!=(after.st_size,after.st_mtime_ns,after.st_ino): raise RuntimeError('Source changed during copy: '+str(rel))
        if digest(tmp)!=(h,size,kind): raise RuntimeError('BACKUP VERIFICATION FAILURE: '+str(rel))
        os.replace(tmp,dst)
        external,external_size,external_kind=digest(dst)
        if (external,external_size,external_kind)!=(h,size,kind): raise RuntimeError('BACKUP VERIFICATION FAILURE: '+str(rel))
        now=datetime.datetime.now(datetime.timezone.utc)
        rec={'utc':now.isoformat(),'local_timestamp':now.astimezone().isoformat(),'repository_relative_path':str(rel),'operation':'UPDATE' if exists else 'CREATE','local_sha256':h,'external_sha256':external,'size_bytes':size,'verification_status':'PASS','git_head':git_head(),'type':kind}
        log=MIRROR/'BACKUP_LOG.jsonl'
        if log.is_symlink(): raise RuntimeError('Unsafe log symlink')
        with log.open('a') as f:
            fcntl.flock(f,fcntl.LOCK_EX); f.write(json.dumps(rec)+'\n');f.flush();os.fsync(f.fileno())
        return {'path':str(rel),'sha256':h,'size':size,'type':kind,'operation':rec['operation']}
    finally:
        if tmp.exists() or tmp.is_symlink(): tmp.unlink() # only this invocation's disposable temp

def inventory():
    result=[]
    for d,dirs,files in os.walk(ROOT,followlinks=False):
        dirs.sort();files.sort()
        for n in dirs[:]:
            p=Path(d)/n; rel=p.relative_to(ROOT)
            if excluded(rel): dirs.remove(n)
            elif p.is_symlink():result.append(rel);dirs.remove(n)
        result.extend((Path(d)/n).relative_to(ROOT) for n in files if not excluded((Path(d)/n).relative_to(ROOT)))
    return sorted(result)

def atomic_write_and_backup(rel,data):
    status=preflight();rel=safe_relative(rel)
    if status['status']=='BACKUP_DEBT_PI_AUTHORIZED' and str(rel) not in status['scope']:raise ValueError('Outside PI-authorized backup-debt scope')
    p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.jga-write-',dir=p.parent)
    try:
        with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
        if p.exists():os.chmod(name,p.stat().st_mode)
        os.replace(name,p)
        return backup_file(rel)
    finally:
        if os.path.exists(name):os.unlink(name)

def atomic_external_write_and_backup(path,data):
    if preflight()['status']!='BACKUP_VERIFIED':raise RuntimeError('BACKUP_BLOCKED: external persistent outputs require verified backup')
    c=configuration();p=Path(path);primary=Path(c['primary_scientific_root'])
    decisions=[json.loads(x) for x in (ROOT/'docs/project/PI_DECISION_LOG.jsonl').read_text().splitlines() if x.strip()]
    decision=next(x for x in decisions if x.get('decision_id')==c['PI_decision'])
    if decision.get('primary_scientific_root')!=str(primary):raise ValueError('Primary scientific root must be explicitly PI linked')
    if not p.is_absolute() or '..' in p.parts or not p.is_relative_to(primary):raise ValueError('Outside primary scientific root')
    if any(x.is_symlink() for x in [p,*p.parents]):raise ValueError('External symlink prohibited')
    if p.exists():raise ValueError('Existing scientific output preserved')
    dest=BACKUP_ROOT/'SSD_TRACK_JGA'/'JGA'/p.relative_to(primary)
    if any(x.is_symlink() for x in [dest,*dest.parents]):raise ValueError('Backup symlink prohibited')
    # Install primary without overwrite, then copy/hash verify the completed bytes.
    for output in (p,dest):
        output.parent.mkdir(parents=True,exist_ok=True)
        if output.exists():
            if digest(output)[0]!=hashlib.sha256(data).hexdigest():raise ValueError('Different existing backup preserved')
            continue
        fd,n=tempfile.mkstemp(prefix='.jga-output-',dir=output.parent)
        try:
            with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
            if output.exists():raise ValueError('Concurrent destination creation')
            os.replace(n,output)
        finally:
            if os.path.exists(n):os.unlink(n)
        if digest(output)[:2]!=(hashlib.sha256(data).hexdigest(),len(data)):raise RuntimeError('BACKUP VERIFICATION FAILURE')
    return {'status':'BACKUP_VERIFIED','path':str(p),'backup':str(dest),'sha256':digest(p)[0],'size':len(data)}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('mode',choices=['check','files','all','staged']);ap.add_argument('paths',nargs='*');args=ap.parse_args()
    status=preflight()
    if args.mode=='check':print(json.dumps(status));return
    if status['status']=='BACKUP_DEBT_PI_AUTHORIZED':
        if args.mode=='all':raise RuntimeError('BACKUP_DEBT_PI_AUTHORIZED: inventory certification blocked')
        if args.mode=='staged':publication_debt_authorization()
    if args.mode=='all':paths=inventory()
    elif args.mode=='staged':
        raw=subprocess.check_output(['git','diff','--cached','--name-only','--diff-filter=ACMRT','-z'],cwd=ROOT)
        paths=[Path(p.decode()) for p in raw.split(b'\0') if p]
        if status['status']=='BACKUP_DEBT_PI_AUTHORIZED':
            publication_debt_authorization(paths)
            deleted=subprocess.check_output(['git','diff','--cached','--name-only','--diff-filter=D','-z'],cwd=ROOT)
            if deleted:raise RuntimeError('Checkpoint backup-debt exception does not authorize staged deletion')
        for p in paths:
            if excluded(p):raise RuntimeError('Excluded file staged: '+str(p))
            blob=subprocess.check_output(['git','show',':'+p.as_posix()],cwd=ROOT)
            if hashlib.sha256(blob).hexdigest()!=digest(ROOT/p)[0]:raise RuntimeError('Staged bytes differ from working file: '+str(p))
    else:paths=[Path(p) for p in args.paths]
    if args.mode=='files' and not paths:raise ValueError('Provide completed file paths')
    rows=[];last=time.monotonic()
    for p in paths:
        rows.append(backup_file(p))
        if time.monotonic()-last>30:print(json.dumps({'verified':len(rows),'total':len(paths)}),flush=True);last=time.monotonic()
    if args.mode=='all':
        if inventory()!=paths:raise RuntimeError('Repository inventory changed during backup; stop and review')
        for r in rows:
            expected=(r['sha256'],r['size'],r['type'])
            if digest(ROOT/r['path'])!=expected or digest(MIRROR/r['path'])!=expected:raise RuntimeError('BACKUP VERIFICATION FAILURE in final inventory: '+r['path'])
    print(json.dumps({'status':status['status'],'mode':args.mode,'files':len(rows),'bytes':sum(r['size'] for r in rows),'mirror':str(MIRROR),'deleted_backup_files':0}),flush=True)
if __name__=='__main__':
    try:main()
    except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
