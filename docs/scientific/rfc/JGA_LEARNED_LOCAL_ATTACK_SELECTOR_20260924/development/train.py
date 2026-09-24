from pathlib import Path
import json,numpy as np,soundfile as sf,csv,joblib,datetime
from selector import *
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
W=Path(__file__).resolve().parent;O=W/'output';check_isolation(W);records=generate(W)
gt=json.loads((W/'input/GT_DEVELOPMENT.json').read_text());dur={m['clip_id']:sf.info(W/'input'/m['audio']).duration for m in json.loads((W/'input/MANIFEST.json').read_text())};ass=associate(records,gt,dur);resolved=[a for a in ass if a['record']];report={'GT_events':len(gt),'recognized_unique':len(resolved),'window_GT_coverage':sum(a['record']['search_start_s']<=float(a['GT']['final_center_s'])<=a['record']['search_end_s'] for a in resolved)}
for k in [5,10,20]:report[f'candidate_covered_{k}ms']=sum(any(abs(c['time_s']-float(a['GT']['final_center_s']))<=k/1000 for c in a['record']['candidates']) for a in resolved)
counts=[len(a['record']['candidates']) for a in resolved];report['candidate_count']={'mean':float(np.mean(counts)),'min':min(counts),'Q25':float(np.percentile(counts,25)),'median':float(np.median(counts)),'Q75':float(np.percentile(counts,75)),'max':max(counts)};save(O/'CANDIDATE_COVERAGE.json',report);print('COVERAGE',report,flush=True)
if report['candidate_covered_20ms']!=len(resolved):save(O/'STOP.json',{'reason':'Candidate coverage gate failed'});raise SystemExit(0)
X=[];y=[];weights=[];groups=[];labels={};types={}
for a in resolved:
 g=a['GT'];lo=float(g['final_earliest_s']);hi=float(g['final_latest_s'])
 for c in a['record']['candidates']:
  t=c['time_s'];inside=lo<=t<=hi;near=(lo-.005<=t<=hi+.005);kind='INTERVAL_COMPATIBLE' if inside else 'NEAR_INTERVAL_PROXY' if near else 'NEGATIVE';labels[c['candidate_id']]=kind;types[kind]=types.get(kind,0)+1;X.append(c['features']);y.append(int(near));weights.append(1 if inside or not near else .5);groups.append(g['clip_id'])
X=np.array(X);y=np.array(y);weights=np.array(weights);groups=np.array(groups)
with (O/'DEVELOPMENT_CANDIDATES.csv').open('w',newline='') as f:
 fields=['clip_id','BP_id','candidate_id','time_s','label']+FEATURES;w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in records:
  for c in r['candidates']:w.writerow({'clip_id':r['clip_id'],'BP_id':r['BP']['native_note_id'],'candidate_id':c['candidate_id'],'time_s':c['time_s'],'label':labels.get(c['candidate_id'],'UNLABELLED_BP_CORRESPONDENCE'),**dict(zip(FEATURES,c['features']))})
def build(name):
 return make_pipeline(StandardScaler(),LogisticRegression(C=.1 if name=='LOGISTIC_C0.1' else 1,class_weight='balanced',max_iter=2000,random_state=24)) if name.startswith('LOGISTIC') else make_pipeline(StandardScaler(),DecisionTreeClassifier(max_depth=3,min_samples_leaf=5,class_weight='balanced',random_state=24))
def fit(model,mask):
 key=list(model.named_steps)[-1]+'__sample_weight';model.fit(X[mask],y[mask],**{key:weights[mask]});return model
results=[]
for name in ['LOGISTIC_C0.1','LOGISTIC_C1','TREE_DEPTH3_LEAF5']:
 scores={th:[] for th in [.5,.75]};cv=[]
 for clip in sorted(set(groups)):
  model=fit(build(name),groups!=clip)
  for a in resolved:
   if a['GT']['clip_id']!=clip:continue
   for th in scores:
    d=decide(a['record'],model,th);e=(d['selected_s']-float(a['GT']['final_center_s']))*1000 if d['selected_s'] is not None else None
    if e is not None:scores[th].append(e)
    cv.append({'GT_id':a['GT']['event_id'],'threshold':th,'status':d['status'],'error_ms':e})
 for th,errs in scores.items():results.append({'model':name,'threshold':th,'metrics':metrics(errs,len(resolved))})
 save(O/f'CV_{name}.json',cv)
chosen=sorted(enumerate(results),key=lambda pair:(-pair[1]['metrics']['useful_yield_10_pct'],pair[1]['metrics'].get('P95_absolute_ms',1e9),pair[0]))[0][1];model=fit(build(chosen['model']),np.ones(len(X),bool));joblib.dump(model,O/'MODEL.joblib');save(O/'CV_RESULTS.json',results)
last=model.steps[-1][1];params={'features':FEATURES,'scaler_mean':model.steps[0][1].mean_.tolist(),'scaler_scale':model.steps[0][1].scale_.tolist(),'model':chosen['model'],'threshold':chosen['threshold'],'window_half_s':.15,'label_counts':types,'chosen_cv':chosen}
if hasattr(last,'coef_'):params.update(coefficients=last.coef_.tolist(),intercept=last.intercept_.tolist())
else:params['tree']={k:getattr(last.tree_,k).tolist() for k in ['children_left','children_right','feature','threshold','value']}
save(O/'SELECTOR_RULE.json',params)
files=[O/'SELECTOR_RULE.json',O/'MODEL.joblib',O/'CV_RESULTS.json',O/'CANDIDATE_COVERAGE.json',W/'selector.py',W/'morphology.py',W/'train.py'];save(O/'SELECTOR_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{str(p.relative_to(W)):sha(p) for p in files}});print('FROZEN',chosen,flush=True)
