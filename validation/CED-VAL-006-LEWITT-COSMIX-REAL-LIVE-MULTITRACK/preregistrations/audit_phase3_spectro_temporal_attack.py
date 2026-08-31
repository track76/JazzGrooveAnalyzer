#!/usr/bin/env python3
"""Frozen read-only Phase-3 spectro-temporal Bass attack audit."""
from __future__ import annotations
import argparse, json, math, statistics
from hashlib import sha256
from pathlib import Path
import librosa, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import resample_poly
import soundfile as sf

DATASET=Path(__file__).resolve().parent.parent
PROTOCOL=Path(__file__).with_name("PR-CEDVAL006-PHASE3-SPECTRO-TEMPORAL-ATTACK-AUDIT-01.json")
P2=DATASET/"bass_preservation_phase2_20260825_01/scoring_execution_1.json"
P3=DATASET/"bass_preservation_phase3_remediated_20260831_01/scoring_execution_1.json"
PATHS={"original":Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/raw/BASS - DI.wav"),"unprocessed":Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE2-01/M1_run_1/htdemucs_ft/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/bass.wav"),"processed":Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-PHASE3-DETERMINISTIC-WAV-SERIALIZATION-01/run_1/bass.wav")}
EXPECTED={P2:"8534734ccb2eb84e18e80a92b54f801d0aff812bd59d12b32cb588aa6b1cc163",P3:"3923f17b1859204bfd6aa68b6843e99209cb35eba634b0dfb099311e9e321f48",PATHS["original"]:"c0a99f65158d12a69e062cc990e86631a0d29d7e83f30537d34eb301516855a9",PATHS["unprocessed"]:"a9949d98dd914de8a7aaa330b7a149340929c31b2665bc00d55eac8df230fe6b",PATHS["processed"]:"ac612091d963bcd5673b96cf5b906589decf8f0c7201599a5c0903bbf3cddc91"}
SR,NFFT,HOP,HALF=44100,1024,64,.12
def canonical(v): return json.dumps(v,ensure_ascii=True,allow_nan=False,sort_keys=True,separators=(",",":")).encode("ascii")
def digest(p):
 h=sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1048576),b""): h.update(b)
 return h.hexdigest()
def sec(x,k): return x[k]["seconds"]
def stats(v):
 v=sorted(float(x) for x in v)
 return {"count":len(v),"minimum":min(v) if v else None,"median":statistics.median(v) if v else None,"maximum":max(v) if v else None,"mean":statistics.fmean(v) if v else None,"population_sd":statistics.pstdev(v) if v else None}
def cliff(a,b):
 return (sum(x>y for x in a for y in b)-sum(x<y for x in a for y in b))/(len(a)*len(b))
def load_audio():
 out={}
 for name,p in PATHS.items():
  x,sr=sf.read(p,dtype="float64",always_2d=True); x=np.mean(x,axis=1)
  if sr!=SR: x=resample_poly(x,147,160)
  out[name]=x
 return out
FREQ=np.fft.rfftfreq(NFFT,1/SR); FMASK=(FREQ>=20)&(FREQ<=8000); FREQ=FREQ[FMASK]
FRAME_COUNT=round((2*HALF)*SR)//HOP+1; TIMES=-HALF+np.arange(FRAME_COUNT)*HOP/SR
ATTACK=(TIMES>=-.03)&(TIMES<=.03); BASE=(TIMES>=-.12)&(TIMES<=-.06)
def tf(x,t):
 c=round(t*SR); span=(FRAME_COUNT-1)*HOP; start=c-round(HALF*SR)-NFFT//2; length=span+NFFT
 seg=np.zeros(length); lo=max(0,start); hi=min(len(x),start+length); seg[lo-start:hi-start]=x[lo:hi]
 z=librosa.stft(seg,n_fft=NFFT,hop_length=HOP,window="hann",center=False); mag=np.abs(z)[FMASK,:FRAME_COUNT]; power=mag*mag; db=10*np.log10(np.maximum(power,1e-12))
 flux_map=np.maximum(mag[:,1:]-mag[:,:-1],0); flux=np.sqrt(np.sum(flux_map*flux_map,axis=0)); peak_i=int(np.argmax(flux)); f_i,t_i=np.unravel_index(int(np.argmax(flux_map)),flux_map.shape)
 attack=float(np.sum(power[:,ATTACK])); full=float(np.sum(power)); baseline=float(np.mean(np.sum(power[:,BASE],axis=0))); attack_mean=float(np.mean(np.sum(power[:,ATTACK],axis=0)))
 contrast=10*math.log10(max(attack_mean,1e-30)/max(baseline,1e-30))
 base=np.median(db[:,BASE],axis=1,keepdims=True); transient=np.maximum(db-base,0)
 return {"power":power,"db":db,"transient":transient,"attack_power":attack,"full_power":full,"attack_concentration":attack/full if full else 0.,"attack_baseline_contrast_db":contrast,"peak_flux":float(flux[peak_i]),"strongest_flux_time_seconds":float(TIMES[peak_i+1]),"maximum_transient_change_frequency_hz":float(FREQ[f_i]),"maximum_transient_change_time_seconds":float(TIMES[t_i+1])}
def cosine(a,b):
 x,y=a.ravel(),b.ravel(); den=float(np.linalg.norm(x)*np.linalg.norm(y)); return float(np.dot(x,y)/den) if den else 0.
def descriptor(audio,t):
 q={k:tf(v,t) for k,v in audio.items()}; o,u,p=q["original"],q["unprocessed"],q["processed"]
 r={k:{z:v[z] for z in ("attack_power","full_power","attack_concentration","attack_baseline_contrast_db","peak_flux","strongest_flux_time_seconds","maximum_transient_change_frequency_hz","maximum_transient_change_time_seconds")} for k,v in q.items()}
 r.update({"original_unprocessed_cosine":cosine(o["transient"],u["transient"]),"original_processed_cosine":cosine(o["transient"],p["transient"]),"unprocessed_processed_cosine":cosine(u["transient"],p["transient"]),"compression_attack_gain_db":10*math.log10(max(p["attack_power"],1e-30)/max(u["attack_power"],1e-30)),"compression_peak_flux_ratio":p["peak_flux"]/u["peak_flux"] if u["peak_flux"] else None})
 r["original_attack_present"]=o["attack_baseline_contrast_db"]>=6
 r["unprocessed_structure_preserved"]=r["original_unprocessed_cosine"]>=.75
 r["processed_same_original_structure"]=r["original_processed_cosine"]>=.75 and abs(p["strongest_flux_time_seconds"]-o["strongest_flux_time_seconds"])<=.010 and abs(p["maximum_transient_change_frequency_hz"]-o["maximum_transient_change_frequency_hz"])<=250
 r["C1_residual_attack"]=u["attack_baseline_contrast_db"]>=3 and r["original_unprocessed_cosine"]>=.5
 return r,q
def populations():
 p2=json.loads(P2.read_text())["runs"]["M1_run_1"]["level_2"]["Double Bass"]
 p3=json.loads(P3.read_text())["runs"]["run_1"]["level_2"]["Double Bass"]
 b={x["original_eme_id"]:x for x in p2["matches"]}; a={x["original_eme_id"]:x for x in p3["matches"]}; ids_b,ids_a=set(b),set(a)
 originals={x["original_eme_id"]:x for x in [*p2["matches"],*p2["original_only"]]}; d={x["separated_eme_id"]:x for x in p3["separated_only"]}
 E={i for i in ids_b&ids_a if sec(b[i],"separated_time")!=sec(a[i],"separated_time")}
 defs={"A_STABLE":sorted(ids_b&ids_a-E),"B_RECOVERED":sorted(ids_a-ids_b),"C1_NEVER_MATCHED":sorted({x["original_eme_id"] for x in p3["original_only"]}-ids_b),"C2_LOST":sorted(ids_b-ids_a),"D_PROCESSED_ONLY":sorted(d),"E_CHANGED_SELECTION":sorted(E)}
 out={}
 for pop,ids in defs.items():
  out[pop]=[]
  for i in ids:
   anchor=sec(d[i],"separated_time") if pop=="D_PROCESSED_ONLY" else sec(originals[i],"original_time")
   out[pop].append((i,anchor))
 return out
def plot_example(pop,identity,t,maps,path):
 fig,axes=plt.subplots(3,1,figsize=(7.2,7.2),dpi=110,sharex=True,sharey=True)
 for ax,name in zip(axes,("original","unprocessed","processed")):
  im=ax.imshow(maps[name]["db"],origin="lower",aspect="auto",extent=[TIMES[0]*1000,TIMES[-1]*1000,FREQ[0],FREQ[-1]],vmin=-100,vmax=0,cmap="magma"); ax.axvline(0,color="cyan",lw=.7); ax.set_ylabel(f"{name}\nHz")
 axes[-1].set_xlabel("Time from authority coordinate (ms)"); fig.suptitle(f"{pop} — {identity} — {t:.6f} s"); fig.colorbar(im,ax=axes,label="Power (dBFS)",shrink=.8); fig.subplots_adjust(left=.12,right=.84,bottom=.08,top=.94,hspace=.08); fig.savefig(path,metadata={"Software":"JGA deterministic validation","Creation Time":"2026-08-31T00:00:00Z"}); plt.close(fig)
def plot_aggregate(pop,med,path):
 fig,axes=plt.subplots(4,1,figsize=(7.2,8.8),dpi=110,sharex=True,sharey=True)
 for ax,name in zip(axes[:3],("original","unprocessed","processed")):
  im=ax.imshow(med[name],origin="lower",aspect="auto",extent=[TIMES[0]*1000,TIMES[-1]*1000,FREQ[0],FREQ[-1]],vmin=-100,vmax=0,cmap="magma"); ax.set_ylabel(f"{name}\nHz")
 gain=med["processed"]-med["unprocessed"]; g=axes[3].imshow(gain,origin="lower",aspect="auto",extent=[TIMES[0]*1000,TIMES[-1]*1000,FREQ[0],FREQ[-1]],vmin=-20,vmax=20,cmap="coolwarm"); axes[3].set_ylabel("gain\nHz"); axes[3].set_xlabel("Time (ms)"); fig.suptitle(f"Median maps — {pop}"); fig.colorbar(im,ax=axes[:3],label="dBFS",shrink=.6); fig.colorbar(g,ax=axes[3],label="dB",shrink=.7); fig.subplots_adjust(left=.12,right=.84,bottom=.06,top=.95,hspace=.08); fig.savefig(path,metadata={"Software":"JGA deterministic validation","Creation Time":"2026-08-31T00:00:00Z"}); plt.close(fig)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--output-dir",type=Path,required=True); args=ap.parse_args(); args.output_dir.mkdir(parents=True,exist_ok=True)
 for p,h in EXPECTED.items(): assert digest(p)==h
 protocol=json.loads(PROTOCOL.read_text()); audio=load_audio(); pops=populations(); details={}; summaries={}; plots=[]
 for pop,items in pops.items():
  records=[]; stacks={k:[] for k in ("original","unprocessed","processed")}; example=None
  for identity,t in sorted(items,key=lambda x:(x[1],x[0])):
   desc,maps=descriptor(audio,t); records.append({"identity":identity,"anchor_seconds":t,"descriptors":desc})
   for k in stacks: stacks[k].append(maps[k]["db"])
   if example is None: example=(identity,t,maps)
  details[pop]=records
  med={k:np.median(np.stack(v),axis=0) for k,v in stacks.items()}
  for k,v in med.items(): np.save(args.output_dir/f"aggregate_{pop.lower()}_{k}.npy",v,allow_pickle=False)
  agg=f"aggregate_{pop.lower()}.png"; plot_aggregate(pop,med,args.output_dir/agg); plots.append({"type":"aggregate","population":pop,"filename":agg,"sha256":digest(args.output_dir/agg)})
  identity,t,maps=example; ex=f"example_{pop.lower()}.png"; plot_example(pop,identity,t,maps,args.output_dir/ex); plots.append({"type":"example","population":pop,"identity":identity,"anchor_seconds":t,"filename":ex,"sha256":digest(args.output_dir/ex)})
  keys=["original_unprocessed_cosine","original_processed_cosine","unprocessed_processed_cosine","compression_attack_gain_db","compression_peak_flux_ratio"]
  summaries[pop]={"count":len(records),**{k:stats(r["descriptors"][k] for r in records if r["descriptors"][k] is not None) for k in keys},"original_attack_present_count":sum(r["descriptors"]["original_attack_present"] for r in records),"unprocessed_structure_preserved_count":sum(r["descriptors"]["unprocessed_structure_preserved"] for r in records),"processed_same_original_structure_count":sum(r["descriptors"]["processed_same_original_structure"] for r in records),"C1_residual_attack_count":sum(r["descriptors"]["C1_residual_attack"] for r in records)}
 eligible=[("processed_attack_concentration",lambda d:d["processed"]["attack_concentration"]),("processed_attack_contrast_db",lambda d:d["processed"]["attack_baseline_contrast_db"]),("processed_peak_flux",lambda d:d["processed"]["peak_flux"]),("compression_attack_gain_db",lambda d:d["compression_attack_gain_db"]),("compression_peak_flux_ratio",lambda d:d["compression_peak_flux_ratio"])]
 B,D=details["B_RECOVERED"],details["D_PROCESSED_ONLY"]; comparisons={}; large=[]
 for name,fn in eligible:
  bv=[fn(r["descriptors"]) for r in B]; dv=[fn(r["descriptors"]) for r in D]; delta=cliff(bv,dv); bh=[[],[]]; dh=[[],[]]
  for j,r in enumerate(sorted(B,key=lambda x:x["identity"])): bh[j%2].append(fn(r["descriptors"]))
  for j,r in enumerate(sorted(D,key=lambda x:x["identity"])): dh[j%2].append(fn(r["descriptors"]))
  halves=[cliff(bh[i],dh[i]) for i in (0,1)]; consistent=all(abs(x)>=.474 and x*delta>0 for x in halves); comparisons[name]={"cliffs_delta":delta,"lexical_half_deltas":halves,"large_direction_consistent":consistent}; large.append(abs(delta)>=.474 and consistent)
 b_attack=summaries["B_RECOVERED"]["original_attack_present_count"]/len(B); b_pres=summaries["B_RECOVERED"]["unprocessed_structure_preserved_count"]/len(B)
 deltas=[abs(x["cliffs_delta"]) for x in comparisons.values()]; gate=protocol["spectral_eq_gate"]
 outcome="YES" if b_attack>=.6 and b_pres>=.6 and any(large) else "NO" if b_pres<.4 or all(x<.147 for x in deltas) else "INDETERMINATE"
 result={"audit_id":protocol["audit_id"],"protocol_fingerprint":protocol["preregistration_fingerprint"],"configuration":{"analysis_window":protocol["analysis_window"],"representation":protocol["representation"]},"authorities":{str(k):v for k,v in EXPECTED.items()},"population_summaries":summaries,"B_vs_D":comparisons,"B_original_attack_present_fraction":b_attack,"B_unprocessed_preservation_fraction":b_pres,"spectral_eq_hypothesis":outcome,"principle":None,"diagnostic_plots":plots,"complete_records":details,"firewall":protocol["firewall"]}
 result["audit_fingerprint"]=sha256(canonical(result)).hexdigest(); (args.output_dir/"audit.json").write_bytes(canonical(result)+b"\n"); print(result["audit_fingerprint"])
if __name__=="__main__": main()
