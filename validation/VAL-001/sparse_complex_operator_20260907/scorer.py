"""Independent algebraic oracle; never imported by the evaluated operator.

Uses polynomial long reduction rather than the evaluator's vector arithmetic.
No event/window summation, evaluator imports or floating-point trigonometry.
"""
import json
import sys
from fractions import Fraction as Q
from protocol import HERE, PRE, STEM, canonical, digest, rational, write_new, verify_freeze


class P:
    def __init__(self, terms=None):
        self.terms = {k: Q(v) for k, v in (terms or {}).items() if v}
        for degree in sorted(list(self.terms), reverse=True):
            if degree >= 8:
                value = self.terms.pop(degree)
                # All multiplication inputs have degree <=7, so degree<=14.
                self.terms[degree-8] = self.terms.get(degree-8, Q(0)) - value
        self.terms = {k: v for k, v in self.terms.items() if v}

    @staticmethod
    def constant(value):
        return P({0: Q(value)})

    @staticmethod
    def z(k):
        if Q(k).denominator != 1:
            raise ValueError("nonintegral oracle exponent")
        cycles, residue = divmod(int(k), 8)
        return P({residue: -1 if cycles % 2 else 1})

    def __add__(self, other):
        other = other if isinstance(other, P) else P.constant(other)
        keys = set(self.terms) | set(other.terms)
        return P({k: self.terms.get(k, 0)+other.terms.get(k, 0) for k in keys})

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.terms.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, P) else -Q(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = other if isinstance(other, P) else P.constant(other)
        terms = {}
        for j, x in self.terms.items():
            for k, y in other.terms.items():
                terms[j+k] = terms.get(j+k, 0) + x*y
        return P(terms)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (1 / Q(scalar))

    def conjugate(self):
        return sum((P.z(-k)*v for k, v in self.terms.items()), P())

    def vector(self):
        return [rational(self.terms.get(k, 0)) for k in range(8)]

    @staticmethod
    def read(values):
        if len(values) != 8 or any(not isinstance(x, str) or rational(x) != x for x in values):
            raise ValueError("noncanonical field vector")
        return P(dict(enumerate(map(Q, values))))


def symbolic(value):
    conj = value.conjugate()
    real, imag = (value+conj)/2, (value-conj)*P.z(-4)/2
    square = (value*conj).vector()
    phase = {"status": "UNDEFINED"} if not value.terms else {
        "status": "EXACT_SYMBOLIC", "kind": "principal_atan2",
        "real_vector": real.vector(), "imag_vector": imag.vector(),
        "unit_direction": {"numerator_vector": value.vector(), "denominator": {
            "kind": "nonnegative_sqrt", "radicand_vector": square}}}
    return {"complex_field_vector": value.vector(), "magnitude_squared_vector": square,
            "magnitude": {"kind": "nonnegative_sqrt", "radicand_vector": square}, "phase": phase}


def oracle_tables():
    one, zero = P.constant(1), P()
    r = P.z(2)-P.z(6)
    c1, c3 = (P.z(1)+P.z(-1))/2, (P.z(3)+P.z(-3))/2
    c = one+(c1+c3)/2
    return {
        "A_MU": {4: [one, zero, 2*one, 2*one],
                 8: [zero, one-r/2, 3*one+r/2, 3*one+r/2]},
        "A_NU": {4: [one/2, zero, -one, one],
                 8: [r*(c1-c3)/4, zero, -c, c]},
        "A_RHO": {4: [one/2]*4, 8: [zero, one, one, one]},
        "E": {4: [3*one/2, one/2, 5*one/2, 5*one/2],
              8: [zero, 2*one-r/2, 4*one+r/2, 4*one+r/2]},
        "F": {4: [2*one, zero, zero, 4*one],
              8: [r*(c1-c3)/2, one-r/2, 3*one+r/2-2*c, 3*one+r/2+2*c]},
    }


def main(number):
    if number not in ("1", "2"):
        raise ValueError("only two scoring passes authorized")
    freeze = verify_freeze()
    path = HERE / ("run_"+number+".json")
    output_bytes = path.read_bytes()  # output must exist BEFORE constructing oracle
    output = json.loads(output_bytes)
    prepared = json.loads((HERE / "prepared_inputs.json").read_bytes())
    raw = json.loads((PRE / (STEM+".inputs.json")).read_bytes())
    checks, mismatches = [], []

    def check(name, actual, expected=True):
        passed = actual == expected
        checks.append({"check": name, "pass": passed})
        if not passed:
            mismatches.append({"check": name, "actual": actual, "expected": expected})

    check("canonical_operator_bytes", digest(output_bytes), digest(canonical(output)))
    check("freeze_hash", output["freeze_sha256"], digest((HERE/"freeze.json").read_bytes()))
    check("input_hash", output["input_sha256"], freeze["prepared_inputs_sha256"])
    for parent, triples in raw["measures"].items():
        manifest = {"authority_id": raw["authority_id"], "measure_id": parent,
                    "units": raw["time_unit"], "events": triples}
        check("source_manifest_"+parent, prepared["source_manifests"][parent], manifest)
        check("source_hash_"+parent, prepared["source_checksums"][parent], digest(canonical(manifest)))

    # Independent declaration of exactly the frozen query keys, not discovery.
    cases = ["A_MU", "A_NU", "A_RHO", "B", "C", "D", "E", "F"]
    freq = [Q(1, 4), Q(1, 2), Q(1), Q(2)]
    keys = [(case, Q(1,4) if case == "C" else Q(0),
             f/Q(3,2) if case == "D" else f,
             Q(length)*Q(3,2) if case == "D" else Q(length))
            for case in cases for f in freq for length in (4,8)]
    records = output["records"]
    actual_keys = [(r["case_id"], *(Q(r["query"][k]) for k in ("u","f","L"))) for r in records]
    show_key = lambda key: [key[0], *map(rational, key[1:])]
    check("population_64", len(records), 64)
    check("unique_keys_64", len(set(actual_keys)), 64)
    check("exact_ordered_keys", list(map(show_key, actual_keys)), list(map(show_key, keys)))
    index = dict(zip(actual_keys, records))
    tables = oracle_tables()
    parents_by_case = {"A_MU":["MU"],"A_NU":["NU"],"A_RHO":["RHO"],
                       "B":["MU","NU","RHO"],"C":["MU"],"D":["MU","NU"],
                       "E":["MU","RHO"],"F":["MU","NU"]}
    property_counts = {case: 0 for case in cases}
    nonzero_translation = 0
    for key in keys:
        case,u,f,length = key
        label = ":".join(show_key(key))
        if key not in index:
            continue
        record = index[key]
        base_f = f*Q(3,2) if case == "D" else f
        base_l = int(length/Q(3,2)) if case == "D" else int(length)
        slot = freq.index(base_f)
        m,n,r = (tables[c][base_l][slot] for c in ("A_MU","A_NU","A_RHO"))
        expected = {"B": m+n+r, "C": P.z(-4*base_f)*m, "D": m+n}.get(case)
        if expected is None:
            expected = tables[case][base_l][slot]
        check(label+":oracle", record["complex_field_vector"], expected.vector())
        for name,value in symbolic(expected).items():
            check(label+":"+name, record[name], value)
        property_counts[case] += 1
        nonzero_translation += int(case == "C" and bool(expected.terms))
        expected_events = []
        for parent in parents_by_case[case]:
            for eid,t,s in raw["measures"][parent]:
                time = Q(t)*Q(3,2) if case == "D" else Q(t)+Q(1,4) if case == "C" else Q(t)
                strength = Q(s)*2 if case == "F" and parent == "NU" else Q(s)
                expected_events.append({"id":eid,"timestamp":rational(time),"strength":rational(strength),
                     "parent_id":eid,"parent_measure":parent,"parent_timestamp":t,"parent_strength":s,
                     "parent_checksum":prepared["source_checksums"][parent]})
        expected_events.sort(key=lambda e:(Q(e["timestamp"]),e["id"]))
        manifest = prepared["derived_manifests"][case]
        check(label+":derived_events", manifest["events"], expected_events)
        check(label+":parents", manifest["parents"],
              {p:prepared["source_checksums"][p] for p in parents_by_case[case]})
        check(label+":operation", manifest["operation"], {
            "nu_weight_multiplier":"2/1" if case=="F" else "1/1",
            "translation":"1/4" if case=="C" else "0/1",
            "dilation":"3/2" if case=="D" else "1/1"})
        checksum = digest(canonical(manifest))
        check(label+":construction_hash", record["construction_checksum"],checksum)
        check(label+":source_identity", record["source_measure_id"],checksum)
        parameter = digest(canonical({"authority":raw["authority_id"],"query":record["query"]}))
        check(label+":parameter_hash",record["parameter_authority"],parameter)
        contribution_events = [{k:v for k,v in e.items() if k not in ("window_vector","contribution_vector")}
                               for e in record["contributions"]]
        check(label+":event_lineage", contribution_events, expected_events)
        total = P()
        for event in record["contributions"]:
            weight = P.read(event["window_vector"])
            contribution = P.read(event["contribution_vector"])
            # Checks serialized contributions using exact independent field semantics,
            # without reproducing window/onset summation as an expected-answer oracle.
            term = weight*P.z(-16*f*Q(event["timestamp"]))*Q(event["strength"])
            check(label+":contribution:"+event["id"], contribution.vector(),term.vector())
            total = total+contribution
        check(label+":contribution_total",total.vector(),expected.vector())
        if case in ("B","C","D","E","F"):
            def component(c):
                return P.read(index[(c,Q(0),base_f,Q(base_l))]["complex_field_vector"])
            cm,cn,cr = (component(c) for c in ("A_MU","A_NU","A_RHO"))
            relation = {"B":cm+cn+cr,"C":P.z(-4*base_f)*cm,"D":cm+cn,
                        "E":cm+cr,"F":cm+2*cn}[case]
            check(label+":transformation_relation",record["complex_field_vector"],relation.vector())

    check("property_populations",property_counts,{c:8 for c in cases})
    check("nonzero_translation_coverage",nonzero_translation>0)
    cancel = index.get(("F",Q(0),Q(1),Q(4)),{})
    check("exact_cancellation",cancel.get("complex_field_vector"),P().vector())
    check("cancellation_phase_undefined",cancel.get("phase"),{"status":"UNDEFINED"})
    construct = index.get(("F",Q(0),Q(2),Q(4)),{})
    check("constructive_superposition",construct.get("complex_field_vector"),P.constant(4).vector())
    result = {"classification":"FAIL_REPRESENTATION_VALIDATION" if mismatches else "PASS",
              "query_count":len(records),"property_counts":property_counts,
              "operator_sha256":digest(output_bytes),"mismatches":mismatches,"checks":checks,
              "claim_scope":"EXACT_SYNTHETIC_MEASURES_64_QUERIES_ONLY; replay still required"}
    write_new("score_"+number+".json",result)
    print(json.dumps({"classification":result["classification"],"checks":len(checks),"mismatches":mismatches}))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
