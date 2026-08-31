#!/usr/bin/env python3
"""Frozen read-only direct-mix Bass observability audit."""
from __future__ import annotations
import argparse, gc, hashlib, json, math, statistics
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from scipy.signal import get_window

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
PROTO=REPO/"validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/preregistrations/H-CEDVAL006-DIRECT-MIX-NEITHER-OBSERVABILITY-AUDIT-01.json"
P2=REPO/"validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/bass_preservation_phase2_20260825_01/scoring_execution_1.json"
TIMES=np.arange(-.1,.1000001,.001); FREQ=np.arange(20.,2000.1,5.); NFFT=2048
ATTACK=(TIMES>=-.02)&(TIMES<=.03); BASE=(TIMES>=-.1)&(TIMES<=-.05); LOW=(FREQ>=30)&(FREQ<=500)
BANDS=[(30,80),(80,160),(160,320),(320,500),(500,1000),(1000,2000)]

def canonical(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def digest(p):
 h=hashlib.sha256()
 with Path(p).open("rb") as f:
  for b in iter(lambda:f.read(1048576),b""): h.update(b)
 return h.hexdigest()
def stats(v):
 v=sorted(float(x) for x in v)
 return {"count":len(v),"minimum":min(v),"q1_linear":float(np.quantile(v,.25)),"median":statistics.median(v),"q3_linear":float(np.quantile(v,.75)),"maximum":max(v),"mean":statistics.fmean(v),"population_sd":statistics.pstdev(v)}
def cosine(a,b):
 x,y=a.ravel(),b.ravel(); den=float(np.linalg.norm(x)*np.linalg.norm(y)); return float(np.dot(x,y)/den) if den else 0.
def load_audio(path):
 x,sr=sf.read(path,dtype="float64",always_2d=True); return np.mean(x,axis=1),sr
def tf(audio,sr,t):
 win_n=round(.012*sr); hop=round(.001*sr); window=get_window("hann",win_n,fftbins=True)
 center=round(t*sr); first=center-round(.1*sr)-win_n//2
 frames=np.zeros((len(TIMES),win_n))
 for j in range(len(TIMES)):
  start=first+j*hop; lo=max(0,start); hi=min(len(audio),start+win_n)
  if hi>lo: frames[j,lo-start:hi-start]=audio[lo:hi]
 frames*=window
 z=np.fft.rfft(frames,n=NFFT,axis=1); power=(np.abs(z)**2).T
 native=np.fft.rfftfreq(NFFT,1/sr)
 out=np.empty((len(FREQ),len(TIMES)),dtype=np.float32)
 for j in range(len(TIMES)): out[:,j]=np.interp(FREQ,native,power[:,j]).astype(np.float32)
 return out
def measures(power):
 db=10*np.log10(np.maximum(power,1e-12)); base=np.median(db[:,BASE],axis=1,keepdims=True); transient=np.maximum(db-base,0)
 lowp=power[LOW]; lowmag=np.sqrt(lowp); flux=np.maximum(lowmag[:,1:]-lowmag[:,:-1],0); curve=np.sqrt(np.sum(flux*flux,axis=0)); pi=int(np.argmax(curve)); fi,ti=np.unravel_index(int(np.argmax(flux)),flux.shape)
 def band(lo,hi):
  m=(FREQ>=lo)&(FREQ<hi if hi<2000 else FREQ<=hi); p=power[m]
  attack=float(np.mean(np.sum(p[:,ATTACK],axis=0))); baseline=float(np.mean(np.sum(p[:,BASE],axis=0))); full=float(np.sum(p))
  return {"attack_power":attack,"attack_concentration":float(np.sum(p[:,ATTACK])/full) if full else 0.,"attack_baseline_contrast_db":10*math.log10(max(attack,1e-30)/max(baseline,1e-30))}
 return {"bands":{f"{lo}_{hi}_hz":band(lo,hi) for lo,hi in BANDS},"low_contrast_db":band(30,500)["attack_baseline_contrast_db"],"low_flux_peak":float(curve[pi]),"low_flux_peak_time_seconds":float(TIMES[pi+1]),"low_max_change_frequency_hz":float(FREQ[LOW][fi]),"transient_low":transient[LOW],"db":db}
def event_times():
 s=json.loads(P2.read_text())["runs"]["M1_run_1"]["level_2"]
 bass=s["Double Bass"]; originals={x["original_eme_id"]:x["original_time"]["seconds"] for x in bass["matches"]+bass["original_only"]}
 drums=s["Drums"]; drum_times=sorted(x["original_time"]["seconds"] for x in drums["matches"]+drums["original_only"])
 return originals,drum_times
def plot_example(identity,t,maps,path):
 fig,axes=plt.subplots(4,1,figsize=(7.2,8.8),dpi=110,sharex=True,sharey=True)
 names=("original_bass","controlled_mix","htdemucs_ft_bass","rx_bass")
 for ax,name in zip(axes,names):
  im=ax.imshow(maps[name],origin="lower",aspect="auto",extent=[-100,100,20,2000],vmin=-100,vmax=0,cmap="magma"); ax.axvline(0,color="cyan",lw=.7); ax.set_ylabel(name+"\nHz")
 axes[-1].set_xlabel("Time from original Bass EME (ms)"); fig.suptitle(f"{identity} — {t:.6f} s"); fig.colorbar(im,ax=axes,label="Power (dBFS)",shrink=.72); fig.subplots_adjust(left=.15,right=.83,bottom=.06,top=.95,hspace=.08); fig.savefig(path,metadata={"Software":"JGA deterministic validation","Creation Time":"2026-08-31T00:00:00Z"}); plt.close(fig)
def plot_aggregate(pop,maps,path):
 fig,axes=plt.subplots(4,1,figsize=(7.2,8.8),dpi=110,sharex=True,sharey=True)
 for ax,name in zip(axes,("original_bass","controlled_mix","htdemucs_ft_bass","rx_bass")):
  im=ax.imshow(maps[name],origin="lower",aspect="auto",extent=[-100,100,20,2000],vmin=-100,vmax=0,cmap="magma"); ax.axvline(0,color="cyan",lw=.7); ax.set_ylabel(name+"\nHz")
 axes[-1].set_xlabel("Time from original Bass EME (ms)"); fig.suptitle(f"Median absolute maps — {pop}"); fig.colorbar(im,ax=axes,label="Power (dBFS)",shrink=.72); fig.subplots_adjust(left=.15,right=.83,bottom=.06,top=.95,hspace=.08); fig.savefig(path,metadata={"Software":"JGA deterministic validation","Creation Time":"2026-08-31T00:00:00Z"}); plt.close(fig)
def main(outdir):
 outdir.mkdir(parents=True,exist_ok=True); proto=json.loads(PROTO.read_text()); pp=dict(proto); expected=pp.pop("protocol_fingerprint"); assert hashlib.sha256(canonical(pp)).hexdigest()==expected
 for a in proto["authorities"].values():
  p=Path(a["path"]); p=p if p.is_absolute() else REPO/p; assert digest(p)==a["sha256"]
 comp=json.loads(Path(proto["authorities"]["complementarity_result"]["path"]).read_text() if Path(proto["authorities"]["complementarity_result"]["path"]).is_absolute() else (REPO/proto["authorities"]["complementarity_result"]["path"]).read_text())
 popkeys={"A_BOTH":"A_BOTH","B_HTDEMUCSFT_ONLY":"B_DEMUCS_ONLY","C_RX_ONLY":"C_RX_ONLY","D_NEITHER":"D_NEITHER"}
 pops={k:comp["partition"][v]["original_eme_ids"] for k,v in popkeys.items()}; assert {k:len(v) for k,v in pops.items()}==proto["populations"]
 originals,drum_times=event_times(); sources={k:load_audio(v["path"]) for k,v in proto["authorities"].items() if k in ("original_bass","controlled_mix","htdemucs_ft_bass","rx_bass","original_drum_overheads")}
 drum_flux=[]
 for t in drum_times: drum_flux.append(measures(tf(*sources["original_drum_overheads"],t))["low_flux_peak"])
 strong_threshold=statistics.median(drum_flux)
 summaries={}; records={}; plot_records=[]
 for pop,ids in pops.items():
  rec=[]; stack={name:[] for name in ("original_bass","controlled_mix","htdemucs_ft_bass","rx_bass")}
  selected=set(sorted(ids,key=lambda x:(hashlib.sha256(x.encode()).hexdigest(),x))[:2]) if pop in ("A_BOTH","D_NEITHER") else set()
  for identity in ids:
   t=originals[identity]; q={}
   for name in stack:
    m=measures(tf(*sources[name],t)); q[name]=m; stack[name].append(m["db"].astype(np.float32))
   c=cosine(q["original_bass"]["transient_low"],q["controlled_mix"]["transient_low"]); dt=abs(q["original_bass"]["low_flux_peak_time_seconds"]-q["controlled_mix"]["low_flux_peak_time_seconds"])
   observable=q["original_bass"]["low_contrast_db"]>=6 and q["controlled_mix"]["low_contrast_db"]>=3 and c>=.5 and dt<=.020
   nearest_i=min(range(len(drum_times)),key=lambda i:abs(drum_times[i]-t)); nearest_dt=abs(drum_times[nearest_i]-t); coincident=nearest_dt<=.030; strong=coincident and drum_flux[nearest_i]>=strong_threshold
   descriptor={name:{k:v for k,v in m.items() if k not in ("transient_low","db")} for name,m in q.items()}
   row={"original_eme_id":identity,"original_time_seconds":t,"original_mix_transient_cosine_30_500_hz":c,"original_mix_peak_flux_time_difference_seconds":dt,"observable":observable,"nearest_drum_eme_distance_seconds":nearest_dt,"drum_coincident":coincident,"strong_drum_coincident":strong,"descriptors":descriptor}; rec.append(row)
   if identity in selected:
    filename=f"example_{pop.lower()}_{len([x for x in plot_records if x['population']==pop])+1}.png"; plot_example(identity,t,{n:q[n]["db"] for n in stack},outdir/filename); plot_records.append({"population":pop,"identity":identity,"filename":filename})
  med={name:np.median(np.stack(values),axis=0) for name,values in stack.items()}; filename=f"aggregate_{pop.lower()}.png"; plot_aggregate(pop,med,outdir/filename); plot_records.append({"population":pop,"type":"aggregate","filename":filename}); del stack,med; gc.collect()
  obs=sum(x["observable"] for x in rec); no_drum=sum(x["observable"] and not x["drum_coincident"] for x in rec); no_strong=sum(x["observable"] and not x["strong_drum_coincident"] for x in rec)
  summaries[pop]={"count":len(rec),"observable_count":obs,"observable_fraction":obs/len(rec),"observable_without_drum_coincidence_count":no_drum,"observable_without_drum_coincidence_fraction":no_drum/len(rec),"observable_without_strong_drum_count":no_strong,"observable_without_strong_drum_fraction":no_strong/len(rec),"drum_coincident_count":sum(x["drum_coincident"] for x in rec),"strong_drum_coincident_count":sum(x["strong_drum_coincident"] for x in rec),"mix_low_contrast_db":stats(x["descriptors"]["controlled_mix"]["low_contrast_db"] for x in rec),"original_mix_transient_cosine_30_500_hz":stats(x["original_mix_transient_cosine_30_500_hz"] for x in rec),"peak_flux_time_difference_seconds":stats(x["original_mix_peak_flux_time_difference_seconds"] for x in rec)}; records[pop]=rec
 both=summaries["A_BOTH"]; neither=summaries["D_NEITHER"]
 if neither["observable_fraction"]>=.25 and neither["observable_without_strong_drum_fraction"]>=.10 and neither["observable_fraction"]>=.5*both["observable_fraction"]: outcome="YES"
 elif neither["observable_fraction"]<.10 or neither["observable_without_strong_drum_fraction"]<.05: outcome="NO"
 else: outcome="INDETERMINATE"
 for x in plot_records: x["sha256"]=digest(outdir/x["filename"])
 result={"audit_id":proto["audit_id"],"protocol_fingerprint":expected,"configuration":proto["configuration"],"population_summaries":summaries,"drum_control":{"authorized_drum_eme_count":len(drum_times),"strong_drum_flux_median_threshold":strong_threshold,"definition":proto["drum_control"]},"direct_mix_bass_observability":outcome,"observational_principle":"Prospectively test low-frequency transient shape, local contrast, and timing consistency in the unmodified mix, with explicit Drum-coincidence handling, without original-stem access." if outcome=="YES" else None,"plots":plot_records,"complete_records":records,"firewall":proto["firewall"]}; result["audit_fingerprint"]=hashlib.sha256(canonical(result)).hexdigest(); (outdir/"audit.json").write_bytes(canonical(result)+b"\n"); print(result["audit_fingerprint"])
if __name__=="__main__":
 ap=argparse.ArgumentParser(); ap.add_argument("--output-dir",type=Path,required=True); args=ap.parse_args(); main(args.output_dir)
