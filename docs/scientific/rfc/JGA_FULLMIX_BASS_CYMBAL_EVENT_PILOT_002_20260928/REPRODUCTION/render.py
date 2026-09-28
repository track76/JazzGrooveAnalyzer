"""Figures generated exclusively from completed Pilot002 machine-readable evidence."""
import os,sys,json,io,hashlib,platform
from pathlib import Path
R=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer');sys.path.insert(0,str(R));sys.dont_write_bytecode=True
import numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tools import jga_governance as g
O='docs/scientific/rfc/JGA_FULLMIX_BASS_CYMBAL_EVENT_PILOT_002_20260928/';TOKEN='codex-pilot002-20260928';base=R/O
C=json.loads((base/'CONFIGURATION/CONFIGURATION.json').read_text());meta=json.loads((base/'EXTERNAL_ARRAYS.json').read_text());src=Path(meta['files'][0]['path'])
with src.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==meta['files'][0]['sha256']
A=np.load(src,allow_pickle=False);t=A['time_s'];sr=C['sample_rate'];start=meta['processing_start_sample'];lo,hi=C['region_s'];hop=C['stft']['hop_length'];wave_t=(start+np.arange(len(A['fullmix_waveform'])))/sr
rows={};plotdata={'plots':{},'source_arrays_sha256':meta['files'][0]['sha256'],'matplotlib_version':matplotlib.__version__,'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'selection_rule':C['figures']['selection'],'rendered_at':g.now(),'disposable_cache':'TEMPORARY_NO_BACKUP; matplotlib/numba reconstructible caches only, no scientific evidence'}
for arm in ['bass','cymbal']:
 rows[arm]={kind:json.loads((base/arm.upper()/(kind+'.json')).read_text()) for kind in ['ALL_LOCAL_MAXIMA','DEDUPLICATED_CANDIDATES']}
colors={'BASS_COMPATIBLE':'#2458ac','BASS_POSSIBLE':'#528cba','CYMBAL_COMPATIBLE':'#d47115','OTHER_PERCUSSIVE_COMPATIBLE':'#864b8c','AMBIGUOUS':'#707070','UNRESOLVED':'#b52626'}
def points(ax,arm,rr,name,ykey='flux',height=None):
 for state in sorted(set(r['state'] for r in rr)):
  subset=[r for r in rr if r['state']==state];ax.scatter([r['landmark_timestamp_s'] for r in subset],[r[ykey] if height is None else height for r in subset],s=11,color=colors[state],label=state,alpha=.8,zorder=3)
 for r in rr:plotdata['plots'].setdefault(name,[]).append({'arm':arm,'candidate_id':r['candidate_id'],'timestamp_s':r['landmark_timestamp_s'],'y':r[ykey] if height is None else height,'state':r['state']})
def save(fig,name):
 fig.suptitle('Pilot 002 — experimental candidate evidence, NOT observed instrument attacks',fontsize=11);fig.tight_layout(rect=[0,0,1,.965]);b=io.BytesIO();fig.savefig(b,format='png',dpi=130);plt.close(fig);print(g.write(R,TOKEN,O+'FIGURES/'+name+'.png',b.getvalue()),flush=True)
for arm in ['bass','cymbal']:
 name=arm.upper()+'_EVIDENCE';fig,axes=plt.subplots(3,1,figsize=(14,8),sharex=True)
 axes[0].plot(t,A[arm+'_flux'],lw=.7,color='#aaaaaa');raw=rows[arm]['ALL_LOCAL_MAXIMA'];axes[0].scatter([r['landmark_timestamp_s'] for r in raw],[r['flux'] for r in raw],s=3,color='#888888',label='all local maxima');points(axes[0],arm,raw,name);axes[0].set_ylabel('Band flux (L2)');axes[0].legend(loc='upper right',fontsize=6,ncol=3)
 if arm=='bass':
  axes[1].plot(t,A['bass_f0_hz'],'.',ms=1,label='F0 low-band / missing = gap');axes[1].set_ylabel('F0 Hz');axes[2].plot(t,A['bass_harmonic_magnitude_sum'],lw=.7,label='Full-mix harmonic-bin sum');axes[2].set_ylabel('Magnitude sum')
 else:
  axes[1].plot(t,A['cymbal_centroid_hz'],lw=.7,label='Band-conditioned centroid');axes[1].set_ylabel('Hz');axes[2].plot(t,A['cymbal_post_event_energy'],lw=.7,label='Post-event energy, NOT decay constant');axes[2].set_ylabel('Band magnitude² sum')
 for ax in axes:ax.set_xlim(lo,hi);ax.grid(alpha=.15)
 for ax in axes[1:]:ax.legend(fontsize=7)
 axes[-1].set_xlabel('Original full-mix native time (s)');save(fig,name)
name='COMBINED_EVENT_MAP';fig,ax=plt.subplots(figsize=(14,4))
for arm,height in [('bass',1),('cymbal',0)]:points(ax,arm,rows[arm]['DEDUPLICATED_CANDIDATES'],name,height=height)
ax.set_yticks([0,1],['Cymbal-compatible evidence stream','Bass-compatible evidence stream']);ax.set_xlim(lo,hi);ax.set_ylim(-.5,1.5);ax.set_xlabel('Original full-mix native time (s) — no grid');ax.legend(fontsize=6,ncol=3);save(fig,name)
name='REPRESENTATIVE_ZOOMS';fig,axes=plt.subplots(4,3,figsize=(15,13));categories=['COMPATIBLE','AMBIGUOUS','CONFUSER_HYPOTHESIS_UNRESOLVED','BOUNDARY_SUPPORT'];catalog=[(a,r) for a in ['bass','cymbal'] for r in rows[a]['DEDUPLICATED_CANDIDATES']]
for rowidx,category in enumerate(categories):
 pool=[(a,r) for a,r in catalog if (r['state'] in ['BASS_COMPATIBLE','CYMBAL_COMPATIBLE'] if category=='COMPATIBLE' else r['state']=='AMBIGUOUS' if category=='AMBIGUOUS' else r['state']=='OTHER_PERCUSSIVE_COMPATIBLE' if category=='CONFUSER_HYPOTHESIS_UNRESOLVED' else r['evaluation_boundary_crossed'])];pool=sorted(pool,key=lambda p:(p[1]['landmark_timestamp_s'],p[0]))
 ids=sorted(set([0,len(pool)//2,len(pool)-1])) if pool else []
 for col,ax in enumerate(axes[rowidx]):
  if col>=len(ids):ax.text(.1,.5,category+'\nNOT AVAILABLE',transform=ax.transAxes,fontsize=8);ax.set_axis_off();continue
  arm,r=pool[ids[col]];v=r['landmark_timestamp_s'];halfwidth=C['figures']['zoom_width_s']/2;sel=(t>=v-halfwidth)&(t<=v+halfwidth);ax.plot(t[sel],A[arm+'_flux'][sel],lw=.8,color='#aaaaaa');near=[p for p in rows[arm]['DEDUPLICATED_CANDIDATES'] if abs(p['landmark_timestamp_s']-v)<=halfwidth];points(ax,arm,near,name);ax.axvline(v,color='black',ls='--',lw=.7);ax.set_title(category+'\n'+r['candidate_id'],fontsize=8);ax.set_xlabel('native seconds');ax.set_ylabel(arm+' flux')
save(fig,name)
name='TIMESTAMP_DIAGNOSTIC';fig,axes=plt.subplots(2,1,figsize=(13,7))
for ax,arm in zip(axes,['bass','cymbal']):
 rr=rows[arm]['DEDUPLICATED_CANDIDATES'];r=rr[0];v=r['landmark_timestamp_s'];sel=(wave_t>=v-.10)&(wave_t<=v+.10);ax.plot(wave_t[sel],A['fullmix_waveform'][sel],lw=.5,alpha=.65,label='Unfiltered original mono');ax.plot(wave_t[sel],A[arm+'_filtered_waveform'][sel],lw=.7,label='Zero-phase bandpass');ax.axvline(v,color='red',lw=1,label='Immutable frame-derived landmark');ax.set_title(arm+' / '+r['candidate_id']+' — no physical onset accuracy claim',fontsize=9);ax.set_xlabel('native seconds');ax.legend(fontsize=7);plotdata['plots'].setdefault(name,[]).append({'arm':arm,'candidate_id':r['candidate_id'],'timestamp_s':v,'state':r['state']})
save(fig,name)
name='BOUNDARY_SUPPORT';fig,axes=plt.subplots(2,2,figsize=(14,7))
for rowidx,arm in enumerate(['bass','cymbal']):
 for col,bound in enumerate([lo,hi]):
  ax=axes[rowidx,col];sel=(t>=bound-.7)&(t<=bound+.7);ax.plot(t[sel],A[arm+'_flux'][sel],lw=.8);near=[r for r in rows[arm]['ALL_LOCAL_MAXIMA'] if abs(r['landmark_timestamp_s']-bound)<=.7];points(ax,arm,near,name);ax.axvline(bound,color='red',ls='--');ax.axvspan(bound-.7 if col==0 else bound,bound if col==0 else bound+.7,color='gray',alpha=.15,label='Real source context outside admission');ax.set_title(arm+' '+('start' if col==0 else 'end')+' [start, end)');ax.set_xlabel('native seconds');ax.legend(fontsize=7)
save(fig,name)
print(g.write(R,TOKEN,O+'PLOT_DATA.json',(json.dumps(plotdata,indent=2,allow_nan=False)+'\n').encode()),flush=True)
