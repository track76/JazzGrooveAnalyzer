"""Frozen tables, not distance discovery. No constructor import."""
from fractions import Fraction as Q

SHELLS={
'A':[(0,[(0,'a'),(1,'b'),(3,'c')]),(1,[(0,'b'),(1,'a'),(2,'c')]),(3,[(0,'c'),(2,'b'),(3,'a')])],
'D':[(0,[(0,'a'),(1,'b'),(2,'d'),(3,'c')]),(1,[(0,'b'),(1,'ad'),(2,'c')]),(2,[(0,'d'),(1,'bc'),(2,'a')]),(3,[(0,'c'),(1,'d'),(2,'b'),(3,'a')])]}
PAIRS={'A':{1:['ab'],2:['bc'],3:['ac']},'D':{1:['ab','bd','dc'],2:['ad','bc'],3:['ac']},'I':{1:['ab','ae'],2:['bc','ec'],3:['ac']}}
WINDOWS={(0,1):([-1,1],[0,1]),(0,2):([-2,2],[0,2]),(0,3):([-3,3],[0,3]),
 (1,1):([0,2],[0,2]),(1,2):([-1,3],[0,3]),(2,1):([1,3],[1,3]),(2,2):([0,4],[0,3]),
 (3,1):([2,4],[2,3]),(3,2):([1,5],[1,3]),(3,3):([0,6],[0,3])}
CLIPS={(0,2):[-1,2],(0,3):[-1,3],(3,2):[1,4],(3,3):[0,4]}

def expected(pid,authority):
    a=Q(3,2) if pid=='C' else Q(1);d=Q(1,2) if pid=='B' else Q(0)
    transform=lambda t:a*Q(t)+d
    times={'a':0,'b':1,'c':3}
    if pid=='D':times['d']=2
    if pid=='I':times['e']=1
    if pid=='H':times={'a':1}
    if pid=='Z':times={}
    idof=lambda i:pid+'.'+i
    parent=lambda i:'A.'+i if pid in ('B','C','D','I') and i in 'abc' else None
    pop={'population':pid,'events':[{'id':idof(i),'t':transform(t),'parent':parent(i)} for i,t in sorted(times.items(),key=lambda v:(v[1],v[0]))],
         'asset':[transform(-1),transform(4)],'scope':[transform(0),transform(3)],'construction_authority':authority,
         'transformation':{'kind':'translation','value':d} if pid=='B' else {'kind':'dilation','value':a} if pid=='C' else None}
    def pair(s):return {'ids':[idof(i) for i in s],'times':[transform(times[i]) for i in s],'parents':[parent(i) for i in s]}
    def role(ps,sets):
        ids=sorted(set(i for p in ps for i in p['ids']))
        return {'generating_ids':ids,'intersections':{k:[i for i in ids if i in v] for k,v in sets.items()},
                'pairs':[{'ids':p['ids'],'intersections':{k:[i for i in sorted(p['ids']) if i in v] for k,v in sets.items()}} for p in ps]}
    result={'population':pid,'centers':[],'scales':[],'periods':[],'coincident_pairs':[pair('be')] if pid=='I' else [],'queries':[]}
    if pid in ('H','Z'):
        if pid=='H':result['centers']=[{'id':[pid,Q(1)],'u':Q(1),'event_ids':[idof('a')],'parents':[None]}]
        return pop,result
    ptable=PAIRS[pid if pid in ('D','I') else 'A']
    for t,ps in ptable.items():
        pp=sorted([pair(sorted(p)) for p in ps],key=lambda v:v['ids'])
        result['periods'].append({'id':[pid,a*t],'T':a*t,'f':1/(a*t),'pairs':pp})
    for center,shell in SHELLS['D' if pid=='D' else 'A']:
        shell=[(r,s.replace('b','be') if pid=='I' else s) for r,s in shell]
        u=transform(center);centerletters=shell[0][1];centerids=sorted(map(idof,centerletters))
        result['centers'].append({'id':[pid,u],'u':u,'event_ids':centerids,'parents':[parent(i) for i in sorted(centerletters)]})
        earlier=list(centerletters)
        for radius,letters in shell[1:]:
            L=2*a*radius
            ps=[pair((i,j)) for i in sorted(centerletters) for j in sorted(letters)]
            result['scales'].append({'id':[pid,u,L],'u':u,'L':L,'pairs':ps})
            sets={'contained':sorted(map(idof,earlier+list(letters))),'boundary':sorted(map(idof,letters)),'positive':sorted(map(idof,earlier))}
            ww,aa=WINDOWS[center,radius];cc=CLIPS.get((center,radius),ww)
            w=list(map(transform,ww));av=list(map(transform,aa));clip=list(map(transform,cc))
            # Exact endpoint-complement oracle; no window/intersection discovery.
            def complements(available):
                pieces=[]
                for lo,hi,closed in [(w[0],available[0],[True,False]),(available[1],w[1],[False,True])]:
                    if lo!=hi:pieces.append({'ends':[lo,hi],'closed':closed})
                return pieces
            coverage={'requested':w,'asset_clipped':clip,'available':av,'asset_unavailable':complements(clip),'unavailable':complements(av),
                      'asset_truncated':ww!=cc,'scope_truncated':cc!=aa}
            for period in result['periods']:
                t=period['T']
                result['queries'].append({'id':[pid,u,L,t],'u':u,'L':L,'T':t,'f':period['f'],'center_ids':centerids,'coverage':coverage,'membership':sets,
                  'scale_generation':role(ps,sets),'period_generation':role(period['pairs'],sets),'scientific_status':'RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED'})
            earlier+=list(letters)
    return pop,result
