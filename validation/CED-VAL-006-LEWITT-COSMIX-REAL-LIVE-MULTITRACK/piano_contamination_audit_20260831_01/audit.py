#!/usr/bin/env python3
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly
SR=44100;FRAME=4096;HOP=1024;NFFT=16384;HARM=np.arange(1,9,dtype=float);WIN=np.hanning(FRAME+1)[:-1];FF=np.fft.rfftfreq(NFFT,1/SR)
HERE=Path(__file__).parent
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def load(path):
 rate,x=wavfile.read(path);assert rate==48000;x=x.astype(np.float64);x=x.mean(axis=1) if x.ndim==2 else x;return resample_poly(x/2147483648.,147,160,padtype='constant')
def interp(power,freq):
 x=freq*NFFT/SR;lo=np.floor(x).astype(int);fr=x-lo;ok=(lo>=0)&(lo+1<len(power));o=np.zeros_like(x,float);o[ok]=power[lo[ok]]*(1-fr[ok])+power[lo[ok]+1]*fr[ok];return o
def f0_frame(power,f0):
 hf=f0*HARM;hp=interp(power,hf);noise=np.median(np.stack([interp(power,hf*2**(o/1200)) for o in (-200,-175,-150,-125,-100,100,125,150,175,200)]),axis=0)+1e-30;prom=10*np.log10(hp/noise);sup=int((prom>=6).sum());score=float(np.mean(np.sort(np.log1p(hp/noise))[-4:]));bands=np.zeros_like(FF,bool)
 for h in HARM:
  c=f0*h
  if c<=1600:bands|=(FF>=c*2**(-35/1200))&(FF<=c*2**(35/1200))
 dom=(FF>=40)&(FF<=1600);ratio=float(power[bands&dom].sum()/power[dom].sum());return {'supported_partials':sup,'harmonic_energy_ratio':ratio,'harmonic_score':score,'supported':bool(sup>=3 and ratio>=.12)}
def source_support(audio,cand):
 start=round(cand['timestamp_seconds']*SR);dur=min(cand['duration_seconds'],.3);positions=list(range(start,round((cand['timestamp_seconds']+dur)*SR)-FRAME+1,HOP));per=[]
 for frozen in cand['f0_candidates']:
  frames=[]
  for pos in positions:
   y=audio[pos:pos+FRAME]
   if len(y)!=FRAME:continue
   y=(y-y.mean())*WIN;frames.append(f0_frame(np.abs(np.fft.rfft(y,NFFT))**2+1e-30,frozen['f0_hz']))
  persistent=any(all(q['supported'] for q in frames[i:i+3]) for i in range(max(0,len(frames)-2))) and bool(frames) and sum(q['supported'] for q in frames)/len(frames)>=.5
  per.append({'f0_hz':frozen['f0_hz'],'valid_frames':len(frames),'supported_frame_count':sum(q['supported'] for q in frames),'supported_frame_fraction':sum(q['supported'] for q in frames)/len(frames) if frames else None,'median_harmonic_energy_ratio':float(np.median([q['harmonic_energy_ratio'] for q in frames])) if frames else None,'median_supported_partials':float(np.median([q['supported_partials'] for q in frames])) if frames else None,'median_harmonic_score':float(np.median([q['harmonic_score'] for q in frames])) if frames else None,'persistent_support':persistent})
 valid=all(x['valid_frames']>=3 for x in per);return {'valid':valid,'supported':bool(valid and any(x['persistent_support'] for x in per)),'per_frozen_f0':per}
def wilson(k,n,z=1.959963984540054):
 p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return [c-h,c+h]
def summary(rows):
 classes=['BASS_DOMINANT_SUPPORT','PIANO_DOMINANT_SUPPORT','BOTH_SUPPORTED','NEITHER_SUPPORTED','INDETERMINATE'];counts={k:sum(x['attribution_class']==k for x in rows) for k in classes};n=len(rows);ap=counts['PIANO_DOMINANT_SUPPORT']+counts['BOTH_SUPPORTED'];ab=counts['BASS_DOMINANT_SUPPORT']+counts['BOTH_SUPPORTED'];return {'count':n,'classes':{k:{'count':v,'proportion':v/n,'wilson_95':wilson(v,n)} for k,v in counts.items()},'any_piano_support':{'count':ap,'proportion':ap/n,'wilson_95':wilson(ap,n)},'any_bass_support':{'count':ab,'proportion':ab/n,'wilson_95':wilson(ab,n)}}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();p=json.load(open(HERE/'protocol.json'));q=dict(p);fp=q.pop('protocol_fingerprint');assert hashlib.sha256(canon(q)).hexdigest()==fp
 for authority in (p['candidate_authority'],p['group_authority'],p['provenance'],p['source_authorities']['bass'],p['source_authorities']['piano']):assert sha(authority.get('path',authority.get('manifest_path')))==authority['sha256']
 cs=json.load(open(p['candidate_authority']['path']));assert cs['candidate_count']==593 and cs['candidate_fingerprint']==p['candidate_authority']['candidate_fingerprint'];ev=json.load(open(p['group_authority']['path']));match={m['candidate_id']:m['baseline_status'] for m in ev['matches']};bass=load(p['source_authorities']['bass']['path']);piano=load(p['source_authorities']['piano']['path']);rows=[]
 for c in cs['candidates']:
  b=source_support(bass,c);r=source_support(piano,c)
  if not b['valid'] or not r['valid']:cl='INDETERMINATE'
  elif b['supported'] and r['supported']:cl='BOTH_SUPPORTED'
  elif b['supported']:cl='BASS_DOMINANT_SUPPORT'
  elif r['supported']:cl='PIANO_DOMINANT_SUPPORT'
  else:cl='NEITHER_SUPPORTED'
  group='UNMATCHED' if c['candidate_id'] not in match else ('NEWLY_RECOVERED_MISSED_BASS' if match[c['candidate_id']]=='MISSED_BASS' else 'ALREADY_RECOVERED_BASS')
  rows.append({'candidate_id':c['candidate_id'],'group':group,'timestamp_seconds':c['timestamp_seconds'],'frozen_f0_candidates':c['f0_candidates'],'bass_support':b,'piano_support':r,'attribution_class':cl})
 groups={'ALL_593':summary(rows)}
 for name in ('NEWLY_RECOVERED_MISSED_BASS','UNMATCHED','ALREADY_RECOVERED_BASS'):groups[name]=summary([x for x in rows if x['group']==name])
 g=groups['NEWLY_RECOVERED_MISSED_BASS'];ind=g['classes']['INDETERMINATE']['proportion'];pd=g['classes']['PIANO_DOMINANT_SUPPORT']['proportion'];anyp=g['any_piano_support']['proportion'];anyb=g['any_bass_support']['proportion']
 if ind>.2:cl='INDETERMINATE'
 elif pd<=.1 and anyp<=.25 and anyb>=.5:cl='LOW'
 elif pd>=.3 or anyp>=.6 or anyb<=.2:cl='HIGH'
 else:cl='MATERIAL'
 out={'protocol_id':p['protocol_id'],'protocol_fingerprint':fp,'candidate_stream_sha256':p['candidate_authority']['sha256'],'candidate_fingerprint':cs['candidate_fingerprint'],'source_sha256':{'bass':p['source_authorities']['bass']['sha256'],'piano':p['source_authorities']['piano']['sha256']},'candidate_attribution':rows,'populations':groups,'piano_contamination':'PIANO_CONTAMINATION: '+cl,'bounded_filtering_count_range_new_recovery':[g['classes']['PIANO_DOMINANT_SUPPORT']['count'],g['any_piano_support']['count']],'interpretation_firewall':p['interpretation_firewall']};out['result_fingerprint']=hashlib.sha256(canon(out)).hexdigest();a.output.write_bytes(canon(out)+b'\n');print(out['result_fingerprint'],out['piano_contamination'])
if __name__=='__main__':main()
