"""Safety regression tests with disposable repositories; no JGA scientific execution."""
import importlib.util,json,subprocess,tempfile,unittest,types,sys
from unittest.mock import patch
from pathlib import Path
SPEC=importlib.util.spec_from_file_location('gov',Path(__file__).resolve().parents[1]/'jga_governance.py')
g=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(g)

class GovernanceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  self.git('init','-q');self.git('config','user.email','test@example.invalid');self.git('config','user.name','Fixture')
  (self.root/'base.txt').write_text('baseline');self.git('add','base.txt');self.git('commit','-qm','fixture')
  p=self.root/'docs/project';p.mkdir(parents=True)
  (p/'AGENT_REGISTRY.json').write_text(json.dumps({'agents':[{'agent_id':'writer','write_authority_status':'AUTHORIZED_FOR_CURRENT_TASK','current_task':'T','current_mode':'AUTHORIZED_WRITER','allowed_modes':['AUTHORIZED_WRITER']}]}))
  (p/'AGENT_WORK_LEDGER.jsonl').write_text(json.dumps({'task_id':'T','write_paths':['new.txt']})+'\n')
 def tearDown(self):self.tmp.cleanup()
 def git(self,*args):return subprocess.check_output(['git','-C',str(self.root),*args],stderr=subprocess.DEVNULL)
 def test_second_writer_rejected(self):
  g.acquire(self.root,'writer','T','one')
  with self.assertRaises(FileExistsError):g.acquire(self.root,'writer','T','two')
  g.release(self.root,'one')
 def publication_fixture(self):
  branch=self.git('branch','--show-current').decode().strip()
  (self.root/'JGA_BOOTSTRAP.md').write_text('Single recovery root\n')
  p=self.root/'docs/project/JGA_CHAT_HANDOFF.md';p.write_text(branch+'\nPublication HEAD: $Format:%H$\n')
  (self.root/'.gitattributes').write_text('docs/project/JGA_CHAT_HANDOFF.md export-subst\n')
  self.git('add','.');self.git('commit','-qm','publication fixture')
  return p
 def test_exported_handoff_has_exact_commit(self):
  p=self.publication_fixture()
  spec=importlib.util.spec_from_file_location('recovery',Path(__file__).resolve().parents[1]/'export_chat_recovery.py')
  mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
  head,data=mod.export_payloads(self.root)
  self.assertIn(head,data['JGA_CHAT_HANDOFF.md'].decode());self.assertNotIn('$Format',data['JGA_CHAT_HANDOFF.md'].decode())
  self.assertTrue(g.handoff_git_current(self.root,p.read_text(),g.state(self.root)))
 def test_symbolic_handoff_rejects_unsynchronized_commit(self):
  p=self.publication_fixture();(self.root/'other.txt').write_text('new work');self.git('add','other.txt');self.git('commit','-qm','other task')
  self.assertFalse(g.handoff_git_current(self.root,p.read_text(),g.state(self.root)))
 def test_symbolic_handoff_rejects_dirty_text(self):
  p=self.publication_fixture();p.write_text(p.read_text()+'uncommitted edit')
  self.assertFalse(g.handoff_git_current(self.root,p.read_text(),g.state(self.root)))
 def test_read_only_mode_rejects_writer_flag(self):
  p=self.root/'docs/project/AGENT_REGISTRY.json';d=json.loads(p.read_text());d['agents'][0]['current_mode']='READ_ONLY_RESEARCH';d['agents'][0]['allowed_modes']=['READ_ONLY_RESEARCH'];p.write_text(json.dumps(d))
  with self.assertRaises(ValueError):g.acquire(self.root,'writer','T','one')
 def test_unknown_writer_rejected(self):
  with self.assertRaises(ValueError):g.acquire(self.root,'reader','T','one')
 def test_foreign_token_cannot_release(self):
  g.acquire(self.root,'writer','T','one')
  with self.assertRaises(ValueError):g.release(self.root,'two')
  self.assertTrue(g.lock_path(self.root).exists())
 def test_existing_unrelated_dirty_work_is_preserved(self):
  (self.root/'base.txt').write_text('prior dirty');g.acquire(self.root,'writer','T','one');g.lease(self.root,'one');g.release(self.root,'one')
  self.assertEqual((self.root/'base.txt').read_text(),'prior dirty')
 def test_concurrent_change_blocks_release(self):
  g.acquire(self.root,'writer','T','one');(self.root/'base.txt').write_text('other writer')
  with self.assertRaisesRegex(ValueError,'STALE'):g.release(self.root,'one')
 def test_new_untracked_file_detected(self):
  g.acquire(self.root,'writer','T','one');(self.root/'unexpected.txt').write_text('new')
  with self.assertRaisesRegex(ValueError,'STALE'):g.lease(self.root,'one')
 def test_ignored_new_payload_detected(self):
  (self.root/'.gitignore').write_text('ignored.dat\n');g.acquire(self.root,'writer','T','one')
  (self.root/'ignored.dat').write_text('unexpected hidden payload')
  with self.assertRaisesRegex(ValueError,'STALE'):g.lease(self.root,'one')
 def test_index_change_detected(self):
  g.acquire(self.root,'writer','T','one');self.git('add','docs')
  with self.assertRaisesRegex(ValueError,'STALE'):g.lease(self.root,'one')
 def test_authorized_write_advances_lease_after_backup(self):
  g.acquire(self.root,'writer','T','one');called=[]
  def save(name,payload):
   (self.root/name).write_bytes(payload);called.append(name)
  adapter=types.SimpleNamespace(ROOT=self.root,atomic_write_and_backup=save)
  with patch.dict(sys.modules,{'continuous_backup':adapter}):g.write(self.root,'one','new.txt',b'payload')
  self.assertEqual(called,['new.txt']);g.lease(self.root,'one');g.release(self.root,'one')
 def test_failed_backup_does_not_advance_lease(self):
  g.acquire(self.root,'writer','T','one')
  def fail(name,payload):
   (self.root/name).write_bytes(payload);raise OSError('backup unavailable')
  adapter=types.SimpleNamespace(ROOT=self.root,atomic_write_and_backup=fail)
  with patch.dict(sys.modules,{'continuous_backup':adapter}):
   with self.assertRaises(OSError):g.write(self.root,'one','new.txt',b'payload')
  with self.assertRaisesRegex(ValueError,'STALE'):g.lease(self.root,'one')
 def test_wrong_write_scope_rejected_before_backup(self):
  g.acquire(self.root,'writer','T','one')
  with self.assertRaisesRegex(ValueError,'scope'):g.write(self.root,'one','base.txt',b'overwrite')
  self.assertEqual((self.root/'base.txt').read_text(),'baseline')
 def test_heavy_blob_guard_uses_staged_bytes(self):
  p=self.root/'large.csv';p.write_bytes(b'X'*(g.MAX_GIT_BYTES+1));self.git('add','large.csv');p.write_text('small now')
  self.assertTrue(g.staged_guard(self.root))
 def test_audio_extension_guard_and_light_metadata(self):
  (self.root/'sample.wav').write_bytes(b'x');self.git('add','sample.wav');self.assertTrue(g.staged_guard(self.root))
  self.git('reset','-q','HEAD');(self.root/'small.csv').write_text('q,value\n1,2\n');self.git('add','small.csv');self.assertEqual(g.staged_guard(self.root),[])
 def test_path_traversal_and_symlink_rejected(self):
  with self.assertRaises(ValueError):g.safe(self.root,'../escape')
  (self.root/'link').symlink_to(self.root/'base.txt')
  with self.assertRaises(ValueError):g.safe(self.root,'link')
 def test_external_missing_and_hash_mismatch(self):
  src=self.root/'source';src.write_text('source');bak=self.root/'backup';bak.write_text('wrong')
  d={'coverage_scope':'fixture','artifacts':[{'artifact_id':'A','canonical_external_path':str(src),'size_bytes':6,'sha256':g.sha(src),'backup_destination':str(bak),'backup_class':'SSD_AND_BACKUP','source_provenance':'base.txt'}]}
  p=self.root/'docs/project/EXTERNAL_ARTIFACT_MANIFEST.json';p.write_text(json.dumps(d))
  self.assertEqual(g.external_check(self.root,'full')['findings'][0]['issue'],'BACKUP_HASH_MISMATCH')
  src.unlink();self.assertEqual(g.external_check(self.root,'metadata')['findings'][0]['issue'],'SOURCE_MISSING')
 def test_secret_not_printed(self):
  token='ghp_'+'a'*32;(self.root/'secret.txt').write_text(token)
  findings=g.secrets(self.root,['secret.txt']);self.assertTrue(findings);self.assertNotIn(token,str(findings))

if __name__=='__main__':unittest.main()
