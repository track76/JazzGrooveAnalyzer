#!/usr/bin/env python3
"""Deterministic read-only RX/htdemucs_ft complementarity audit."""

import hashlib
import json
import math
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PROTO_PATH = REPO / "validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/preregistrations/H-CEDVAL006-RX-HTDEMUCSFT-COMPLEMENTARITY-AUDIT-01.json"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def quantile(values, q):
    values = sorted(values)
    pos = (len(values) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    return values[lo] if lo == hi else values[lo] * (hi - pos) + values[hi] * (pos - lo)


def stats(values):
    values = list(values)
    return {"count": len(values), "minimum": min(values), "q1_linear": quantile(values, .25),
            "median": statistics.median(values), "q3_linear": quantile(values, .75),
            "maximum": max(values), "mean": statistics.fmean(values),
            "population_sd": statistics.pstdev(values),
            "rmse": math.sqrt(statistics.fmean(x*x for x in values))}


def seconds(value):
    return value["seconds"]


def map_matches(level2):
    return {m["original_eme_id"]: {"original_time": seconds(m["original_time"]),
            "separated_time": seconds(m["separated_time"]),
            "signed_displacement": seconds(m["signed_displacement"]),
            "absolute_displacement": seconds(m["absolute_displacement"])} for m in level2["matches"]}


def main(output_name):
    proto = json.loads(PROTO_PATH.read_text())
    fingerprint_payload = dict(proto)
    expected = fingerprint_payload.pop("protocol_fingerprint")
    assert hashlib.sha256(canonical(fingerprint_payload).encode()).hexdigest() == expected
    authorities = proto["authority"]
    dp = REPO / authorities["demucs_scoring_path"]
    rp = REPO / authorities["rx_scoring_path"]
    assert sha(dp) == authorities["demucs_scoring_sha256"]
    assert sha(rp) == authorities["rx_scoring_sha256"]
    demucs_l2 = json.loads(dp.read_text())["runs"]["M1_run_1"]["level_2"]["Double Bass"]
    rx_l2 = json.loads(rp.read_text())["runs"]["run_1"]["level_2"]["Double Bass"]
    dm, rx = map_matches(demucs_l2), map_matches(rx_l2)
    original_ids = set(dm) | {x["original_eme_id"] for x in demucs_l2["original_only"]}
    assert len(original_ids) == 1055
    assert original_ids == set(rx) | {x["original_eme_id"] for x in rx_l2["original_only"]}
    both = sorted(set(dm) & set(rx))
    donly = sorted(set(dm) - set(rx))
    rxonly = sorted(set(rx) - set(dm))
    neither = sorted(original_ids - set(dm) - set(rx))
    assert len(both)+len(donly)+len(rxonly)+len(neither) == 1055
    union = len(both)+len(donly)+len(rxonly)
    jaccard = len(both)/union
    cond_rx = len(rxonly)/(1055-len(dm))
    cond_dm = len(donly)/(1055-len(rx))
    increment = union-max(len(dm), len(rx))
    if increment >= 106 and jaccard <= .75 and cond_rx >= .20 and cond_dm >= .20:
        classification = "HIGH_COMPLEMENTARITY"
    elif increment >= 22 or jaccard < .90 or cond_rx >= .05 or cond_dm >= .05:
        classification = "LIMITED_COMPLEMENTARITY"
    else:
        classification = "NEGLIGIBLE_COMPLEMENTARITY"
    fusion = "YES" if classification in ("HIGH_COMPLEMENTARITY", "LIMITED_COMPLEMENTARITY") and len(donly) >= 22 and len(rxonly) >= 22 else "NO"
    def timing(mapping, ids):
        signed = [mapping[i]["signed_displacement"] for i in ids]
        absolute = [mapping[i]["absolute_displacement"] for i in ids]
        return {"signed_displacement_seconds": stats(signed), "absolute_displacement_seconds": stats(absolute)}
    pairdiff = [rx[i]["absolute_displacement"]-dm[i]["absolute_displacement"] for i in both]
    closer = {"demucs_closer": sum(dm[i]["absolute_displacement"] < rx[i]["absolute_displacement"] for i in both),
              "rx_closer": sum(rx[i]["absolute_displacement"] < dm[i]["absolute_displacement"] for i in both),
              "equal": sum(rx[i]["absolute_displacement"] == dm[i]["absolute_displacement"] for i in both)}
    result = {
        "audit_id": proto["audit_id"], "protocol_id": proto["protocol_id"],
        "protocol_fingerprint": expected,
        "authorities": authorities,
        "partition": {"A_BOTH": {"count": len(both), "percentage": len(both)/10.55, "original_eme_ids": both},
            "B_DEMUCS_ONLY": {"count": len(donly), "percentage": len(donly)/10.55, "original_eme_ids": donly},
            "C_RX_ONLY": {"count": len(rxonly), "percentage": len(rxonly)/10.55, "original_eme_ids": rxonly},
            "D_NEITHER": {"count": len(neither), "percentage": len(neither)/10.55, "original_eme_ids": neither}},
        "overlap": {"demucs_recall": len(dm)/1055, "rx_recall": len(rx)/1055,
            "union_count": union, "union_recall": union/1055,
            "intersection_count": len(both), "intersection_recall": len(both)/1055,
            "jaccard": jaccard, "union_increment_over_best_count": increment},
        "conditional_recovery": {"rx_among_demucs_missed": {"numerator": len(rxonly), "denominator": 1055-len(dm), "rate": cond_rx},
            "demucs_among_rx_missed": {"numerator": len(donly), "denominator": 1055-len(rx), "rate": cond_dm}},
        "timing": {"both": {"demucs": timing(dm, both), "rx": timing(rx, both),
            "closer_counts": closer, "rx_absolute_minus_demucs_absolute_seconds": stats(pairdiff)},
            "demucs_only": timing(dm, donly), "rx_only": timing(rx, rxonly)},
        "classification": classification,
        "future_non_ground_truth_consensus_fusion_study": fusion,
        "principle_if_yes": "Prospectively test separator agreement and detector-native confidence/consistency as Ground-Truth-independent evidence for consensus or abstention; never select using original-event proximity." if fusion == "YES" else None,
        "firewall": proto["firewall"],
    }
    result["audit_fingerprint"] = hashlib.sha256(canonical(result).encode()).hexdigest()
    (HERE / output_name).write_text(canonical(result) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
