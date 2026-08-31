#!/usr/bin/env python3
import argparse, hashlib, importlib.util, json
from pathlib import Path
AUTH=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer/validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/run_20260824_112305/execute.py')
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--bass',type=Path,required=True);p.add_argument('--drums',type=Path,required=True);p.add_argument('--execution',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 spec=importlib.util.spec_from_file_location('frozen_ced005_observer',AUTH);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 m.EXECUTION_ID=a.execution;m.STUDY_ID='H-CEDVAL005-CONTROLLED-MIX-HTDEMUCSFT-JGA-PRESERVATION-01';m.INPUT_FP='08ac45969fc449503f67ea4e8bda77495c4807e9dd0e0adbe0c37c9cb506b876'
 m.SOURCES=(("Drums","TEMPORAL_REFERENCE",a.drums.name,sha(a.drums),2),("Double Bass","ACCOMPANIMENT",a.bass.name,sha(a.bass),2))
 result=m.execute_once({'Drums':a.drums,'Double Bass':a.bass}); result['execution_id']=a.execution; result['input_sha256']={'Double Bass':sha(a.bass),'Drums':sha(a.drums)}; result['observer_authority_sha256']=sha(AUTH)
 a.output.write_bytes(m.canonical(result)+b'\n'); print(hashlib.sha256(m.canonical(result)).hexdigest())
if __name__=='__main__':main()
