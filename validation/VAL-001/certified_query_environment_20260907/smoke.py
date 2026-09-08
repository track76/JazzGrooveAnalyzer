"""Environment API probes only. No scientific fixture input or evaluator."""
import ctypes, hashlib, json, platform, sys
from pathlib import Path
import flint
from flint import arb, acb, ctx
ctx.prec = 128
ctx.threads = 1
root = Path(flint.__file__).parent
libpath = root / '.dylibs/libflint.24.0.dylib'
lib = ctypes.CDLL(str(libpath))
lib.flint_get_num_threads.restype = ctypes.c_int
assert lib.flint_get_num_threads() == 1
assert ctx.prec == 128 and ctx.threads == 1
assert platform.python_version() == '3.13.14' and flint.__version__ == '0.9.0'
version = (ctypes.c_char * 32).in_dll(lib, 'flint_version').value.decode()
def dyadic(v):
    m,e = map(int,v.man_exp())
    if not m: return ['0','0']
    while m % 2 == 0: m //= 2; e += 1
    assert arb((m,e)) == v
    return [str(m),str(e)]
def ball(v): return {'mid':dyadic(v.mid()), 'rad':dyadic(v.rad())}
z = acb(3,4)
assert z.abs_lower() == 5 and z.abs_upper() == 5
assert not z.contains(0) and acb(arb(0,1),arb(0,1)).contains(0)
r = arb('7/19')
assert r.contains(flint.fmpq(7,19))
p = arb.pi()
smoke = {'rational':ball(r),'real':ball(z.real),'imag':ball(z.imag),
         'magnitude_lower':dyadic(z.abs_lower()),'magnitude_upper':dyadic(z.abs_upper()),
         'argument':ball(z.arg()),'pi':ball(p),'cos':ball(arb(0).cos()),
         'exp_real':ball(acb(0).exp().real),'negative_ray_argument':ball(acb(-3).arg())}
# Exact ball extraction and reconstruction, without decimal display.
for v in [r,p,z.arg()]:
    assert arb(v.mid(),v.rad()).contains(v)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'status':'ENVIRONMENT_SMOKE_PASS','scientific_fixtures_evaluated':0,
 'python':{'version':sys.version,'executable':str(Path(sys.executable).resolve()),'binary_sha256':sha(Path(sys.executable).resolve())},
 'python_flint':'0.9.0','flint_version':version,'platform':platform.platform(),'machine':platform.machine(),
 'precision_bits':ctx.prec,'ctx_threads':ctx.threads,'flint_get_num_threads':lib.flint_get_num_threads(),
 'arb_acb_identity':'Integrated into bound libflint; Python wrappers bound below',
 'installed_binary_hashes':{str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.suffix in ('.so','.dylib')},
 'smoke':smoke}
print(json.dumps(report,sort_keys=True,separators=(',',':')),end='')
