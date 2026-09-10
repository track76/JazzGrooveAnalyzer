"""Bounded PI-authorized ENST development / frozen MDB validation. No timing inference."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import sys, pathlib, hashlib, json, csv, collections, io, math, platform, importlib.metadata
BASE=pathlib.Path('/Volumes/SSD Track/JGA')
OUT=BASE/'experiments/RIDE-HIHAT-ENST-MDB-02'
os.environ['NUMBA_CACHE_DIR']=str(OUT/'cache')
import numpy as np
import scipy.signal
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_recall_curve,average_precision_score,roc_auc_score,balanced_accuracy_score
from sklearn.exceptions import ConvergenceWarning
import soundfile as sf
import librosa
import warnings
HERE=pathlib.Path(__file__).resolve().parent
ENST=BASE/'datasets/RIDE-HIHAT-EXTERNAL/ENST-legacy-audio-20260910'
MDB=BASE/'datasets/RIDE-HIHAT-EXTERNAL/MDB-original-b29e2d63'
EM={'rc':'RIDE_UNSPECIFIED','chh':'HH_CLOSED','ohh':'HH_OPEN'}
MM={'RDC':'RIDE_UNSPECIFIED','RDB':'RIDE_BELL','CHH':'HH_CLOSED','OHH':'HH_OPEN','PHH':'HH_PEDAL'}
SR=44100; N=11025
MEL=librosa.filters.mel(sr=SR,n_fft=2048,n_mels=32,fmin=20,fmax=20000,htk=False,norm='slaney')
WIN=scipy.signal.get_window('hann',2048,fftbins=True)
def digest(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(name,obj):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(obj,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
    return p
def environment():
    return {'python':sys.version,'platform':platform.platform(),'executable':sys.executable,'packages':{k:importlib.metadata.version(k) for k in ['numpy','scipy','scikit-learn','soundfile','librosa']},'threads':1}
def checked(path,sha):
    data=path.read_bytes();assert hashlib.sha256(data).hexdigest()==sha,str(path);return data
def subtype(label,descriptor):
    import re
    base=re.sub(r'[0-9]+$','',label)
    sub='UNRESOLVED_GENERIC_CYMBAL' if base=='c' else EM.get(base,'OTHER_'+label)
    if base in ('chh','ohh') and '_pedal_' in descriptor and 'hi-hat' in descriptor:
        sub='HH_PEDAL_'+('CLOSED' if base=='chh' else 'OPEN')
    if base in ('chh','ohh') and 'half-opened' in descriptor:sub='HH_HALF_OPEN'
    elif base in ('chh','ohh') and 'wide-opened' in descriptor:sub='HH_WIDE_OPEN'
    if base=='rc' and '-dome_' in descriptor:sub='RIDE_DOME'
    elif base=='rc' and 'played-as-crash' in descriptor:sub='RIDE_PLAYED_AS_CRASH'
    return sub
def eligible(ts,index,duration):
    t=ts[index]
    if t<.125 or t+.125>duration:return 'BOUNDARY'
    if (index and t-ts[index-1]<=.125) or (index+1<len(ts) and ts[index+1]-t<=.125):return 'OTHER_ONSET_IN_WINDOW'
    return None
def patch(audio,t):
    center=int(np.rint(t*SR));start=center-N//2
    if start<0 or start+N>len(audio):return None
    x=audio[start:start+N].astype(np.float64)
    rms=np.sqrt(np.mean(x*x))
    if rms==0:return None
    x=x/rms
    frames=np.lib.stride_tricks.sliding_window_view(np.pad(x,(1024,1024)),2048)[::441]
    mag=np.abs(np.fft.rfft(frames*WIN,axis=1)).T
    z=np.log1p(MEL@mag).astype(np.float32)
    assert z.shape==(32,26) and np.isfinite(z).all()
    return z.ravel()
def inventory(which):
    root=ENST if which=='enst' else MDB
    manifest_path=root/'authority/admission_manifest.json'
    if which=='mdb':assert digest(manifest_path)=='3c66085a119419d21d8268b8aac37f8bc16cb613c399af825d7b248c87d92421'
    manifest=json.loads(manifest_path.read_text());sha={r['path']:r['sha256'] for r in manifest['files']}
    events=[];excluded=[];available=collections.Counter();missing=[]
    if which=='enst':
        for row in manifest['performances']:
            rel=row['audio'];group=row['group']
            split={'drummer_1':'calibration','drummer_2':'train','drummer_3':'development_evaluation'}[group]
            text=checked(root/row['annotation'],sha[row['annotation']]).decode()
            notes=[]
            for line in text.splitlines():
                if not line.strip():continue
                fields=line.split();assert len(fields)==2,(row['annotation'],fields)
                time,label=fields
                notes.append((float(time),label,subtype(label,row['descriptor'])))
            dur=sf.info(str(root/rel)).duration
            add_events(events,excluded,available,notes,dur,rel,group,split,sha[rel],which)
    else:
        rows=[r for r in manifest['files'] if '/subclass/' in r['path']]
        for row in rows:
            text=checked(root/row['path'],row['sha256']).decode()
            b=pathlib.Path(row['path']).name.removesuffix('_subclass.txt')
            rel='original/MDB Drums/audio/drum_only/'+b+'_Drum.wav'
            notes=[]
            for line in text.splitlines():
                if not line.strip():continue
                t,label=line.split();notes.append((float(t),label,MM.get(label,'OTHER_'+label)))
            dur=sf.info(str(root/rel)).duration
            add_events(events,excluded,available,notes,dur,rel,b,'independent_validation',sha[rel],which)
    if which=='enst':
        buckets=collections.defaultdict(list);retained=[]
        for e in events:
            if e['split']=='train':buckets[(e['group'],e['subtype'])].append(e)
            else:retained.append(e)
        for bucket in buckets.values():
            bucket.sort(key=lambda e:hashlib.sha256(e['id'].encode()).hexdigest())
            retained.extend(bucket[:250]);excluded.extend(dict(e,reason='TRAIN_RESOURCE_CAP') for e in bucket[250:])
        events=retained
    events.sort(key=lambda e:e['id'])
    result={'dataset':which,'input_manifest_sha256':digest(manifest_path),'available_native_counts':dict(available),'missing_audio_performances':missing,'selected_counts':dict(collections.Counter(e['subtype'] for e in events)),'exclusion_counts':dict(collections.Counter(e['reason'] for e in excluded)),'events':events,'excluded':excluded}
    write(which+'/inventory.json',result)
    print(which,'selected',len(events),'counts',result['selected_counts'],'excluded',result['exclusion_counts'],flush=True)
    return events,root
def add_events(events,excluded,available,notes,duration,rel,group,split,sha,which):
    assert all(math.isfinite(n[0]) and n[0]>=0 for n in notes)
    assert notes==sorted(notes,key=lambda n:n[0])
    ts=[n[0] for n in notes]
    for i,(t,label,sub) in enumerate(notes):
        available[sub]+=1
        e={'id':which+':'+rel+':'+str(i),'path':rel,'source_sha256':sha,'time':t,'native_label':label,'subtype':sub,'group':group,'split':split,'ride':sub.startswith('RIDE_')}
        reason='UNRESOLVED_PROVIDER_SOURCE_CLASS' if sub.startswith('UNRESOLVED_') else eligible(ts,i,duration)
        if reason:excluded.append(dict(e,reason=reason))
        else:events.append(e)
def features(which,events,root):
    byfile=collections.defaultdict(list)
    for e in events:byfile[e['path']].append(e)
    xs=[];kept=[];unresolved=[]
    for i,(path,es) in enumerate(sorted(byfile.items())):
        data=checked(root/path,es[0]['source_sha256'])
        audio,rate=sf.read(io.BytesIO(data),dtype='float64',always_2d=True);audio=audio.mean(axis=1)
        if rate!=SR:
            g=math.gcd(rate,SR);audio=scipy.signal.resample_poly(audio,SR//g,rate//g)
        for e in es:
            v=patch(audio,e['time'])
            if v is None:unresolved.append(dict(e,reason='ZERO_OR_INCOMPLETE_CROP'))
            else:xs.append(v);kept.append(e)
        if i%100==0:print(which,'features files',i+1,'/',len(byfile),flush=True)
    assert xs,'No usable features'
    X=np.stack(xs);write(which+'/feature_lineage.json',{'events':kept,'unresolved':unresolved})
    np.save(OUT/which/'features.npy',X)
    return X,kept
def scores(X,params):
    Z=(X-params['mean'])/params['scale']
    from scipy.special import expit
    return expit(Z@params['coef']+params['intercept'])
def metrics(y,p,low,high):
    y=np.asarray(y,dtype=bool);p=np.asarray(p);pred=p>=.5
    tp=int(np.sum(y&pred));fp=int(np.sum(~y&pred));fn=int(np.sum(y&~pred));tn=int(np.sum(~y&~pred))
    both=len(np.unique(y))==2
    pos=p>=high;neg=p<=low;covered=pos|neg
    return {'n':len(y),'ride':int(y.sum()),'precision':tp/(tp+fp) if tp+fp else None,'recall':tp/(tp+fn) if tp+fn else None,'tp':tp,'fp':fp,'fn':fn,'tn':tn,'balanced_accuracy':float(balanced_accuracy_score(y,pred)) if both else None,'AP':float(average_precision_score(y,p)) if both else None,'ROC_AUC':float(roc_auc_score(y,p)) if both else None,'prevalence':float(y.mean()) if len(y) else None,'selective':{'ride_admitted':int(pos.sum()),'ride_true':int((pos&y).sum()),'ride_false':int((pos&~y).sum()),'not_ride_admitted':int(neg.sum()),'not_ride_false':int((neg&y).sum()),'abstained':int((~covered).sum()),'coverage':float(covered.mean()) if len(y) else None,'precision':float((pos&y).sum()/pos.sum()) if pos.any() else None,'ride_recall':float((pos&y).sum()/y.sum()) if y.any() else None}}
def evaluate(which,es,p,low,high):
    y=np.array([e['ride'] for e in es]);result=metrics(y,p,low,high)
    result['by_subtype']={};result['by_group']={}
    rh=np.array([e['subtype'].startswith(('RIDE_','HH_')) for e in es])
    result['ride_vs_hihat']=metrics(y[rh],p[rh],low,high)
    for key,target in [('subtype','by_subtype'),('group','by_group')]:
        for val in sorted({e[key] for e in es}):
            ix=np.array([e[key]==val for e in es]);result[target][val]=metrics(y[ix],p[ix],low,high)
    pr,re,th=precision_recall_curve(y,p)
    write(which+'/precision_recall.json',{'precision':pr.tolist(),'recall':re.tolist(),'thresholds':th.tolist()})
    write(which+'/predictions.json',[{'event_id':e['id'],'probability_score_not_calibrated':float(v),'truth':e['ride'],'decision':'RIDE_COMPATIBLE' if v>=high else ('NOT_RIDE_COMPATIBLE' if v<=low else 'ABSTAIN')} for e,v in zip(es,p)])
    return result
def dev():
    assert not (OUT/'enst/inventory.json').exists(),'No overwriting real results'
    write('execution_binding.json',{'implementation_sha256':digest(__file__),'protocol_sha256':digest(HERE/'PROTOCOL.md'),'environment':environment(),'phase':'BEFORE_ENST_FEATURES'})
    es,root=inventory('enst');X,es=features('enst',es,root)
    splits=np.array([e['split'] for e in es]);y=np.array([e['ride'] for e in es])
    for split in ['train','calibration','development_evaluation']:assert len(np.unique(y[splits==split]))==2,split+' missing class'
    train=splits=='train';cal=splits=='calibration';test=splits=='development_evaluation'
    scaler=StandardScaler().fit(X[train])
    with warnings.catch_warnings():
        warnings.simplefilter('error',ConvergenceWarning)
        model=LogisticRegression(C=1,class_weight='balanced',solver='lbfgs',max_iter=2000,tol=1e-6).fit(scaler.transform(X[train]),y[train])
    params={'mean':scaler.mean_,'scale':scaler.scale_,'coef':model.coef_[0],'intercept':model.intercept_[0]}
    cp=scores(X[cal],params)
    high=max(.5,float(np.nextafter(np.max(cp[~y[cal]]),np.inf)));low=min(.5,float(np.nextafter(np.min(cp[y[cal]]),-np.inf)))
    np.savez(OUT/'enst/model.npz',**params)
    tes=[e for e in es if e['split']=='development_evaluation'];p=scores(X[test],params)
    result=evaluate('enst',tes,p,low,high)
    works=(result['balanced_accuracy']>.5 and result['AP']>result['prevalence'] and result['ride_vs_hihat']['balanced_accuracy'] is not None and result['ride_vs_hihat']['balanced_accuracy']>.5 and result['ride_vs_hihat']['AP']>result['ride_vs_hihat']['prevalence'])
    result.update({'outcome':'ENST_CONTROLLED_DISCRIMINATION_WORKS' if works else 'ENST_CONTROLLED_DISCRIMINATION_FAILS','low':low,'high':high,'training_counts':dict(collections.Counter(e['subtype'] for e in es if e['split']=='train')),'calibration_counts':dict(collections.Counter(e['subtype'] for e in es if e['split']=='calibration')),'model_iterations':model.n_iter_.tolist(),'calibration_result':metrics(y[cal],cp,low,high)})
    write('enst/result.json',result)
    if works:
        write('freeze.json',{'implementation_sha256':digest(__file__),'protocol_sha256':digest(HERE/'PROTOCOL.md'),'model_sha256':digest(OUT/'enst/model.npz'),'ENST_result_sha256':digest(OUT/'enst/result.json'),'ENST_manifest_sha256':digest(ENST/'authority/admission_manifest.json'),'MDB_manifest_sha256':'3c66085a119419d21d8268b8aac37f8bc16cb613c399af825d7b248c87d92421','environment':environment(),'low':low,'high':high,'MDB_NOT_EXECUTED_AT_FREEZE':True})
    print(json.dumps({k:v for k,v in result.items() if k not in ['by_subtype','by_group','training_counts','calibration_counts']},indent=2),flush=True)
def validate():
    f=json.loads((OUT/'freeze.json').read_text())
    assert f['implementation_sha256']==digest(__file__) and f['protocol_sha256']==digest(HERE/'PROTOCOL.md')
    assert f['environment']==environment() and f['model_sha256']==digest(OUT/'enst/model.npz')
    assert f['ENST_result_sha256']==digest(OUT/'enst/result.json')
    es,root=inventory('mdb');X,es=features('mdb',es,root)
    params=dict(np.load(OUT/'enst/model.npz'));p=scores(X,params)
    result=evaluate('mdb',es,p,f['low'],f['high'])
    if result['balanced_accuracy'] is None:outcome='INSUFFICIENT_EVIDENCE'
    else:outcome='ENST_CONTROLLED_DISCRIMINATION_WORKS_MDB_TRANSFER_SUPPORTED' if (result['balanced_accuracy']>.5 and result['AP']>result['prevalence'] and result['ride_vs_hihat']['balanced_accuracy'] is not None and result['ride_vs_hihat']['balanced_accuracy']>.5 and result['ride_vs_hihat']['AP']>result['ride_vs_hihat']['prevalence']) else 'ENST_CONTROLLED_DISCRIMINATION_WORKS_MDB_TRANSFER_FAILS'
    result['outcome']=outcome;result['freeze_sha256']=digest(OUT/'freeze.json');write('mdb/result.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['by_subtype','by_group']},indent=2),flush=True)
def test():
    assert subtype('rc2','001_hits_ride_sticks_x5')=='RIDE_UNSPECIFIED'
    assert subtype('chh','007_hits_pedal-hi-hat-close_pedal_x1')=='HH_PEDAL_CLOSED'
    assert subtype('ohh','007_hits_hi-hat_sticks_x5')=='HH_OPEN'
    assert subtype('cr1','001_hits_crash_sticks_x5')=='OTHER_cr1'
    assert subtype('c4','015_hits_ride-cymbal-2_sticks_x5')=='UNRESOLVED_GENERIC_CYMBAL'
    assert eligible([.5,.5],0,2)=='OTHER_ONSET_IN_WINDOW'
    assert eligible([.5,.6],1,2)=='OTHER_ONSET_IN_WINDOW'
    assert eligible([.5,1.],0,2) is None
    assert eligible([.01],0,2)=='BOUNDARY'
    x=np.random.default_rng(1).normal(size=44100);a=patch(x,.5);b=patch(x*7,.5)
    assert a.shape==(832,) and np.allclose(a,b,rtol=1e-6,atol=1e-6)
    assert patch(np.zeros(44100),.5) is None
    print('11 synthetic ENST mapping/eligibility/representation checks PASS')
if __name__=='__main__':
    if sys.argv[1]!='test':OUT.mkdir(parents=True,exist_ok=True)
    {'test':test,'enst':dev,'mdb':validate}[sys.argv[1]]()
