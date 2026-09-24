"""PI-authorized versioned complete backup. No deletion or overwrite; no science."""
from pathlib import Path
import os,sys,json,hashlib,datetime,subprocess,shutil,time
ROOT=Path(__file__).resolve().parents[4];PKG=Path(__file__).resolve().parent
DESTROOT=Path('/Volumes/HD BackUp/JGA_BACKUP');SSD=Path('/Volumes/SSD Track/JGA')
EXCLUDED_DIRS={'.venv','venv','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','.cache','.ipynb_checkpoints'}
EXCLUDED_FILES={'.DS_Store'}
sha=lambda p:hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()
def git(*args,cwd=ROOT):return subprocess.check_output(['git',*args],cwd=cwd,text=True).strip()
def main():
 assert DESTROOT.is_dir() and SSD.is_dir()
 assert os.stat(DESTROOT).st_dev!=os.stat(ROOT).st_dev and os.stat(DESTROOT).st_dev!=os.stat(SSD).st_dev
 commit=git('rev-parse','HEAD');branch=git('branch','--show-current');assert branch=='scientific/translation-layer-finalization'
 final=json.load(open(PKG/'FINAL_FREEZE.json'));assert sha(PKG/'MANIFEST.json')==final['final_baseline_freeze_sha256']
 assert git('rev-parse','refs/remotes/origin/'+branch)==commit
 stamp=datetime.datetime.now().strftime('%Y%m%dT%H%M%S');dest=DESTROOT/f'JazzGrooveAnalyzer_BACKUP_{stamp}_BEST_BASS_BASELINE_{commit[:12]}'
 assert not dest.exists()
 entries=[];excluded=[]
 for source,prefix in [(ROOT,'JazzGrooveAnalyzer'),(SSD,'SSD_TRACK_JGA/JGA')]:
  for d,dirs,files in os.walk(source,followlinks=False):
   dirs.sort();files.sort();kept=[]
   for n in dirs:
    p=Path(d)/n
    if n in EXCLUDED_DIRS:excluded.append(str(p));continue
    if p.is_symlink():entries.append((p,prefix+'/'+str(p.relative_to(source))))
    else:kept.append(n)
   dirs[:]=kept
   for n in files:
    p=Path(d)/n
    if n in EXCLUDED_FILES or n.startswith('._') or p.suffix in ['.pyc','.pyo']:excluded.append(str(p));continue
    if not (p.is_file() or p.is_symlink()):raise RuntimeError('Unsupported source entry '+str(p))
    entries.append((p,prefix+'/'+str(p.relative_to(source))))
 total=sum(p.lstat().st_size if not p.is_symlink() else len(os.readlink(p).encode()) for p,_ in entries)
 assert shutil.disk_usage(DESTROOT).free>total+5_000_000_000
 dest.mkdir();meta={'source_repository':str(ROOT),'source_data':str(SSD),'destination':str(dest),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'branch':branch,'commit':commit,'baseline_freeze_sha256':final['final_baseline_freeze_sha256'],'bootstrap_sha256':sha(ROOT/'JGA_BOOTSTRAP.md'),'planned_file_count':len(entries),'planned_bytes':total,'excluded_disposable_paths':excluded,'count_scope':'Source regular files plus symlinks; backup-created manifests/receipts excluded to avoid self-reference. Symlinks hashed as UTF-8 link text; Python system binaries must be reinstalled, not represented as bundled project data.'}
 (dest/'BACKUP_IN_PROGRESS.json').write_text(json.dumps(meta,indent=2)+'\n')
 print(json.dumps({'destination':str(dest),'files':len(entries),'bytes':total}),flush=True)
 records=[];done=0;last=time.monotonic()
 with open(dest/'BACKUP_SHA256SUMS.txt','x') as sums:
  for p,rel in entries:
   q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True)
   if p.is_symlink():
    target=os.readlink(p);q.symlink_to(target);h=hashlib.sha256(target.encode()).hexdigest();assert os.readlink(q)==target;size=len(target.encode());kind='symlink'
   else:
    before=p.stat();hsh=hashlib.sha256()
    with p.open('rb') as src,q.open('xb') as out:
     while True:
      buf=src.read(8*1024*1024)
      if not buf:break
      hsh.update(buf);out.write(buf)
    shutil.copystat(p,q);after=p.stat();assert (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns),('Source changed',str(p))
    h=hsh.hexdigest();assert sha(q)==h,('Backup hash mismatch',rel);size=before.st_size;kind='file'
   records.append({'relative_path':rel,'size':size,'sha256':h,'type':kind});done+=size;sums.write(h+'  '+rel+'\n')
   if time.monotonic()-last>30:
    sums.flush();print(json.dumps({'verified_files':len(records),'total_files':len(entries),'verified_GB':round(done/1e9,3),'total_GB':round(total/1e9,3)}),flush=True);last=time.monotonic()
 assert done==total and len(records)==len(entries)
 # Independently enumerate destination payload after all copies.
 actual=[]
 for prefix in ['JazzGrooveAnalyzer','SSD_TRACK_JGA/JGA']:
  for d,dirs,files in os.walk(dest/prefix,followlinks=False):
   for n in dirs[:]:
    p=Path(d)/n
    if p.is_symlink():actual.append(p);dirs.remove(n)
   actual.extend(Path(d)/n for n in files)
 assert len(actual)==len(records)
 assert sum(len(os.readlink(p).encode()) if p.is_symlink() else p.stat().st_size for p in actual)==total
 repo=dest/'JazzGrooveAnalyzer';assert git('rev-parse','HEAD',cwd=repo)==commit and git('branch','--show-current',cwd=repo)==branch
 critical=['JGA_BOOTSTRAP.md',str((PKG/'MANIFEST.json').relative_to(ROOT)),str((PKG/'FINAL_FREEZE.json').relative_to(ROOT)),'docs/scientific/rfc/JGA_BASS_BEST_VALIDATED_BASELINE_20260924.md','docs/scientific/rfc/JGA_LEARNED_LOCAL_ATTACK_SELECTOR_20260924/development/output/MODEL.joblib','docs/scientific/rfc/JGA_BASS_V1_HISTORICAL_TRANSFER_20260924/JGA_BASS_V1_HISTORICAL_REPORT.md']
 for rel in critical:assert (repo/rel).is_file() and sha(repo/rel)==sha(ROOT/rel),rel
 assert (repo/'.git').is_dir()
 meta.update({'file_count':len(records),'total_bytes':total,'hash_verification':'PASS (every source regular file streamed SHA256 and destination independently reread; every symlink text verified)','recovery_check':'PASS','critical_files':critical,'files':records,'status':'VERIFIED'})
 (dest/'BACKUP_MANIFEST.txt').write_text(json.dumps(meta,indent=2)+'\n')
 receipt={k:v for k,v in meta.items() if k not in ['files','excluded_disposable_paths']};receipt['backup_manifest_sha256']=sha(dest/'BACKUP_MANIFEST.txt');receipt['backup_checksums_sha256']=sha(dest/'BACKUP_SHA256SUMS.txt')
 (dest/'BACKUP_VERIFIED_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2),flush=True)
if __name__=='__main__':main()
