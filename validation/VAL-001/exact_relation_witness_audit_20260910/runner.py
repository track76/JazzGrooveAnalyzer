"""Authorization, byte admission and replay orchestration; no discovery formulas.

Real execution requires a separate PI authorization artifact. This implementation
task creates no such artifact. Synthetic mode refuses the real source/population
before importing either scientific implementation.
"""
import argparse
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

from transport import canonical, content_id, files_index, read, rows, sha, verify_sha, write

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
NAME = 'H-VAL001-DRUM-EXACT-RELATION-WITNESS-AUDIT-01'
PREREG = REPO/'validation/VAL-001/preregistrations'/NAME
PREREG_HASH = 'c609cfabdfd31f5122cd0883da861c2b742aa2af7a659cf691dbe0d56161e48a'
AUTH_HASH = '477cd53b11778091907058ad6157bd0a881b85240d8fd13fa5e9dc3ef676e059'
REAL_SOURCE = 'c46d6cb9-b99c-5bd6-8d81-656dc1ad48ec'
INPUT_PATH = 'validation/VAL-001/preregistrations/H-VAL001-COMPLETE-REAL-DRUM-PERIODICITY-01.inputs.json'
CANONICAL_FILES = ('events.json', 'relations.jsonl', 'witnesses.jsonl', 'witness_relations.jsonl',
    'windows.jsonl', 'reuse_audit.json', 'relation_ratios.jsonl', 'candidate_population.json', 'result.json')


def demand(condition, detail):
    if not condition:
        raise ValueError(detail)


def synthetic_bundle(path):
    bundle = read(path)
    demand(bundle.get('synthetic_fixture') is True, 'not a synthetic fixture')
    b = bundle['binding']
    demand(b['source_uuid'] == 'SYNTHETIC_SOURCE_NOT_REAL' and
           b['population'] == 'SYNTHETIC_POPULATION', 'synthetic source guard')
    demand(len(bundle['input']['events']) <= 16, 'synthetic population guard')
    demand(all(e['source_identity'] == 'SYNTHETIC_SOURCE_NOT_REAL' and
               e['eme_id'].startswith('E') and e['pulse_candidate_id'].startswith('P')
               for e in bundle['input']['events']), 'synthetic event guard')
    demand(REAL_SOURCE not in canonical(bundle).decode('ascii'), 'real authority in fixture')
    return bundle


def authenticate_real(authorization_path, destination):
    """Hash admission invoked afresh by generator and checker worker processes.

    Hash-only upstream records are never semantically read. Only the implementation
    closure and explicit allowlisted map catalogues enter the execution bundle.
    """
    # Missing permission stops before any scientific authority or input is read.
    approval = read(authorization_path)
    demand(approval.get('experiment') == NAME and approval.get('pi_authorized') is True and
           approval.get('action') == 'REAL_INPUT_GENERATOR_CHECKER_AND_REPLAY' and
           bool(approval.get('pi_identity')) and bool(approval.get('decision_reference')),
           'missing PI real-input authorization')
    binding_path = HERE/'implementation_binding_v2.json'
    binding = read(binding_path)
    demand(
           approval.get('implementation_sha256') == sha(binding_path) and
           bool(approval.get('pi_identity')) and bool(approval.get('decision_reference')),
           'missing PI real-input authorization')
    review_path = Path(approval['independent_review_path'])
    demand(sha(review_path) == approval['independent_review_sha256'], 'review hash mismatch')
    review = read(review_path)
    demand(review.get('implementation_sha256') == sha(binding_path) and
           review.get('independent_review_complete') is True and
           bool(review.get('reviewer_identity')) and bool(review.get('review_scope')),
           'independent implementation review not complete')
    demand(sha(Path(str(PREREG)+'.md')) == PREREG_HASH and
           sha(Path(str(PREREG)+'.authorities.json')) == AUTH_HASH, 'preregistration changed')
    for relative, expected in binding['implementation_files'].items():
        demand(sha(HERE/relative) == expected, 'implementation file changed: '+relative)
    env = binding['environment']
    demand(sys.version == env['python_version'] and sys.implementation.name == env['implementation']
           and platform.machine() == env['machine'] and platform.platform() == env['platform'] and
           sha(Path(sys.executable).resolve()) == env['executable_sha256'], 'runtime mismatch')
    for path, expected in env['runtime_files'].items():
        demand(sha(path) == expected, 'runtime dependency changed: '+path)
    external_output = Path('/Volumes/SSD Track/JGA/experiments')/NAME
    demand(destination.parent == external_output and destination.name in ('run_1', 'run_2'),
           'unauthorized scientific output destination')
    # Capacity is operational only; a shortage cannot become a scientific negative.
    probe = external_output if external_output.exists() else external_output.parent
    demand(shutil.disk_usage(probe).free >= int(binding['resources']['free_bytes_before_run'][destination.name]),
           'insufficient reserved storage')
    for path, expected in binding['upstream_hash_closure'].items():
        verify_sha(REPO/path, expected)
    auth = read(Path(str(PREREG)+'.authorities.json'))
    # Independent invocation checks every original named authority, not only closure.
    for path, expected in auth['repository_files'].items():
        verify_sha(REPO/path, expected)
    external = Path(auth['external_read_only_root'])
    demand(str(external) == binding['external_read_only_root'], 'input relocation not authorized')
    for name, expected in auth['external_files'].items():
        verify_sha(external/name, expected)
    root = read(external/'root.json')
    demand(root['index_sha256'] == auth['external_files']['index.json'], 'root/index mismatch')
    demand(root['manifests'] == {name: auth['external_files'][name]
                                for name in ('inputs.json', 'periods.json', 'windows.jsonl')},
           'root/catalogue mismatch')
    # Only after authorization and all hashes: decode the allowed evidence files.
    inp = read(REPO/INPUT_PATH)
    # Operational capacity qualification: accepted identities are UUID strings.
    # A violation stops the entire run; no event is filtered or renamed.
    demand(all(len(e['eme_id']) <= 36 and len(e['pulse_candidate_id']) <= 36
               for e in inp['events']), 'resource identity-width assumption exceeded')
    admitted = {'input_freeze_sha256': auth['repository_files'][INPUT_PATH],
        'source_uuid': auth['source_uuid'], 'source_authority_id': auth['source_authority_id'],
        'source_instance_key': auth['source_instance_key'],
        'asset_sha256': auth['asset_sha256_reference_only'], 'population': 'VAL001_DIRECT_DRUM_COMPLETE_01',
        'preregistration_sha256': PREREG_HASH, 'input_authority_sha256': AUTH_HASH,
        'implementation_sha256': sha(binding_path), 'environment_sha256': content_id(env),
        'counts': auth['frozen_counts']}
    return {'binding': admitted, 'input': inp,
            'admission_receipt': {'authorized_input_sha256': admitted['input_freeze_sha256'],
                                  'pi_authorization_sha256': sha(authorization_path)},
            'inputs': read(external/'inputs.json'),
            'periods': read(external/'periods.json'), 'windows': rows(external/'windows.jsonl')}


def failure_report(exception, stage):
    """No failure is a negative recurrence observation."""
    if isinstance(exception, (OSError, MemoryError, KeyboardInterrupt)):
        outcome = 'INSUFFICIENT_EVIDENCE'
        integrity = 'STOP_PREFLIGHT' if stage == 'PREFLIGHT' else 'STOP_INCOMPLETE'
    else:
        outcome = 'INDETERMINATE'
        integrity = ('STOP_PREFLIGHT' if stage == 'PREFLIGHT' else
                     'CHECKER_DISAGREEMENT' if stage == 'CHECKER' else 'FAIL_CONTRACT')
    return {'schema': 'JGA-EXACT-RELATION-WITNESS-V1', 'scientific_outcome': outcome,
        'integrity_status': integrity, 'population_classification': 'AMBIGUOUS_OR_UNRESOLVED_RELATIONS',
        'candidate_acceptance': 'WITHHELD_INCOMPLETE_AUTHORITY', 'stage': stage,
        'exception_type': type(exception).__name__,
        'scientific_status': 'RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED',
        'beat_reference_authorized': False, 'bpm_authorized': False}


def freeze_run(directory):
    result = read(directory/'result.json')
    root = {'schema': 'JGA-EXACT-RELATION-WITNESS-V1', 'authority': result['authority'],
        'files': files_index(directory, (*CANONICAL_FILES, 'checker.json')),
        'proposed_outcome': result['proposed_outcome'], 'acceptance': 'PENDING_REPLAY',
        'scientific_status': 'RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED',
        'beat_reference_authorized': False, 'bpm_authorized': False}
    root['logical_fingerprint'] = content_id(root['files'])
    write(directory/'root.json', root)


def execution_identity(directory, authority_directory):
    """Validate against a caller-selected custody ledger, never a receipt-selected path."""
    directory = Path(directory).resolve(strict=True)
    receipt = read(directory/'execution.json')
    identity = receipt['execution_id']
    demand(isinstance(identity, str) and len(identity) == 32 and
           all(c in '0123456789abcdef' for c in identity), 'invalid execution identity')
    ledger = Path(authority_directory).resolve(strict=True)
    issued = read(ledger/(identity+'.json'))
    demand(receipt['custody_directory'] == str(ledger), 'wrong execution custody authority')
    demand(receipt == issued, 'execution receipt differs from custody authority')
    st = directory.stat()
    demand(receipt['directory'] == {'resolved_path': str(directory),
        'device': str(st.st_dev), 'inode': str(st.st_ino)}, 'execution directory mismatch')
    demand(receipt['status'] == 'COMPLETED_FRESH_WORKERS', 'incomplete execution')
    demand([w['role'] for w in receipt['workers']] == ['generator', 'checker'], 'worker roles')
    demand(len({w['launch_id'] for w in receipt['workers']}) == 2 and
           all(w['exit_code'] == '0' for w in receipt['workers']), 'worker completion')
    demand(receipt['canonical_files'] == files_index(directory,
           (*CANONICAL_FILES, 'checker.json', 'root.json')), 'execution output binding')
    demand(receipt['scientific_authority'] == read(directory/'result.json')['authority'],
           'execution scientific authority mismatch')
    return receipt


def compare_replay(first, second, destination, *, authority_directory):
    first, second = Path(first).resolve(strict=True), Path(second).resolve(strict=True)
    demand(not first.samefile(second), 'self-comparison is not replay')
    executions = [execution_identity(d, authority_directory) for d in (first, second)]
    demand(executions[0]['execution_id'] != executions[1]['execution_id'], 'same execution reused')
    demand(set(w['launch_id'] for w in executions[0]['workers']).isdisjoint(
        w['launch_id'] for w in executions[1]['workers']), 'worker execution reused')
    demand(executions[0]['binding'] == executions[1]['binding'] and
           executions[0]['scientific_authority'] == executions[1]['scientific_authority'],
           'replay requires identical input/software/environment authority')
    names = (*CANONICAL_FILES, 'checker.json', 'root.json')
    before = files_index(first, names)
    after = files_index(second, names)
    mismatches = [name for name in names if before[name] != after[name]]
    # Hash equality plus actual streamed byte equality, not numeric tolerance.
    for name in names:
        with (first/name).open('rb') as a, (second/name).open('rb') as b:
            while True:
                left, right = a.read(1024*1024), b.read(1024*1024)
                if left != right and name not in mismatches:
                    mismatches.append(name)
                if not left and not right:
                    break
    checks = [read(d/'checker.json') for d in (first, second)]
    results = [read(d/'result.json') for d in (first, second)]
    roots = [read(d/'root.json') for d in (first, second)]
    for index, d in enumerate((first, second)):
        demand(checks[index]['status'] == 'CONTRACT_VALID', 'checker not accepting')
        demand(checks[index]['generator_files'] == files_index(d, CANONICAL_FILES), 'unfrozen generator')
        demand(roots[index]['files'] == files_index(d, (*CANONICAL_FILES, 'checker.json')), 'root mismatch')
        demand(roots[index]['logical_fingerprint'] == content_id(roots[index]['files']), 'fingerprint')
        demand(results[index]['proposed_outcome'] == checks[index]['independent_proposed_outcome'], 'outcome conflict')
    valid = not mismatches
    report = {'schema': 'JGA-EXACT-RELATION-WITNESS-V1',
        'execution_receipts': [content_id(e) for e in executions],
        'authority': results[0]['authority'], 'run_1': before, 'run_2': after,
        'mismatches': sorted(mismatches), 'integrity_status': 'CONTRACT_VALID' if valid else 'REPLAY_MISMATCH',
        'scientific_outcome': results[0]['proposed_outcome'] if valid else 'INDETERMINATE',
        'candidate_acceptance': 'ADMISSIBLE_COMPLETE_POPULATION' if valid else 'WITHHELD_INCOMPLETE_AUTHORITY',
        'scientific_status': 'RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED',
        'beat_reference_authorized': False, 'bpm_authorized': False}
    write(destination, report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('synthetic', 'real'))
    parser.add_argument('input', help='Synthetic fixture JSON or separate PI authorization JSON')
    parser.add_argument('destination')
    parser.add_argument('--worker', choices=('generator', 'checker'))
    parser.add_argument('--execution-authority', help='Custodian-controlled ledger outside run directories')
    args = parser.parse_args()
    destination = Path(args.destination).resolve()
    if args.worker != 'checker':
        demand(not destination.exists(), 'output already exists')
    # Real-input guard before loading any map. No default scientific input exists.
    if args.mode == 'synthetic':
        bundle = synthetic_bundle(args.input)
    else:
        bundle = authenticate_real(args.input, destination)
        expected = Path('/Volumes/SSD Track/JGA/experiments')/NAME
        demand(destination.parent == expected and destination.name in ('run_1', 'run_2'),
               'unauthorized scientific output destination')
    if args.worker == 'generator':
        import generator
        try:
            generator.generate(bundle, destination)
        except BaseException as exc:
            # Never modify frozen generator files after failure or checking.
            if destination.exists():
                write(destination/'failure.json', failure_report(exc, 'GENERATOR'))
            raise
    elif args.worker == 'checker':
        import checker
        try:
            checker.verify(bundle, destination)
            freeze_run(destination)
        except BaseException as exc:
            write(destination/'checker_failure.json', failure_report(exc, 'CHECKER'))
            raise
    else:
        demand(not destination.exists(), 'output already exists')
        demand(args.execution_authority is not None, 'execution custody ledger required')
        ledger = Path(args.execution_authority).resolve()
        demand(ledger != destination and destination not in ledger.parents,
               'ledger must be outside run output')
        if args.mode == 'real':
            approval = read(args.input)
            demand(str(ledger) == approval.get('execution_authority_directory'),
                   'custody ledger requires PI binding')
        ledger.mkdir(parents=True, exist_ok=True)
        execution_id = os.urandom(16).hex()
        binding = {'input_or_authorization_sha256': sha(args.input),
                   'source_files': {n: sha(HERE/n) for n in
                       ('runner.py', 'generator.py', 'checker.py', 'transport.py')},
                   'python_version': sys.version,
                   'executable_sha256': sha(Path(sys.executable).resolve()),
                   'mode': args.mode}
        workers = []
        # Two fresh processes independently re-admit all input authorities.
        for worker in ('generator', 'checker'):
            launch_id = os.urandom(16).hex()
            with subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()), args.mode,
                args.input, str(destination), '--worker', worker]) as process:
                code = process.wait()
                demand(code == 0, 'worker failed; no execution receipt issued')
                workers.append({'role': worker, 'launch_id': launch_id,
                                'pid': str(process.pid), 'exit_code': str(code)})
        demand(binding['input_or_authorization_sha256'] == sha(args.input) and
               all(sha(HERE/n) == h for n,h in binding['source_files'].items()),
               'execution binding changed while running')
        st = destination.stat()
        receipt = {'schema': 'JGA-FRESH-EXECUTION-V1', 'execution_id': execution_id,
            'status': 'COMPLETED_FRESH_WORKERS', 'workers': workers, 'binding': binding,
            'custody_directory': str(ledger),
            'directory': {'resolved_path': str(destination), 'device': str(st.st_dev), 'inode': str(st.st_ino)},
            'scientific_authority': read(destination/'result.json')['authority'],
            'canonical_files': files_index(destination, (*CANONICAL_FILES, 'checker.json', 'root.json'))}
        # Operational evidence is outside byte-identical scientific streams.
        write(ledger/(execution_id+'.json'), receipt)
        write(destination/'execution.json', receipt)


if __name__ == '__main__':
    main()
