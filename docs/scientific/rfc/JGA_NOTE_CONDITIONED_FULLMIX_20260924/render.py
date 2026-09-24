import os
os.environ['MPLCONFIGDIR']='/private/tmp/jga_domain_mpl'
from pathlib import Path
import json,csv,hashlib,datetime,shutil,re
import numpy as np,soundfile as sf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
P=Path(__file__).resolve().parent;I=P/'inference/input';O=P/'inference/output';load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
T=load(O/'TEMPLATES_SIGNATURES.json');R=load(O/'CANDIDATE_ATTRIBUTIONS.json');E=load(O/'EPISODE_RESULTS.json');ident={e['episode_id']:e for e in load(O/'TARGET_IDENTITIES.json')};Q=load(I/'QUERY_EVIDENCE.json');S=load(O/'SUMMARY.json');Z0=np.load(O/'HARMONIC_CURVES.npz');Z={k:Z0[k] for k in Z0.files}
b,sr=sf.read(I/'BASS.wav');f,_=sf.read(I/'FULLMIX.wav');b=b.mean(axis=1);f=f.mean(axis=1)
plt.rcParams.update({'font.size':8,'pdf.fonttype':42})
def page(e):
 eid=e['episode_id'];keys=[k for k in T if k.startswith(eid+'_')];fig,ax=plt.subplots(5,len(keys),figsize=(max(12,4.3*len(keys)),11),squeeze=False)
 for col,k in enumerate(keys):
  template=T[k];rr=[r for r in R if r['template_id']==k];bid=rr[0]['BP_member_id'];q=Q[bid];a=q['search_start_s'];end=q['search_end_s'];ix=np.arange(int(np.ceil(a*sr)),int(np.floor(end*sr))+1);t=Z[k+'_t'];harm=np.array(template['harmonics_hz']);sig=np.array(template['signature']);native=next(m for m in ident[eid]['members'] if m['note_id']==bid)
  ax[0,col].plot(ix/sr,b[ix],lw=.6,color='#20637c');ax[0,col].axvspan(float(native['onset_s']),float(native['offset_s']),color='#a38cb0',alpha=.17)
  ax[1,col].bar(harm,sig,width=min(template['f0']*.6,60),color=['#237c5e' if v else '#aaa' for v in template['observable']]);ax[1,col].set_xlim(0,2000);ax[1,col].set_xlabel('Harmonic frequency (Hz); tolerance ±43.07 Hz')
  ax[2,col].plot(ix/sr,f[ix],lw=.6,color='#444')
  mat=Z[k+'_mix'];mat=np.log10(mat+1e-15);im=ax[3,col].imshow(mat,origin='lower',aspect='auto',extent=[t[0],t[-1],.5,len(harm)+.5],cmap='magma');ax[3,col].set_ylabel('Harmonic index / log10 energy')
  times=[r['candidate_s'] for r in rr];ax[4,col].plot(times,[r['stem_signature_similarity'] for r in rr],'.-',ms=2,label='FM rise / stem signature');ax[4,col].plot(times,[r['synchronous_stem_mix_similarity'] for r in rr],'.-',ms=2,label='FM / stem synchronous rise');ax[4,col].set_ylim(-.03,1.05);ax[4,col].legend(fontsize=6,loc='lower left')
  for j in [0,2,3,4]:
   aa=ax[j,col];aa.set_xlim(a,end);aa.axvline(q['BP_onset_s'],ls='--',color='#9a4ab0',lw=1)
   if e['previous_selected_s'] is not None and a<=e['previous_selected_s']<=end:aa.axvline(e['previous_selected_s'],color='#197dcc',lw=1.5)
   aa.ticklabel_format(axis='x',useOffset=False);aa.grid(alpha=.1)
  for r in rr:ax[2,col].axvline(r['candidate_s'],color='#999',lw=.35,alpha=.45)
  for tt in [x['timestamp_s'] for x in q['salient_fronts']]:ax[2,col].axvline(tt,color='#cc6a1b',lw=.8)
  ax[0,col].set_title(f'{bid} · MIDI {template["pitch"]} / f0 {template["f0"]:.2f} Hz\nObservable bands: {sum(template["observable"])}; sufficient: {template["resolution_sufficient"]}')
  ax[0,col].set_ylabel('Bass / BP activity');ax[1,col].set_ylabel('Stem harmonic energy fraction');ax[2,col].set_ylabel('Full mix / every candidate');ax[4,col].set_ylabel('Unthresholded cosine');ax[4,col].set_xlabel('Original recording coordinate (s)')
 fig.suptitle(f'{eid} · {e["status"]}\nExact independent member windows; root and member pitch hypotheses retained',fontsize=12)
 fig.text(.015,.012,'All candidates UNRESOLVED: template sufficiency gate fails. Raw similarity is not Bass proof. Orange: prior generic salience cue.\nPurple: native BP origin; shaded: BP activity; blue: unchanged prior stem selection. No full-mix timing selection; no PLP.',fontsize=8)
 fig.tight_layout(rect=[0,.06,1,.94]);return fig
sets=[('JGA_NOTE_CONDITIONED_FULLMIX_ATTRIBUTION_63.pdf',E),('JGA_MULTIPLE_CUE_BASS_ATTRIBUTION.pdf',[e for e in E if e['previous_multiple_cue_abstention']]),('JGA_HF044_HF047_NOTE_ATTRIBUTION.pdf',[e for e in E if e['episode_id'] in ['HF044','HF047']])]
for name,events in sets:
 with PdfPages(P/name) as pdf:
  for e in events:
   fig=page(e);pdf.savefig(fig)
   if name==sets[-1][0]:fig.savefig(P/(e['episode_id']+'_REVIEW.png'),dpi=110)
   plt.close(fig)
 print(name,len(events),flush=True)
shutil.copyfile(O/'NOTE_CONDITIONED_FULLMIX_ATTRIBUTION.csv',P/'NOTE_CONDITIONED_FULLMIX_ATTRIBUTION.csv')
# Explicit descriptive early/later candidate comparisons, without choosing a winner.
special=[]
for eid in ['HF044','HF047']:
 e=next(x for x in E if x['episode_id']==eid);rr=[x for x in R if x['episode_id']==eid];sel=e['previous_selected_s']
 for label,sub in [('earlier prior salience cues',[r for r in rr if r['prior_salient_cue'] and r['candidate_s']<sel]),('nearest existing FM candidate to old stem selection (diagnostic only)',[min(rr,key=lambda r:abs(r['candidate_s']-sel))])]:
  for r in sub:special.append({k:r[k] for k in ['episode_id','candidate_s','candidate_minus_BP_ms','harmonic_coherence','target_enrichment','stem_signature_similarity','synchronous_stem_mix_similarity','temporal_rise_similarity','non_target_change_fraction','source_classification']}|{'comparison_role':label})
(P/'HF044_HF047_RAW_COMPARISON.json').write_text(json.dumps(special,indent=2)+'\n')
text='''# Note-conditioned stem → full-mix attribution

PROCESS-BLINDED RESTART AFTER INVESTIGATOR PLP EXPOSURE

## Result

The prospectively frozen diagnostic does not resolve any episode. All 34 previous multiple-cue abstentions remain UNRESOLVED_ATTRIBUTION; zero become unique, multiple-confirmed or no-compatible-front cases. All 63 episodes remain unresolved, rather than being classified as no Bass activity. None of the 17 previous selections receives a declared Bass-compatible counterpart, earlier alternative or later alternative. These zero counts reflect the sufficiency gate, not evidence that Bass fronts are absent.

No upstream selector, candidate, window, BP output, fundamental, fragment classification, routing or historical timestamp was changed. No model was trained or applied to full-mix features. PLP was never loaded. Prior investigator exposure, including two legacy PLP-bearing rows and required bootstrap context, remains disclosed; attribution execution itself denied timing authority access.

## Frozen method and input verification

RULE_INPUT_FREEZE.json precedes inference. Its rule and exact copied inputs include all 63 frozen episodes, all 98 native member records, independent prior BP windows, prior stem decisions/candidates, fragment audit, and bounded full-mix population. Candidate generation was not repeated. Root and exact member pitch hypotheses are both retained, yielding 117 template evaluations and 4532 candidate–note evaluations. These are not counts of physical attacks. Every one of the 3842 previous full-mix query candidates is retained.

Both original PCM signals use their unchanged recording coordinates and 44100 Hz. Hann1024/hop44 gives 43.066 Hz FFT bins, 23.220 ms window support and 0.998 ms frame spacing. Note-specific descriptive power/energy changes are derived on this common grid; this adds attribution features without changing the frozen 30–250 Hz candidate generator.

Harmonic templates extend to 2000 Hz, with ±43.066 Hz bands. Mean stem energy over native member activity intersected with the frozen episode defines normalized empirical harmonic weights; the preceding equal-length interval supplies background context. A harmonic is operationally observable if its energy exceeds uniform spectral-density expectation. This is a convention, not an instrument/noise-calibrated observability test.

The prospective sufficiency gate requires nonoverlapping bands (f0 > 86.133 Hz) and at least three observable harmonics. At each unchanged FM candidate, 12-frame pre/post energy vectors, harmonic changes, enrichment over broadband expectation, coordinated harmonic-rise fraction, stem-signature cosine, synchronous stem/FM cosine, temporal derivative similarity and harmonic rank similarity are retained. Candidate gates are documented exactly in inference/input/RULE.json: cosine ≥0.8, target enrichment ≥1.5 and coherent fraction ≥0.5. No outcome-based adjustment was made. These are transparent diagnostic conventions, not controlled-validation thresholds.

## Why attribution remains unresolved

Of 117 templates, 59 fail the nonoverlap criterion. The remaining 58 fail the minimum-three-observable-harmonics criterion. None passes both. Some low-pitch templates show three or more elevated bands, but overlapping bands cannot count as independent harmonic evidence under this rule. Higher-pitch templates have sparse empirical harmonic energy under the uniform-density convention.

Therefore all 4532 candidate evaluations are INSUFFICIENT / UNRESOLVED before source-compatibility thresholds can establish attribution. It would be incorrect to infer that the source hypothesis is disproved, that the raw similarities contain no information, or that a different representation would fail. This experiment primarily identifies a limitation of the chosen resolution and sufficiency convention. Thresholds were not relaxed after inspecting outcomes.

## HF044 and HF047

Both preserve target MIDI53 (F3, f0 174.614 Hz). Only the fundamental band exceeds the empirical observability criterion. It accounts for 89.1% of template harmonic energy in HF044 and 97.0% in HF047. High one-band similarity can arise without a coherent multi-harmonic family and cannot reject percussion or another pitched instrument reliably.

The earlier generic cues and the existing FM candidate nearest the old stem selection are compared below solely as diagnostic samples, not selected attack alternatives. Every candidate is preserved in the full table. Coordinates are original recording seconds.

| Episode | FM coordinate | Role | Signature cosine | Synchronous stem/mix cosine | Harmonic coherence | Non-target change fraction |
|---|---:|---|---:|---:|---:|---:|
'''
for r in special:text+=f'| {r["episode_id"]} | {r["candidate_s"]:.6f} | {r["comparison_role"]} | {r["stem_signature_similarity"]:.3f} | {r["synchronous_stem_mix_similarity"]:.3f} | {r["harmonic_coherence"]:.3f} | {r["non_target_change_fraction"]:.3f} |\n'
text+='''
All rows remain UNRESOLVED regardless of raw similarity. Harmonic coherence here is computed over operationally observable bands; with one band it cannot establish multi-harmonic coherence. A nearest-FM diagnostic sample is not a replacement of the historical selection.

## Decisions

- BASIC-PITCH NOTE CONDITIONING REDUCES FULL-MIX TRANSIENT AMBIGUITY: NO under this frozen diagnostic.
- STEM SPECTRAL SIGNATURE ADDS SOURCE-ATTRIBUTION INFORMATION: INSUFFICIENT EVIDENCE; raw differences are available, but no attribution passes the sufficiency gate.
- FULL-MIX BASS TRANSIENT ATTRIBUTION FEASIBLE: PARTIAL as an executable local evidence comparison; successful source resolution has not been demonstrated.
- PROMISING CONTROLLED-CORPUS VALIDATION TARGET: YES as a research target, not a validated mechanism.

There is no historical onset/source Ground Truth. Piano may share the target pitch; drums can excite its bands. Demucs derives from the same mix and is not independent corroboration. No millisecond accuracy, physical correctness, Demucs latency, replacement timestamp or microtiming profile is claimed.

## Proposed next experiment — not executed

On controlled Gallegati recordings and explicitly labelled controlled mixtures, assess the sufficiency of this exact harmonic representation before training any attribution model. Compare harmonic observability against independent audio/annotation evidence across Fishman/DPA/NT5 and mixtures with percussion/pitched competitors. If inadequate, design any multi-resolution extension prospectively on controlled development data, with its temporal/frequency trade-off documented and a held-out evaluation. Do not relax thresholds or redesign the method on Ray Brown.

## Preservation and deliverables

PRE_RESULT_FREEZE.json hashes target identities, templates/signatures, all candidate evidence and classifications before aggregate results. RESULT_FREEZE.json hashes the aggregate outputs. The main CSV contains episode, BP member, target pitch/f0, template, signature, every local candidate, energy/coherence/similarity measures, source classification, episode status and previous selection status. Three PDFs provide 63 episode pages, 34 primary-cohort pages and two enlarged HF044/HF047 pages, with no PLP. Prior sources and freezes are verified unchanged. No canonical changes, commit, push, bootstrap update or external backup. STOP for PI review.
'''
(P/'RESULT.md').write_text(text)
