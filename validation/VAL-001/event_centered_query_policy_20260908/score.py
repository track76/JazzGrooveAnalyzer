"""Independent full-field table scoring after candidate artifacts are frozen."""
import hashlib,json,sys
from pathlib import Path
from encoding import canonical,digest,encode
from oracle import expected
P=Path(__file__).parent;run=Path(sys.argv[1]);checks=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(name,ok,actual=None,expect=None):
    row={'name':name,'pass':bool(ok)}
    if not ok:row.update(actual=actual,expected=expect)
    checks.append(row)
policy=json.loads((run/'policy.json').read_bytes());prov=json.loads((run/'provenance.json').read_bytes())
authority='e8f4d2ff17ff445bf9633d9cf52d28af55262c77feeaf54556a3052606542292'
check('authority',sha(P.parent/'preregistrations/H-VAL001-EVENT-CENTERED-QUERY-POLICY-01.md')==authority==prov['preregistration_sha256'])
check('provenance_binding',policy['provenance_sha256']==sha(run/'provenance.json'))
for name in ('policy','provenance'):
    raw=(run/(name+'.json')).read_bytes();check(name+':canonical',raw==canonical(json.loads(raw)))
for name,h in prov['code_sha256'].items():check('code:'+name,sha(P/name)==h)
check('runtime',prov['python_version']=='3.13.14')
check('population_order',[x['population'] for x in policy['populations']]==list('ABCDHIZ'))
counts={'A':18,'B':18,'C':18,'D':30,'H':0,'I':18,'Z':0};summaries=[]
for index,pid in enumerate('ABCDHIZ'):
    pop,want=expected(pid,authority);want=encode(want);actual=policy['populations'][index];m=prov['manifests'][index];start=len(checks)
    check(pid+':input_exact',m['input']==encode(pop),m['input'],encode(pop))
    check(pid+':manifest_hash',m['sha256']==digest(pop))
    check(pid+':query_count',len(actual['queries'])==counts[pid])
    for field in ('centers','scales','periods','coincident_pairs'):
        check(pid+':'+field,actual[field]==want[field],actual[field],want[field])
    for i in range(max(len(actual['queries']),len(want['queries']))):
        x=actual['queries'][i] if i<len(actual['queries']) else None
        y=want['queries'][i] if i<len(want['queries']) else None
        check(pid+':query:'+str(i),x==y,x,y)
    check(pid+':complete_record',actual==want,actual,want)
    summaries.append({'population':pid,'queries':len(actual['queries']),'pass':all(c['pass'] for c in checks[start:])})
    if not summaries[-1]['pass']:break
check('total_102',sum(len(x['queries']) for x in policy['populations'])==102)
# Explicit addition invariants, separate from complete table equality.
base=policy['populations'][0];added=policy['populations'][3]
def unqualify(x):
    if isinstance(x,str):return x.replace('D.','A.') if x.startswith('D.') else ('A' if x=='D' else x)
    if isinstance(x,list):return [unqualify(y) for y in x]
    if isinstance(x,dict):return {k:unqualify(v) for k,v in x.items()}
    return x
for catalog in ('centers','scales','periods'):
    targets={json.dumps(unqualify(x['id'])):x for x in added[catalog]}
    check('addition:'+catalog+':coordinates',all(json.dumps(x['id']) in targets for x in base[catalog]))
    if catalog!='centers':
        def pairids(record):return {tuple(p['ids']) for p in record['pairs']}
        check('addition:'+catalog+':generators',all(pairids(x)<=pairids(unqualify(targets[json.dumps(x['id'])])) for x in base[catalog]))
# B/C full table equality above checks exact transformed coordinates, endpoints,
# frequencies, memberships and parent links, not just counts.
failed=sum(not x['pass'] for x in checks)
result={'status':'FAIL' if failed else 'PASS','passed':len(checks)-failed,'failed':failed,'checks':checks,'populations':summaries,
        'policy_sha256':sha(run/'policy.json'),'provenance_sha256':sha(run/'provenance.json')}
(run/'score.json').write_bytes(canonical(result));print(result['status'],result['passed'],result['failed'])
sys.exit(1 if failed else 0)
