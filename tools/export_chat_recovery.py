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
    import continuous_backup as backup
    backup_state=backup.preflight()['status']
    exception=backup.publication_debt_authorization() if backup_state=='BACKUP_DEBT_PI_AUTHORIZED' else None
    if backup_state not in {'BACKUP_VERIFIED','BACKUP_DEBT_PI_AUTHORIZED'}:raise ValueError('Publication blocked')
    root=Path(os.environ['JGA_EXTERNAL_ROOT']).resolve();dst=args.destination.resolve()
    if not dst.is_relative_to(root):raise ValueError('Recovery export must use authorized external JGA root')
    if exception and not any(dst.is_relative_to(Path(p)) for p in exception['external_write_roots']):raise ValueError('Recovery destination outside PI-authorized checkpoint scope')
    if exception:
        import jga_governance as governance
        lease=governance.lease(ROOT,os.environ.get('JGA_WRITER_TOKEN',''))
        if lease['task']!=exception['task_id'] or not any(dst.is_relative_to(Path(p)) for p in lease.get('external_write_roots',[])):raise ValueError('Recovery export requires current task writer lease')
    head,data=export_payloads(ROOT)
    branch=git(ROOT,'branch','--show-current').decode().strip()
    line=git(ROOT,'ls-remote','--heads','origin',branch).decode().strip().split()
    if not line or line[0]!=head:raise ValueError('Remote HEAD mismatch; no final recovery export')
    mirror=None if exception else backup.BACKUP_ROOT/'SSD_TRACK_JGA'/'JGA'/dst.relative_to(root)
    hashes={}
    def install(path,body):
        if exception:governance.lease(ROOT,os.environ.get('JGA_WRITER_TOKEN',''))
        digest=install_immutable(path,body)
        if exception:
            lease['external_baseline'][str(path)]=governance.external_state([str(path)])[str(path)]
            governance.save_lease(ROOT,lease)
        return digest
    for name,body in data.items():
        hashes[name]=install(dst/name,body)
        if mirror is not None:assert install_immutable(mirror/name,body)==hashes[name]
    manifest={'status':'VERIFIED','git_head':head,'remote_head_verified':head,'branch':branch,'commit_time':git(ROOT,'show','-s','--format=%cI',head).decode().strip(),'source':'git archive with export-subst','files':hashes,'backup':str(mirror) if mirror is not None else None,'backup_state':backup_state,'PI_publication_exception':exception,'historical_SSD_inventory':'NOT FULLY CERTIFIED','scientific_work_authorized':False,'task_id':lease['task'] if exception else None,'PI_decision':lease['PI_decision'] if exception else None,'artifact_identity':'CHAT_RECOVERY_EXPORT-'+head,'authority_classification':'COMMITTED_RECOVERY_EXPORT_NOT_SCIENTIFIC_EVIDENCE'}
    payload=(json.dumps(manifest,indent=2)+'\n').encode();install(dst/'EXPORT_MANIFEST.json',payload)
    if mirror is not None:install_immutable(mirror/'EXPORT_MANIFEST.json',payload)
    print(json.dumps({'status':'PASS','HEAD':head,'destination':str(dst),'backup':str(mirror) if mirror is not None else None,'backup_state':backup_state}))
if __name__=='__main__':main()
