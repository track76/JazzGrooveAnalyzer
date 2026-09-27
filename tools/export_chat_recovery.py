#!/usr/bin/env python3
"""Export the two-file ChatGPT recovery package from a committed Git revision.
Git export-subst embeds the actual commit hash without a self-referential commit.
No scientific files are rendered or changed.
"""
from pathlib import Path
import argparse,datetime,hashlib,io,json,os,subprocess,tarfile,tempfile
ROOT=Path(__file__).resolve().parents[1]
FILES=['JGA_BOOTSTRAP.md','docs/project/JGA_CHAT_HANDOFF.md']

def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args])
def export_payloads(root,revision='HEAD'):
    head=git(root,'rev-parse',revision+'^{commit}').decode().strip()
    touched=git(root,'log','-1','--format=%H',head,'--',FILES[1]).decode().strip()
    if touched!=head:raise ValueError('HANDOFF_STALE: final revision must include handoff synchronization')
    raw=git(root,'archive','--format=tar',head,*FILES)
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        data={Path(p).name:archive.extractfile(p).read() for p in FILES}
    text=data['JGA_CHAT_HANDOFF.md'].decode()
    if '$Format:%H$' in text or head not in text:raise ValueError('Recovery HEAD substitution failed')
    return head,data

def install_immutable(p,data):
    digest=hashlib.sha256(data).hexdigest();p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        if hashlib.sha256(p.read_bytes()).hexdigest()!=digest:raise ValueError('Refuse overwrite of different recovery payload: '+str(p))
        return digest
    fd,n=tempfile.mkstemp(prefix='.recovery-',dir=p.parent)
    try:
        with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
        # One authorized writer; rename works on the existing ExFAT SSD (hard links do not).
        if p.exists():raise ValueError('Concurrent recovery destination creation; STOP')
        os.replace(n,p)
    finally:
        if os.path.exists(n):os.unlink(n)
    if hashlib.sha256(p.read_bytes()).hexdigest()!=digest:raise ValueError('Recovery verification failed')
    return digest

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--destination',type=Path,required=True);args=ap.parse_args()
    from continuous_backup import preflight,BACKUP_ROOT
    preflight();root=Path(os.environ['JGA_EXTERNAL_ROOT']).resolve();dst=args.destination.resolve()
    if not dst.is_relative_to(root):raise ValueError('Recovery export must use authorized external JGA root')
    head,data=export_payloads(ROOT)
    branch=git(ROOT,'branch','--show-current').decode().strip()
    line=git(ROOT,'ls-remote','--heads','origin',branch).decode().strip().split()
    if not line or line[0]!=head:raise ValueError('Remote HEAD mismatch; no final recovery export')
    mirror=BACKUP_ROOT/'SSD_TRACK_JGA'/'JGA'/dst.relative_to(root)
    hashes={}
    for name,body in data.items():
        hashes[name]=install_immutable(dst/name,body);assert install_immutable(mirror/name,body)==hashes[name]
    manifest={'status':'VERIFIED','git_head':head,'remote_head_verified':head,'branch':branch,'commit_time':git(ROOT,'show','-s','--format=%cI',head).decode().strip(),'source':'git archive with export-subst','files':hashes,'backup':str(mirror),'historical_SSD_inventory':'NOT FULLY CERTIFIED','scientific_work_authorized':False}
    payload=(json.dumps(manifest,indent=2)+'\n').encode();install_immutable(dst/'EXPORT_MANIFEST.json',payload);install_immutable(mirror/'EXPORT_MANIFEST.json',payload)
    print(json.dumps({'status':'PASS','HEAD':head,'destination':str(dst),'backup':str(mirror)}))
if __name__=='__main__':main()
