#!/usr/bin/env python3
import argparse,hashlib,importlib.util,json
from pathlib import Path

AUTH=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer/validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/run_20260824_112305/execute.py')
SCOPE=7422225
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path,required=True);parser.add_argument('--authority-sha',required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 spec=importlib.util.spec_from_file_location('frozen_observer',AUTH);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 analysis=module.AnalysisPipeline().analyze(str(args.input));events=[]
 for event in analysis.elementary_metric_events:
  record=module.eme_record(event)
  if record['producer_sample_coordinate']<SCOPE:events.append(record)
 result={'protocol_id':'H-CEDVAL010-EVENT-BLIND-UPPER-PARTIAL-HARMONIC-STRUCTURE-REPLICATION-01','scope_samples':SCOPE,'source_authority_sha256':args.authority_sha,'analyzed_file_sha256':sha(args.input),'observer_authority_sha256':sha(AUTH),'elementary_metric_events':sorted(events,key=lambda item:(item['producer_frame'],item['eme_id']))}
 payload=(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode();args.output.write_bytes(payload);print(json.dumps({'events':len(events),'sha256':hashlib.sha256(payload).hexdigest()}))
if __name__=='__main__':main()
