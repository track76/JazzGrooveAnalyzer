"""Independent Fraction interval closed-form oracle; no flint/evaluator import."""
import json,sys,hashlib
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
canon=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def pt(x):return (Q(x),Q(x))
def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):
    v=[x*y for x in a for y in b];return min(v),max(v)
def scale(a,b):return mul(a,pt(b))
def atan(x,N):
    s=sum(((-1)**k*x**(2*k+1)/Q(2*k+1) for k in range(N)),Q(0))
    t=s+(-1)**N*x**(2*N+1)/Q(2*N+1)
    return min(s,t),max(s,t)
def pi(N):return add(scale(atan(Q(1,5),N),16),scale(atan(Q(1,239),N),-4))
def trig(x,N,sine):
    degree=2*N+int(sine); power=pt(1); result=pt(0)
    for k in range(degree+1):
        if k%2==int(sine):result=add(result,scale(power,Q((-1)**((k-int(sine))//2),factorial(k))))
        power=mul(power,x)
    M=max(abs(x[0]),abs(x[1]));r=M**(degree+1)/factorial(degree+1)
    return result[0]-r,result[1]+r

def oracle(case,N):
    p=pi(N)
    if case=='F':return pt(0),pt(0),pt(0),None,p
    if case=='G':return pt(Q(-2,7)),pt(0),pt(Q(2,7)),p,p
    if case=='E':mag=pt(Q(1,2**81));angle=scale(p,Q(-89,154))
    else:
        mag=scale(trig(scale(p,Q(10,99)),N,False),Q(3,5))
        if case=='D':mag=add(mag,pt(Q(1,5)))
        angle=scale(p,Q(-4,77)-(Q(8,143) if case=='B' else 0))
    return mul(mag,trig(angle,N,False)),mul(mag,trig(angle,N,True)),mag,angle,p

def dy(v):
    m,e=map(int,v);assert (m==0 and e==0) or m%2!=0
    return Q(m)*Q(2)**e

def interval(b):
    m,r=dy(b['mid']),dy(b['rad']);assert r>=0;return m-r,m+r

def inside(a,b):return b[0]<=a[0]<=a[1]<=b[1]
raw=Path(sys.argv[1]).read_bytes();data=json.loads(raw);checks=[];results=[]
def check(name,value):checks.append({'check':name,'pass':bool(value)})
check('canonical_input',raw==canon(data))
check('population',[r['case'] for r in data['records']]==list('ABCDEFG'))
check('precision_threads',data['precision']==128 and data['threads']==1)
for field,path in [('preregistration_sha256','../preregistrations/H-VAL001-CERTIFIED-SPARSE-QUERY-01.md'),('binding_sha256','../certified_query_environment_20260907/binding.json')]:
    check(field,hashlib.sha256((Path(__file__).parent/path).read_bytes()).hexdigest()==data[field])
for name,digest in data['code_hashes'].items():check('code:'+name,hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()==digest)
for rec in data['records']:
    c=rec['case'];r=rec['result'];m=rec['manifest'];start=len(checks)
    check(c+':construction',hashlib.sha256(canon(m)).hexdigest()==rec['construction_sha256'])
    ids=[e['id'] for e in m['events']]
    check(c+':lineage',r['contributing_ids']==ids and len(set(ids))==len(ids))
    x,y=interval(r['real']),interval(r['imag']); mag=tuple(map(dy,r['magnitude']))
    zero=x[0]<=0<=x[1] and y[0]<=0<=y[1];branch=x[0]<0 and y[0]<=0<=y[1]
    status='UNRESOLVED_ZERO_CONTAINMENT' if zero else 'BRANCH_CUT_ENCLOSURE' if branch else 'RESOLVED_INTERVAL'
    check(c+':status_predicate',r['phase_status']==status)
    check(c+':required_status', (c not in 'ABCD' or status=='RESOLVED_INTERVAL') and (c!='F' or status=='UNRESOLVED_ZERO_CONTAINMENT') and (c!='G' or status=='BRANCH_CUT_ENCLOSURE'))
    check(c+':magnitude_order',0<=mag[0]<=mag[1])
    success=False
    for N in (64,128,256,512,1024):
        ox,oy,om,op,p=oracle(c,N)
        tests=[inside(ox,x),inside(oy,y),inside(om,mag)]
        if status=='UNRESOLVED_ZERO_CONTAINMENT':tests.append(r['phase'] is None)
        elif status=='BRANCH_CUT_ENCLOSURE':
            ph=r['phase'];tests.append(ph['full_circle'] and dy(ph['lower'])<=-p[1] and dy(ph['upper'])>=p[1])
        else:
            ph=interval(r['phase']);tests.append(op is not None and inside(op,ph) and ph[1]-ph[0]<2*p[0])
        if all(tests):success=True;break
        if any(a[1]<b[0] or a[0]>b[1] for a,b in [(ox,x),(oy,y),(om,mag)]):break
    for label,value in zip(('real_containment','imag_containment','magnitude_containment','phase_contract'),tests):check(c+':'+label,value)
    results.append({'case':c,'phase_status':status,'oracle_N':N,'pass':all(v['pass'] for v in checks[start:])})
    if not success or not results[-1]['pass']:break
out={'operator_sha256':hashlib.sha256(raw).hexdigest(),'results':results,'checks':checks,'passed':sum(v['pass'] for v in checks),'failed':sum(not v['pass'] for v in checks)}
out['status']='PASS' if out['failed']==0 and len(results)==7 else 'FAIL'
Path(sys.argv[2]).write_bytes(canon(out));print(out['status'],out['passed'],out['failed'],flush=True)
sys.exit(0 if out['status']=='PASS' else 1)
