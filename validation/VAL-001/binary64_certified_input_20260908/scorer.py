"""Independent literal/IEEE rational oracle. No adapter or FLINT imports."""
import hashlib,json,struct,sys
from fractions import Fraction as Q
from pathlib import Path
TABLE={
'A':('3fb999999999999a','0x1.999999999999ap-4',3602879701896397,36028797018963968,'0.1'),
'B':('3ff8000000000000','0x1.8000000000000p+0',3,2,'1.5'),
'C':('3fb99999a0000000','0x1.99999a0000000p-4',13421773,134217728,'0.10000000149011612'),
'D':('3ff4000000000000','0x1.4000000000000p+0',5,4,'1.25'),
'E':('c004000000000000','-0x1.4000000000000p+1',-5,2,'-2.5'),
'F':('0000000000000000','0x0.0p+0',0,1,'0.0'),
'G':('8000000000000000','-0x0.0p+0',0,1,'-0.0'),
'H':('3fd3333333333333','0x1.3333333333333p-2',5404319552844595,18014398509481984,'0.3')}
REJECT={'I1':('7ff8000000000000','NONFINITE_NAN'),'I2':('7ff0000000000000','NONFINITE_POSITIVE_INFINITY'),'I3':('fff0000000000000','NONFINITE_NEGATIVE_INFINITY')}
def decode(bits,width=64):
    word=int(bits,16);fracbits,bias=(52,1023) if width==64 else (23,127)
    e=(word>>fracbits)&(2047 if width==64 else 255);s=word>>(width-1);m=word&((1<<fracbits)-1)
    if e:m+=1<<fracbits
    return (-1)**s*Q(m)*Q(2)**((e if e else 1)-bias-fracbits)
def verify_tables():
    return all(decode(b)==Q(n,d) for b,h,n,d,t in TABLE.values()) and decode('3dcccccd',32)==Q(13421773,134217728)
P=Path(__file__).parent
canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if sys.argv[1]=='--verify-tables':
    ok=verify_tables();(P/'table_consistency.json').write_bytes(canonical({'status':'PASS' if ok else 'FAIL','method':'Independent integer IEEE rational decode of literal oracle before adapter execution'}));print('TABLE_CONSISTENCY',ok);sys.exit(0 if ok else 1)
run=Path(sys.argv[1]);a=json.loads((run/'adapter.json').read_bytes());p=json.loads((run/'scope_provenance.json').read_bytes());checks=[];summary=[]
def check(name,ok,actual=None,expected=None):
    row={'name':name,'pass':bool(ok)}
    if not ok:row.update(actual=actual,expected=expected)
    checks.append(row)
check('frozen_table_consistency',verify_tables())
for name in ('adapter','scope_provenance'):
    f=run/(name+'.json');check(name+':canonical',f.read_bytes()==canonical(json.loads(f.read_bytes())))
manifest=json.loads((P/'inputs.json').read_bytes());freeze=json.loads((P/'source_freeze.json').read_bytes())
expectedauth={'conversion':'JGA-ACCEPTED-BINARY64-OBSERVATION-INPUT-V1','preregistration_sha256':'5a3a2a3607d71db4a9e878466fb77d5492e8c9b43105ea208e19494efe3f3d46','binding_sha256':'5242ca974311694e7bf0d20e4459e25336232fc201bc55f80e43e58f7166f468','input_manifest_sha256':sha(P/'inputs.json'),'source_freeze_sha256':sha(P/'source_freeze.json'),'precision_bits':'128','threads':'1'}
check('authority',a['authority']==p['authority']==expectedauth)
check('manifest_provenance',p['inputs']==manifest and p['code_sha256']==freeze['files'])
for name,h in freeze['files'].items():check('frozen:'+name,sha(P/name)==h)
check('runtime',p['runtime']=={'python':'3.13.14','python_flint':'0.9.0','FLINT':'3.6.0','precision':'128','threads':'1'})
check('finite_population',[r['input']['fixture_id'] for r in a['accepted']]==list(TABLE))
check('rejected_population',[r['input']['fixture_id'] for r in a['rejected']]==list(REJECT))
def dy(v):
    m,e=map(int,v);assert v==[str(m),str(e)] and ((m==0 and e==0) or m%2!=0)
    return Q(m)*Q(2)**e
for r in a['accepted']:
    i=r['input']['fixture_id'];bits,h,n,d,t=TABLE[i];start=len(checks)
    check(i+':input',r['input']==next(x for x in manifest if x['fixture_id']==i))
    check(i+':original_token',r['input']['original_json_numeric_token']==t)
    check(i+':bits',r['bits']==r['input']['producer_bits']==bits)
    check(i+':hex',r['hex']==h)
    check(i+':ratio',r['ratio']==[str(n),str(d)])
    check(i+':json_roundtrip',r['canonical_json_token']==t and struct.pack('>d',json.loads(t)).hex()==bits)
    sign='1' if i in ('E','G') else '0';zero='NEGATIVE_ZERO' if i=='G' else 'POSITIVE_ZERO' if i=='F' else 'NONZERO'
    check(i+':signed_zero',r['sign_bit']==sign and r['zero_status']==zero)
    try:
        mid,rad=dy(r['enclosure']['mid']),dy(r['enclosure']['rad']);contained=rad>=0 and mid-rad<=Q(n,d)<=mid+rad
    except (ValueError,AssertionError,KeyError):contained=False
    check(i+':certified_enclosure',contained)
    check(i+':status_authority',r['status']=='ACCEPTED' and r['authority']==expectedauth and r['numerical_authority_status']=='EXACT_ACCEPTED_BINARY64_RECONSTRUCTION' and r['measurement_authority_status']=='NOT_ESTABLISHED_BY_ADAPTER')
    if i in ('A','H'):
        numerator=1 if i=='A' else 3;difference=Q(1,180143985094819840) if i=='A' else Q(-1,90071992547409920)
        diag={'sample_coordinate' if i=='A' else 'sample_count':str(numerator),'sample_rate':'10','diagnostic_rational':[str(numerator),'10']}
        check(i+':diagnostics',r['input']['diagnostics']==diag)
        check(i+':producer_division',struct.pack('>d',numerator/10).hex()==bits)
        check(i+':diagnostic_difference',Q(n,d)-Q(numerator,10)==difference)
    elif i=='C':
        check(i+':float32_provenance',r['input']['diagnostics']=={'binary32_bits':'3dcccccd','binary32_exact_ratio':['13421773','134217728']})
        check(i+':float32_exact_widening',decode('3dcccccd',32)==Q(n,d) and struct.pack('>d',struct.unpack('>f',bytes.fromhex('3dcccccd'))[0]).hex()==bits)
    else:check(i+':no_diagnostics',r['input']['diagnostics'] is None)
    summary.append({'fixture':i,'pass':all(x['pass'] for x in checks[start:])})
for r in a['rejected']:
    i=r['input']['fixture_id'];bits,kind=REJECT[i]
    want={'input':next(x for x in manifest if x['fixture_id']==i),'status':'REJECTED_NONFINITE','classification':kind,'authority':expectedauth}
    check(i+':rejection',r==want and r['input']['producer_bits']==bits and r['input']['original_json_numeric_token'] is None)
    summary.append({'fixture':i,'pass':checks[-1]['pass'],'expected_rejection':kind})
scope={'temporal_origin_ref':'F','observation_scope_start_ref':'F','analysis_input_duration_ref':'H','observation_scope_end_ref':'H','clipping_lower_ref':'F','clipping_upper_ref':'H','closed':[True,True],'start':['0','1'],'end':['5404319552844595','18014398509481984'],'sample_count':'3','sample_rate':'10','diagnostic_duration':['3','10'],'diagnostic_equals_accepted':False,'witness_membership':[True,True,False]}
check('scope_binding',p['scope']==scope,p['scope'],scope)
failed=sum(not c['pass'] for c in checks)
out={'status':'FAIL' if failed else 'PASS','passed':str(len(checks)-failed),'failed':str(failed),'fixtures':summary,'checks':checks,'adapter_sha256':sha(run/'adapter.json'),'scope_provenance_sha256':sha(run/'scope_provenance.json')}
(run/'score.json').write_bytes(canonical(out));print(out['status'],out['passed'],out['failed']);sys.exit(1 if failed else 0)
