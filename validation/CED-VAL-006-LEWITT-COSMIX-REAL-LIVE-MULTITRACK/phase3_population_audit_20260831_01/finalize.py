#!/usr/bin/env python3
from hashlib import sha256
import json
import math
from pathlib import Path
import statistics

HERE = Path(__file__).resolve().parent

def canonical(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")

def digest(path):
    h = sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def subgroup(records):
    result = {"count": len(records), "audio": {}}
    for asset in ("original", "unprocessed", "processed"):
        result["audio"][asset] = {
            "median_rms_dbfs": statistics.median(item["features"][asset]["rms_dbfs"] for item in records),
            "median_peak_dbfs": statistics.median(item["features"][asset]["peak_dbfs"] for item in records),
            "rms_below_threshold_count": sum(item["features"][asset]["rms_below_threshold"] for item in records),
            "median_band_energy_fraction": {band: statistics.median(item["features"][asset]["band_energy_fraction"][band] for item in records) for band in records[0]["features"][asset]["band_energy_fraction"]},
        }
    displacement = [item["unprocessed_signed_displacement_seconds"] for item in records if item["unprocessed_signed_displacement_seconds"] is not None]
    result["unprocessed_timing"] = None if not displacement else {"signed_median_seconds": statistics.median(displacement), "absolute_median_seconds": statistics.median(map(abs, displacement)), "rmse_seconds": math.sqrt(statistics.fmean(value * value for value in displacement)), "maximum_absolute_seconds": max(map(abs, displacement))}
    return result

execution_1 = HERE / "audit_execution_1.json"
execution_2 = HERE / "audit_execution_2.json"
assert execution_1.read_bytes() == execution_2.read_bytes()
audit = json.loads(execution_1.read_text())
expected_audit_fingerprint = audit.pop("audit_fingerprint")
assert sha256(canonical(audit)).hexdigest() == expected_audit_fingerprint
audit["audit_fingerprint"] = expected_audit_fingerprint
summaries = audit["population_summaries"]
records = audit["complete_population_records"]
c_records = records["C_STILL_UNMATCHED_AFTER_PROCESSING"]
never = [item for item in c_records if item["unprocessed_timestamp_seconds"] is None]
lost = [item for item in c_records if item["unprocessed_timestamp_seconds"] is not None]
assert {name: summaries[name]["count"] for name in summaries} == {"A_MATCHED_BEFORE_AND_AFTER": 606, "B_RECOVERED_AFTER_PROCESSING": 140, "C_STILL_UNMATCHED_AFTER_PROCESSING": 309, "D_PROCESSED_ONLY": 188, "E_MATCH_IDENTITY_CHANGED": 232}
assert (len(never), len(lost), 140 - len(lost)) == (296, 13, 127)

compact = {}
for name, summary in summaries.items():
    compact[name] = {
        "count": summary["count"],
        "original_timestamp_seconds": summary["original_timestamp_seconds"],
        "processed_timestamp_seconds": summary["processed_timestamp_seconds"],
        "unprocessed_absolute_displacement_seconds": summary["unprocessed_absolute_displacement_seconds"],
        "processed_absolute_displacement_seconds": summary["processed_absolute_displacement_seconds"],
        "audio": {asset: {"rms_dbfs": data["rms_dbfs"], "peak_dbfs": data["peak_dbfs"], "rms_below_threshold_count": data["rms_below_threshold_count"], "sample_fraction_below_threshold_nonzero": data["sample_fraction_below_threshold_nonzero"], "band_energy_fraction": data["band_energy_fraction"]} for asset, data in summary["audio"].items()},
    }

result = {
    "audit_id": audit["audit_id"],
    "status": "COMPLETE_FROZEN",
    "protocol": {"commit": "18b6e5f", "fingerprint": audit["protocol_fingerprint"]},
    "evidence_conflict_resolution": {"conflict": "PI authorization described 127 as newly recovered, while frozen assignments establish 140 gross recoveries and 13 lost prior matches.", "resolution": "PI authorized repository-canonical partition; 127 is NET additional matches only.", "gross_recovered": 140, "lost_prior_matches": 13, "net_additional_matches": 127, "resolved": True},
    "populations": compact,
    "C_subgroups": {"never_matched": subgroup(never), "previously_matched_lost_after_processing": subgroup(lost)},
    "E_overlap_status": "OVERLAPPING_SUBGROUP_OF_A_NOT_ADDITIONAL_POPULATION",
    "threshold_linear": 10.0 ** (-30.0 / 20.0),
    "spectral_eq_hypothesis": audit["spectral_eq_hypothesis_test"],
    "explanations": {
        "gross_recovery_140": "Recovered events were predominantly represented by weak pre-compression residual signal: unprocessed median local RMS was -39.12763791293628 dBFS and 125/140 windows were below the -30 dBFS threshold. Processing raised median local RMS to -35.28358705123124 dBFS without changing sample timing. This supports bounded recovery of previously weak evidence, not physical-onset creation.",
        "processed_only_188": "Processed-only events were also commonly associated with weak existing residual signal: unprocessed median local RMS was -33.789454411474196 dBFS and 127/188 windows were below threshold; processing raised the median to -32.40804565081177 dBFS. All 188 lie within original scope. The evidence supports amplification of additional onset-candidate structure not selected by the frozen one-to-one original-EME assignment; it does not authorize false-positive terminology or event identity.",
        "timing_degradation": "The 140 recovered matches have much wider processed displacement (median absolute 0.031092970521541953 s; RMSE 0.06348290398089844 s) than the 606 retained matches (0.0075464852607709755 s; RMSE 0.01892066112447509 s). Within retained matches, 232 changed selected producer timestamp and their median absolute displacement rose from 0.007727891156462585 s to 0.011102040816326531 s. The added wide-displacement matches plus changed selections explain the degraded aggregate timing bounds.",
        "lost_13": "Thirteen previously matched originals became unmatched after processing. Their unprocessed match median absolute displacement was 0.009142857142857144 s. They are preserved as an explicit subgroup of C and offset gross recovery from 140 to +127 net.",
    },
    "eq_hypothesis_status": audit["spectral_eq_hypothesis_test"]["status"],
    "eq_hypothesis_regions": audit["spectral_eq_hypothesis_test"]["qualifying_bands"],
    "replay": {"complete_outputs_byte_identical": True, "execution_1_sha256": digest(execution_1), "execution_2_sha256": digest(execution_2), "audit_fingerprint_identical": True},
    "audit_fingerprint": expected_audit_fingerprint,
    "firewall": audit["firewall"],
}
result["result_record_fingerprint"] = sha256(canonical(result)).hexdigest()
(HERE / "result.json").write_bytes(canonical(result) + b"\n")
(HERE / "report.md").write_text(
    "# CED-VAL-006 Phase-3 Population Transition Audit\n\n"
    "Status: **COMPLETE — READ-ONLY — REPLAY VERIFIED**\n\n"
    "The Evidence Conflict is resolved by the repository-authoritative partition: 140 gross recoveries minus 13 lost prior matches equals +127 net matches. The 13 losses remain an explicit C subgroup; E overlaps A.\n\n"
    "Weak residual evidence best explains gross recovery: 125/140 recovered-event windows had unprocessed local RMS below -30 dBFS. Processed-only events show the same mechanism less strongly (127/188 below threshold), supporting amplification of additional onset-candidate structure. Recovered matches have substantially wider displacement, and 232 retained matches changed selected timestamp, explaining aggregate timing degradation.\n\n"
    "No fixed spectral band passed the preregistered separation gate. A subsequent bounded spectral/EQ hypothesis is therefore not justified. No audio, processing, matching, JGA, production code or historical evidence changed.\n\n"
    f"Audit fingerprint: `{expected_audit_fingerprint}`\n"
    f"Result-record fingerprint: `{result['result_record_fingerprint']}`\n"
)
names = ["audit_execution_1.json", "audit_execution_2.json", "finalize.py", "result.json", "report.md", "verify.py"]
manifest = {"audit_id": result["audit_id"], "audit_fingerprint": expected_audit_fingerprint, "result_record_fingerprint": result["result_record_fingerprint"], "repository_artifacts": {name: digest(HERE / name) for name in names if (HERE / name).exists()}}
(HERE / "artifact_manifest.json").write_bytes(canonical(manifest) + b"\n")
print(expected_audit_fingerprint, result["result_record_fingerprint"])
