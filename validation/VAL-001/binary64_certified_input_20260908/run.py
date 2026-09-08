"""Bound environment and input harness; no oracle logic."""
import ctypes,hashlib,json,platform,sys
from fractions import Fraction as Q
from pathlib import Path
import flint
from adapter import adapt
P=Path(__file__).parent
canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pr=P.parent/'preregistrations/H-VAL001-BINARY64-CERTIFIED-INPUT-01.md'
bp=P.parent/'certified_query_environment_20260907/binding.json'
assert sha(pr)=='5a3a2a3607d71db4a9e878466fb77d5492e8c9b43105ea208e19494efe3f3d46'
assert sha(bp)=='5242ca974311694e7bf0d20e4459e25336232fc201bc55f80e43e58f7166f468'
binding=json.loads(bp.read_bytes());root=Path(flint.__file__).parent
assert platform.python_version()=='3.13.14' and flint.__version__=='0.9.0' and platform.machine()=='arm64'
assert sha(Path(sys.executable).resolve())==binding['binding']['python']['binary_sha256']
for name,h in binding['binding']['installed_binary_hashes'].items():assert sha(root/name)==h
flint.ctx.prec=128;flint.ctx.threads=1
lib=ctypes.CDLL(str(root/'.dylibs/libflint.24.0.dylib'));lib.flint_get_num_threads.restype=ctypes.c_int
assert flint.ctx.prec==128 and lib.flint_get_num_threads()==1
assert (ctypes.c_char*32).in_dll(lib,'flint_version').value.decode()=='3.6.0'
freeze=json.loads((P/'source_freeze.json').read_bytes())
for name,h in freeze['files'].items():assert sha(P/name)==h
manifest=json.loads((P/'inputs.json').read_bytes())
authority={'conversion':'JGA-ACCEPTED-BINARY64-OBSERVATION-INPUT-V1','preregistration_sha256':sha(pr),'binding_sha256':sha(bp),'input_manifest_sha256':sha(P/'inputs.json'),'source_freeze_sha256':sha(P/'source_freeze.json'),'precision_bits':'128','threads':'1'}
accepted=[];rejected=[]
for record in manifest:
    result=adapt(record,authority)
    (accepted if result['status']=='ACCEPTED' else rejected).append(result)
byid={r['input']['fixture_id']:r for r in accepted}
ratio=lambda row:Q(*map(int,row['ratio']))
start,end=ratio(byid['F']),ratio(byid['H'])
rr=lambda x:[str(x.numerator),str(x.denominator)]
scope={'temporal_origin_ref':'F','observation_scope_start_ref':'F','analysis_input_duration_ref':'H','observation_scope_end_ref':'H','clipping_lower_ref':'F','clipping_upper_ref':'H',
       'closed':[True,True],'start':rr(start),'end':rr(end),'sample_count':'3','sample_rate':'10','diagnostic_duration':['3','10'],
       'diagnostic_equals_accepted':end==Q(3,10),'witness_membership':[start<=q<=end for q in (Q(0),end,Q(3,10))]}
output={'authority':authority,'accepted':accepted,'rejected':rejected}
prov={'authority':authority,'inputs':manifest,'code_sha256':freeze['files'],'scope':scope,'runtime':{'python':'3.13.14','python_flint':'0.9.0','FLINT':'3.6.0','precision':'128','threads':'1'}}
dest=Path(sys.argv[1]);dest.mkdir(exist_ok=False)
(dest/'adapter.json').write_bytes(canonical(output));(dest/'scope_provenance.json').write_bytes(canonical(prov))
