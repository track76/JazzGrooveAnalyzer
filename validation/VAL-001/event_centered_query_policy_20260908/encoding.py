"""Canonical encoding only; no policy or oracle logic."""
from fractions import Fraction
import hashlib,json

def encode(x):
    if isinstance(x,Fraction):return [str(x.numerator),str(x.denominator)]
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    if isinstance(x,bool) or x is None or isinstance(x,str):return x
    if isinstance(x,int):return str(x)
    raise TypeError(type(x))
def canonical(x):return json.dumps(encode(x),sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('utf-8')
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
