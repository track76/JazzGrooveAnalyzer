"""Bounded recovery-authority contract; no scientific algorithm execution."""
from pathlib import Path
import hashlib
import json
import re
import runpy
import sys
from unittest.mock import Mock

import pytest
from tools.bootstrap.bootstrap_generator import generate_bootstrap, render_bootstrap

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / 'docs/scientific/rfc/JGA_SINGLE_ROOT_BOOTSTRAP_MIGRATION_20260922'


def test_root_matches_canonical_sources_and_links():
    text = render_bootstrap(ROOT)
    assert text == (ROOT / 'JGA_BOOTSTRAP.md').read_text()
    for target in re.findall(r'\]\(([^)]+)\)', text):
        assert (ROOT / target).exists(), target
    assert '## Preserved historical checkpoints' not in text


def test_checkpoint_preserves_fail_and_distinct_engineering_decision():
    text = render_bootstrap(ROOT)
    for required in ['FAIL', '10 aligned / 10 mostly aligned / 3 misaligned / 1 uncertain',
                     'ACCEPTED AS PRIMARY TEMPO / LOCAL-PULSE EVIDENCE ENGINE',
                     'NOT YET COMPLETE', 'ORIGINAL FULL MIX', 'not final musical-quarter Ground Truth',
                     '4/4 PRIMARY', '3/4 SUPPORTED', 'odd meters EXPERIMENTAL',
                     'Tempo-Existence / Confidence Gate', 'Metric-Level Selection',
                     'Metric-Level Lock / Continuity', 'YES / LOW_CONFIDENCE / NO',
                     'not Ground Truth and not a required runtime dependency',
                     'Beat This!', 'DEFERRED', 'independent', '+27 ms',
                     'Double Bass, Ride and Hi-Hat', 'Precise recorded Bass onset',
                     'physical Bass–Drum microtiming remain unestablished',
                     'No groove recalculation authorized', 'separate PI authorization']:
        assert required in text, required


def test_snapshot_bytes_preserved():
    for record in json.loads((PACKAGE / 'PRESERVATION_FREEZE.json').read_text())['records']:
        assert hashlib.sha256((ROOT / record['snapshot']).read_bytes()).hexdigest() == record['sha256']


def test_agent_and_compatibility_contract():
    agents = (ROOT / 'AGENTS.md').read_text()
    assert 'Load root `JGA_BOOTSTRAP.md`' in agents
    assert 'artifacts/JGA_BOOTSTRAP.md' not in agents
    redirect = (ROOT / 'artifacts/JGA_BOOTSTRAP.md').read_text()
    assert 'NON-AUTHORITATIVE' in redirect and '(../JGA_BOOTSTRAP.md)' in redirect
    assert len(redirect.splitlines()) < 10
    assert 'PLP' not in redirect


@pytest.fixture
def minimal_repo(tmp_path):
    (tmp_path / 'docs/project').mkdir(parents=True)
    (tmp_path / 'docs/state.md').write_text('Current\n\n[Evidence](evidence.md)\n\n---\nSTALE INSTRUCTION\n')
    (tmp_path / 'docs/evidence.md').write_text('Evidence')
    (tmp_path / 'docs/project/BOOTSTRAP_SOURCES.json').write_text(json.dumps({
        'sections': [{'path': 'docs/state.md', 'current_section_only': True}],
        'recovery_links': ['docs/evidence.md']}))
    return tmp_path


def test_generation_is_root_only_and_deterministic(minimal_repo):
    output = generate_bootstrap(minimal_repo)
    assert output == minimal_repo / 'JGA_BOOTSTRAP.md'
    first = output.read_bytes()
    generate_bootstrap(minimal_repo)
    assert output.read_bytes() == first
    assert not (minimal_repo / 'artifacts').exists()
    assert 'STALE' not in first.decode()
    assert '(docs/evidence.md)' in first.decode()


def test_generator_leaves_legacy_redirect_untouched(minimal_repo):
    legacy = minimal_repo / 'artifacts/JGA_BOOTSTRAP.md'
    legacy.parent.mkdir(); legacy.write_text('NON-AUTHORITATIVE redirect')
    generate_bootstrap(minimal_repo)
    assert legacy.read_text() == 'NON-AUTHORITATIVE redirect'


def test_invalid_source_link_does_not_overwrite_root(minimal_repo):
    root = minimal_repo / 'JGA_BOOTSTRAP.md'; root.write_text('last valid recovery')
    (minimal_repo / 'docs/evidence.md').unlink()
    with pytest.raises(ValueError):
        generate_bootstrap(minimal_repo)
    assert root.read_text() == 'last valid recovery'


def test_recovery_only_skips_broad_workflow(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / 'tools'))
    namespace = runpy.run_path(str(ROOT / 'tools/bootstrap.py'))
    main = namespace['main']; calls = {}
    for name in ['generate_bootstrap', 'check_git_status', 'run_tests', 'update_docs',
                 'export_repository', 'generate_architecture_map', 'export_session_context',
                 'export_context', 'export_scientific_state', 'export_pipeline_state',
                 'export_runtime_state', 'print_report']:
        calls[name] = Mock(); main.__globals__[name] = calls[name]
    monkeypatch.setattr(sys, 'argv', ['bootstrap.py', '--recovery-only'])
    main()
    calls['generate_bootstrap'].assert_called_once_with()
    for name, mock in calls.items():
        if name != 'generate_bootstrap': mock.assert_not_called()
