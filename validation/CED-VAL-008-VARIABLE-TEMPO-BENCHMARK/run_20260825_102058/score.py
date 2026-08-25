"""Frozen common CED-VAL-008 scorer; invoked only after blind raw freeze."""
from fractions import Fraction
from hashlib import sha256
import json, math, sys
from pathlib import Path

blind_path,jga_path,librosa_path,essentia_path,gt_path,out_path=map(Path,sys.argv[1:])
blind=json.loads(blind_path.read_text())
if blind["status"]!="PASS_FROZEN_BEFORE_GT_ACCESS" or blind["ground_truth_accessed"] is not False: raise RuntimeError("BLIND_FREEZE_CONFLICT")
raws={p.stem.replace("_raw_output","").upper():json.loads(p.read_text()) for p in (jga_path,librosa_path,essentia_path)}
for a in blind["assets"]:
    p={"JGA":jga_path,"LIBROSA":librosa_path,"ESSENTIA":essentia_path}[a["system"]]
    if sha256(p.read_bytes()).hexdigest()!=a["sha256"]: raise RuntimeError("RAW_AUTHORITY_CONFLICT")
gt_doc=json.loads(gt_path.read_text())
if gt_doc["authority"]!="SYMBOLIC_BEAT_GROUND_TRUTH" or gt_doc["beat_count"]!=64: raise RuntimeError("GT_CONFLICT")
gt=[Fraction(row[4]) for row in gt_doc["events"]]
end=Fraction(1463433,44100)
left=[Fraction(0)]+[(gt[i-1]+gt[i])/2 for i in range(1,64)]
right=[(gt[i]+gt[i+1])/2 for i in range(63)]+[end]

def exact(x): return f"{x.numerator}/{x.denominator}"
def qrec(x): return {"seconds_exact":exact(x),"seconds":float(x),"milliseconds":float(x*1000)}
def output_time(system,row):
    if system in ("JGA","LIBROSA"):
        sample=row["producer_sample_coordinate"] if system=="JGA" else row["beat_sample"]
        return Fraction(sample,44100)
    return Fraction.from_float(float.fromhex(row["timestamp_binary64_hex"]))
def quantile(values,p):
    if not values: return None
    v=sorted(values); rank=Fraction(len(v)-1)*p; lo=rank.numerator//rank.denominator; hi=math.ceil(rank)
    return v[lo] if lo==hi else v[lo]+(v[hi]-v[lo])*(rank-lo)
def stats(values):
    if not values: return {"status":"UNDEFINED","count":0}
    n=len(values); mean=sum(values,Fraction())/n; variance=sum((x-mean)**2 for x in values)/n; mse=sum(x*x for x in values)/n
    return {"status":"DEFINED","count":n,"exact_zero_count":sum(x==0 for x in values),"minimum":qrec(min(values)),"q1_linear":qrec(quantile(values,Fraction(1,4))),"median_linear":qrec(quantile(values,Fraction(1,2))),"q3_linear":qrec(quantile(values,Fraction(3,4))),"maximum":qrec(max(values)),"mean":qrec(mean),"population_variance_seconds_squared_exact":exact(variance),"population_sd_seconds":math.sqrt(float(variance)),"rmse_seconds":math.sqrt(float(mse)),"mean_square_seconds_exact":exact(mse)}
def ratio(n,d):
    x=Fraction(n,d) if d else Fraction(0); return {"exact":exact(x),"decimal":float(x)}
def locate(t):
    if t<0: raise RuntimeError("NEGATIVE_TIME_AUTHORITY_FAILURE")
    for i in range(64):
        if left[i]<=t<right[i]: return i
    return None
def assign(system,raw):
    outputs=[]
    for row in raw["outputs"]:
        t=output_time(system,row); outputs.append({"index":row["frozen_native_index"],"id":row["output_id"],"time":t,"cell":locate(t)})
    selected={}; candidates={}; used=set()
    for i in range(64):
        eligible=[x for x in outputs if x["index"] not in used and x["cell"]==i]
        eligible.sort(key=lambda x:(abs(x["time"]-gt[i]),x["time"],x["index"]))
        candidates[i]=eligible
        if eligible: selected[i]=eligible[0]; used.add(eligible[0]["index"])
    matches=[]
    for i,x in selected.items():
        err=x["time"]-gt[i]
        matches.append({"gt_index":i,"output_id":x["id"],"native_output_index":x["index"],"system_time":qrec(x["time"]),"gt_time":qrec(gt[i]),"signed_error":qrec(err),"absolute_error":qrec(abs(err)),"eligible_candidates":[{"output_id":v["id"],"native_output_index":v["index"],"absolute_displacement_exact":exact(abs(v["time"]-gt[i]))} for v in candidates[i]],"selection_reason":"MIN_ABSOLUTE_DISPLACEMENT_THEN_EARLIER_TIMESTAMP_THEN_LOWER_NATIVE_INDEX"})
    return outputs,selected,matches,used
def recovery(outputs,selected,used,indices):
    cells=set(indices); raw=[x for x in outputs if x["cell"] in cells]; matched=sum(i in selected for i in indices); extras=sum(x["index"] not in used for x in raw)
    p=Fraction(matched,len(raw)) if raw else Fraction(); r=Fraction(matched,len(indices)); f=Fraction(2)*p*r/(p+r) if p+r else Fraction()
    errs=[selected[i]["time"]-gt[i] for i in indices if i in selected]
    return {"expected_gt_count":len(indices),"raw_outputs_in_cell_scope":len(raw),"matched":matched,"missed":len(indices)-matched,"extra":extras,"precision":ratio(p.numerator,p.denominator),"recall":ratio(r.numerator,r.denominator),"f1":ratio(f.numerator,f.denominator),"signed_errors":[qrec(x) for x in errs],"absolute_errors":[qrec(abs(x)) for x in errs],"signed_timing_statistics":stats(errs),"absolute_timing_statistics":stats([abs(x) for x in errs]),"timing_rmse_seconds":stats(errs).get("rmse_seconds")}
def intervals(selected,indices):
    pairs=[]
    allowed=set(indices)
    for i in range(63):
        if i in allowed and i+1 in allowed and i in selected and i+1 in selected:
            si=selected[i+1]["time"]-selected[i]["time"]; gi=gt[i+1]-gt[i]; e=si-gi
            pairs.append({"gt_pair":[i,i+1],"system_interval":qrec(si),"gt_interval":qrec(gi),"signed_interval_error":qrec(e),"absolute_interval_error":qrec(abs(e))})
    e=[Fraction(x["signed_interval_error"]["seconds_exact"]) for x in pairs]; a=[abs(x) for x in e]
    return {"interval_count":len(pairs),"population":pairs,"signed_interval_error_statistics":stats(e),"absolute_interval_error_statistics":stats(a),"median_absolute_interval_error":stats(a).get("median_linear"),"mean_absolute_interval_error":stats(a).get("mean"),"population_sd_signed_interval_error_seconds":stats(e).get("population_sd_seconds"),"interval_error_rmse_seconds":stats(e).get("rmse_seconds")}

systems={}; segments={"S1":list(range(0,16)),"S2":list(range(16,32)),"S3":list(range(32,48)),"S4":list(range(48,64))}; transitions={"T1":{"boundary":16,"indices":list(range(12,21))},"T2":{"boundary":32,"indices":list(range(28,37))},"T3":{"boundary":48,"indices":list(range(44,53))}}
for system,raw in raws.items():
    outputs,selected,matches,used=assign(system,raw)
    global_rec=recovery(outputs,selected,used,list(range(64)))
    seg={name:{**recovery(outputs,selected,used,idx),"intervals":intervals(selected,idx)} for name,idx in segments.items()}
    trans={}
    for name,spec in transitions.items():
        b=spec["boundary"]; idx=spec["indices"]; rec=recovery(outputs,selected,used,idx)
        pre=[selected[i]["time"]-gt[i] for i in range(b-4,b) if i in selected]; post=[selected[i]["time"]-gt[i] for i in range(b+1,b+5) if i in selected]
        beat_errors={str(i):(qrec(selected[i]["time"]-gt[i]) if i in selected else None) for i in idx}
        post_intervals=[]
        for i in range(b,b+4):
            if i in selected and i+1 in selected:
                si=selected[i+1]["time"]-selected[i]["time"]; gi=gt[i+1]-gt[i]; post_intervals.append({"gt_pair":[i,i+1],"system_interval":qrec(si),"gt_interval":qrec(gi),"interval_error":qrec(si-gi)})
            else: post_intervals.append({"gt_pair":[i,i+1],"status":"MISSING_INTERVAL"})
        trans[name]={**rec,"gt_indices":idx,"signed_error_per_beat":beat_errors,"pre_transition_mean_signed_error":qrec(sum(pre,Fraction())/len(pre)) if pre else None,"boundary_beat_error":beat_errors[str(b)],"post_transition_mean_signed_error":qrec(sum(post,Fraction())/len(post)) if post else None,"maximum_absolute_error":stats([abs(selected[i]["time"]-gt[i]) for i in idx if i in selected]).get("maximum"),"recovery_continuity":all(i in selected for i in idx),"first_four_post_change_intervals":post_intervals}
    systems[system]={"raw_output_count":raw["raw_output_count"],"global":global_rec,"matches":matches,"segments":seg,"transitions":trans,"intervals_global":intervals(selected,list(range(64))),"native_tempo_metadata":raw.get("reported_tempo",raw.get("reported_bpm")),"native_intervals_metadata":raw.get("intervals"),"raw_scientific_fingerprint":raw["scientific_fingerprint"]}
record={"execution_id":"EXEC-CEDVAL008-THREE-SYSTEM-BENCHMARK-20260825-102058","study_id":"H-CEDVAL008-THREE-SYSTEM-VARIABLE-TEMPO-SYMBOLIC-BEAT-RECOVERY-01","preregistration_commit":"e5ecfa8","dataset_fingerprint":"9aab028fb1ac6740f1e257d0254afea485225879be888d0e4b60c20ba46ee86d","blind_raw_freeze_fingerprint":blind["blind_freeze_fingerprint"],"ground_truth_accessed_after_raw_freeze":True,"assignment":"EXACT_RATIONAL_LOCAL_VORONOI_ONE_TO_ONE","latency_correction":False,"marker_correction":False,"systems":systems,"algorithmic_dependency_caveat":"JGA uses librosa-based observational functionality; librosa cannot independently validate JGA. Essentia is the more algorithmically independent comparator.","weighted_composite_score":False,"universal_superiority_claim":False}
record["combined_benchmark_fingerprint"]=sha256(json.dumps(record,sort_keys=True,separators=(",",":")).encode()).hexdigest(); out_path.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n"); print(json.dumps({"combined_benchmark_fingerprint":record["combined_benchmark_fingerprint"],"systems":{k:{"raw":v["raw_output_count"],"matched":v["global"]["matched"],"missed":v["global"]["missed"],"extra":v["global"]["extra"]} for k,v in systems.items()}},sort_keys=True))
