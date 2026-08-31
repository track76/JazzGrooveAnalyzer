#!/usr/bin/env python3
import argparse,hashlib,json,math
from pathlib import Path
from pitch_core import canonical,sha,load_pcm,analyze_event
HERE=Path(__file__).parent
def wilson(k,n,z=1.959963984540054):
    if not n:return None
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return [c-h,c+h]
def stats(rows):
    ev=[x for x in rows if x['reference']['evaluable']]; comp=[x for x in ev if x['evaluation']['compatible']]; n=len(rows); k=len(comp)
    errors=[x['evaluation']['minimum_pitch_error_cents'] for x in comp]
    return {'population':n,'mix_status_counts':{s:sum(x['mix_analysis']['status']==s for x in rows) for s in ('PITCHED_EVIDENCE_PRESENT','PITCHED_EVIDENCE_ABSENT','INDETERMINATE')},'bassdi_evaluable':len(ev),'bassdi_evaluable_proportion':len(ev)/n if n else None,'compatible':k,'compatible_proportion_among_evaluable':k/len(ev) if ev else None,'wilson_95':wilson(k,len(ev)),'compatible_error_cents':({'median':float(__import__('numpy').median(errors)),'q1':float(__import__('numpy').quantile(errors,.25)),'q3':float(__import__('numpy').quantile(errors,.75)),'rmse':math.sqrt(sum(e*e for e in errors)/len(errors))} if errors else None)}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--candidates',type=Path,required=True); ap.add_argument('--candidate-sha',required=True); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args(); assert sha(a.candidates)==a.candidate_sha
    p=json.loads((HERE/'protocol.json').read_text()); assert sha(p['authorities']['bassdi_evaluation_only']['path'])==p['authorities']['bassdi_evaluation_only']['sha256']; cand=json.loads(a.candidates.read_text()); audio=load_pcm(p['authorities']['bassdi_evaluation_only']['path']); outrows=[]
    for x in cand['events']:
        ref=analyze_event(audio,x['time_seconds']); evaluable=ref['status']=='PITCHED_EVIDENCE_PRESENT'; errs=[]
        if evaluable and x['mix_analysis']['status']=='PITCHED_EVIDENCE_PRESENT':
            for m in x['mix_analysis']['candidates']:
                for r in ref['candidates']: errs.append(abs(1200*math.log2(m['f0_hz']/r['f0_hz'])))
        err=min(errs) if errs else None; outrows.append({**x,'reference':{'evaluable':evaluable,'limitation':p['independent_bassdi_evaluation']['limitation'],'analysis':ref},'evaluation':{'compatible':bool(err is not None and err<=50),'minimum_pitch_error_cents':err}})
    groups={};
    for preservation in ('RECOVERED_BASS','MISSED_BASS'):
        z=[x for x in outrows if x['preservation']==preservation]; groups[preservation]=stats(z)
        for kick in ('WITH_KICK','WITHOUT_KICK'): groups[preservation+'_'+kick]=stats([x for x in z if x['kick_status']==kick])
    m=groups['MISSED_BASS']; invariants=(m['bassdi_evaluable_proportion']>=.8); prop=m['compatible_proportion_among_evaluable']; low=m['wilson_95'][0] if m['wilson_95'] else -1
    if not invariants: cls='INDETERMINATE'
    elif prop>=.5 and low>=.4: cls='STRONG'
    elif prop>=.2 and low>=.1: cls='PARTIAL'
    else: cls='INSUFFICIENT'
    result={'protocol_id':p['protocol_id'],'protocol_fingerprint':p['protocol_fingerprint'],'candidate_file_sha256':a.candidate_sha,'candidate_fingerprint':cand['candidate_fingerprint'],'bassdi_sha256':sha(p['authorities']['bassdi_evaluation_only']['path']),'events':outrows,'summary':groups,'classification':'MIXED_AUDIO_PITCHED_BASS_EVIDENCE: '+cls,'firewall':p['interpretation_firewall']}; result['result_fingerprint']=hashlib.sha256(canonical(result)).hexdigest(); a.output.write_bytes(canonical(result)+b'\n'); print(result['result_fingerprint'],result['classification'])
if __name__=='__main__':main()
