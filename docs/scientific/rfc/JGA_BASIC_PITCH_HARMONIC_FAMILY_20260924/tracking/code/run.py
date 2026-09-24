from pathlib import Path
import csv,json,hashlib,datetime,math
import numpy as np,soundfile as sf
B=Path(__file__).resolve().parents[1];I=B/'input';O=B/'output';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(O/n).write_text(json.dumps(x,indent=2)+'\n')
assert json.loads((O/'ISOLATION_PROBE.json').read_text())['passed']
raw=list(csv.DictReader((I/'notes.csv').open()));assert len(raw)==98
notes=[dict(n,onset=float(n['onset_s']),offset=float(n['offset_s']),pitch=int(n['midi_pitch']),amp=float(n['amplitude']),frequency_hz=440*2**((int(n['midi_pitch'])-69)/12)) for n in raw];notes.sort(key=lambda n:(n['onset'],n['note_id']));lookup={n['note_id']:n for n in notes};T=512/22050
# Naive lowest-active-note baseline, independently of family tracking.
boundaries=sorted({n[k] for n in notes for k in ['onset','offset']});naive=[]
for start,end in zip(boundaries,boundaries[1:]):
 active=[n for n in notes if n['onset']<=start<n['offset']]
 if not active:continue
 pitch=min(n['pitch'] for n in active);ids=[n['note_id'] for n in active if n['pitch']==pitch]
 if naive and naive[-1]['pitch']==pitch and naive[-1]['end_s']==start:naive[-1]['end_s']=end;naive[-1]['note_ids']=sorted(set(naive[-1]['note_ids']+ids))
 else:naive.append(dict(start_s=start,end_s=end,pitch=pitch,note_ids=ids))
for j,e in enumerate(naive):e['episode_id']=f'LOW{j+1:03}'
def harmonic(root,note):
 ratio=note/root;k=int(round(ratio));cents=1200*math.log2(ratio/k) if k>0 else None
 return (k,cents) if 2<=k<=8 and abs(cents)<=50 else None
groups=[]
for n in notes:
 if groups and n['onset']-groups[-1][0]['onset']<=T+1e-9 and n['onset']<min(a['offset'] for a in groups[-1]):groups[-1].append(n)
 else:groups.append([n])
families=[];members=[]
for gi,g in enumerate(groups):
 def rootscore(n):return n['amp']+sum(m['amp']/h[0] for m in g if m['note_id']!=n['note_id'] and (h:=harmonic(n['frequency_hz'],m['frequency_hz'])))
 for n in sorted(g,key=lambda n:(-rootscore(n),-n['amp'],n['onset'],n['note_id'])):
  current=max(families,key=lambda e:e['root_onset_s']) if families else None
  if current and n['pitch']==current['fundamental_midi'] and n['onset']<=max(lookup[i]['offset'] for i in current['root_note_ids'])+T and n['onset']>=current['root_onset_s']-T:
   current['root_note_ids'].append(n['note_id']);current['member_ids'].append(n['note_id']);current['flags'].append('FRAGMENT_OR_REARTICULATION');members.append(dict(note_id=n['note_id'],role='POSSIBLE_ROOT_FRAGMENT',family_id=current['id'],possible_family_ids=[current['id']],harmonic_number=1,cents_error=0.,reason='same-MIDI current-family continuation within two output frames',root_score=rootscore(n)));continue
  compatible=[]
  for e in families:
   h=harmonic(e['fundamental_hz'],n['frequency_hz'])
   active=any(lookup[i]['onset']<=n['onset']<lookup[i]['offset'] for i in e['member_ids']) or e['opening_group']==gi
   if h and active:compatible.append((e,h))
  if len(compatible)==1:
   e,h=compatible[0];e['member_ids'].append(n['note_id']);e['harmonic_ids'].append(n['note_id']);e['flags'].append('HARMONIC_VS_NEW_HIGHER_FUNDAMENTAL');members.append(dict(note_id=n['note_id'],role='HARMONIC_HYPOTHESIS',family_id=e['id'],possible_family_ids=[e['id']],harmonic_number=h[0],cents_error=h[1],reason='frequency-compatible active family; separate higher note remains alternative',root_score=rootscore(n)))
  elif len(compatible)>1:
   for e,h in compatible:e['flags'].append('MULTIPLE_FAMILY_OWNERSHIP');e['possible_member_ids'].append(n['note_id'])
   members.append(dict(note_id=n['note_id'],role='UNRESOLVED_FAMILY_OR_NEW_ROOT',family_id=None,possible_family_ids=[e['id'] for e,h in compatible],harmonic_number=None,cents_error=None,reason='multiple compatible active families; independent fundamental also possible',root_score=rootscore(n)))
  else:
   eid=f'T{len(families)+1}';e=dict(id=eid,root_onset_s=n['onset'],fundamental_midi=n['pitch'],fundamental_hz=n['frequency_hz'],root_note_ids=[n['note_id']],member_ids=[n['note_id']],harmonic_ids=[],possible_member_ids=[],opening_group=gi,opening_reason='new observed pitch incompatible with active harmonic families' if families else 'first observed root proposal',flags=[]);families.append(e);members.append(dict(note_id=n['note_id'],role='ROOT_HYPOTHESIS',family_id=eid,possible_family_ids=[eid],harmonic_number=1,cents_error=0.,reason=e['opening_reason'],root_score=rootscore(n)))
x,sr=sf.read(I/'bass.wav',always_2d=True);x=x.mean(axis=1)
for e in families:
 e['start_s']=min(lookup[i]['onset'] for i in e['member_ids']);e['end_s']=max(lookup[i]['offset'] for i in e['member_ids']);e['fundamental_support_end_s']=max(lookup[i]['offset'] for i in e['root_note_ids'])
families.sort(key=lambda e:(e['start_s'],e['root_onset_s'],e['id']));mapping={e['id']:f'HF{i+1:03}' for i,e in enumerate(families)}
for e in families:e['episode_id']=mapping[e.pop('id')]
for m in members:
 m['family_id']=mapping[m['family_id']] if m['family_id'] else None;m['possible_family_ids']=[mapping[k] for k in m['possible_family_ids']];m['native_hypothesis']=lookup[m['note_id']]
byid={e['episode_id']:e for e in families};mem={m['note_id']:m for m in members};lingering=[]
for i,e in enumerate(families):
 e['inherited_previous_family_hypotheses']=[]
 for m in members:
  if m['role']!='HARMONIC_HYPOTHESIS' or m['family_id']==e['episode_id']:continue
  n=lookup[m['note_id']];parent=byid[m['family_id']]
  if parent['root_onset_s']<e['root_onset_s'] and n['onset']<=e['root_onset_s']<n['offset']:
   e['inherited_previous_family_hypotheses'].append(n['note_id']);lingering.append(dict(note_id=n['note_id'],parent_family=m['family_id'],new_family=e['episode_id'],transition_s=e['root_onset_s'],new_root_below_harmonic=e['fundamental_hz']<n['frequency_hz']))
 e['overlapping_root_episodes']=[a['episode_id'] for a in families if a['episode_id']!=e['episode_id'] and max(a['root_onset_s'],e['root_onset_s'])<min(a['fundamental_support_end_s'],e['fundamental_support_end_s'])]
 if e['overlapping_root_episodes']:e['flags'].append('OVERLAPPING_FUNDAMENTAL_HYPOTHESES')
 e['flags']=sorted(set(e['flags']));e['ambiguity']=bool(e['flags']);e['next_root_onset_s']=min((a['root_onset_s'] for a in families if a['root_onset_s']>e['root_onset_s']),default=None);e['display_current_end_s']=min(e['fundamental_support_end_s'],e['next_root_onset_s']) if e['next_root_onset_s'] is not None else e['fundamental_support_end_s'];a=max(0,int((e['start_s']-45)*sr));b=min(len(x),int((e['end_s']-45)*sr));e['bass_rms_context']=float(np.sqrt(np.mean(x[a:b]**2)));e['provenance']='saved official BP0.4.0 native hypotheses; exploratory frequency-family interpretation; not timing authority'
assert len(members)==98 and len({m['note_id'] for m in members})==98
members.sort(key=lambda m:(m['native_hypothesis']['onset'],m['note_id']))
summary={'raw_hypotheses':98,'naive_episodes':len(naive),'harmonic_family_episodes':len(families),'lingering_harmonic_hypotheses':len({r['note_id'] for r in lingering}),'lingering_transition_pairs':len(lingering),'new_roots_under_lingering_harmonics':len({r['new_family'] for r in lingering if r['new_root_below_harmonic']}),'fragments_collapsed':sum(m['role']=='POSSIBLE_ROOT_FRAGMENT' for m in members),'harmonic_hypotheses':sum(m['role']=='HARMONIC_HYPOTHESIS' for m in members),'unresolved_hypothesis_ownership':sum(m['role']=='UNRESOLVED_FAMILY_OR_NEW_ROOT' for m in members),'ambiguous_episodes':sum(e['ambiguity'] for e in families),'late_starting_harmonics':sum(m['role']=='HARMONIC_HYPOTHESIS' and m['native_hypothesis']['onset']>byid[m['family_id']]['root_onset_s'] for m in members)}
save('FUNDAMENTAL_EPISODES.json',families);save('HYPOTHESIS_MEMBERSHIP.json',members);save('LINGERING_CASES.json',lingering);save('NAIVE_LOWEST_EPISODES.json',naive);save('SUMMARY.json',summary)
save('EPISODE_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{p.name:sha(p) for p in O.iterdir() if p.is_file()},'input_hashes':{p.name:sha(p) for p in I.iterdir()},'implementation_sha256':sha(Path(__file__))});print(json.dumps(summary,indent=2))
