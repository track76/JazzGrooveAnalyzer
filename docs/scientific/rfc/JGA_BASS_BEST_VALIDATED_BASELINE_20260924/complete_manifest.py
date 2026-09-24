"""Resume documentation/preservation only; never execute scientific experiments."""
from pathlib import Path
import json,hashlib,datetime,subprocess
P=Path(__file__).resolve().parent;ROOT=P.parents[3];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
old=json.load(open(P/'BASELINE_FREEZE.json'));oldhash=sha(P/'BASELINE_FREEZE.json');assert oldhash=='fd768ec83bc77a5e32938bed743edef10d1355d0c1a961c623be5ea4728b850d'
for e in old['entries']:
 p=Path(old['roots'][e['root']])/e['relative_path'];assert p.stat().st_size==e['size'] and sha(p)==e['sha256'],e['relative_path']
assert not (P/'MANIFEST.json').exists()
public=P.parent/'JGA_BASS_BEST_VALIDATED_BASELINE_20260924.md';(P/'RECOVERY_PUBLIC_AUTHORITY.md').write_bytes(public.read_bytes())
text=(P/'AUTHORITY_CORE.md').read_text().split('## Package and hash convention')[0]
text+='''## Definitive milestone identity and recovery

The definitive Bass baseline freeze SHA-256 is the byte SHA-256 of JGA_BASS_BEST_VALIDATED_BASELINE_20260924/MANIFEST.json, calculated only after the manifest/checksum set is complete and verified. Its exact value is recorded in FINAL_FREEZE.json, the root bootstrap and the closure commit summary. FINAL_FREEZE.json is the nonrecursive digest receipt for this authority document and its dependencies. The manifest hashes this document; it therefore cannot embed its own final digest here without a self-reference.

The prior fd768ec83bc77a5e32938bed743edef10d1355d0c1a961c623be5ea4728b850d value is an INCOMPLETE PAYLOAD hash, not the final milestone. BASELINE_FREEZE.json, AUTHORITY_CORE.md, RECOVERY_PUBLIC_AUTHORITY.md and INCOMPLETE_CLOSURE_RECEIPT.json are preserved recovery records; their old hash-convention language is superseded by this paragraph and the final MANIFEST/receipt. They do not replace this current PI authority.

MANIFEST.json records all intended immutable scientific assets, code, model, outputs, authority and package artifacts with roots, relative paths, byte counts, roles and SHA-256s. SHA256SUMS.txt lists the same actual-file digests using root-qualified paths, plus the manifest digest. Source-audio/raw-array entries may be references rather than Git blobs; the full external project backup preserves these files. Future operational bootstrap/commit/backup receipts are outside the immutable scientific manifest and independently verified. No new science is authorized by closure.
'''
public.write_text(text)
(P/'README.md').write_text('''# Best validated Bass baseline — definitive closure package

Current PI authority: ../JGA_BASS_BEST_VALIDATED_BASELINE_20260924.md.

Verification order: verify every MANIFEST.json entry using its declared root, then SHA256SUMS.txt, then compare SHA256(MANIFEST.json) with FINAL_FREEZE.json. The latter is the definitive baseline freeze hash. Recovery files and the former partial payload digest are not final authority. All controlled35/40results remain unchanged; historical Bass timing is not finalized.

Audio/raw arrays are referenced rather than unnecessarily duplicated or pushed as large Git blobs. The independently verified versioned external backup contains both the complete working repository and SSD_TRACK_JGA data root, including untracked scientific artifacts. Python virtual environments/caches can be rebuilt from preserved configuration/environment metadata; they are not scientific audio.

Do not execute historical experiment scripts as part of recovery. No training/inference/recalculation is needed to verify these hashes. build_package.py records the interrupted preparation and must not be rerun; complete_manifest.py records this successful resume sequence and is not idempotent by design. backup_versioned.py creates a fresh non-destructive complete backup after verified commit/push.
''')
# Capture pre-existing unrelated working state for staging audit; do not alter it.
(P/'PRE_CLOSURE_GIT_STATUS.txt').write_text(subprocess.check_output(['git','status','--porcelain=v1'],cwd=ROOT,text=True))
entries=[]
for original in old['entries']:
 e=dict(original)
 if e['relative_path'].startswith(str(P.relative_to(ROOT))+'/') and Path(e['relative_path']).name=='AUTHORITY_CORE.md':e['authority_status']='RECOVERY_INCOMPLETE_NOT_FINAL'
 entries.append(e)
known={(e['root'],e['relative_path']) for e in entries}
for p in [public,*sorted(P.iterdir())]:
 if not p.is_file() or p.name in ['MANIFEST.json','SHA256SUMS.txt','FINAL_FREEZE.json']:continue
 key=('REPOSITORY',str(p.relative_to(ROOT)))
 if key in known:continue
 recovery=p.name in ['BASELINE_FREEZE.json','INCOMPLETE_CLOSURE_RECEIPT.json','RECOVERY_PUBLIC_AUTHORITY.md','PREVIOUS_PROJECT_STATE.md','build_package.py']
 entries.append({'root':key[0],'relative_path':key[1],'role':'recovery_record' if recovery else 'baseline_closure_authority_or_tool','size':p.stat().st_size,'sha256':sha(p),'authority_status':'RECOVERY_INCOMPLETE_NOT_FINAL' if recovery else 'PI_SELECTED_BASELINE_CLOSURE','dependency':'PI resume instruction','git_payload':True})
entries.sort(key=lambda e:(e['root'],e['relative_path']))
manifest={'schema':'JGA_FINAL_BASS_BASELINE_MANIFEST_V1','roots':old['roots'],'entries':entries,'authority_document':str(public.relative_to(ROOT)),'definitive_hash':'SHA256 of exact MANIFEST.json bytes, recorded after verification in FINAL_FREEZE.json','incomplete_payload_hash_not_final':oldhash,'scientific_reexecution':False}
save(P/'MANIFEST.json',manifest)
# Build complete checksum set before publishing definitive identity.
lines=[e['sha256']+'  '+e['root']+'/'+e['relative_path'] for e in entries]
lines.append(sha(P/'MANIFEST.json')+'  REPOSITORY/'+str((P/'MANIFEST.json').relative_to(ROOT)))
(P/'SHA256SUMS.txt').write_text('\n'.join(lines)+'\n')
for line in (P/'SHA256SUMS.txt').read_text().splitlines():
 h,qualified=line.split('  ',1);root,rel=qualified.split('/',1);p=Path(manifest['roots'][root])/rel;assert sha(p)==h,qualified
for e in manifest['entries']:
 p=Path(manifest['roots'][e['root']])/e['relative_path'];assert p.stat().st_size==e['size']
final=sha(P/'MANIFEST.json');assert final!=oldhash
save(P/'FINAL_FREEZE.json',{'status':'VERIFIED_FINAL_BASELINE_FREEZE','final_baseline_freeze_sha256':final,'manifest_sha256':final,'checksum_set_sha256':sha(P/'SHA256SUMS.txt'),'manifest_entries':len(entries),'authority_sha256':sha(public),'incomplete_payload_sha256_not_final':oldhash,'hash_algorithm':'SHA-256 of exact final MANIFEST.json bytes','verification_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_entries_verified':True,'scientific_experiments_rerun':False})
print(json.dumps(json.load(open(P/'FINAL_FREEZE.json')),indent=2))
