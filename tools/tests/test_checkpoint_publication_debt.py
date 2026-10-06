"""Checkpoint publication exception stays PI-linked and never certifies backup."""
import importlib.util,json
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location('checkpoint_backup',Path(__file__).parents[1]/'continuous_backup.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
@pytest.fixture
def config(tmp_path,monkeypatch):
    monkeypatch.setattr(b,'ROOT',tmp_path)
    p=tmp_path/'docs/project';p.mkdir(parents=True)
    debt={'scope':['safe.md'],'reason':'failed device','permitted_work':['checkpoint'],'prohibited_work':['science'],'settlement_condition':'replacement verified'}
    d={'decision_id':'PI-T','task_id':'T','decision':'APPROVED','backup_debt':debt,'write_paths':['safe.md'],'publication_under_backup_debt':True,'external_write_roots':['/approved/recovery']}
    c={'task_id':'T','PI_decision':'PI-T','state':'BACKUP_DEBT_PI_AUTHORIZED',**debt,'publication_under_backup_debt':True}
    (p/'PI_DECISION_LOG.jsonl').write_text(json.dumps(d)+'\n');(p/'BACKUP_CONFIGURATION.json').write_text(json.dumps(c))
    return p,d,c
def test_explicit_exception_never_reports_verified(config):
    r=b.publication_debt_authorization(['safe.md']);assert r['status']=='BACKUP_DEBT_PI_AUTHORIZED';assert r['backup_verified'] is False
    assert b.preflight()['status']=='BACKUP_DEBT_PI_AUTHORIZED'
def test_unregistered_staged_path_rejected(config):
    with pytest.raises(RuntimeError,match='scope'):b.publication_debt_authorization(['other.md'])
def test_configuration_alone_cannot_authorize(config):
    p,d,c=config;d.pop('publication_under_backup_debt');(p/'PI_DECISION_LOG.jsonl').write_text(json.dumps(d)+'\n')
    with pytest.raises(RuntimeError,match='blocked'):b.publication_debt_authorization()
def test_other_task_link_rejected(config):
    p,d,c=config;d['task_id']='OTHER';(p/'PI_DECISION_LOG.jsonl').write_text(json.dumps(d)+'\n')
    with pytest.raises(RuntimeError,match='linkage'):b.publication_debt_authorization()
def test_ordinary_debt_still_blocks_publication(config):
    p,d,c=config;c.pop('publication_under_backup_debt');(p/'BACKUP_CONFIGURATION.json').write_text(json.dumps(c))
    with pytest.raises(RuntimeError,match='blocked'):b.publication_debt_authorization()
