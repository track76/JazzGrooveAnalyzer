from pathlib import Path
import json,hashlib
import numpy as np,soundfile as sf
from scipy.ndimage import uniform_filter1d
from scipy.signal import find_peaks
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).resolve().parent;I=O/'input'
# Explicit negative read test: no coordinate/metric artifact is available to this process.
for path in ['/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/scientific/rfc/JGA_V1_OPERATIONAL_PLP_QUARTER_NEAREST_001_20260922/PLP_REFERENCE.csv','/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/historical_reports/JGA_HISTORICAL_REPORT_001/FINAL_SCORE_V1/METRIC_REFERENCE.csv']:
 try:
  open(path,'rb').read(1)
 except PermissionError:pass
 else:raise RuntimeError('PLP exclusion failed')
(O/'ISOLATION_VALIDATION.json').write_text(json.dumps({'PLP_reads_denied':True,'investigator_previously_exposed_to_PLP':True,'classification_inputs':'sanitized native notes, families, PCM and saved spectral tensor only'},indent=2))
m=json.loads((I/'HYPOTHESIS_MEMBERSHIP.json').read_text());e=json.loads((I/'FUNDAMENTAL_EPISODES.json').read_text());notes={x['note_id']:x['native_hypothesis'] for x in m};members={x['note_id']:x for x in m};bound=[]
for pitch in sorted(set(n['pitch'] for n in notes.values())):
 ns=sorted([n for n in notes.values() if n['pitch']==pitch],key=lambda n:n['onset'])
 for a,b in zip(ns,ns[1:]):
  gap=b['onset']-a['offset']
  if -1e-9<=gap<=512/22050+1e-9:bound.append(dict(A=a['note_id'],B=b['note_id'],pitch=pitch,A_start=a['onset'],A_end=a['offset'],B_start=b['onset'],B_end=b['offset'],gap_ms=gap*1000,family_A=members[a['note_id']]['family_id'],family_B=members[b['note_id']]['family_id']))
bound.sort(key=lambda b:b['B_start'])
for i,b in enumerate(bound):b['boundary_id']=f'FR{i+1:02}'
(O/'BOUNDARY_POPULATION.json').write_text(json.dumps(bound,indent=2))
z=np.load(I/'SYNCHRONIZED_TF.npz');t=z['times_s'];freq=z['frequencies_hz'];band=(freq>=30)&(freq<250)
x={};rms={};energy={}
for s in ['bass','mix']:
 xx,sr=sf.read(I/f'{s}.wav',always_2d=True);x[s]=xx.mean(axis=1);assert sr==44100;rms[s]=np.sqrt(uniform_filter1d(x[s]**2,size=221));energy[s]=np.sum(z[s+'_mag'][band]**2,axis=0)
xt=45+np.arange(len(x['bass']))/sr
pname=lambda p:['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][p%12]+str(p//12-1)
metrics=[]
for b in bound:
 tb=b['B_start'];rel=(t-tb)*1000;rx=(xt-tb)*1000;bm=(rx>=-260)&(rx<=180);sm=(rel>=-260)&(rel<=180);row=dict(b)
 for s in ['bass','mix']:
  pre=(rel>=-60)&(rel<=-15);post=(rel>=15)&(rel<=60);v=z[s+'_low'];row[s+'_energy_after_before_ratio']=float(np.median(energy[s][post])/max(np.median(energy[s][pre]),1e-20));local=(rel>=-30)&(rel<=30);early=(rel>=-220)&(rel<=-50);row[s+'_boundary_flux_vs_earlier_max']=float(v[local].max()/max(v[early].max(),1e-20));j=np.flatnonzero(local)[np.argmax(v[local])];row[s+'_local_flux_max_s']=float(t[j]);row[s+'_local_flux_max_relative_ms']=float(rel[j])
 metrics.append(row)
 fig,axs=plt.subplots(5,1,figsize=(13,11),sharex=True);fig.subplots_adjust(top=.9,bottom=.08,hspace=.45,left=.08,right=.97)
 fig.suptitle(f"{b['boundary_id']} {b['family_A']} → {b['family_B']} | {pname(b['pitch'])} MIDI {b['pitch']} | {b['A']} → {b['B']}",fontsize=14,y=.98)
 fig.text(.5,.945,f"A end {b['A_end']:.9f} s | B start {tb:.9f} s | gap {b['gap_ms']:.3f} ms — UNCLASSIFIED acoustic inspection, no PLP",ha='center',fontsize=10)
 axs[0].plot(rx[bm][::3],x['bass'][bm][::3],color='.45',lw=.5);axs[0].plot(rx[bm][::10],rms['bass'][bm][::10],color='#007faa',lw=1);axs[0].set_ylabel('Bass PCM\n+ 5ms RMS')
 for s,col in [('bass','#007faa'),('mix','#b45d22')]:
  v=z[s+'_low'];scale=max(v[sm].max(),1e-20);axs[1].plot(rel[sm],v[sm]/scale,color=col,label=s+' flux / local display max',lw=.8)
  v=energy[s];axs[2].plot(rel[sm],v[sm]/max(v[sm].max(),1e-20),color=col,label=s+' energy',lw=.8)
 axs[1].set_ylabel('Positive flux\n30–250 Hz');axs[1].legend(fontsize=7,loc='upper right');axs[2].set_ylabel('Low-band energy\nnormalized display')
 axs[3].plot(rx[bm][::3],x['mix'][bm][::3],color='.4',lw=.5);axs[3].set_ylabel('Original mix PCM')
 for nid,y,col in [(b['A'],1,'#777777'),(b['B'],.45,'#007faa')]:
  n=notes[nid];axs[4].plot([(n['onset']-tb)*1000,(n['offset']-tb)*1000],[y,y],lw=5,color=col);axs[4].text(max(-255,(n['onset']-tb)*1000),y+.12,nid,fontsize=9)
 axs[4].set_ylim(0,1.5);axs[4].set_yticks([]);axs[4].set_ylabel('Native BP segments');axs[4].set_xlabel('Milliseconds relative to native B start (not PLP)')
 for ax in axs:
  ax.axvline(0,color='black',lw=1,ls='--');ax.axvline((b['A_end']-tb)*1000,color='#8e4fa8',lw=1,ls=':');ax.set_xlim(-260,180)
 fig.savefig(O/f"{b['boundary_id']}_INSPECT.png",dpi=110);plt.close(fig)
(O/'ACOUSTIC_METRICS.json').write_text(json.dumps(metrics,indent=2))
print('Boundaries:',len(bound))
for b in metrics:print(b['boundary_id'],b['family_A'],b['family_B'],'energy B/M',round(b['bass_energy_after_before_ratio'],2),round(b['mix_energy_after_before_ratio'],2),'flux B/M',round(b['bass_boundary_flux_vs_earlier_max'],2),round(b['mix_boundary_flux_vs_earlier_max'],2))
