#!/usr/bin/env python3
import argparse, hashlib, importlib.util, json
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).parent
ORIG=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer/validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/run_20260824_112305/scientific_content.json')
SCORER=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer/validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/separation_robustness_20260825_01/score.py')
PROTO=HERE/'protocol.json'; SCOPE=Fraction(10068072,44100)
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def load_scorer():
 s=importlib.util.spec_from_file_location('frozen_scorer',SCORER);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.SCOPE_END=SCOPE;return m
def events(report,label):
 out=[]
 for i,x in enumerate(report['elementary_metric_events'][label]):
  coord=x['producer_sample_coordinate'];out.append({'eme_id':x['eme_id'],'native_index':x.get('producer_frame',i),'time':Fraction(coord,44100)})
 return sorted(out,key=lambda x:(x['time'],x['native_index'],x['eme_id']))
def ad_preservation(original,candidate,bass_assignment,drum_assignment):
 bm={x['separated_eme_id']:x['original_eme_id'] for x in bass_assignment['matches']};dm={x['separated_eme_id']:x['original_eme_id'] for x in drum_assignment['matches']}
 ol={x['target_eme_id']:x for x in original['drum_relative_localizations']}; counts={'scorable_target_and_nearest':0,'nearest_preserved':0,'preceding_preserved':0,'following_preserved':0}
 for x in candidate['drum_relative_localizations']:
  ot=bm.get(x['target_eme_id']);nr=x['nearest_drum_reference']; mapped=dm.get(nr['eme_id']) if nr else None
  if ot in ol and mapped is not None:
   counts['scorable_target_and_nearest']+=1;o=ol[ot]
   if o['nearest_drum_reference'] and mapped==o['nearest_drum_reference']['eme_id']:counts['nearest_preserved']+=1
   pr=x['preceding_drum_reference'];fr=x['following_drum_reference']
   if pr and o['preceding_drum_reference'] and dm.get(pr['eme_id'])==o['preceding_drum_reference']['eme_id']:counts['preceding_preserved']+=1
   if fr and o['following_drum_reference'] and dm.get(fr['eme_id'])==o['following_drum_reference']['eme_id']:counts['following_preserved']+=1
 return counts
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();proto=json.loads(PROTO.read_text());pc=dict(proto);pf=pc.pop('protocol_fingerprint');assert hashlib.sha256(canonical(pc)).hexdigest()==pf
 orig=json.loads(ORIG.read_text());sc=load_scorer();runs={}
 for n in (1,2):
  p=HERE/f'jga_run_{n}.json';r=json.loads(p.read_text());levels={};assignments={}
  for label in ('Double Bass','Drums'):
   o=events(orig,label);c=events(r,label);ass=sc.assign(o,c);assignments[label]=ass;levels[label]={'level_1':sc.level1(o,c,SCOPE),'level_2':ass}
  bass=assignments['Double Bass'];drum=assignments['Drums'];br=bass['descriptive_recall'];bf=bass['descriptive_f1']
  levels['descriptive_cross_material']={'DELTA_BASS_RECALL':br-0.5867298578199052,'RELATIVE_BASS_RECALL_CHANGE_PERCENT':(br/0.5867298578199052-1)*100,'DELTA_BASS_F1':bf-0.7278071722516166,'RELATIVE_BASS_F1_CHANGE_PERCENT':(bf/0.7278071722516166-1)*100}
  levels['ad038_preservation']=ad_preservation(orig,r,bass,drum)
  levels['ad038_candidate_summary']={k:r['geometry_summary'][k] for k in ('eligible_count','localized_count','unresolved_count','nearest_tie_count','nearest_selection_status_counts','relationship_status_counts','signed_displacement_descriptive','absolute_displacement_descriptive')}
  levels['ad040_candidate_profile']=r['rhythm_section_timing_profile'];levels['jga_report_sha256']=sha(p);runs[f'run_{n}']=levels
 r1=runs['run_1'];r2=runs['run_2'];b1=r1['Double Bass']['level_2'];b2=r2['Double Bass']['level_2'];d1=r1['Drums']['level_2'];d2=r2['Drums']['level_2']
 if abs(b1['descriptive_recall']-b2['descriptive_recall'])>.02 or abs(b1['descriptive_f1']-b2['descriptive_f1'])>.02:outcome='INDETERMINATE_CROSS_RUN_VARIABILITY'
 elif all(x['descriptive_recall']>=.5367298578199052 and x['descriptive_f1']>=.6778071722516166 for x in (b1,b2)) and all(x['descriptive_recall']>=.90 for x in (d1,d2)):outcome='PRESERVATION_REPLICATED_WITHIN_MARGIN'
 elif all(x['descriptive_recall']<.5367298578199052 and x['descriptive_f1']<.6778071722516166 for x in (b1,b2)):outcome='LOWER_BASS_PRESERVATION'
 else:outcome='MIXED_REPLICATION'
 result={'protocol_id':proto['protocol_id'],'protocol_fingerprint':pf,'input_mix_sha256':'7d9d3f1f07f7760152ce560ae0bbb6f1706b443278a41af4a31dfb2638396a0f','original_authority':{'BassDI_EME':1138,'Overheads_Drum_EME':907,'scientific_fingerprint':'074d84768f508e6ceee9c9225c34e9ea881ce50d88e0d5f930525b92e87bd9d6'},'runs':runs,'outcome':outcome,'interpretation_firewall':proto['interpretation_firewall']}
 result['result_fingerprint']=hashlib.sha256(canonical(result)).hexdigest();a.output.write_bytes(canonical(result)+b'\n');print(result['result_fingerprint'])
if __name__=='__main__':main()
