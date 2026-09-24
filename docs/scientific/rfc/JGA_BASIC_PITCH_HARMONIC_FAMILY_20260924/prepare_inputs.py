from pathlib import Path
import json,hashlib,shutil,datetime
R=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer');P=R/'docs/scientific/rfc/JGA_CROSS_REPRESENTATION_TRANSIENT_ATTRIBUTION_20260924';O=R/'docs/scientific/rfc/JGA_BASIC_PITCH_HARMONIC_FAMILY_20260924'
assert not O.exists()
for d in ['tracking/input','tracking/code','tracking/output','crosscheck/input','crosscheck/code','crosscheck/output','figures']:(O/d).mkdir(parents=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['notes.csv','bass.wav','alignment.json']:shutil.copyfile(P/'blind/input'/n,O/'tracking/input'/n)
shutil.copyfile(P/'blind/input/bass_native.json',O/'crosscheck/input/bass_native.json')
protocol='''# PROCESS-BLINDED RESTART AFTER INVESTIGATOR PLP EXPOSURE

Exploratory fundamental/harmonic-family identity tracking only, not onset timing validation. Investigator previously saw historical reference results; computation excludes every PLP-bearing artifact. No temporal ruler is opened, even in evaluation. Inherited target98-hypothesis cohort membership is a scope limitation, not a new independent regional selection. Native transcription is reused unchanged, no model execution.

## Prospective rules

A. Raw baseline: preserve all98 native hypotheses, onset/offset/MIDI/amplitude/pitch_bends. Frequency=440*2^((MIDI-69)/12). Activation/amplitude is not calibrated source probability. Pitch bends retained without unverified conversion.
B. Naive baseline: sweep every onset/offset boundary, choose lowest MIDI among active notes, merge adjacent intervals of identical selected MIDI. Gaps remain. This baseline may expose old held pitches after newer notes end; record contributing IDs.
C. Tracker: operate chronologically on native onset groups, using the prior two-frame maximum-span grouping (512/22050s and positive overlap). No note suppression or expected count.
- Plausible roots are observed native pitches only, no invented subharmonic pitches and no hard register exclusion. Upper roots remain ambiguous hypotheses, not proof of low Bass F0.
- Harmonic compatibility: nearest integer frequency ratio k in2..8, |1200log2(f_note/(k*f_root))|<=50 cents. This tolerance accommodates semitone quantization, not a validated acoustic classifier. Fundamental equality is same native MIDI; no near-semitone merging.
- Within one near-onset group, process root proposals in descending score: own amplitude plus sum(amplitude/k) for other compatible harmonic hypotheses in that group; tie by amplitude, onset, ID. This does not automatically choose the lowest note. The score is an uncalibrated prospective heuristic, not fitted.
- For a new note, first allow same-MIDI continuation of the current-most-recent root episode if onset<=last root-hypothesis offset+512/22050s. Merge as possible fragmentation, preserve original pieces/gaps and flag fragment-versus-rearticulation uncertainty. Root onset/offset never moved.
- Otherwise, an older family can support a harmonic assignment only while its own root or an already assigned family member is active at this note's exact native onset (or started in this same co-onset group). Test frequency ratios against family root.
- One compatible family: assign as harmonic hypothesis, retaining octave-new-fundamental alternative as ambiguity. Multiple compatible families: retain every possible parent, do not force ownership; do not emit a confirmed new root. Store unresolved membership and a possible independent-fundamental alternative.
- No compatible family: open a new plausible root episode. A lingering incompatible family never blocks it. Existing roots/members retain all native offsets; no truncation of audio hypotheses. Overlapping different roots are flagged rather than forced monophonic. Later lower notes do not retroactively reassign earlier higher roots.
- After processing, activity bounds span the root and unambiguously assigned members. Fundamental support end spans only root/fragments. Display 'current-root line' ends at next episode start or root-support end, whichever first, while native root/member tails remain separately visible. This is an identity display convention, not an attack or physical duration estimate.
- Counts: lingering harmonic=assigned k>=2 hypothesis active across any later distinct episode start; count unique note IDs and transition pairs separately. New roots under lingering harmonics=count episodes opening below at least one active inherited higher-frequency harmonic. Fragment collapse=count native root-fragment hypotheses merged, not deleted.
- Root/amplitude scoring, family tests and episode boundaries cannot read native detector events. Bass audio RMS inside each activity interval is recorded as context only; it does not alter assignments.

Freeze chronological episode table, complete memberships/alternatives and naive baseline before diagnostic native Bass-event crosscheck. Crosscheck in a second isolated process: existing Bass events inside activity interval; nearest native event minus episode start, without window-based acceptance or boundary modification. These source-native events are not independent Ground Truth. No reference-grid comparison permitted.

No optimization, timing correction, canonical changes, Report001 changes, commit or push. No claim that reconstructed episode starts are precise attacks. Demucs is not independent source truth; harmonic compatibility cannot prove ownership or distinguish a new octave note. Final musical coherence requires PI listening/score review. Freeze only experimental fundamental/episode artifacts.
'''
(O/'PROTOCOL.md').write_text(protocol)
for phase in ['tracking','crosscheck']:
 (O/f'{phase}.sb').write_text((P/'blind.sb').read_text().replace(str(P/'blind'),str(O/phase)))
 (O/phase/'code/probe.py').write_text((P/'blind/code/probe.py').read_text().replace(str(P/'blind/output'),str(O/phase/'output')))
# Add a specific denial probe: tracker may not access even its later native-event crosscheck input.
p=O/'tracking/code/probe.py';s=p.read_text();s+='\ntry:\n open('+repr(str(O/'crosscheck/input/bass_native.json'))+", 'rb').read(1)\n raise RuntimeError('Crosscheck input unexpectedly readable')\nexcept PermissionError: print('Native detector evidence also blocked during tracking')\n";p.write_text(s)
(O/'INPUT_AUDIT.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'protocol_sha256':sha(O/'PROTOCOL.md'),'files':{str(p.relative_to(O)):sha(p) for phase in ['tracking','crosscheck'] for p in (O/phase/'input').iterdir()},'source_audit':str(P/'ALIGNMENT_AUDIT.json'),'source_audit_sha256':sha(P/'ALIGNMENT_AUDIT.json'),'tracking_schema':['note_id','onset_s','offset_s','midi_pitch','amplitude','pitch_bends'],'no_native_detector_input_to_tracking':True},indent=2))
print(O)
