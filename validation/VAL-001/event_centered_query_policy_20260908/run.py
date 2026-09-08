"""Input harness only. Writes outputs before scorer is invoked."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,platform,sys
from encoding import canonical,digest
from constructor import construct
P=Path(__file__).parent
pr=P.parent/'preregistrations/H-VAL001-EVENT-CENTERED-QUERY-POLICY-01.md'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
authority='e8f4d2ff17ff445bf9633d9cf52d28af55262c77feeaf54556a3052606542292'
assert sha(pr)==authority and platform.python_version()=='3.13.14'
rows=[('A',[('a','0'),('b','1'),('c','3')],['-1','4'],['0','3']),
('B',[('a','1/2'),('b','3/2'),('c','7/2')],['-1/2','9/2'],['1/2','7/2']),
('C',[('a','0'),('b','3/2'),('c','9/2')],['-3/2','6'],['0','9/2']),
('D',[('a','0'),('b','1'),('d','2'),('c','3')],['-1','4'],['0','3']),
('H',[('a','1')],['-1','4'],['0','3']),
('I',[('a','0'),('b','1'),('e','1'),('c','3')],['-1','4'],['0','3']),
('Z',[],['-1','4'],['0','3'])]
manifest=[];outputs=[]
for pid,es,asset,scope in rows:
    events=[{'id':pid+'.'+i,'t':Q(t),'parent':'A.'+i if pid in ('B','C','D','I') and i in 'abc' else None} for i,t in es]
    pop={'population':pid,'events':sorted(events,key=lambda e:(e['t'],e['id'])),'asset':list(map(Q,asset)),'scope':list(map(Q,scope)),
         'construction_authority':authority,'transformation':({'kind':'translation','value':Q('1/2')} if pid=='B' else {'kind':'dilation','value':Q('3/2')} if pid=='C' else None)}
    manifest.append({'input':pop,'sha256':digest(pop)});outputs.append(construct(pop))
prov={'preregistration_sha256':authority,'python_version':platform.python_version(),'python_binary_sha256':sha(Path(sys.executable).resolve()),
      'code_sha256':{f.name:sha(f) for f in sorted(P.glob('*.py'))},'manifests':manifest}
out={'provenance_sha256':digest(prov),'populations':outputs}
run=Path(sys.argv[1]);run.mkdir(exist_ok=False)
(run/'provenance.json').write_bytes(canonical(prov));(run/'policy.json').write_bytes(canonical(out))
