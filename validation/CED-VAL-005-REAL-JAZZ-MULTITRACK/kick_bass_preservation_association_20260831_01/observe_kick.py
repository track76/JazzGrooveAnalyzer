#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--asset-sha',required=True);p.add_argument('--sample-rate',type=int,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();assert sha(a.input)==a.asset_sha
 c=AnalysisPipeline().analyze(str(a.input));rows=[]
 for e in c.elementary_metric_events:
  coord=round(e.timestamp*a.sample_rate/512)*512;rows.append({'eme_id':str(e.id),'producer_sample_coordinate':coord,'timestamp_seconds':e.timestamp,'timestamp_hex':e.timestamp.hex()})
 rows.sort(key=lambda x:(x['producer_sample_coordinate'],x['eme_id']));r={'asset':str(a.input),'asset_sha256':a.asset_sha,'sample_rate_hz':a.sample_rate,'hop_samples':512,'eme_count':len(rows),'events':rows};b=json.dumps(r,sort_keys=True,separators=(',',':')).encode();a.output.write_bytes(b+b'\n');print(hashlib.sha256(b).hexdigest(),len(rows))
if __name__=='__main__':main()
