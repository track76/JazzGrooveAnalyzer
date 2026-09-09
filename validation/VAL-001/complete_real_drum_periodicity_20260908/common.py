"""Frozen input/environment binding and lossless catalogues. No response evaluation."""
import sys,json,struct,hashlib,ctypes,importlib.util
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
import flint
P=Path(__file__).resolve().parent;V=P.parent;NAME='H-VAL001-COMPLETE-REAL-DRUM-PERIODICITY-01'
sys.path.insert(0,str(V/'production_streaming_harness_20260908'))
from streaming import canonical,sha,digest,LRU,Writer,array_rows
PR=V/'preregistrations';EXT=Path('/Volumes/SSD Track/JGA/experiments')/NAME
PID='VAL001_DIRECT_DRUM_COMPLETE_01'
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def setup():
 binding=json.loads((P/'implementation_binding.json').read_bytes())
 for path,h in binding['files'].items():assert sha(Path(path))==h,('source_hash',path)
 assert sha(PR/(NAME+'.md'))=='d36995de8fa9c24046eb1d4a56dd81abe7d6ad367238bba4006d98d1391130e0'
 auth=json.loads((PR/(NAME+'.authorities.json')).read_bytes())
 for path,h in auth.items():assert sha(Path(path))==h,('authority_hash',path)
 bp=V/'certified_query_environment_20260907/binding.json';b=json.loads(bp.read_bytes());fr=Path(flint.__file__).parent
 assert sys.version_info[:3]==(3,13,14) and flint.__version__=='0.9.0'
 assert sha(Path(sys.executable).resolve())==b['binding']['python']['binary_sha256']
 for n,h in b['binding']['installed_binary_hashes'].items():assert sha(fr/n)==h
 flint.ctx.prec=128;flint.ctx.threads=1
 lib=ctypes.CDLL(str(fr/'.dylibs/libflint.24.0.dylib'));lib.flint_get_num_threads.restype=ctypes.c_int;assert lib.flint_get_num_threads()==1
 inp=json.loads((PR/(NAME+'.inputs.json')).read_bytes())
 adapter=load('bound_adapter',V/'binary64_certified_input_20260908/adapter.py')
 for row in inp['events']:
  for key in ('timestamp','observation_timestamp','strength'):
   f=row[key];out=adapter.adapt(f,'H-VAL001-BINARY64-CERTIFIED-INPUT-01')
   assert out['status']=='ACCEPTED' and out['bits']==f['producer_bits'] and out['hex']==f['hex'] and out['ratio']==f['ratio']
 for key in ('origin','start','end'):
  f=inp['scope'][key];out=adapter.adapt(f,'H-VAL001-BINARY64-CERTIFIED-INPUT-01');assert out['status']=='ACCEPTED' and out['ratio']==f['ratio']
 events=inp['events'];assert len(events)==len({e['eme_id'] for e in events})==len({e['pulse_candidate_id'] for e in events})==63
 return inp,binding
q=lambda v:Q(*map(int,v))
def catalogues(inp):
 events=inp['events'];byid={e['eme_id']:e for e in events};times={i:q(e['timestamp']['ratio']) for i,e in byid.items()}
 def pair(i,j):return {'ids':[i,j],'times':[times[i],times[j]],'parents':[byid[i]['pulse_candidate_id'],byid[j]['pulse_candidate_id']]}
 groups={};coincident=[]
 for i,j in combinations(sorted(byid),2):
  T=abs(times[i]-times[j]);p=pair(i,j)
  if T:groups.setdefault(T,[]).append(p)
  else:coincident.append(p)
 centers=sorted(set(times.values()));scales_count=sum(len({2*abs(t-u) for t in times.values() if t!=u}) for u in centers)
 accum=sum(sum(abs(t-u)<=L/2 for t in times.values()) for u in centers for L in {2*abs(t-u) for t in times.values() if t!=u})*len(groups)
 assert (len(centers),len(groups),scales_count,scales_count*len(groups),accum)==(63,1056,3864,4080384,133195392)
 return byid,times,groups,coincident,centers,pair

def provenance(inp):
 return {'population':PID,'source':inp['source_identity'],'asset':inp['asset_sha256'],'source_authority_id':inp['source_authority_id'],'source_instance_key':inp['source_instance_key'],'input_manifest_sha256':sha(PR/(NAME+'.inputs.json')),'canonical_report_sha256':inp['canonical_report_sha256'],'events':inp['events'],'scope':inp['scope'],'measurement_authority':'PRESERVED_ACCEPTED_JGA_OBSERVATIONS_NO_NEW_CALIBRATION','numerical_authority':'EXACT_ACCEPTED_BINARY64_RECONSTRUCTION'}
