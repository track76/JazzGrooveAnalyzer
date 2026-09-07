"""Read-only result checks and preservation; never evaluates operator queries."""
import json
import subprocess
from protocol import HERE, canonical, digest, write_new, verify_freeze


def main():
    verify_freeze()
    run1, run2 = ((HERE/name).read_bytes() for name in ("run_1.json","run_2.json"))
    score1, score2 = ((HERE/name).read_bytes() for name in ("score_1.json","score_2.json"))
    first, second = json.loads(score1), json.loads(score2)
    passed = first["classification"] == second["classification"] == "PASS"
    passed = passed and run1 == run2 and score1 == score2
    replay = {"operator_byte_identical":run1==run2,"scorer_byte_identical":score1==score2,
              "operator_sha256":digest(run1),"scoring_sha256":digest(score1),
              "unique_queries":64,"operator_evaluations_including_replay":128,
              "process_policy":"two independent CPython invocations per operator/scorer"}
    write_new("replay.json",replay)
    canonical_val = HERE.parent / "ad041_direct_input_acceptance_20260907/canonical_report_run_1.json"
    unchanged = digest(canonical_val.read_bytes()) == "eeb189217a722679d5f40bef4d809e2b38ab381e9dea81057023dfd3d80e05c7"
    result = {"classification":"LOCAL_COMPLEX_PERIODICITY_REPRESENTATION_VALIDATED" if passed and unchanged
              else "FAIL_REPRESENTATION_VALIDATION",
              "scope":"Only preregistered synthetic sparse measures, 64 queries, Q(zeta_16) exact path",
              "replay":replay,"checks_per_scoring_pass":len(first["checks"]),
              "mismatches":first["mismatches"]+second["mismatches"],
              "accepted_VAL001_unchanged":unchanged,
              "scientific_fingerprint_definition":"SHA-256 of byte-identical canonical operator output",
              "scientific_fingerprint":digest(run1),
              "unauthorized":["audio validity","detector validity","floating-point evaluator",
                  "frequency discovery","window optimization","trajectory tracking","Drum beat tracking",
                  "BeatReference","musical phase","tactus","BPM"]}
    write_new("result.json",result)
    tracked = subprocess.check_output(["git","diff","HEAD","--name-only","--","src","docs","validation"],text=True)
    write_new("preservation.json",{"tracked_src_docs_validation_diff":tracked.splitlines(),
              "runtime_sha256":digest((HERE/"runtime.json").read_bytes()),
              "artifact_checksums":{p.name:digest(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file()}})
    print(json.dumps(result))
    return 0 if result["classification"] == "LOCAL_COMPLEX_PERIODICITY_REPRESENTATION_VALIDATED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
