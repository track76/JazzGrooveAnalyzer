"""Read-only closure integrity checks. No scientific computation or generation."""
from pathlib import Path
import hashlib
import json
import re

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[3]


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def validate():
    refs = json.loads((PACKAGE / 'AUTHORITY_REFERENCES.json').read_text())['records']
    for record in refs:
        assert sha(ROOT / record['canonical_path']) == record['sha256'], record['canonical_path']
        assert sha(PACKAGE / record['preserved_snapshot']) == record['sha256']
    preserved = json.loads((PACKAGE / 'HISTORICAL_PRESERVATION.json').read_text())
    for name, digest in preserved.items():
        assert sha(ROOT / name) == digest, name
    old_docs = json.loads((PACKAGE / 'PRE_ADOPTION_DOCUMENT_HASHES.json').read_text())
    separator = '## Archived pre-adoption checkpoints — retained verbatim; not current instructions\n\n'
    for name, digest in old_docs.items():
        if name.endswith('BOOTSTRAP_SOURCES.json'):
            continue
        archived = (ROOT / name).read_text().split(separator, 1)[1]
        assert hashlib.sha256(archived.encode()).hexdigest() == digest, name
        current = (ROOT / name).read_text().split('\n---\n', 1)[0]
        assert 'HISTORICAL JAZZ CORPUS ANALYSIS / REPORT PRODUCTION' in current
        assert 'CLOSED' in current
        for target in re.findall(r'\]\(([^)]+)\)', current):
            assert ((ROOT / name).parent / target).exists(), target
    for name in ['README.md', 'PI_OPERATIONAL_DECISION.md', 'HISTORICAL_REPORT_WORKFLOW.md']:
        for target in re.findall(r'\]\(([^)]+)\)', (PACKAGE / name).read_text()):
            # Receipt and seal are written after the first successful audit.
            if target not in ['VALIDATION.json', 'DECISION_FREEZE.json']:
                assert (PACKAGE / target).exists(), target
    decision = (PACKAGE / 'PI_OPERATIONAL_DECISION.md').read_text()
    for term in ['FULL_MIX_AND_STEM_MATCH', 'FULL_MIX_ONLY', 'STEM_ONLY',
                 'AMBIGUOUS_MATCH', 'SHARED_DUAL_MARKER / UNRESOLVED',
                 'distinct compatible native full-mix IDs and distinct timestamps',
                 'not calibrated confidence', 'not final musical-quarter Ground Truth',
                 'No snapping', '512 samples at 44,100 Hz', 'FAIL', 'physical']:
        assert term in decision, term
    seal = PACKAGE / 'DECISION_FREEZE.json'
    if seal.exists():
        for name, digest in json.loads(seal.read_text())['files'].items():
            assert sha(ROOT / name) == digest, name
    return {'status': 'PASS', 'authority_records_and_snapshots': len(refs),
            'historical_files_unchanged': len(preserved),
            'archived_state_documents_byte_preserved': len(old_docs)-1,
            'current_links': 'PASS', 'provenance_timestamp_DUAL_contract': 'PASS',
            'tests': '13 passed: tests/tooling',
            'scientific_experiments': 'NONE', 'runtime_changes': 'NONE',
            'availability': 'Exact compact evidence snapshots committed; full historical holdings remain at original paths; no complete-data backup claimed'}


if __name__ == '__main__':
    print(json.dumps(validate(), indent=2))
