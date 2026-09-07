"""Construction and execution harness. No expected-answer values."""
import hashlib
import json
import platform
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRE = HERE.parent / "preregistrations"
STEM = "H-VAL001-SPARSE-COMPLEX-OPERATOR-01"
BINDINGS = {
    STEM + ".md": "ca5f7f082875f297df3374f8cacc485d86132e299f434f70eb3267f91b501f1e",
    STEM + ".inputs.json": "c340e6bc7041c475b9f9f7989c94e662b22b2ce135c5e09040b60b298c2e20f5",
    "H-VAL001-LOCAL-COMPLEX-DRUM-PERIODICITY-01.md": "0eb3732a0b9cd3d43ad1ea3016a8d1a46841ead6738a7c17094eb5acf8f5bb15",
    "H-VAL001-DRUM-STRENGTH-ORGANIZATION-01.md": "bea46dbfe5b1cdcef114d45af86fe65302bfc208e8855de78161419964429089",
}


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("utf-8")


def digest(x):
    return hashlib.sha256(x).hexdigest()


def rational(x):
    x = Q(x)
    return f"{x.numerator}/{x.denominator}"


def write_new(name, value):
    with (HERE / name).open("xb") as stream:
        stream.write(canonical(value))


def verify_authority():
    if platform.python_implementation() != "CPython" or platform.python_version() != "3.13.14":
        raise RuntimeError("unsupported runtime")
    for name, expected in BINDINGS.items():
        if digest((PRE / name).read_bytes()) != expected:
            raise RuntimeError("authority checksum mismatch: " + name)


def prepare():
    verify_authority()
    raw = json.loads((PRE / (STEM + ".inputs.json")).read_bytes())
    authority, units = raw["authority_id"], raw["time_unit"]
    manifests = {}
    for name, triples in raw["measures"].items():
        manifests[name] = {"authority_id": authority, "measure_id": name,
                           "units": units, "events": triples}
    parent_hashes = {k: digest(canonical(v)) for k, v in manifests.items()}

    def events(parents, multiplier=Q(1), shift=Q(0), dilation=Q(1)):
        result = []
        for parent in parents:
            for eid, t, s in raw["measures"][parent]:
                factor = multiplier if parent == "NU" else Q(1)
                result.append({"id": eid, "timestamp": rational(Q(t)*dilation+shift),
                               "strength": rational(Q(s)*factor), "parent_id": eid,
                               "parent_measure": parent, "parent_timestamp": t,
                               "parent_strength": s, "parent_checksum": parent_hashes[parent]})
        return sorted(result, key=lambda e: (Q(e["timestamp"]), e["id"]))

    p = raw["scoring_query_authority"]
    configurations = [
        ("A_MU", ["MU"], Q(1), Q(0), Q(1)),
        ("A_NU", ["NU"], Q(1), Q(0), Q(1)),
        ("A_RHO", ["RHO"], Q(1), Q(0), Q(1)),
        ("B", ["MU", "NU", "RHO"], Q(1), Q(0), Q(1)),
        ("C", ["MU"], Q(1), Q(p["translation"]), Q(1)),
        ("D", ["MU", "NU"], Q(1), Q(0), Q(p["dilation"])),
        ("E", ["MU", "RHO"], Q(1), Q(0), Q(1)),
        ("F", ["MU", "NU"], Q(p["superposition_multiplier"]), Q(0), Q(1)),
    ]
    queries, derived = [], {}
    for case, parents, factor, shift, dilation in configurations:
        manifest = {"authority_id": authority, "measure_id": case, "units": units,
                    "parents": {k: parent_hashes[k] for k in parents},
                    "operation": {"nu_weight_multiplier": rational(factor),
                                  "translation": rational(shift), "dilation": rational(dilation)},
                    "events": events(parents, factor, shift, dilation)}
        derived[case] = manifest
        for f in p["frequencies"]:
            for length in p["window_lengths"]:
                query = {"u": rational(Q(p["center"])*dilation+shift),
                         "f": rational(Q(f)/dilation), "L": rational(Q(length)*dilation)}
                queries.append({"case_id": case, "query": query,
                                "construction_checksum": digest(canonical(manifest)),
                                "parameter_authority": digest(canonical({"authority": authority, "query": query}))})
    queries.sort(key=lambda x: (x["case_id"], *(Q(x["query"][k]) for k in ("u", "f", "L"))))
    prepared = {"authority_id": authority, "source_manifests": manifests,
                "source_checksums": parent_hashes, "derived_manifests": derived,
                "queries": queries}
    write_new("prepared_inputs.json", prepared)
    freeze = {"authority_bindings": BINDINGS,
              "source_hashes": {p.name: digest(p.read_bytes()) for p in sorted(HERE.glob("*.py"))},
              "prepared_inputs_sha256": digest(canonical(prepared)),
              "baseline": "51cedd8dba23906e870f2df6d64382831f4d3e74",
              "scientific_scope": "EXACT_SYNTHETIC_OPERATOR_ONLY"}
    write_new("freeze.json", freeze)
    write_new("runtime.json", {"version": sys.version, "implementation": platform.python_implementation(),
                               "platform": platform.platform(), "arithmetic": "Fraction / Q(zeta_16)",
                               "runtime_policy": "CPython 3.13.14; standard library only"})
    print("FROZEN; no operator queries executed")


def verify_freeze():
    verify_authority()
    freeze = json.loads((HERE / "freeze.json").read_bytes())
    for name, expected in freeze["source_hashes"].items():
        if digest((HERE / name).read_bytes()) != expected:
            raise RuntimeError("implementation changed after freeze: " + name)
    if digest((HERE / "prepared_inputs.json").read_bytes()) != freeze["prepared_inputs_sha256"]:
        raise RuntimeError("prepared input changed")
    return freeze


def run(label):
    freeze = verify_freeze()
    if label not in ("run_1", "run_2"):
        raise ValueError("only two executions authorized")
    if (HERE / (label + ".json")).exists():
        raise RuntimeError("refusing repeated/overwritten execution")
    if label == "run_2":
        first = json.loads((HERE / "score_1.json").read_bytes())
        if first["classification"] != "PASS":
            raise RuntimeError("STOP: first score failed")
    from evaluator import evaluate
    prepared = json.loads((HERE / "prepared_inputs.json").read_bytes())
    records = []
    for q in prepared["queries"]:
        # API boundary deliberately excludes case/operation/expected-answer data.
        try:
            value = evaluate(prepared["derived_manifests"][q["case_id"]]["events"],
                             q["query"], q["parameter_authority"])
        except Exception as error:
            write_new(label + "_failure.json", {
                "classification": "FAIL_REPRESENTATION_VALIDATION", "query": q,
                "completed_records": records, "error": type(error).__name__+": "+str(error)})
            raise
        records.append({**q, "source_measure_id": q["construction_checksum"], **value})
    write_new(label + ".json", {"freeze_sha256": digest((HERE / "freeze.json").read_bytes()),
              "input_sha256": freeze["prepared_inputs_sha256"],
              "numeric_authority": "Q(zeta_16); exact rational vectors; zero tolerance",
              "records": records})
    print(f"{label}: {len(records)} queries executed")


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    else:
        run(sys.argv[1])
