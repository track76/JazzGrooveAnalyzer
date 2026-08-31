#!/usr/bin/env python3
from hashlib import sha256
import json, statistics
from pathlib import Path
HERE=Path(__file__).resolve().parent
def canonical(v): return json.dumps(v,ensure_ascii=True,allow_nan=False,sort_keys=True,separators=(",",":")).encode("ascii")
def digest(p): return sha256(p.read_bytes()).hexdigest()
def stats(v):
 v=sorted(float(x) for x in v); return {"count":len(v),"minimum":min(v),"median":statistics.median(v),"maximum":max(v),"mean":statistics.fmean(v),"population_sd":statistics.pstdev(v)}
r1,r2=HERE/"run_1",HERE/"run_2"; n1=sorted(x.name for x in r1.iterdir()); n2=sorted(x.name for x in r2.iterdir()); assert n1==n2
for name in n1: assert (r1/name).read_bytes()==(r2/name).read_bytes(),name
audit=json.loads((r1/"audit.json").read_text()); afp=audit.pop("audit_fingerprint"); assert sha256(canonical(audit)).hexdigest()==afp; audit["audit_fingerprint"]=afp
fine={}
for pop,records in audit["complete_records"].items():
 fine[pop]={}
 for condition in ("original","unprocessed","processed"):
  fine[pop][condition]={
   "attack_concentration":stats(x["descriptors"][condition]["attack_concentration"] for x in records),
   "attack_baseline_contrast_db":stats(x["descriptors"][condition]["attack_baseline_contrast_db"] for x in records),
   "peak_flux":stats(x["descriptors"][condition]["peak_flux"] for x in records),
   "strongest_flux_time_seconds":stats(x["descriptors"][condition]["strongest_flux_time_seconds"] for x in records),
   "maximum_transient_change_frequency_hz":stats(x["descriptors"][condition]["maximum_transient_change_frequency_hz"] for x in records),
  }
result={
 "audit_id":audit["audit_id"],"status":"COMPLETE_FROZEN","protocol":{"commit":"6c2b6c7","fingerprint":audit["protocol_fingerprint"]},"configuration":audit["configuration"],
 "population_counts":{k:v["count"] for k,v in audit["population_summaries"].items()},"population_summaries":audit["population_summaries"],"fine_descriptor_summaries":fine,
 "original_vs_demucs":{"B_original_attack_present_fraction":audit["B_original_attack_present_fraction"],"B_unprocessed_preservation_fraction":audit["B_unprocessed_preservation_fraction"],"interpretation":"Fine transient-map preservation is uncommon in B under frozen criteria; original authority was retrospective only."},
 "demucs_vs_compressed":{"B_compression_attack_gain_db":audit["population_summaries"]["B_RECOVERED"]["compression_attack_gain_db"],"B_compression_peak_flux_ratio":audit["population_summaries"]["B_RECOVERED"]["compression_peak_flux_ratio"],"B_same_original_structure_count":audit["population_summaries"]["B_RECOVERED"]["processed_same_original_structure_count"]},
 "B_vs_D":audit["B_vs_D"],"C1_residual_attack":{"count":audit["population_summaries"]["C1_NEVER_MATCHED"]["C1_residual_attack_count"],"denominator":296,"fraction":audit["population_summaries"]["C1_NEVER_MATCHED"]["C1_residual_attack_count"]/296},
 "structure_conclusion":"For B, compression generally promotes a spectro-temporal structure that does not satisfy the frozen correspondence to the original attack: 0/140 pass the complete same-structure criterion. This supports heterogeneous displaced/alternative local structure, not frequency-selective restoration of a reproducible original attack.",
 "spectral_eq_hypothesis":audit["spectral_eq_hypothesis"],"principle":audit["principle"],
 "plots":[{**x,"canonical_path":f"run_1/{x['filename']}"} for x in audit["diagnostic_plots"]],"example_selection_rule":"Earliest anchor timestamp, then lexical identity, independently for A stable, B, C1, C2, D and E.",
 "replay":{"status":"PASS_BYTE_IDENTICAL","complete_json_byte_identical":True,"all_png_and_npy_byte_identical":True,"run_1_audit_sha256":digest(r1/"audit.json"),"run_2_audit_sha256":digest(r2/"audit.json"),"artifact_count_per_run":len(n1)},"audit_fingerprint":afp,"firewall":audit["firewall"]}
result["result_record_fingerprint"]=sha256(canonical(result)).hexdigest(); (HERE/"result.json").write_bytes(canonical(result)+b"\n")
(HERE/"report.md").write_text("# CED-VAL-006 Phase-3 Spectro-Temporal Attack Audit\n\nStatus: **COMPLETE — READ-ONLY — REPLAY VERIFIED**\n\nThe frozen fine-resolution analysis found only 7/140 B events with preserved unprocessed transient-map structure and 0/140 compressed B candidates satisfying the complete same-original-structure criterion. Only 14/296 C1 cells met the frozen residual-attack definition.\n\nNo B-versus-D non-Ground-Truth descriptor reached the preregistered large split-half effect. The largest full-population effects were processed peak flux (Cliff's delta -0.4054) and compression peak-flux ratio (+0.3859), both below 0.474. `SPECTRAL_EQ_HYPOTHESIS: NO`. No EQ principle is authorized.\n\nAll JSON, PNG and aggregate NPY evidence replayed byte-identically.\n\nAudit fingerprint: `"+afp+"`\nResult-record fingerprint: `"+result["result_record_fingerprint"]+"`\n")
tracked=[x for x in HERE.rglob("*") if x.is_file() and x.name!="artifact_manifest.json"]
(HERE/"artifact_manifest.json").write_bytes(canonical({"audit_id":result["audit_id"],"audit_fingerprint":afp,"result_record_fingerprint":result["result_record_fingerprint"],"artifacts":{str(x.relative_to(HERE)):digest(x) for x in sorted(tracked)}})+b"\n")
print(afp,result["result_record_fingerprint"])
