import numpy as np

def metrics(rows):
 x=np.array([r['signed_error_ms'] for r in rows if r['signed_error_ms'] is not None]); n=len(x)
 if not n:return {'N':0}
 a=abs(x)
 return {'N':n,'median_signed_ms':float(np.median(x)),'mean_signed_ms':float(np.mean(x)),'median_absolute_ms':float(np.median(a)),'IQR_signed_ms':float(np.percentile(x,75)-np.percentile(x,25)),'P95_absolute_ms':float(np.percentile(a,95)),'maximum_absolute_ms':float(max(a)),'minimum_ms':float(min(x)),'maximum_ms':float(max(x)),**{f'within_{k}_ms_pct':float(100*np.mean(a<=k)) for k in [5,10,20,30,50]},'interval_counts':{v:sum(r.get('interval_relation')==v for r in rows) for v in ['BEFORE','INSIDE','AFTER']}}
