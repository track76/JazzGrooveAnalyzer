"""Generic exact coordinate construction. No fixtures or expected answers."""
from fractions import Fraction as Q
from itertools import combinations

def intersection(a,b):
    l,h=max(a[0],b[0]),min(a[1],b[1])
    return [l,h] if l<=h else None

def missing(w,a):
    if a is None:return [{'ends':w,'closed':[True,True]}]
    pieces=[]
    if w[0]<a[0]:pieces.append({'ends':[w[0],a[0]],'closed':[True,False]})
    if a[1]<w[1]:pieces.append({'ends':[a[1],w[1]],'closed':[False,True]})
    return pieces

def overlaps(pairs,membership):
    ids=sorted({i for p in pairs for i in p['ids']})
    return {'generating_ids':ids,'intersections':{k:sorted(set(ids)&set(v)) for k,v in membership.items()},
            'pairs':[{'ids':p['ids'],'intersections':{k:sorted(set(p['ids'])&set(v)) for k,v in membership.items()}} for p in pairs]}

def construct(pop):
    pid=pop['population'];events=sorted(pop['events'],key=lambda e:(e['t'],e['id']))
    asset,scope=pop['asset'],pop['scope'];byid={e['id']:e for e in events}
    assert len(byid)==len(events) and asset[0]<=scope[0]<=scope[1]<=asset[1]
    assert all(scope[0]<=e['t']<=scope[1] for e in events)
    def pair(ids):
        return {'ids':list(ids),'times':[byid[i]['t'] for i in ids],'parents':[byid[i]['parent'] for i in ids]}
    groups={};coincident=[]
    for i,j in combinations(sorted(byid),2):
        t=abs(byid[i]['t']-byid[j]['t']);p=pair((i,j))
        if t:groups.setdefault(t,[]).append(p)
        else:coincident.append(p)
    periods=[{'id':[pid,t],'T':t,'f':1/t,'pairs':groups[t]} for t in sorted(groups)]
    centers=[];scales=[];queries=[]
    for u in sorted({e['t'] for e in events}):
        centerids=sorted(e['id'] for e in events if e['t']==u)
        centers.append({'id':[pid,u],'u':u,'event_ids':centerids,'parents':[byid[i]['parent'] for i in centerids]})
        for L in sorted({2*abs(e['t']-u) for e in events if e['t']!=u}):
            boundary=sorted(e['id'] for e in events if abs(e['t']-u)==L/2)
            # Ordered center/boundary pairs preserve their distinct generation roles.
            pairs=[pair((i,j)) for i in centerids for j in boundary]
            scales.append({'id':[pid,u,L],'u':u,'L':L,'pairs':pairs})
            w=[u-L/2,u+L/2];clip=intersection(w,asset);available=intersection(clip,scope)
            member={'contained':sorted(e['id'] for e in events if available[0]<=e['t']<=available[1]),
                    'boundary':boundary,'positive':sorted(e['id'] for e in events if abs(e['t']-u)<L/2)}
            coverage={'requested':w,'asset_clipped':clip,'available':available,
                      'asset_unavailable':missing(w,clip),'unavailable':missing(w,available),
                      'asset_truncated':clip!=w,'scope_truncated':available!=clip}
            for t in sorted(groups):
                queries.append({'id':[pid,u,L,t],'u':u,'L':L,'T':t,'f':1/t,'center_ids':centerids,
                    'coverage':coverage,'membership':member,'scale_generation':overlaps(pairs,member),
                    'period_generation':overlaps(groups[t],member),
                    'scientific_status':'RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED'})
    return {'population':pid,'centers':centers,'scales':scales,'periods':periods,'coincident_pairs':coincident,'queries':queries}
