"""Generic accepted-binary64 adapter; no fixtures or oracle imports."""
import json,struct
from flint import arb

def dyadic(x):
    m,e=map(int,x.man_exp())
    if not m:return ['0','0']
    while m%2==0:m//=2;e+=1
    return [str(m),str(e)]

def adapt(record,authority):
    bits=record['producer_bits'];word=int(bits,16)
    sign=word>>63;exponent=(word>>52)&2047;fraction=word&((1<<52)-1)
    if exponent==2047:
        kind='NONFINITE_NAN' if fraction else 'NONFINITE_NEGATIVE_INFINITY' if sign else 'NONFINITE_POSITIVE_INFINITY'
        return {'input':record,'status':'REJECTED_NONFINITE','classification':kind,'authority':authority}
    value=struct.unpack('>d',bytes.fromhex(bits))[0]
    assert struct.pack('>d',json.loads(record['original_json_numeric_token'])).hex()==bits
    n,d=value.as_integer_ratio()
    z=arb(n)/arb(d)
    return {'input':record,'status':'ACCEPTED','authority':authority,'bits':struct.pack('>d',value).hex(),
            'hex':value.hex(),'ratio':[str(n),str(d)],'sign_bit':str(sign),
            'zero_status':('NEGATIVE_ZERO' if sign else 'POSITIVE_ZERO') if n==0 else 'NONZERO',
            'canonical_json_token':json.dumps(value,allow_nan=False),
            'enclosure':{'mid':dyadic(z.mid()),'rad':dyadic(z.rad())},
            'numerical_authority_status':'EXACT_ACCEPTED_BINARY64_RECONSTRUCTION',
            'measurement_authority_status':'NOT_ESTABLISHED_BY_ADAPTER'}
