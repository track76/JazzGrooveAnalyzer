#!/usr/bin/env python3
import argparse,json,platform,sys
from fractions import Fraction
from pathlib import Path
from pitch_core import canonical,sha,load_pcm,analyze_event
HERE=Path(__file__).parent
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args()
    p=json.loads((HERE/'protocol.json').read_text()); q=dict(p); fp=q.pop('protocol_fingerprint'); assert sha_bytes(canonical(q))==fp
    for x in p['authorities'].values():
        if 'path' in x and 'bassdi' not in str(x['path']).lower(): assert sha(x['path'])==x['sha256']
    k_auth=p['authorities']['frozen_kick_subdivision']; assert sha(k_auth['kick_events_path'])==k_auth['kick_events_sha256']
    score=json.load(open(p['authorities']['frozen_correspondence']['path']))['runs']['run_1']['Double Bass']['level_2']
    kick=json.load(open('/private/tmp/cedval-kick-bass-preservation-20260831-01/ced005_kick_run_1.json'))
    kt=[Fraction(x['producer_sample_coordinate'],44100) for x in kick['events']]
    rows=[]
    for rec,key in ((True,'matches'),(False,'original_only')):
        for x in score[key]:
            t=Fraction(x['original_time']['numerator'],x['original_time']['denominator'])
            rows.append((t,x['original_eme_id'],rec,min(abs(t-k) for k in kt)<=Fraction(3,100)))
    rows.sort()
    audio=load_pcm(p['authorities']['controlled_mix']['path']); events=[]
    for i,(t,ident,rec,wk) in enumerate(rows):
        events.append({'index':i,'original_eme_id':ident,'time_seconds':float(t),'time_fraction':[t.numerator,t.denominator],'preservation':'RECOVERED_BASS' if rec else 'MISSED_BASS','kick_status':'WITH_KICK' if wk else 'WITHOUT_KICK','mix_analysis':analyze_event(audio,float(t))})
    out={'protocol_id':p['protocol_id'],'protocol_fingerprint':fp,'stage':'MIX_ONLY_CANDIDATES_LOCKABLE','bassdi_read':False,'controlled_mix_sha256':sha(p['authorities']['controlled_mix']['path']),'events':events}
    out['candidate_fingerprint']=sha_bytes(canonical(out)); a.output.write_bytes(canonical(out)+b'\n'); print(out['candidate_fingerprint'])
def sha_bytes(b):
    import hashlib; return hashlib.sha256(b).hexdigest()
if __name__=='__main__': main()
