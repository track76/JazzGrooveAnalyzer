"""PI-authorized completed-file backup; never delete mirror payloads.
Call check before work, files after EACH completed write, all after a batch,
staged before commit. This is a synchronous workflow gate, not a watcher.
"""
from pathlib import Path
import argparse, datetime, fcntl, hashlib, json, os, shutil, subprocess, sys, tempfile, time
ROOT = Path('/Users/StarTrack/Development/JazzGrooveAnalyzer')
VOLUME = Path('/Volumes/HD BackUp')
BACKUP_ROOT = VOLUME / 'JGA_BACKUP'
MIRROR = BACKUP_ROOT / 'JazzGrooveAnalyzer_CURRENT'
SKIP_DIRS = {'.venv','venv','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','.ipynb_checkpoints'}
SKIP_NAMES = {'.DS_Store'}

def digest(p):
    if p.is_symlink():
        b=os.readlink(p).encode(); return hashlib.sha256(b).hexdigest(),len(b),'symlink'
    with p.open('rb') as f: h=hashlib.file_digest(f,'sha256').hexdigest()
    return h,p.stat().st_size,'file'

def excluded(rel):
    return any(x in SKIP_DIRS for x in rel.parts) or rel.name in SKIP_NAMES or rel.name.startswith('._') or rel.suffix in {'.pyc','.pyo','.lock'} or rel.name.endswith('.tmp')

def preflight():
    if not VOLUME.is_mount() or not BACKUP_ROOT.is_dir() or BACKUP_ROOT.stat().st_dev == ROOT.stat().st_dev:
        raise RuntimeError('CONTINUOUS EXTERNAL BACKUP UNAVAILABLE: ask PI to stop or explicitly authorize local backup debt')
    with tempfile.TemporaryFile(dir=BACKUP_ROOT) as f:
        f.write(b'JGA preflight'); f.flush(); os.fsync(f.fileno())
    if MIRROR.is_symlink(): raise RuntimeError('Mirror must not be a symlink')
    MIRROR.mkdir(exist_ok=True)

def git_head():
    return subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()

def safe_relative(value):
    p=Path(value)
    if p.is_absolute(): p=p.relative_to(ROOT)
    if '..' in p.parts or not p.parts or p == Path('.') or p.name == 'BACKUP_LOG.jsonl': raise ValueError('Unsafe/reserved path')
    # Never traverse source or destination symlink directories.
    for root in (ROOT,MIRROR):
        for parent in p.parents:
            if (root/parent).is_symlink(): raise ValueError('Symlink parent: '+str(root/parent))
    return p

def backup_file(rel):
    rel=safe_relative(rel)
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
    preflight(); rel=safe_relative(rel);p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.jga-write-',dir=p.parent)
    try:
        with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
        if p.exists():os.chmod(name,p.stat().st_mode)
        os.replace(name,p)
        return backup_file(rel)
    finally:
        if os.path.exists(name):os.unlink(name)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('mode',choices=['check','files','all','staged']);ap.add_argument('paths',nargs='*');args=ap.parse_args()
    preflight()
    if args.mode=='check':print('CONTINUOUS EXTERNAL BACKUP AVAILABLE');return
    if args.mode=='all':paths=inventory()
    elif args.mode=='staged':
        raw=subprocess.check_output(['git','diff','--cached','--name-only','--diff-filter=ACMRT','-z'],cwd=ROOT)
        paths=[Path(p.decode()) for p in raw.split(b'\0') if p]
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
    print(json.dumps({'status':'PASS','mode':args.mode,'files':len(rows),'bytes':sum(r['size'] for r in rows),'mirror':str(MIRROR),'deleted_backup_files':0}),flush=True)
if __name__=='__main__':
    try:main()
    except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
