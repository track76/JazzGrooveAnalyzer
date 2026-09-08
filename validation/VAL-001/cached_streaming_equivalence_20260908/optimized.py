"""Conservative caching; no fixture constants or expected responses."""
from fractions import Fraction as Q
from flint import arb,acb
class Optimized:
    def __init__(self,namespace,reference):
        self.namespace=namespace;self.ref=reference
        self.parsed={};self.exp={};self.hann={};self.amp={}
        self.counts=dict(exponentials=0,hann=0,amplitudes=0,accumulations=0)
    def evaluate(self,pid,measure,query):
        u,f,L=map(Q,(query['u'],query['f'],query['L']));pi=arb.pi();z=acb(0);used=[]
        a=lambda x:arb(str(x))
        for event in sorted(measure,key=lambda e:(Q(e['t']),e['id'])):
            pk=(self.namespace,pid,event['id'],event['t'],event['s'])
            if pk not in self.parsed:self.parsed[pk]=(Q(event['t']),Q(event['s']))
            t,s=self.parsed[pk]
            if abs(t-u)>L/2:continue
            wk=(self.namespace,pid,u,L,event['id'],t)
            if wk not in self.hann:
                self.hann[wk]=(1+(2*pi*a((t-u)/L)).cos())/2;self.counts['hann']+=1
            ak=wk+(s,)
            if ak not in self.amp:self.amp[ak]=a(s)*self.hann[wk];self.counts['amplitudes']+=1
            ek=(self.namespace,pid,event['id'],t,f)
            if ek not in self.exp:self.exp[ek]=acb(0,-2*pi*a(f*t)).exp();self.counts['exponentials']+=1
            z+=self.amp[ak]*self.exp[ek];self.counts['accumulations']+=1;used.append(event['id'])
        real,imag=self.ref.ball(z.real),self.ref.ball(z.imag)
        x,y=self.ref.bounds(real),self.ref.bounds(imag)
        zero=x[0]<=0<=x[1] and y[0]<=0<=y[1];branch=x[0]<0 and y[0]<=0<=y[1]
        if zero:status='UNRESOLVED_ZERO_CONTAINMENT';phase=None
        elif branch:status='BRANCH_CUT_ENCLOSURE';phase={'full_circle':True,'lower':self.ref.dy(-pi.upper()),'upper':self.ref.dy(pi.upper())}
        else:status='RESOLVED_INTERVAL';phase=self.ref.ball(z.arg())
        return {'real':real,'imag':imag,'magnitude':[self.ref.dy(z.abs_lower()),self.ref.dy(z.abs_upper())],'phase_status':status,'phase':phase,'contributing_ids':used}
