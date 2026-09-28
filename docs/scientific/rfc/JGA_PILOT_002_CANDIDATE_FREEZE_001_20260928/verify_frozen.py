#!/usr/bin/env python3
"""Fail-closed frozen evidence gate; never extract, rank, alter or analyze audio."""
from pathlib import Path
import argparse,json,hashlib
ROOT=Path(__file__).resolve().parents[4]
FREEZE=Path(__file__).with_name('FREEZE_RECORD.json')
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--method-p',type=Path);ap.add_argument('--method-d',type=Path);a=ap.parse_args();f=json.loads(FREEZE.read_text())
 for p,h in f['package_file_hashes'].items():
  if sha(ROOT/p)!=h:raise ValueError('FROZEN_SOURCE_HASH_MISMATCH: '+p)
 for e in f['external_evidence']:
  if sha(e['path'])!=e['sha256'] or sha(e['backup_path'])!=e['sha256']:raise ValueError('EXTERNAL_EVIDENCE_OR_BACKUP_MISMATCH')
 for arm,counts in f['counts'].items():
  for name,n in counts.items():
   if len(json.loads((ROOT/f['package']/arm/(name+'.json')).read_text()))!=n:raise ValueError('COUNT_MISMATCH')
 if bool(a.method_p)!=bool(a.method_d):raise ValueError('BOTH_METHOD_SOURCE_MANIFESTS_REQUIRED')
 if a.method_p:
  for p in [a.method_p,a.method_d]:
   m=json.loads(p.read_text())
   if m.get('freeze_id')!=f['freeze_id'] or m.get('source_sha256')!=f['candidate_and_cluster_hashes'] or m.get('external_evidence_sha256')!=f['external_evidence'][0]['sha256']:raise ValueError('METHOD_SOURCE_IDENTITY_MISMATCH')
 print(json.dumps({'status':'PASS','freeze_id':f['freeze_id'],'package_files':len(f['package_file_hashes']),'method_manifests_checked':bool(a.method_p),'scientific_promotion':False}))
if __name__=='__main__':main()
