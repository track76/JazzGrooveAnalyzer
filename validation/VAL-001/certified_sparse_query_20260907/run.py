"""Frozen input harness; no scoring values."""
import ctypes,hashlib,json,platform,sys
from pathlib import Path
import flint
from evaluator import evaluate
P=Path(__file__).parent
canon=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pr=P.parent/'preregistrations/H-VAL001-CERTIFIED-SPARSE-QUERY-01.md'
bp=P.parent/'certified_query_environment_20260907/binding.json'
assert sha(pr)=='bfc514d764c7b800821ca11875827b7ed4565b1013f2c579b7a7d1435c1f92f8'
assert sha(bp)=='5242ca974311694e7bf0d20e4459e25336232fc201bc55f80e43e58f7166f468'
binding=json.loads(bp.read_bytes()); root=Path(flint.__file__).parent
assert platform.python_version()=='3.13.14' and flint.__version__=='0.9.0'
assert sha(Path(sys.executable).resolve())==binding['binding']['python']['binary_sha256']
for path,digest in binding['binding']['installed_binary_hashes'].items():assert sha(root/path)==digest
flint.ctx.prec=128;flint.ctx.threads=1
lib=ctypes.CDLL(str(root/'.dylibs/libflint.24.0.dylib'));lib.flint_get_num_threads.restype=ctypes.c_int
assert lib.flint_get_num_threads()==1
rows=[
([('-17/126','2/5'),('53/126','2/5')],'1/7','2/11','5/3'),
([('31/1638','2/5'),('941/1638','2/5')],'27/91','2/11','5/3'),
([('-17/84','2/5'),('53/84','2/5')],'3/14','4/33','5/2'),
([('-17/126','2/5'),('1/7','1/5'),('53/126','2/5')],'1/7','2/11','5/3'),
([('-65/84','1'),('89/84','1208925819614629174706177/1208925819614629174706176')],'1/7','3/11','11/3'),
([('-65/84','1'),('89/84','1')],'1/7','3/11','11/3'),
([('11/6','2/7')],'11/6','3/11','5/3')]
records=[]
for case,(pairs,u,f,L) in zip('ABCDEFG',rows):
    events=[]
    for i,(t,s) in enumerate(pairs):
        parent=None
        if case in 'BC':parent=f'A{i}'
        if case=='D' and i in (0,2):parent=f'A{i//2}'
        events.append({'id':f'{case}{i}','t':t,'s':s,'parent':parent})
    query={'u':u,'f':f,'L':L}
    manifest={'events':events,'query':query,'construction_authority':sha(pr)}
    result=evaluate(events,query)
    records.append({'case':case,'manifest':manifest,'construction_sha256':hashlib.sha256(canon(manifest)).hexdigest(),'result':result})
output={'preregistration_sha256':sha(pr),'binding_sha256':sha(bp),'precision':128,'threads':1,
        'code_hashes':{p.name:sha(p) for p in sorted(P.glob('*.py'))},'records':records}
Path(sys.argv[1]).write_bytes(canon(output))
