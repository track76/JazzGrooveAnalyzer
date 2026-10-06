"""PI-qualified history and governed Git transitions in isolated repositories."""
import importlib.util,json,subprocess,types,sys
from pathlib import Path
from unittest.mock import patch
import pytest
spec=importlib.util.spec_from_file_location('publication_gov',Path(__file__).parents[1]/'jga_governance.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def run(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.DEVNULL)

def dump(path,value):path.write_text(json.dumps(value)+'\n')

@pytest.fixture
def repo(tmp_path,monkeypatch):
    root=tmp_path/'work';root.mkdir();run(root,'init','-q');run(root,'config','user.email','fixture@example.invalid');run(root,'config','user.name','Fixture')
    (root/'base.txt').write_text('base');run(root,'add','base.txt');run(root,'commit','-qm','base')
    branch=run(root,'branch','--show-current').decode().strip();p=root/'docs/project';p.mkdir(parents=True)
    paths=['new.txt','validation.json'];pi={'decision_id':'PI','task_id':'T','agent_id':'writer','decision':'APPROVED','write_paths':paths,'publication':{'commit':True,'push':True,'remote':'origin','branch':branch}}
    dump(p/'PI_DECISION_LOG.jsonl',pi);dump(p/'AGENT_WORK_LEDGER.jsonl',{'task_id':'T','PI_authorization':'PI','write_paths':paths})
    dump(p/'AGENT_REGISTRY.json',{'agents':[{'agent_id':'writer','current_task':'T','current_mode':'AUTHORIZED_WRITER','allowed_modes':['AUTHORIZED_WRITER'],'write_authority_status':'AUTHORIZED_FOR_CURRENT_TASK'}]})
    (root/'new.txt').write_text('new');dump(root/'validation.json',{'test_exit_code':0,'publication_tests_passed':True})
    bare=tmp_path/'remote.git';subprocess.check_call(['git','init','--bare','-q',str(bare)]);run(root,'remote','add','origin',str(bare))
    monkeypatch.setattr(g,'publication_guards',lambda root,review:{'backup':{'status':'BACKUP_DEBT_PI_AUTHORIZED'},'governance':{'status':'PASS'}})
    g.acquire(root,'writer','T','token');return root,paths

def review(repo):return g.reviewed_manifest(repo[0],'token',repo[1])
def staged(repo):r=review(repo);g.publication_stage(repo[0],'token',r);return r
def verified(repo):staged(repo);g.publication_verify(repo[0],'token','validation.json')
def committed(repo):verified(repo);return g.publication_commit(repo[0],'token','scoped fixture')['commit']

def history(kind='CORRECTIVE_PI_LINKAGE'):
    original={'task_id':'OLD','event':'STARTED','pi_authorization':'OLD-PI'}
    pi={'decision_id':'PI','task_id':'CURRENT','decision':'APPROVED','historical_reconciliation_authorized':True,'historical_qualification_acceptance':True}
    c={'event':'HISTORICAL_GOVERNANCE_CORRECTION','task_id':'CURRENT','PI_authorization':'PI','original_record_number':1,'original_record_sha256':g.row_digest(original),'original_task_id':'OLD','resolution_kind':kind,'source_provenance':'PI instruction','preservation_requirement':'PRESERVE','scientific_bytes_shown_invalid':False,'verified_existing_PI_decision':'OLD-PI'}
    return original,c,[pi,{'decision_id':'OLD-PI','task_id':'OLD'}]

def test_corrective_linkage_preserves_original():
    o,c,d=history();before=dict(o);r,w,e=g.historical_resolutions([o,c],d);assert not e and (0,'CORRECTIVE_PI_LINKAGE',None) in r and o==before

def test_unresolved_authorization_is_warning_not_authorized():
    o,c,d=history('HISTORICAL_AUTHORIZATION_UNRESOLVED');o.pop('pi_authorization');o['PI_authorization']='MISSING';c['missing_decision_id']='MISSING';c['original_record_sha256']=g.row_digest(o)
    r,w,e=g.historical_resolutions([o,c],d);assert not e and w[0]['historically_authorized'] is False

@pytest.mark.parametrize('change',['hash','task','duplicate','missing_pi','current'])
def test_invalid_correction_rejected(change):
    o,c,d=history();rows=[o,c]
    if change=='hash':c['original_record_sha256']='0'*64
    if change=='task':d[1]['task_id']='WRONG'
    if change=='duplicate':rows.append(dict(c))
    if change=='missing_pi':d.pop()
    if change=='current':d[0]['task_id']='OLD'
    assert g.historical_resolutions(rows,d)[2]

def test_resolved_historical_reference():
    o,c,d=history('HISTORICAL_REFERENCE_RESOLUTION');o['artifact_paths']=['old.json'];c.update(missing_path='old.json',reference_status='UNKNOWN',original_record_sha256=g.row_digest(o))
    r,w,e=g.historical_resolutions([o,c],d);assert not e and (0,'HISTORICAL_REFERENCE_RESOLUTION','old.json') in r

def test_current_reference_cannot_receive_historical_exception():
    o,c,d=history('HISTORICAL_REFERENCE_RESOLUTION');o['artifact_paths']=['old.json'];c.update(missing_path='old.json',reference_status='UNKNOWN',original_record_sha256=g.row_digest(o));d[0]['task_id']='OLD'
    assert g.historical_resolutions([o,c],d)[2]

def test_legacy_mapping():
    a=[{'name':'a','path':'/ssd/a','sha256':'a'*64,'bytes':1},{'name':'b','path':'/ssd/b','sha256':'b'*64,'bytes':2}]
    assert len(g.validate_legacy_mapping(['EXT-001','EXT-002'],a,'EXT-'))==2

@pytest.mark.parametrize('ids',[['EXT-002','EXT-001'],['EXT-001'],['EXT-001','EXT-001']])
def test_invalid_legacy_mapping(ids):
    a=[{'name':'a','path':'/ssd/a','sha256':'a'*64,'bytes':1},{'name':'b','path':'/ssd/b','sha256':'b'*64,'bytes':2}]
    with pytest.raises(ValueError):g.validate_legacy_mapping(ids,a,'EXT-')

def test_scoped_stage_and_full_publication(repo):
    root,_=repo;h=committed(repo);r=g.publication_push(root,'token');assert r['remote_head']==h and r['backup_state']=='BACKUP_DEBT_PI_AUTHORIZED';g.lease(root,'token');g.release(root,'token');assert not g.lock_path(root).exists()

def test_same_lease_survives_each_transition(repo):
    root,_=repo;ino=g.lock_path(root).stat().st_ino;acquired=g.lease(root,'token')['acquired_at'];staged(repo);g.publication_verify(root,'token','validation.json');g.publication_commit(root,'token','fixture');g.publication_push(root,'token');d=g.lease(root,'token');assert d['acquired_at']==acquired and d['token']=='token';g.release(root,'token')

def test_wrong_owner(repo):
    with pytest.raises(ValueError,match='token'):g.publication_stage(repo[0],'wrong',review(repo))

@pytest.mark.parametrize('key',['task_id','agent_id','PI_decision','branch','parent'])
def test_wrong_review_binding(repo,key):
    r=review(repo);r[key]='WRONG'
    with pytest.raises(ValueError):g.publication_stage(repo[0],'token',r)

def test_wrong_pi_scope(repo):
    root,_=repo;pi=root/'docs/project/PI_DECISION_LOG.jsonl';d=json.loads(pi.read_text());d['publication']['commit']=False
    # Authorized fixture edit is included in a fresh baseline before attempting publication.
    g.release(root,'token');dump(pi,d);g.acquire(root,'writer','T','token')
    with pytest.raises(ValueError,match='PI publication'):review(repo)

def test_prestaged_unexpected_file(repo):
    run(repo[0],'add','base.txt','docs')
    with pytest.raises(ValueError):review(repo)

def test_out_of_scope(repo):
    r=review(repo);r['entries'][0]['path']='base.txt'
    with pytest.raises(ValueError,match='scope'):g.publication_stage(repo[0],'token',r)

def test_reviewed_bytes_changed(repo):
    r=review(repo);(repo[0]/'new.txt').write_text('changed')
    with pytest.raises(ValueError):g.publication_stage(repo[0],'token',r)

def test_partial_staging(repo):
    r=staged(repo);run(repo[0],'reset','-q','HEAD','new.txt')
    with pytest.raises(ValueError,match='Partial'):g.verify_index(repo[0],r)

def test_unexpected_deletion(repo):
    r=review(repo);r['entries'][0]['operation']='D'
    with pytest.raises(ValueError,match='deletion'):g.publication_stage(repo[0],'token',r)

def test_concurrent_unrelated_change(repo):
    r=review(repo);(repo[0]/'base.txt').write_text('other writer')
    with pytest.raises(ValueError,match='STALE'):g.publication_stage(repo[0],'token',r)

def test_unrelated_dirty_files_excluded(repo):
    root,paths=repo;g.release(root,'token');(root/'base.txt').write_text('prior dirty');(root/'unrelated').write_text('untracked');g.acquire(root,'writer','T','token');h=committed(repo)
    assert (root/'base.txt').read_text()=='prior dirty' and (root/'unrelated').read_text()=='untracked';assert run(root,'show',h+':base.txt')==b'base'
    assert b'unrelated' not in run(root,'ls-tree','--name-only',h)

def test_hook_induced_change_rejected(repo):
    root,_=repo;verified(repo);hook=root/'.git/hooks/pre-commit';hook.write_text('#!/bin/sh\nprintf unexpected > base.txt\ngit add base.txt\n');hook.chmod(0o700)
    with pytest.raises(ValueError,match='hook'):g.publication_commit(root,'token','fixture')

def test_commit_requires_staged_gate(repo):
    staged(repo)
    with pytest.raises(ValueError,match='gate'):g.publication_commit(repo[0],'token','fixture')

def test_failing_test_receipt(repo):
    root,_=repo;g.release(root,'token');dump(root/'validation.json',{'test_exit_code':1,'publication_tests_passed':True});g.acquire(root,'writer','T','token');staged(repo)
    with pytest.raises(ValueError,match='test receipt'):g.publication_verify(root,'token','validation.json')

def test_push_failure_keeps_owned_lease(repo):
    root,_=repo;committed(repo);original=g.git
    def fail(r,*args):
        if args[0]=='push':raise subprocess.CalledProcessError(1,['git','push'])
        return original(r,*args)
    with patch.object(g,'git',side_effect=fail):
        with pytest.raises(ValueError,match='Push failed'):g.publication_push(root,'token')
    assert g.lease(root,'token')['publication']['phase']=='PUSH_FAILED'

def test_remote_mismatch(repo):
    root,_=repo;committed(repo);original=g.git
    def wrong(r,*args):return b'0'*40+b' refs/heads/x\n' if args[0]=='ls-remote' else original(r,*args)
    with patch.object(g,'git',side_effect=wrong):
        with pytest.raises(ValueError,match='Remote mismatch'):g.publication_push(root,'token')
    assert g.lease(root,'token')['publication']['phase']=='REMOTE_MISMATCH'

def check_fixture(root,monkeypatch):
    p=root/'docs/project'
    dump(p/'BOOTSTRAP_SOURCES.json',{'sections':[],'recovery_links':[]})
    dump(p/'EMBARGO_REGISTRY.json',{'embargoes':[]});dump(p/'EXTERNAL_ARTIFACT_MANIFEST.json',{'artifacts':[]})
    for name in ['JGA_CHAT_HANDOFF.md','MULTI_AGENT_COORDINATION_STATE.md']:(p/name).write_text('fixture')
    for name in ['JGA_PROJECT_STATE.md','JGA_SCIENTIFIC_STATE.md']:(root/'docs'/name).write_text('fixture')
    (root/'JGA_BOOTSTRAP.md').write_text('fixture')
    import tools.bootstrap.bootstrap_generator as generator
    monkeypatch.setattr(generator,'render_bootstrap',lambda root:'fixture')
    monkeypatch.setattr(g,'handoff_git_current',lambda *args:True)
    return p

def test_current_missing_reference_still_fails(repo,monkeypatch):
    root,_=repo;p=check_fixture(root,monkeypatch);r=json.loads((p/'AGENT_WORK_LEDGER.jsonl').read_text());r['artifact_paths']=['missing.json'];dump(p/'AGENT_WORK_LEDGER.jsonl',r)
    assert {'issue':'MISSING_REFERENCE','path':'missing.json'} in g.check(root)['findings']

def test_historical_missing_reference_resolves_as_warning(repo,monkeypatch):
    root,_=repo;p=check_fixture(root,monkeypatch);o,c,d=history('HISTORICAL_REFERENCE_RESOLUTION');o.update(PI_authorization='OLD-PI',artifact_paths=['missing.json']);c.update(missing_path='missing.json',reference_status='UNKNOWN',original_record_sha256=g.row_digest(o))
    (p/'PI_DECISION_LOG.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in d));(p/'AGENT_WORK_LEDGER.jsonl').write_text(json.dumps(o)+'\n'+json.dumps(c)+'\n')
    result=g.check(root);assert result['status']=='PASS' and result['historical_qualifications'][0]['reference_status']=='UNKNOWN'

def test_legacy_registration_resolves_exact_id(repo,monkeypatch):
    root,_=repo;p=check_fixture(root,monkeypatch);r=json.loads((p/'AGENT_WORK_LEDGER.jsonl').read_text());r['external_artifact_ids']=['EXT-001'];dump(p/'AGENT_WORK_LEDGER.jsonl',r)
    assert g.check(root)['status']=='FAIL';dump(p/'EXTERNAL_ARTIFACT_MANIFEST.json',{'artifacts':[{'artifact_id':'EXT-001'}]});assert g.check(root)['status']=='PASS'

def test_inactive_existing_mode_passes_but_cannot_acquire(repo,monkeypatch):
    root,_=repo;p=check_fixture(root,monkeypatch);r=json.loads((p/'AGENT_REGISTRY.json').read_text());r['agents'][0].update(current_mode='INDEPENDENT_REVIEW',allowed_modes=['INDEPENDENT_REVIEW'],write_authority_status='NOT_GRANTED',current_task=None);dump(p/'AGENT_REGISTRY.json',r)
    assert g.check(root)['status']=='PASS'
    with pytest.raises(ValueError,match='writer'):g.acquire(root,'writer','T','other')

def test_recovery_export_uses_actual_governed_commit_and_retains_lease(repo,monkeypatch,tmp_path):
    root,_=repo;g.release(root,'token');p=root/'docs/project';branch=run(root,'branch','--show-current').decode().strip()
    (root/'JGA_BOOTSTRAP.md').write_text('Single root\n');handoff=p/'JGA_CHAT_HANDOFF.md';handoff.write_text(branch+'\nPublication HEAD: $Format:%H$\n')
    (root/'.gitattributes').write_text('docs/project/JGA_CHAT_HANDOFF.md export-subst\n');run(root,'add','JGA_BOOTSTRAP.md','docs/project/JGA_CHAT_HANDOFF.md','.gitattributes');run(root,'commit','-qm','recovery fixture')
    handoff.write_text(handoff.read_text()+'Current checkpoint\n');paths=repo[1]+['docs/project/JGA_CHAT_HANDOFF.md'];out=tmp_path/'exports';out.mkdir()
    pi=json.loads((p/'PI_DECISION_LOG.jsonl').read_text());pi['write_paths']=paths;pi['external_write_roots']=[str(out)];dump(p/'PI_DECISION_LOG.jsonl',pi)
    ledger=json.loads((p/'AGENT_WORK_LEDGER.jsonl').read_text());ledger.update(write_paths=paths,external_write_roots=[str(out)]);dump(p/'AGENT_WORK_LEDGER.jsonl',ledger)
    g.acquire(root,'writer','T','token');r=g.reviewed_manifest(root,'token',paths);g.publication_stage(root,'token',r);g.publication_verify(root,'token','validation.json');head=g.publication_commit(root,'token','recovery checkpoint')['commit'];g.publication_push(root,'token')
    spec=importlib.util.spec_from_file_location('fixture_export',Path(__file__).parents[1]/'export_chat_recovery.py');e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e);monkeypatch.setattr(e,'ROOT',root)
    backup=types.SimpleNamespace(preflight=lambda:{'status':'BACKUP_DEBT_PI_AUTHORIZED'},publication_debt_authorization=lambda:{'task_id':'T','external_write_roots':[str(out)]})
    monkeypatch.setenv('JGA_EXTERNAL_ROOT',str(out));monkeypatch.setenv('JGA_WRITER_TOKEN','token');monkeypatch.setattr(sys,'argv',['export','--destination',str(out/head)])
    with patch.dict(sys.modules,{'continuous_backup':backup,'jga_governance':g}):e.main()
    data=json.loads((out/head/'EXPORT_MANIFEST.json').read_text());assert data['git_head']==head and data['remote_head_verified']==head and data['backup_state']=='BACKUP_DEBT_PI_AUTHORIZED';assert head in (out/head/'JGA_CHAT_HANDOFF.md').read_text();assert len(g.lease(root,'token')['external_baseline'])==3;g.release(root,'token')


def test_remote_configuration_change_rejected(repo,tmp_path):
    root,_=repo;committed(repo);other=tmp_path/'other.git';subprocess.check_call(['git','init','--bare','-q',str(other)]);run(root,'remote','set-url','origin',str(other))
    with pytest.raises(ValueError,match='remote changed'):g.publication_push(root,'token')
