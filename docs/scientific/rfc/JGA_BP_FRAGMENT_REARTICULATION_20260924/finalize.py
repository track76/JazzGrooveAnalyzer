from pathlib import Path
import json,csv,hashlib,datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FuncFormatter
O=Path(__file__).resolve().parent;I=O/'input';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert json.loads((O/'ISOLATION_VALIDATION.json').read_text())['PLP_reads_denied']
# Repeat the negative access check in the classification/collapse process.
try:open('/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/scientific/rfc/JGA_V1_OPERATIONAL_PLP_QUARTER_NEAREST_001_20260922/PLP_REFERENCE.csv','rb').read(1)
except PermissionError:pass
else:raise RuntimeError('PLP unexpectedly accessible')
bound=json.loads((O/'ACOUSTIC_METRICS.json').read_text());members=json.loads((I/'HYPOTHESIS_MEMBERSHIP.json').read_text());episodes=json.loads((I/'FUNDAMENTAL_EPISODES.json').read_text());notes={m['note_id']:m['native_hypothesis'] for m in members};mem={m['note_id']:m for m in members}
reasons={
'FR01':('AMBIGUOUS','Continuous decay at B, but the preceding compound attack contains different frozen family identities. Same MIDI does not establish the same fundamental; no cross-family merge.'),
'FR02':('SAME_NOTE_FRAGMENT','An earlier rise is followed by regularly oscillating, gradually declining low-band energy and RMS across the B boundary. No separate envelope restart is visible in Bass or matching mix low-band evidence.'),
'FR03':('SAME_NOTE_FRAGMENT','B starts within the declining tail of an earlier broad energy lobe. Bass amplitude, low-band energy and flux continue downward; the mix low-band curve follows the same decay.'),
'FR04':('AMBIGUOUS','A distinct rise develops roughly 30 ms before B, supported in both representations. A was already labelled E1 during weak activity. It is unclear whether this is a second same-pitch pizzicato or the first actual attack preceded by an early BP hypothesis; do not merge or assert two physical notes.'),
'FR05':('AMBIGUOUS','A short strong pre-B burst is visible in both signals, but the same MIDI changes from root to harmonic of a different frozen family. Attack source/ownership cannot be resolved in this restricted experiment.'),
'FR06':('SAME_NOTE_FRAGMENT','The earlier amplitude/energy establishment decays through B with continued periodic flux. No new low-band energy establishment or discrete waveform attack occurs at the split.'),
'FR07':('SAME_NOTE_FRAGMENT','A smooth energy lobe established well before B falls through B without restarting. Full-mix broadband activity is present, but the matching low-band Bass decay lacks a new front.'),
'FR08':('SAME_NOTE_FRAGMENT','Sustained Bass oscillation and nearly level low-band energy cross B with very small flux. Later mix-only fluctuations do not provide Bass rearticulation evidence at this boundary.'),
'FR09':('SAME_NOTE_FRAGMENT','A modest smooth post-B energy swelling occurs, but waveform oscillation remains continuous and boundary flux is weak compared with the earlier attack. No discrete renewed attack episode is visible; swelling alone is not rearticulation.'),
'FR10':('SAME_NOTE_FRAGMENT','Long established Bass oscillation decays smoothly across B. Boundary flux is very small in both representations; later mix peaks do not restart the Bass envelope.'),
'FR11':('AMBIGUOUS','A strong new low-band rise about 60 ms before B is followed by persistent multi-peak activity. Its position inside A makes the relationship between the MIDI boundary and a second same-pitch attack uncertain; retain both hypotheses.'),
'FR12':('AMBIGUOUS','A pronounced envelope/energy rise about 45 ms before B is supported in Bass and mix, with B on its decay. The existing A onset is much earlier. This may be a delayed segmentation response to an attack rather than proof of two same-pitch physical events.'),
'FR13':('SAME_NOTE_FRAGMENT','B lies in an already established train of declining low-band oscillations. Earlier peaks and a perturbation remain visible, but no independent envelope restart occurs around B.'),
'FR14':('SAME_NOTE_FRAGMENT','The large earlier attack produces a multi-peak oscillatory energy envelope that continues and declines across B. The boundary is not accompanied by renewed establishment in Bass or mix.'),
'FR15':('SAME_NOTE_FRAGMENT','Bass RMS and low-band energy follow the earlier attack into declining oscillatory activity through B. Mix fluctuations do not create a corresponding new Bass envelope.'),
'FR16':('SAME_NOTE_FRAGMENT','After an earlier energy rise, stable same-note oscillation and gently declining energy pass through B. Local flux maxima continue without a distinct second attack episode.'),
'FR17':('SAME_NOTE_FRAGMENT','B is well into the tail of the earlier energy/flux onset. The continuing envelope has no new steep rise; later predominantly mix activity does not corroborate a Bass attack at B.'),
'FR18':('SAME_NOTE_FRAGMENT','The earlier broad energy lobe falls steeply across the short MIDI gap into a weak tail. Both representations show continuation/decay rather than an independent new front.')}
pname=lambda p:['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][p%12]+str(p//12-1)
rows=[]
for b in bound:
 cls,reason=reasons[b['boundary_id']]
 rows.append(dict(boundary_id=b['boundary_id'],fundamental_episode_id=b['family_A'] if b['family_A']==b['family_B'] else b['family_A']+' -> '+b['family_B'],pitch_midi=b['pitch'],pitch_name=pname(b['pitch']),segment_A_id=b['A'],segment_A_end_s=b['A_end'],segment_B_id=b['B'],segment_B_start_s=b['B_start'],A_to_B_gap_ms=b['gap_ms'],bass_stem_attack_evidence=f"Post/pre low-band energy median ratio {b['bass_energy_after_before_ratio']:.4f}; inspect waveform and 5ms RMS",full_mix_attack_evidence=f"Post/pre low-band energy median ratio {b['mix_energy_after_before_ratio']:.4f}; shared decay/rise interpreted in reason",spectral_front_evidence=f"Boundary/earlier maximum flux ratio Bass {b['bass_boundary_flux_vs_earlier_max']:.4f}, mix {b['mix_boundary_flux_vs_earlier_max']:.4f}; these are descriptive, not decision thresholds",classification=cls,confidence='MEDIUM' if cls=='SAME_NOTE_FRAGMENT' else 'LOW',reason=reason))
with (O/'SAME_PITCH_FRAGMENT_REARTICULATION.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(O/'CLASSIFICATIONS.json').write_text(json.dumps(rows,indent=2)+'\n')
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'classification_sha256':sha(O/'CLASSIFICATIONS.json'),'table_sha256':sha(O/'SAME_PITCH_FRAGMENT_REARTICULATION.csv'),'scope':'experimental visual-morphology classifications only; not canonical methodology','input_hashes':json.loads((O/'INPUT_AUDIT.json').read_text()),'no_PLP_access':True,'investigator_previously_exposed_to_PLP':True,'classification_rule':'Descriptive visual morphology; no calibrated classifier or transferred Fishman threshold. Rearticulation requires a distinct renewed envelope/front attributable to a second same-pitch attack, not merely a peak. Ambiguity retained when A/B linkage or family identity is uncertain.'}
freeze=O/'CLASSIFICATION_FREEZE.json'
assert not freeze.exists(),'Do not overwrite experimental freeze'
freeze.write_text(json.dumps(record,indent=2)+'\n')
# Only now construct experimental identity groups. No original note or family is edited.
parent={nid:nid for nid in notes}
def root(n):
 while parent[n]!=n:n=parent[n]
 return n
for r in rows:
 if r['classification']=='SAME_NOTE_FRAGMENT':
  a,b=r['segment_A_id'],r['segment_B_id'];assert mem[a]['family_id']==mem[b]['family_id'];parent[root(b)]=root(a)
groups={}
for nid in notes:groups.setdefault(root(nid),[]).append(nid)
collapsed=[]
for ids in groups.values():
 ids.sort(key=lambda i:notes[i]['onset']);nn=[notes[i] for i in ids]
 collapsed.append(dict(identity_id='C_'+ids[0],family_id=mem[ids[0]]['family_id'],pitch_midi=nn[0]['pitch'],activity_start_s=min(n['onset'] for n in nn),activity_end_s=max(n['offset'] for n in nn),native_member_ids=ids,native_records=nn,collapsed=len(ids)>1,qualification='identity extent only; native gaps and all coordinates preserved in member records; no inferred acoustic onset'))
collapsed.sort(key=lambda r:r['activity_start_s'])
(O/'EXPERIMENTAL_COLLAPSED_REPRESENTATION.json').write_text(json.dumps(collapsed,indent=2)+'\n')
(O/'COLLAPSE_PROVENANCE.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prior_classification_freeze_sha256':sha(freeze),'collapsed_representation_sha256':sha(O/'EXPERIMENTAL_COLLAPSED_REPRESENTATION.json'),'source_note_count':98,'native_records_preserved':sum(len(g['native_records']) for g in collapsed),'status':'hashed derived artifact, no additional methodological freeze'},indent=2)+'\n')
# Final diagnostic pages reuse inspected curves with classifications; no PLP involved.
source=(O/'inspect_boundaries.py').read_text()
source=source.replace("fig.savefig(O/f\"{b['boundary_id']}_INSPECT.png\",dpi=110);plt.close(fig)","""
 cls,reason=reasons[b['boundary_id']]
 for tx in fig.texts:
  if 'UNCLASSIFIED acoustic inspection' in tx.get_text():tx.set_text(tx.get_text().replace('UNCLASSIFIED acoustic inspection',cls))
 # Candidate front regions are visual annotations of the reviewed signal, not new emitted onset coordinates.
 regions={'FR04':(-40,-5),'FR05':(-45,-10),'FR11':(-80,-25),'FR12':(-65,-10)}
 if b['boundary_id'] in regions:
  a0,a1=regions[b['boundary_id']]
  for ax in axs[:4]:ax.axvspan(a0,a1,color='#dcac55',alpha=.13)
 import textwrap
 fig.text(.08,.014,'\\n'.join(textwrap.wrap(reason,145)),fontsize=8)
 finalpdf.savefig(fig);fig.savefig(O/f"{b['boundary_id']}_FINAL.png",dpi=110);plt.close(fig)
""")
with PdfPages(O/'SAME_PITCH_FRAGMENT_VS_REARTICULATION.pdf') as finalpdf:exec(compile(source,str(O/'inspect_boundaries.py'),'exec'))
fmt=FuncFormatter(lambda t,pos:f'{int(t)//60:02}:{t%60:05.2f}')
with PdfPages(O/'BASIC_PITCH_BEFORE_AFTER_FRAGMENT_COLLAPSE.pdf') as pdf:
 lo=min(n['onset'] for n in notes.values())-.05;hi=max(n['offset'] for n in notes.values())+.05
 for page,start in enumerate(np.arange(lo,hi,6)):
  end=min(start+6,hi);fig,axs=plt.subplots(2,1,figsize=(18,10),sharex=True);fig.subplots_adjust(left=.06,right=.98,top=.88,bottom=.10,hspace=.3)
  fig.suptitle('Same-pitch fragment collapse — identity display only; no PLP',fontsize=16)
  for ep in episodes:
   if ep['end_s']>=start and ep['start_s']<=end:
    for ax in axs:ax.axvline(ep['root_onset_s'],color='.7',lw=.5);ax.text(ep['root_onset_s'],66,ep['episode_id'],rotation=90,fontsize=6,clip_on=True)
  for nid,n in notes.items():
   if n['offset']<start or n['onset']>end:continue
   axs[0].plot([n['onset'],n['offset']],[n['pitch']]*2,color='#477c9c',lw=3);axs[0].plot(n['onset'],n['pitch'],'|',color='black');axs[0].text(n['onset'],n['pitch']+.5,nid,fontsize=6,clip_on=True)
  for g in collapsed:
   if g['activity_end_s']<start or g['activity_start_s']>end:continue
   col='#007fa0' if g['collapsed'] else '#888888';axs[1].plot([g['activity_start_s'],g['activity_end_s']],[g['pitch_midi']]*2,color=col,lw=3);axs[1].text(g['activity_start_s'],g['pitch_midi']+.5,'+'.join(g['native_member_ids']),fontsize=6,clip_on=True)
   for n in g['native_records']:axs[1].plot(n['onset'],n['pitch'],'|',color='.6',ms=4)
  for ax in axs:ax.set_ylim(26,70);ax.grid(axis='y',alpha=.1);ax.set_xlim(start,end);ax.set_ylabel('MIDI pitch');ax.xaxis.set_major_formatter(fmt)
  axs[0].set_title('Original 98 native hypotheses + unchanged 63 family origins',fontsize=11);axs[1].set_title('Experimental: only supported SAME_NOTE_FRAGMENT pairs joined; ambiguous pairs retained',fontsize=11);axs[1].set_xlabel('Original recording time (MM:SS.xx)');fig.text(.06,.025,'Blue = merged identity extent; gray = unchanged hypotheses. Native segment starts remain small ticks. Gaps are preserved in JSON; spans are not new timing measurements.',fontsize=9);pdf.savefig(fig);fig.savefig(O/f'BEFORE_AFTER_{page+1}.png',dpi=100);plt.close(fig)
rootids={nid for ep in episodes for nid in ep['root_note_ids']};nroot_after=len({root(nid) for nid in rootids})
s={'same_pitch_boundaries':len(rows),'within_same_family':sum(b['family_A']==b['family_B'] for b in bound),'cross_family_ambiguous':2,'SAME_NOTE_FRAGMENT':sum(r['classification']=='SAME_NOTE_FRAGMENT' for r in rows),'TRUE_REARTICULATION':sum(r['classification']=='TRUE_REARTICULATION' for r in rows),'AMBIGUOUS':sum(r['classification']=='AMBIGUOUS' for r in rows),'native_root_segments_before':len(rootids),'experimental_root_identity_units_after':nroot_after,'all_native_hypotheses_before':98,'all_identity_units_after':len(collapsed),'frozen_fundamental_episodes_before':63,'frozen_fundamental_episodes_after':63,'fragmentation_explains_excess':'PARTIAL','classification_sha256':sha(O/'CLASSIFICATIONS.json')}
(O/'SUMMARY.json').write_text(json.dumps(s,indent=2)+'\n')
for name,a in json.loads((O/'INPUT_AUDIT.json').read_text()).items():assert sha(I/name)==a['sha256']
(O/'RESULT.md').write_text('''# Same-pitch segmentation versus rearticulation — experimental review

## Result

```json
'''+json.dumps(s,indent=2)+'''
```

Thirteen same-family splits are supported as segmentation continuation by the inspected waveform, low-band energy and flux morphology. Five remain ambiguous; no second physical same-pitch attack is established confidently. Zero TRUE_REARTICULATION classifications is not evidence that the recording contains no rearticulations.

## Population and interpretation

All successive same-MIDI pairs from the 98 native hypotheses were tested when B starts at or after A end and the gap is no more than512/22050 s (23.22 ms), the existing frozen family continuity window. This defines a bounded candidate population, not a fragment classifier. It finds16 same-family root pairs plus2 cross-family pairs. Those two remain ambiguous; harmonic ownership is unchanged. All six PI examples are included. Longer-gap repetitions are outside this short-segment study, not declared absent.

Classification used visual acoustic morphology, not PLP, pitch equality, gap length or an automatic probability threshold. All18 windows were individually inspected. Local range is B−260 to B+180 ms. RMS display uses221 samples (~5ms). The existing synchronized magnitude/positive-flux tensor was reused unchanged:30–250Hz, Hann1024, hop44,44100Hz. Energy is sum of squared magnitudes in the same band. Descriptive post/pre energy medians use +15..+60 / −60..−15ms; boundary/earlier flux ratios use maxima in ±30 / −220..−50ms. These numbers were not decision thresholds. Flux and energy normalization is solely per-plot display scaling.

For FR04, FR11 and FR12, a renewed front is observable before B but within A. The evidence does not determine whether A itself was a separate physical pizzicato or an early/misaligned transcription hypothesis. Those cases are not silently collapsed, and no second physical note is invented. FR01/FR05 remain ambiguous because frozen root/harmonic ownership changes. Amber shading shows reviewed front regions, not newly generated attack timestamps. All classifications are qualified, uncalibrated judgments; absence of a visible front is not proof of physical non-rearticulation.

## Counts are different layers

There are79 native root segments in63 frozen families. Collapsing13 supported same-family fragment boundaries produces66 experimental root identity units; including19 unchanged harmonic hypotheses yields85 total identity units from98 native hypotheses. These are not independently verified physical-note counts. The already frozen63-family reconstruction had provisionally grouped these root fragments; its count remains63 and is NOT reduced to50. Thus fragmentation explains part of the native excess segmentation, not the entire note-identification problem or the existence of a particular walking-note population.

## Independence and provenance

The investigator previously saw PLP-based diagnostics; this study is not investigator-blind. The acoustic and final classification processes were filesystem-isolated from PLP, with negative read tests saved in ISOLATION_VALIDATION.json. Only sanitized native note/family records, preserved Bass/full-mix PCM and saved spectral tensors were supplied. No PLP was subsequently reintroduced. No Basic Pitch/model inference, spectral parameter retuning or new continuous peak search was performed.

CLASSIFICATIONS.json and the CSV were saved and SHA-256 frozen before the collapsed representation was constructed. CLASSIFICATION_FREEZE.json records that experimental authority only. The collapsed representation is a hashed derived identity view containing all98 exact native source records. No original hypothesis, timestamp, episode, pitch, previous freeze, Report001 or canonical method is changed. No commit or push.

## PI review

SAME_PITCH_FRAGMENT_VS_REARTICULATION.pdf has one page for each18 boundaries, with exact A-end/B-start and synchronized signals. BASIC_PITCH_BEFORE_AFTER_FRAGMENT_COLLAPSE.pdf covers the entire frozen note sequence in four chronological pages. No quarter grid or musical timing interpretation. Review the five ambiguous cases before any further event-count inference. STOP for PI review.
''')
print(json.dumps(s,indent=2))
