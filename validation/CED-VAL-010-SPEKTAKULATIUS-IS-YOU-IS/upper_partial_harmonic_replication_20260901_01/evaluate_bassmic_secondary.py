#!/usr/bin/env python3
import hashlib,importlib.util,json
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).parent;SR=44100;N=7422225
SCORER=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer/validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/separation_robustness_20260825_01/score.py')
def canonical(value):return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()
def events(payload):
 return sorted([{'eme_id':event['eme_id'],'native_index':event.get('producer_frame',index),'time':Fraction(event['producer_sample_coordinate'],SR)} for index,event in enumerate(payload['elementary_metric_events'])],key=lambda item:(item['time'],item['native_index'],item['eme_id']))
original=json.loads((HERE/'original_bass_observations.json').read_text());bassmic=json.loads((HERE/'bassmic_secondary_observations.json').read_text())
spec=importlib.util.spec_from_file_location('frozen_scorer',SCORER);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.SCOPE_END=Fraction(N,SR);assignment=module.assign(events(original),events(bassmic))
result={'role':'SECONDARY_NON_DECISIONAL','primary_classification_unchanged':'INDEPENDENT_HARMONIC_STRUCTURE_REPLICATION_SUPPORTED','BassDI_count':len(events(original)),'BassMic_count':len(events(bassmic)),'BassDI_vs_BassMic':assignment,'cannot_rescue_or_modify_primary':True};result['fingerprint']=hashlib.sha256(canonical(result)).hexdigest();(HERE/'bassmic_secondary.json').write_bytes(canonical(result));print(json.dumps({'fingerprint':result['fingerprint'],'matched':assignment['matched_count']}))
