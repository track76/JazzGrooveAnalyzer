"""PI-approved alignment regression contracts; isolated files, no real volumes."""
import importlib.util,json,hashlib,sys
from pathlib import Path
from unittest.mock import patch
import pytest
from tools.tests import test_jga_governance as fixturegov
g=fixturegov.g
from tools.bootstrap.bootstrap_generator import current_section,generate_bootstrap,render_bootstrap
spec=importlib.util.spec_from_file_location('backup_alignment',Path(__file__).parents[1]/'continuous_backup.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)

@pytest.fixture
def repo():
    f=fixturegov.GovernanceTests();f.setUp()
    try:yield f
    finally:f.tearDown()

def decision(repo,**changes):
    p=repo.root/'docs/project/PI_DECISION_LOG.jsonl';d=json.loads(p.read_text());d.update(changes);p.write_text(json.dumps(d)+'\n');return d

def test_one_task_multiple_phases_no_cross_task():
    d={'task_id':'T','phases':['PRE_UNSEAL','METHOD_FREEZE','OUTPUT_FREEZE','HUMAN_UNSEAL','VALIDATION']}
    for phase in d['phases'][:3]:assert g.validate_phase(d,'T',phase)['task_id']=='T'
    with pytest.raises(ValueError,match='cross-task'):g.validate_phase(d,'NEXT','PRE_UNSEAL')
    with pytest.raises(ValueError,match='freeze'):g.validate_phase(d,'T','HUMAN_UNSEAL')
    freezes={k:'a'*64 for k in ['method','parameters','population','evaluation','machine_output']}
    assert g.validate_phase(d,'T','HUMAN_UNSEAL',freezes)['status']=='GATE_VALIDATED'
    del freezes['population']
    with pytest.raises(ValueError):g.validate_phase(d,'T','HUMAN_UNSEAL',freezes)

@pytest.mark.parametrize('change,reason',[({'task_id':'WRONG'},'wrong task'),({'agent_id':'wrong'},'wrong agent'),({'write_paths':[]},'scope')])
def test_acquire_pi_link_mismatch(repo,change,reason):
    decision(repo,**change)
    with pytest.raises(ValueError,match=reason):g.acquire(repo.root,'writer','T','one')

def test_missing_pi_link(repo):
    (repo.root/'docs/project/PI_DECISION_LOG.jsonl').write_text('')
    with pytest.raises(ValueError,match='linkage'):g.acquire(repo.root,'writer','T','one')

def external_admission(repo,external):
    decision(repo,external_write_roots=[str(external)])
    p=repo.root/'docs/project/AGENT_WORK_LEDGER.jsonl';d=json.loads(p.read_text());d['external_write_roots']=[str(external)];p.write_text(json.dumps(d)+'\n')
    p=repo.root/'docs/project/AGENT_REGISTRY.json';d=json.loads(p.read_text());d['agents'][0]['external_write_roots']=[str(external)];p.write_text(json.dumps(d))

def test_external_registered_scope_and_manifest(repo,tmp_path):
    external_admission(repo,tmp_path);g.acquire(repo.root,'writer','T','one')
    def install(p,data):p.write_bytes(data);return {'status':'BACKUP_VERIFIED'}
    from types import SimpleNamespace
    adapter=SimpleNamespace(ROOT=repo.root,preflight=lambda:{'status':'BACKUP_VERIFIED'},atomic_external_write_and_backup=install)
    with patch.dict(sys.modules,{'continuous_backup':adapter}):
        result=g.write_external(repo.root,'one',str(tmp_path/'output.json'),b'{}',{'artifact_id':'A','authority_classification':'SYNTHETIC_TEST','source_provenance':'fixture'})
        assert result['task_id']=='T';assert result['sha256']==hashlib.sha256(b'{}').hexdigest()
        assert json.loads(Path(result['manifest']).read_text())['size_bytes']==2
        with pytest.raises(ValueError,match='Unregistered'):g.write_external(repo.root,'one',str(tmp_path.parent/'outside.json'),b'{}',{})
    (tmp_path/'output.json').write_text('changed')
    with pytest.raises(ValueError,match='EXTERNAL'):g.lease(repo.root,'one')

def test_unlinked_external_scope_rejected(repo,tmp_path):
    external_admission(repo,tmp_path);decision(repo,external_write_roots=[])
    with pytest.raises(ValueError,match='external scope'):g.acquire(repo.root,'writer','T','one')

def blind_view(repo,tmp_path):
    machine=tmp_path/'machine.json';machine.write_text('{}');recovery=tmp_path/'coordinator.json';recovery.write_text('full canonical recovery completed')
    target=tmp_path/'human';target.mkdir()
    view={'task_id':'T','agent_id':'writer','PI_decision':'PI-T','coordinator_recovery_record':{'path':str(recovery),'sha256':g.sha(recovery)},'allowed_files':[{'path':str(machine),'sha256':g.sha(machine)}],'denied_paths':[str(target)],'release_condition':'INDEPENDENT_MACHINE_OUTPUT_FREEZE'}
    return view,machine,target

def test_blind_exception_requires_pi_and_no_silent_skip(repo,tmp_path):
    view,machine,target=blind_view(repo,tmp_path)
    with pytest.raises(ValueError,match='Explicit PI'):g.validate_blind_view(repo.root,'T','writer',view)
    d=decision(repo,blind_worker_startup=view)
    assert g.blind_access(repo.root,'T','writer',view,machine,d)==machine
    with pytest.raises(ValueError,match='Protected'):g.blind_access(repo.root,'T','writer',view,target/'answer.json',d)
    with pytest.raises(ValueError,match='permitted'):g.blind_access(repo.root,'T','writer',view,repo.root/'base.txt',d)
    machine.write_text('tampered')
    with pytest.raises(ValueError,match='hash'):g.validate_blind_view(repo.root,'T','writer',view)

@pytest.fixture
def backup_repo(repo,monkeypatch):
    monkeypatch.setattr(b,'ROOT',repo.root);monkeypatch.setattr(b,'MIRROR',None)
    return repo

def configuration(repo,state='BACKUP_DEBT_PI_AUTHORIZED',target=None):
    debt={'scope':['new.txt'],'reason':'fixture target unavailable','permitted_work':['tests'],'prohibited_work':['science'],'settlement_condition':'replacement verified'}
    d=decision(repo,backup_debt=debt,backup_destination=target)
    c={'task_id':'T','PI_decision':'PI-T','state':state,'backup_destination':target,'primary_scientific_root':str(repo.root.parent/'primary'),'historical_backup_destination':'/Volumes/HD BackUp/JGA_BACKUP',**debt}
    (repo.root/'docs/project/BACKUP_CONFIGURATION.json').write_text(json.dumps(c));return c

def test_backup_debt_is_not_pass_and_no_external_access(backup_repo,monkeypatch):
    configuration(backup_repo)
    monkeypatch.setattr(b.tempfile,'TemporaryFile',lambda **kw:pytest.fail('must not access backup'))
    assert b.preflight()['status']=='BACKUP_DEBT_PI_AUTHORIZED'
    assert b.BACKUP_ROOT is None
    result=b.atomic_write_and_backup('new.txt',b'local');assert result['status']!='PASS';assert result['operation']=='LOCAL_ONLY_NOT_BACKED_UP'
    with pytest.raises(ValueError,match='scope'):b.atomic_write_and_backup('forbidden.txt',b'x')
    assert not (backup_repo.root/'forbidden.txt').exists()

def test_no_implicit_old_backup_and_target_pi_authorized(backup_repo,tmp_path):
    with pytest.raises(RuntimeError,match='configuration'):b.preflight()
    target=str(tmp_path/'new-backup')
    c=configuration(backup_repo,'BACKUP_VERIFIED',target)
    assert b.configuration()['backup_destination']==target
    c['backup_destination']='/Volumes/HD BackUp/JGA_BACKUP';(backup_repo.root/'docs/project/BACKUP_CONFIGURATION.json').write_text(json.dumps(c))
    with pytest.raises(RuntimeError,match='authorized'):b.configuration()

def test_backup_target_copy_uses_configured_fixture(backup_repo,tmp_path,monkeypatch):
    target=tmp_path/'new-backup';target.mkdir();configuration(backup_repo,'BACKUP_VERIFIED',str(target))
    # Isolated fixture simulates mount/device preflight only; real byte copy/hash follows.
    def fixture_preflight():
        c=b.configuration();b.BACKUP_ROOT=Path(c['backup_destination']);b.MIRROR=b.BACKUP_ROOT/'JazzGrooveAnalyzer_CURRENT';b.MIRROR.mkdir(exist_ok=True);return {'status':'BACKUP_VERIFIED'}
    monkeypatch.setattr(b,'preflight',fixture_preflight)
    assert b.atomic_write_and_backup('new.txt',b'copied')['sha256']==hashlib.sha256(b'copied').hexdigest()
    assert (target/'JazzGrooveAnalyzer_CURRENT/new.txt').read_bytes()==b'copied'

def test_profiles_evidence_overrides_explicit_disposable(backup_repo):
    c=configuration(backup_repo);ex={'path':'browser','classification':'DISPOSABLE_REPRODUCIBLE','inspection_record':'inspection.json','PI_decision':'PI-T'}
    c.update(disposable_profiles=[ex],scientific_evidence_paths=['browser/responses'])
    decision(backup_repo,backup_debt={k:c[k] for k in ['scope','reason','permitted_work','prohibited_work','settlement_condition']},disposable_profiles=[ex])
    (backup_repo.root/'docs/project/BACKUP_CONFIGURATION.json').write_text(json.dumps(c))
    assert b.profile_classification('browser/responses/answer.json')=='SCIENTIFIC_EVIDENCE'
    assert b.profile_classification('browser/cache')=='DISPOSABLE_REPRODUCIBLE'
    assert b.profile_classification('other-browser')=='PRESERVE'

@pytest.mark.parametrize('text',['current\n---\nstill current\nEND\nhistorical','current\nEND\nhistorical'])
def test_semantic_bootstrap_boundaries(text):
    assert current_section(text,{'current_section_end':'END'})==text.split('END')[0]
    with pytest.raises(ValueError):current_section(text,{'current_section_end':'MISSING'})

def test_only_one_bootstrap_root_is_generated(tmp_path):
    (tmp_path/'docs/project').mkdir(parents=True);(tmp_path/'docs/state.md').write_text('current\nEND\nhistory')
    (tmp_path/'docs/project/BOOTSTRAP_SOURCES.json').write_text(json.dumps({'sections':[{'path':'docs/state.md','current_section_only':True,'current_section_end':'END'}],'recovery_links':[]}))
    assert generate_bootstrap(tmp_path)==tmp_path/'JGA_BOOTSTRAP.md'
    assert not (tmp_path/'BLIND_BOOTSTRAP.md').exists();assert not (tmp_path/'artifacts').exists()
    assert 'history' not in render_bootstrap(tmp_path)


def test_external_only_admission(repo,tmp_path):
    external_admission(repo,tmp_path)
    p=repo.root/'docs/project/AGENT_WORK_LEDGER.jsonl';d=json.loads(p.read_text());d['write_paths']=[];p.write_text(json.dumps(d)+'\n')
    assert g.acquire(repo.root,'writer','T','one')['status']=='ACQUIRED'
    g.release(repo.root,'one')


def test_external_creation_refuses_debt_and_overwrite(repo,tmp_path):
    external_admission(repo,tmp_path);g.acquire(repo.root,'writer','T','one')
    from types import SimpleNamespace
    adapter=SimpleNamespace(ROOT=repo.root,preflight=lambda:{'status':'BACKUP_DEBT_PI_AUTHORIZED'})
    with patch.dict(sys.modules,{'continuous_backup':adapter}):
        with pytest.raises(ValueError,match='verified backup'):g.write_external(repo.root,'one',str(tmp_path/'new'),b'x',{'artifact_id':'A','source_provenance':'fixture','authority_classification':'TEST'})
    assert not (tmp_path/'new').exists()


def test_profile_scientific_cache_not_blanket_excluded(backup_repo):
    c=configuration(backup_repo);c['scientific_evidence_paths']=['browser/__pycache__/response.json']
    (backup_repo.root/'docs/project/BACKUP_CONFIGURATION.json').write_text(json.dumps(c))
    assert not b.excluded(Path('browser/__pycache__/response.json'))
    assert b.profile_classification('unclassified-browser')=='PRESERVE'


def test_blind_alias_cannot_escape_denylist(repo,tmp_path):
    view,machine,target=blind_view(repo,tmp_path);answer=target/'answer.json';answer.write_text('target');alias=tmp_path/'alias';alias.symlink_to(answer)
    view['allowed_files']=[{'path':str(alias),'sha256':g.sha(alias)}];decision(repo,blind_worker_startup=view)
    with pytest.raises(ValueError,match='Protected'):g.validate_blind_view(repo.root,'T','writer',view)


def test_blind_worker_guard_does_not_read_full_pi_log(repo,tmp_path):
    view,machine,target=blind_view(repo,tmp_path);d=decision(repo,blind_worker_startup=view)
    with pytest.raises(ValueError,match='permitted PI record'):g.blind_access(repo.root,'T','writer',view,machine)
    with patch.object(g,'decision_for',side_effect=AssertionError('must not open canonical log')):
        assert g.blind_access(repo.root,'T','writer',view,machine,d)==machine


def test_response_under_profile_cache_remains_in_inventory(backup_repo):
    c=configuration(backup_repo);c['scientific_evidence_paths']=['browser/__pycache__/response.json']
    (backup_repo.root/'docs/project/BACKUP_CONFIGURATION.json').write_text(json.dumps(c))
    p=backup_repo.root/'browser/__pycache__/response.json';p.parent.mkdir(parents=True);p.write_text('synthetic response')
    assert Path('browser/__pycache__/response.json') in b.inventory()


def test_external_backup_mapping_and_existing_bytes_preserved(backup_repo,tmp_path,monkeypatch):
    target=tmp_path/'backup';target.mkdir();c=configuration(backup_repo,'BACKUP_VERIFIED',str(target));primary=tmp_path/'primary'
    c['primary_scientific_root']=str(primary);(backup_repo.root/'docs/project/BACKUP_CONFIGURATION.json').write_text(json.dumps(c))
    decision(backup_repo,backup_destination=str(target),primary_scientific_root=str(primary))
    def preflight():b.BACKUP_ROOT=target;return {'status':'BACKUP_VERIFIED'}
    monkeypatch.setattr(b,'preflight',preflight)
    p=primary/'experiments/T/output.json';result=b.atomic_external_write_and_backup(p,b'fixture')
    assert Path(result['backup']).read_bytes()==b'fixture'
    with pytest.raises(ValueError,match='preserved'):b.atomic_external_write_and_backup(p,b'different')
    assert p.read_bytes()==b'fixture'
