import json,hashlib
from fractions import Fraction as Q

def enc(x):
    if isinstance(x,Q):return [str(x.numerator),str(x.denominator)]
    if isinstance(x,dict):return {k:enc(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [enc(v) for v in x]
    if isinstance(x,bool) or x is None or isinstance(x,str):return x
    if isinstance(x,int):return str(x)
    raise TypeError(type(x))
def canonical(x):return json.dumps(enc(x),sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tagged(x):return {'id':digest(x),'body':x}
def rational(x):return Q(*map(int,x))
