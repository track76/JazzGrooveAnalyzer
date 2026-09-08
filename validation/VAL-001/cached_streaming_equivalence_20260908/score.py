import json,sys
from pathlib import Path
from fractions import Fraction as Q
from common import canonical,digest,sha,rational
base=Path(sys.argv[1]);out=Path(sys.argv[2]);checks=[]
def ck(n,b):checks.append({'name':n,'pass':bool(b)})
n=base/'naive';o=base/'optimized'
naive=json.loads((n/'logical.json').read_bytes());index=json.loads((o/'index.json').read_bytes());maps={}
for name in ('inputs','periods','windows'):
 rows=json.loads((o/(name+'.json')).read_bytes());maps[name]={r['id']:r['body'] for r in rows}
 ck(name+':unique',len(maps[name])==len(rows));ck(name+':content_ids',all(digest(r['body'])==r['id'] for r in rows));ck(name+':index_hash',sha(o/(name+'.json'))==index['manifests'][name+'.json'])
expanded=[]
for pos,s in enumerate(index['shards']):
 ck('shard_name:'+str(pos),s['name']==f'shard-{pos:06d}.json')
 f=o/s['name'];rows=json.loads(f.read_bytes());ck('shard_hash:'+str(pos),sha(f)==s['sha256']);ck('shard_canonical:'+str(pos),f.read_bytes()==canonical(rows))
 ck('shard_bounds:'+str(pos),s['rows']==str(len(rows)) and s['first']==rows[0]['query_id'] and s['last']==rows[-1]['query_id'])
 ck('shard_size:'+str(pos),len(rows)==(4 if pos<5 else 1))
 for r in rows:
  x=dict(r)
  for short,key in [('input','inputs'),('period','periods'),('window','windows')]:x[short+'_provenance']=maps[key][x.pop(short+'_ref')]
  expanded.append(x)
ck('complete_21',len(naive)==len(expanded)==21 and len(index['shards'])==6 and index['total']=='21')
expectedorder=[['P',Q(u),Q(L),Q(t)] for u,ls in [(0,[2,6]),(1,[2,4]),(3,[4,6])] for L in ls for t in (1,2,3)]+[[pid,Q(1) if pid=='R' else Q(3,4),Q(2),Q(2)] for pid in ('N','Z','R')]
ck('query_order',canonical([r['query_id'] for r in expanded])==canonical(expectedorder))
shells={(0,2):('abe','be','a'),(0,6):('abec','c','abe'),(1,2):('abe','a','be'),(1,4):('abec','c','abe'),(3,4):('bec','be','c'),(3,6):('abec','a','bec')}
pp={1:[['P.a','P.b'],['P.a','P.e']],2:[['P.b','P.c'],['P.c','P.e']],3:[['P.a','P.c']]}
intervals={(0,2):([-1,1],[-1,1],[0,1]),(0,6):([-3,3],[-1,3],[0,3]),(1,2):([0,2],[0,2],[0,2]),(1,4):([-1,3],[-1,3],[0,3]),(3,4):([1,5],[1,4],[1,3]),(3,6):([0,6],[0,4],[0,3])}
for i,(a,b) in enumerate(zip(naive,expanded)):
 ck('exact_logical:'+str(i),canonical(a)==canonical(b))
 pid,u,L,t=b['query_id'];u,L,t=map(rational,(u,L,t));w=b['window_provenance'];period=b['period_provenance']
 if pid=='P':
  sets={k:sorted('P.'+c for c in s) for k,s in zip(('contained','boundary','positive'),shells[int(u),int(L)])}
  bounds=intervals[int(u),int(L)];pairs=pp[int(t)]
  center={0:['P.a'],1:['P.b','P.e'],3:['P.c']}[int(u)]
  scale=[[c,j] for c in center for j in sets['boundary']]
 else:
  ids=[pid+'.a'] if pid=='R' else [pid+'.a',pid+'.b'];sets={'contained':ids,'boundary':[],'positive':ids};pairs=[];scale=[];center=['R.a'] if pid=='R' else []
  bounds=([0,2],[0,2],[0,2]) if pid=='R' else ([Q(-1,4),Q(7,4)],[0,Q(7,4)],[0,Q(7,4)])
 ck('membership:'+str(i),w['membership']==sets and w['center_ids']==center and w['scale_pairs']==scale)
 ck('period_pairs:'+str(i),period['pairs']==pairs and period['origin']==('EVENT_DERIVED_POLICY' if pid=='P' else 'CONTROLLED_NUMERICAL_PROBE'))
 for field,bs in zip(('requested','asset_clipped','available'),bounds):ck(field+':'+str(i),canonical(w[field])==canonical(list(map(Q,bs))))
 for role,ps in [('period',pairs),('scale',scale)]:
  ids=sorted({v for pair in ps for v in pair}) if pid=='P' else sets['contained']
  want={'generating_ids':ids,'intersections':{k:sorted(set(ids).intersection(v)) for k,v in sets.items()},'pair_intersections':[{'pair':pair,'intersections':{k:sorted(set(pair).intersection(v)) for k,v in sets.items()}} for pair in ps]}
  ck(role+'_overlap:'+str(i),b['generation_evaluation_overlap'][role]==want)
 ck('status:'+str(i),b['scientific_status']=='RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED')
 if pid=='Z':ck('zero_status',b['numeric']['phase_status']=='UNRESOLVED_ZERO_CONTAINMENT' and b['numeric']['zero_containment'])
 if pid=='R':ck('branch_status',b['numeric']['phase_status']=='BRANCH_CUT_ENCLOSURE' and not b['numeric']['zero_containment'])
for mode in ('naive','optimized'):
 m=json.loads((base/mode/'mechanics.json').read_bytes());wanted={'exponentials':'68','hann':'68','amplitudes':'68','accumulations':'68','membership_builds':'21'} if mode=='naive' else {'exponentials':'17','hann':'26','amplitudes':'26','accumulations':'68','membership_builds':'9'}
 ck(mode+':counts',m['counts']==wanted)
 if mode=='optimized':ck('buffer_bound',m['max_buffered_rows']=='4');ck('cache_sizes',m['caches']=={'parsed':'9','exponentials':'17','hann':'26','amplitudes':'26','membership':'9'})
failed=sum(not c['pass'] for c in checks)
result={'status':'FAIL' if failed else 'PASS','passed':str(len(checks)-failed),'failed':str(failed),'checks':checks,'logical_fingerprint':digest(expanded),'optimized_files':{f.name:sha(f) for f in sorted(o.iterdir()) if f.name!='performance.json'},'naive_logical_sha256':sha(n/'logical.json')}
out.write_bytes(canonical(result));print(result['status'],result['passed'],result['failed']);sys.exit(1 if failed else 0)
