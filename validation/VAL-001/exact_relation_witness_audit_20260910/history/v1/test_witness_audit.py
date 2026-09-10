"""Synthetic/integrity checks only. No scientific input paths are opened."""
import copy
import json
import math
import random
import struct
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

import checker
import generator
from fixtures import fixture
from transport import canonical, content_id, read, rows, parse, verify_sha
import runner


class WitnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='jga-synthetic-witness-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.serial = 0

    def run_fixture(self, bundle):
        self.serial += 1
        path = self.root / str(self.serial)
        result = generator.generate(bundle, path)
        checker.verify(bundle, path)
        return path, result

    def test_A_no_recurrence_and_coordinate_negative(self):
        path, result = self.run_fixture(fixture([0, 1, 3]))
        self.assertEqual(result['proposed_outcome'], 'NO_EXACT_RELATION_RECURRENCE_OBSERVED')
        self.assertEqual(read(path/'candidate_population.json')['members'], [])
        # Multiple center/window coordinates still yield singleton relations.
        self.assertGreater(int(read(path/'reuse_audit.json')['both_contained_occurrences']), 3)
        self.assertTrue(all(r['witness_count'] == '1' for r in rows(path/'relations.jsonl')))

    def test_B_one_relation_with_disjoint_support(self):
        # Coincident but distinct synthetic events: one repeated positive T,
        # including two disjoint pairs; all four supports MUST be retained.
        path, result = self.run_fixture(fixture([0, 1, 1, 2]))
        self.assertEqual(result['population_classification'], 'ONE_REPEATED_EXACT_RELATION')
        members = read(path/'candidate_population.json')['members']
        self.assertEqual([(m['seconds'], m['witness_count']) for m in members], [(['1', '1'], '4')])
        self.assertTrue(any(r['dependence'] == 'EVENT_DISJOINT' for r in rows(path/'witness_relations.jsonl')))
        self.assertEqual(len(read(path/'reuse_audit.json')['coincident_distinct_events']), 1)

    def test_C_shared_endpoint(self):
        path, _ = self.run_fixture(fixture([0, 1, 2]))
        deps = list(rows(path/'witness_relations.jsonl'))
        self.assertEqual(len(deps), 1)
        self.assertEqual(deps[0]['shared_event_ids'], ['E001'])
        self.assertEqual(deps[0]['temporal_relation'], 'TOUCH')
        self.assertEqual(deps[0]['statistical_independence'], 'NOT_ESTABLISHED')

    def test_DE_window_center_reuse(self):
        path, result = self.run_fixture(fixture([0, 1, 2, 4]))
        windows = list(rows(path/'windows.jsonl'))
        witnesses = list(rows(path/'witnesses.jsonl'))
        self.assertEqual(len(witnesses), 6)
        pair = witnesses[0]['witness_id']
        matches = [w for w in windows if pair in w['both_contained']]
        self.assertGreater(len(matches), 1)
        self.assertGreater(len({tuple(w['body']['u']) for w in matches}), 1)
        self.assertEqual(result['counts']['positive_witnesses'], '6')

    def test_FG_multiple_relations_exact_ratios(self):
        path, _ = self.run_fixture(fixture([0, 1, 2, 3]))
        members = read(path/'candidate_population.json')['members']
        self.assertEqual([m['seconds'] for m in members], [['1', '1'], ['2', '1']])
        self.assertEqual(list(rows(path/'relation_ratios.jsonl'))[0]['ratio_b_over_a'], ['2', '1'])
        # All unequal timestamp case: disjoint equal pairs necessarily induce
        # another repeated difference. Neither relation can be suppressed.
        path, _ = self.run_fixture(fixture([0, 1, 4, 5]))
        self.assertEqual([m['seconds'] for m in read(path/'candidate_population.json')['members']],
                         [['1', '1'], ['4', '1']])

    def test_H_close_binary64_differences_do_not_merge(self):
        path, result = self.run_fixture(fixture([0, 1, math.nextafter(2.0, math.inf)]))
        self.assertEqual(result['counts']['repeated_relations'], '0')
        periods = [r['seconds'] for r in rows(path/'relations.jsonl')]
        self.assertEqual(len(periods), 3)
        self.assertIn(['1', '1'], periods)
        self.assertIn(['2251799813685249', '2251799813685248'], periods)

    def test_I_reversed_catalogue_pair_identity(self):
        a, _ = self.run_fixture(fixture([0, 1, 2]))
        b, _ = self.run_fixture(fixture([0, 1, 2], reverse=True))
        self.assertEqual([r['witness_id'] for r in rows(a/'witnesses.jsonl')],
                         [r['witness_id'] for r in rows(b/'witnesses.jsonl')])

    def test_J_duplicate_authoritative_pair_rejected(self):
        bundle = fixture([0, 1, 3])
        record = bundle['periods'][0]
        record['body']['pairs'].append(copy.deepcopy(record['body']['pairs'][0]))
        record['id'] = content_id(record['body'])
        with self.assertRaises(generator.ContractError):
            generator.generate(bundle, self.root/'bad')
        with self.assertRaises(checker.Disagreement):
            checker.verify(bundle, self.root/'absent')

    def test_K_missing_and_invalid_authority(self):
        mutations = [lambda b: b['input']['events'][0].update(source_identity='WRONG'),
            lambda b: b['input']['events'][0].update(pulse_candidate_id='P001'),
            lambda b: b['periods'].pop(),
            lambda b: b['periods'][0].update(id='0'*64),
            lambda b: b['input']['events'][0]['timestamp'].update(producer_bits='7ff0000000000000'),
            lambda b: b['input']['events'][0]['timestamp'].update(ratio=['0', '2'])]
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                bundle = fixture([0, 1, 2])
                mutation(bundle)
                with self.assertRaises((generator.ContractError, KeyError)):
                    generator.generate(bundle, self.root/f'bad{index}')
                with self.assertRaises((checker.Disagreement, KeyError)):
                    checker.verify(bundle, self.root/'absent')

    def test_boundary_and_window_coverage_tampering(self):
        bundle = fixture([0, 1, 2])
        path, _ = self.run_fixture(bundle)
        windows = list(rows(path/'windows.jsonl'))
        self.assertTrue(any(w['body']['membership']['boundary'] for w in windows))
        bundle['windows'][0]['body']['membership']['positive'].append('E999')
        bundle['windows'][0]['id'] = content_id(bundle['windows'][0]['body'])
        with self.assertRaises(generator.ContractError):
            generator.generate(bundle, self.root/'badwindow')
        with self.assertRaises(checker.Disagreement):
            checker.verify(bundle, path)

    def test_checker_detects_every_output_file_tampering(self):
        bundle = fixture([0, 1, 2, 3])
        for name in (*generator.DATA, 'result.json'):
            with self.subTest(name=name):
                self.serial += 1
                path = self.root/str(self.serial)
                generator.generate(bundle, path)
                file = path/name
                file.write_bytes(file.read_bytes()+b'\n')
                with self.assertRaises(checker.Disagreement):
                    checker.verify(bundle, path)

    def test_L_fresh_process_determinism(self):
        fixture_path = self.root/'fixture.json'
        fixture_path.write_bytes(canonical(fixture([0, 1, 2, 3]))+b'\n')
        script = Path(__file__).with_name('runner.py')
        outputs = []
        for index in (1, 2):
            dest = self.root/f'run{index}'
            subprocess.run([sys.executable, '-B', str(script), 'synthetic',
                            str(fixture_path), str(dest)], check=True, capture_output=True)
            outputs.append(dest)
        self.assertEqual({p.name for p in outputs[0].iterdir()}, {p.name for p in outputs[1].iterdir()})
        for file in outputs[0].iterdir():
            self.assertEqual(file.read_bytes(), (outputs[1]/file.name).read_bytes())
        replay = runner.compare_replay(*outputs, self.root/'replay.json')
        self.assertEqual(replay['candidate_acceptance'], 'ADMISSIBLE_COMPLETE_POPULATION')

    def test_preflight_and_failure_vocabularies(self):
        self.assertEqual(runner.failure_report(FileNotFoundError(), 'PREFLIGHT')['scientific_outcome'],
                         'INSUFFICIENT_EVIDENCE')
        self.assertEqual(runner.failure_report(ValueError(), 'CHECKER')['scientific_outcome'],
                         'INDETERMINATE')
        self.assertEqual(runner.failure_report(OSError(), 'GENERATOR')['candidate_acceptance'],
                         'WITHHELD_INCOMPLETE_AUTHORITY')
        # No real input is opened: absent authorization fails at its own open.
        with self.assertRaises(FileNotFoundError):
            runner.authenticate_real(self.root/'NO_PI_AUTHORIZATION', self.root/'run_1')
        bundle = fixture([0, 1, 2])
        bundle['binding']['source_uuid'] = runner.REAL_SOURCE
        path = self.root/'forbidden.json'
        path.write_bytes(canonical(bundle))
        with self.assertRaises(ValueError):
            runner.synthetic_bundle(path)
        with self.assertRaises(generator.ContractError):
            generator.generate(bundle, self.root/'forbidden_result')
        with self.assertRaises(checker.Disagreement):
            checker.verify(bundle, self.root/'forbidden_result')

    def test_replay_mismatch_withholds_admissibility(self):
        first, _ = self.run_fixture(fixture([0, 1, 2]))
        second, _ = self.run_fixture(fixture([0, 1, 3]))
        runner.freeze_run(first)
        runner.freeze_run(second)
        report = runner.compare_replay(first, second, self.root/'mismatch.json')
        self.assertEqual(report['scientific_outcome'], 'INDETERMINATE')
        self.assertEqual(report['candidate_acceptance'], 'WITHHELD_INCOMPLETE_AUTHORITY')

    def test_duplicate_catalogue_and_window_records_rejected(self):
        for name in ('periods', 'windows'):
            bundle = fixture([0, 1, 2])
            valid, _ = self.run_fixture(copy.deepcopy(bundle))
            bundle[name].append(copy.deepcopy(bundle[name][0]))
            with self.assertRaises(generator.ContractError):
                generator.generate(bundle, self.root/f'bad-{name}')
            with self.assertRaises(checker.Disagreement):
                checker.verify(bundle, valid)

    def test_no_semantic_fields_admitted(self):
        bundle = fixture([0, 1, 2])
        bundle['input']['events'][0]['musical_role'] = 'FORBIDDEN_SYNTHETIC_LABEL'
        with self.assertRaises(generator.ContractError):
            generator.generate(bundle, self.root/'semantic')
        with self.assertRaises(checker.Disagreement):
            checker.verify(bundle, self.root/'absent')

    def test_authority_bytes_and_serialization(self):
        path = self.root/'authority.bin'
        path.write_bytes(b'abc')
        expected = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
        self.assertEqual(verify_sha(path, expected), expected)
        path.write_bytes(b'abd')
        with self.assertRaises(ValueError):
            verify_sha(path, expected)
        with self.assertRaises(ValueError):
            parse('{"same":1,"same":2}')
        with self.assertRaises(ValueError):
            parse('{"number":NaN}')
        with self.assertRaises(TypeError):
            canonical({'floating_output': 0.1})

    def test_opaque_identity_renaming(self):
        original = fixture([0, 1, 2, 3])
        first, _ = self.run_fixture(original)
        def rename(value):
            if isinstance(value, str) and len(value) == 4 and value[0] in ('E', 'P') and value[1:].isdigit():
                return ('Z' if value[0] == 'E' else 'Q')+value[1:]
            if isinstance(value, dict):
                return {k: rename(v) for k, v in value.items()}
            if isinstance(value, list):
                return [rename(v) for v in value]
            return value
        changed = rename(original)
        for name in ('inputs', 'periods', 'windows'):
            for entry in changed[name]:
                entry['id'] = content_id(entry['body'])
        second, _ = self.run_fixture(changed)
        self.assertEqual([(r['seconds'], r['witness_count']) for r in rows(first/'relations.jsonl')],
                         [(r['seconds'], r['witness_count']) for r in rows(second/'relations.jsonl')])

    def test_exact_decoder_properties(self):
        words = [0, 1 << 63, 1, (1 << 52)-1, 1 << 52, 0x7fefffffffffffff]
        rng = random.Random(194071)
        words += [rng.getrandbits(64) for _ in range(200)]
        for word in words:
            if (word >> 52) & 2047 == 2047:
                continue
            value = struct.unpack('>d', word.to_bytes(8, 'big'))[0]
            n, d = value.as_integer_ratio()
            record = {'producer_bits': f'{word:016x}', 'ratio': [str(n), str(d)],
                      'hex': value.hex(), 'original_json_numeric_token': json.dumps(value),
                      'field_lineage': '/synthetic/numeric'}
            self.assertEqual(generator.ratio(generator.decode(record)), [str(n), str(d)])
            self.assertEqual(checker.producer(record).json(), [str(n), str(d)])

    def test_seeded_small_population_properties(self):
        rng = random.Random(512913)
        for _ in range(16):
            values = sorted(rng.sample(range(30), 5))
            bundle = fixture(values)
            path, result = self.run_fixture(bundle)
            self.assertEqual(result['counts']['positive_witnesses'], '10')
            expected = {}
            for i in range(5):
                for j in range(i+1, 5):
                    expected.setdefault(values[j]-values[i], 0)
                    expected[values[j]-values[i]] += 1
            self.assertEqual({int(r['seconds'][0]): int(r['witness_count'])
                              for r in rows(path/'relations.jsonl')}, expected)

    def test_input_order_permutation(self):
        bundle = fixture([0, 1, 2, 3])
        a, _ = self.run_fixture(bundle)
        bundle['input']['events'].reverse()
        bundle['inputs'][0]['body']['events'] = bundle['input']['events']
        bundle['inputs'][0]['id'] = content_id(bundle['inputs'][0]['body'])
        bundle['periods'].reverse()
        b, _ = self.run_fixture(bundle)
        # In-memory property fixture intentionally keeps the same identity freeze;
        # operational admission authenticates serialized input bytes separately.
        for name in generator.DATA:
            self.assertEqual((a/name).read_bytes(), (b/name).read_bytes())


if __name__ == '__main__':
    unittest.main(verbosity=2)
