"""Generic operator only: no fixtures, oracle or case dispatch."""
from fractions import Fraction as Q
from flint import arb, acb

def dy(v):
    m,e=map(int,v.man_exp())
    if not m:return ['0','0']
    while m%2==0:m//=2;e+=1
    return [str(m),str(e)]
def ball(v):return {'mid':dy(v.mid()),'rad':dy(v.rad())}
def rat(v):return Q(int(v[0]))*Q(2)**int(v[1])
def bounds(b):
    m,r=rat(b['mid']),rat(b['rad']);return m-r,m+r

def evaluate(measure,query):
    u,f,L=map(Q,(query['u'],query['f'],query['L']))
    a=lambda q:arb(str(q))
    z=acb(0); pi=arb.pi(); used=[]
    for event in sorted(measure,key=lambda e:(Q(e['t']),e['id'])):
        t,s=Q(event['t']),Q(event['s'])
        if abs(t-u)<=L/2:
            w=(1+(2*pi*a((t-u)/L)).cos())/2
            z+=a(s)*w*acb(0,-2*pi*a(f*t)).exp()
            used.append(event['id'])
    real,imag=ball(z.real),ball(z.imag)
    x,y=bounds(real),bounds(imag)
    zero=x[0]<=0<=x[1] and y[0]<=0<=y[1]
    branch=x[0]<0 and y[0]<=0<=y[1]
    phase=None
    if zero:status='UNRESOLVED_ZERO_CONTAINMENT'
    elif branch:
        status='BRANCH_CUT_ENCLOSURE'
        phase={'full_circle':True,'lower':dy(-pi.upper()),'upper':dy(pi.upper())}
    else:
        status='RESOLVED_INTERVAL';phase=ball(z.arg())
    return {'real':real,'imag':imag,'magnitude':[dy(z.abs_lower()),dy(z.abs_upper())],
            'phase_status':status,'phase':phase,'contributing_ids':used}
