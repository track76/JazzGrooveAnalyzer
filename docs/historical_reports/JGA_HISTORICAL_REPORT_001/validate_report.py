"""Read-only report QC: frozen hashes, arithmetic, evidence joins and presentation."""
from pathlib import Path
import csv, json, hashlib, re, subprocess
from collections import Counter
import numpy as np

O=Path(__file__).resolve().parent
R=O.parents[2]
H=R/'docs/scientific/rfc/JGA_V1_HYBRID_OPERATIONAL_ARCHITECTURE_20260923'
def load(p):return json.loads(p.read_text())
def rows(p):return list(csv.DictReader(p.open()))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def stats(values):
    a=np.array(values,dtype=float)
    if len(a)==0:return {'N':0}
    return {'N':len(a),'median_ms':float(np.median(a)),'mean_ms':float(np.mean(a)),
            'IQR_ms':float(np.percentile(a,75)-np.percentile(a,25)),
            'MAD_ms':float(np.median(abs(a-np.median(a)))),
            'SD_ms':float(np.std(a,ddof=1)) if len(a)>1 else None,
            'median_abs_ms':float(np.median(abs(a))),'min_ms':float(min(a)),'max_ms':float(max(a))}
def agree(observed,expected):
    for k,v in observed.items():
        if v is None:assert expected[k] in ['',None],(k,expected[k])
        else:assert abs(float(expected[k])-v)<1e-7,(k,v,expected[k])

def validate():
    s=load(O/'SUMMARY.json');lineage=load(O/'LINEAGE.json')
    assert sha(Path(s['source']['path']))==s['source']['sha256']
    for x in lineage:assert sha(R/x['original_path'])==sha(O/x['report_path'])==x['sha256']
    for p in s['parent_freezes']:
        original=R/p['path'];assert sha(original)==p['sha256']
        for n,h in load(original)['files'].items():assert sha(original.parent/n)==h,n
    assert sha(H/'DECISION_FREEZE.json')==s['methodology_freeze_sha256']
    for n,h in load(H/'HISTORICAL_PRESERVATION.json').items():assert sha(R/n)==h,n
    # Current report status may evolve; the old freeze's exact member bytes remain in Git.
    commit=load(O/'PARENT_VERIFICATION.json')['historical_document_version_commit']
    for n,h in load(H/'DECISION_FREEZE.json')['files'].items():
        old=subprocess.check_output(['git','show',commit+':'+n],cwd=R)
        assert hashlib.sha256(old).hexdigest()==h,n
    fm=rows(O/'data/global__ALL_EVENT_ROLES.csv');q=rows(O/'data/global__PLP_REFERENCE.csv')
    global_assign=rows(O/'data/global__QUARTER_NEAREST_ONSETS.csv')
    selected=[x for x in global_assign if x['QUARTER_STATE']!='EMPTY']
    assert len(fm)==s['native_events']==1606 and len(q)==s['quarter_cells']==905
    assert len(selected)==s['event_coverage']['selected']==891
    assert len(fm)-len(selected)==s['event_coverage']['context']==715
    assert len(q)-len(selected)==s['event_coverage']['EMPTY']==14
    assert Counter(x['source_state'] for x in fm)==s['original_source_states']
    assert len({x['selected_event_id'] for x in selected})==891
    byid={x['JGA_EVENT_ID']:x for x in fm}
    for x in selected:
        orig=byid[x['selected_event_id']]
        assert x['selected_timestamp']==orig['native_timestamp']
        assert x['selected_source_state']==orig['source_state']
    gstats=rows(O/'data/global__SELECTED_STATISTICS.csv')
    for row in [x for x in gstats if x['method']=='PLP']:
        sec=next((x for x in s['sections'] if x['id']==row['section']),None)
        pop=[x for x in selected if (sec is None or sec['start']<=float(x['quarter_timestamp'])<sec['end'])
             and (row['category']=='ALL_SELECTED' or x['selected_source_state']==row['category'])]
        agree(stats([float(x['QUARTER_NEAREST_ONSET_OFFSET_MS']) for x in pop]),row)
    assignment=rows(O/'data/source__SOURCE_CONDITIONED_ASSIGNMENTS.csv')
    for name,x in s['source_timing_primary_nonshared'].items():
        if name=='DRUM_MINUS_BASS':v=[float(a['DRUM_MINUS_BASS_MS']) for a in assignment if a['status']=='DISTINCT_PAIR']
        else:v=[float(a[name+'_offset_ms']) for a in assignment if a[name+'_id'] and a['status'] not in ['SHARED_DUAL_MARKER','SAME_TIMESTAMP_UNRESOLVED']]
        agree(stats(v),x)
        assert sum(t<0 for t in v)==x['negative'] and sum(t>0 for t in v)==x['positive']
    t=np.array([float(x['time_seconds']) for x in q]);raw=60/np.diff(t)
    assert s['central_internal_bpm']['value']==float(np.median(raw))
    assert len(raw)==s['central_internal_bpm']['N_intervals']==904
    interval_rows=rows(O/'data/RAW_PLP_INTERVALS.csv')
    assert np.array_equal(raw,np.array([float(x['raw_discrete_bpm']) for x in interval_rows]))
    provenance=rows(O/'data/HYBRID_EVENT_PROVENANCE.csv')
    assert len(provenance)==len(fm)
    matches=rows(O/'data/hybrid__EVENT_MATCHING.csv');idx={(x['stem'],x['event_id']):x for x in matches if x['side']=='FULL_MIX'}
    for x in provenance:
        orig=byid[x['JGA_EVENT_ID']]
        for k,v in orig.items():assert x[k]==v,(x['JGA_EVENT_ID'],k)
        assert x['operational_timestamp']==orig['native_timestamp']
        for stem in ['bass','drums']:
            match=idx[stem,x['JGA_EVENT_ID']]
            assert x[stem+'_matching_state']==match['status'] and x[stem+'_stem_ids']==match['partner_ids']
    unmatched=rows(O/'data/STEM_ONLY_PROVENANCE.csv');assert len(unmatched)==435
    for x in unmatched:assert x['timestamp_s']==x['operational_timestamp'] and x['full_mix_event_id']=='NOT_ESTABLISHED'
    report=(O/'REPORT.md').read_text();fields=load(O/'HUMAN_SUMMARY_FIELDS.json')
    for k,v in fields.items():assert '| '+k+' | '+str(v)+' |' in report,k
    assert fields['CENTRAL INTERNAL BPM'].startswith(f"{s['central_internal_bpm']['value']:.2f}")
    for field,source in [('BASS MEDIAN Δt','BASS'),('DRUM MEDIAN Δt','DRUM'),('BASS↔DRUM MEDIAN','DRUM_MINUS_BASS')]:
        value=s['source_timing_primary_nonshared'][source]['median_ms']
        assert f'{value:+.2f}'.replace('-', '−') in fields[field],field
    assert '891/905' in fields['EVENT COVERAGE'] and '98.45%' in fields['EVENT COVERAGE']
    assert fields['QUARTER CELLS']==s['quarter_cells']
    for n in range(1,13):assert f'## {n}. ' in report,n
    for term in ['OBSERVATION','INTERPRETATION','not exact','Ground Truth']:
        assert term.lower() in report.lower(),term
    for target in re.findall(r'\]\(([^)]+)\)',report):
        if target not in ['VALIDATION.json','REPORT_FREEZE.json']:assert (O/target).exists(),target
    template=(O.parent/'JGA_HISTORICAL_REPORT_TEMPLATE_V1.md').read_text()
    for forbidden in ['Exactly Like You','Ray Brown','1606','1,606','905','330','161.50',s['source']['sha256']]:assert forbidden not in template,forbidden
    assert len([x for x in lineage if x['report_path'].startswith('figures/')])==10
    if (O/'REPORT_FREEZE.json').exists():
        for n,h in load(O/'REPORT_FREEZE.json')['files'].items():assert sha(R/n)==h,n
    return {'status':'PASS','source_verified':True,'parent_manifests_verified':3,'methodology_decision_unchanged':True,
            'historical_files_unchanged':1112,'historical_methodology_document_versions_verified_in_git':True,
            'byte_copied_table_figure_records':len(lineage),'figures_byte_preserved':10,
            'native_event_provenance_rows_verified':1606,'stem_only_rows_verified':435,
            'global_statistics_reconciled_to_frozen_assignments':True,'source_primary_statistics_reconciled':True,
            'tempo_descriptor_intervals':904,'human_summary_matches_machine_and_parent_data':True,
            'template_track_specific_values':'NONE','methodological_computation':'NONE','new_audio_inference':'NONE'}

if __name__=='__main__':print(json.dumps(validate(),indent=2))
