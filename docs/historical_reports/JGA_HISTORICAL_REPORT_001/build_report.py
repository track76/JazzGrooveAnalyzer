"""Report-only assembly from frozen tables; no audio inference or reselection."""
from pathlib import Path
import csv, json, hashlib, shutil, statistics, subprocess
from collections import Counter
import numpy as np

O=Path(__file__).resolve().parent
R=O.parents[2]
RFC=R/'docs/scientific/rfc'
G=RFC/'JGA_V1_OPERATIONAL_PLP_QUARTER_NEAREST_001_20260922'
C=RFC/'JGA_QUARTER_CENTERED_BASS_DRUM_GEOMETRY_001_20260923'
S=RFC/'JGA_FULLMIX_VS_STEMS_GEOMETRY_001_20260923'
H=RFC/'JGA_V1_HYBRID_OPERATIONAL_ARCHITECTURE_20260923'
def load(p): return json.loads(p.read_text())
def rows(p): return list(csv.DictReader(p.open()))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def put(n,x):
    with (O/n).open('x') as f:json.dump(x,f,indent=2,allow_nan=False);f.write('\n')
def csvout(n,rr):
    with (O/n).open('x',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rr[0]),lineterminator='\n');w.writeheader();w.writerows(rr)
def numeric(row):
    out={}
    for k,v in row.items():
        if v=='':out[k]=None
        else:
            try:out[k]=float(v)
            except ValueError:out[k]=v
    return out
def fmt(v):return 'NOT AVAILABLE' if v is None else f'{v:+.2f}'
def table(headers,rr):
    return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(str(x) for x in row)+' |\n' for row in rr)

parents=[]
for p,expect in [(G,'02b603c6c641b6eb6453bcb39362269710be7f58853a99e18be09ba9915fa6ab'),(C,'6482feb0820ddd929b292fb4a0393d4f9eebf30e2fe00bcfeb86023de011231e'),(S,'079633a7869b2c22827e6c7ee28b8477fe9d50077826b4097313e36684ec9d08')]:
    manifest=p/'RESULT_FREEZE.json';assert sha(manifest)==expect
    for n,h in load(manifest)['files'].items():assert sha(p/n)==h,n
    parents.append({'path':str(manifest.relative_to(R)),'sha256':expect,'members_verified':len(load(manifest)['files'])})
assert sha(H/'DECISION_FREEZE.json')=='d7a51678fc4b8424872b55a73a964c8ccd818d146d13bcb3e24f30b450fd01cf'
for n,h in load(H/'DECISION_FREEZE.json')['files'].items():assert sha(R/n)==h,n
for n,h in load(H/'HISTORICAL_PRESERVATION.json').items():assert sha(R/n)==h,n
source=load(S/'SEPARATION_RESULT.json')['source'];assert sha(Path(source['path']))==source['sha256']
for asset in load(S/'SEPARATION_RESULT.json')['stems']:assert sha(Path(asset['path']))==asset['sha256']
(O/'data').mkdir();(O/'figures').mkdir();lineage=[]
def copy(p,dest):
    shutil.copyfile(p,O/dest)
    lineage.append({'original_path':str(p.relative_to(R)),'report_path':dest,'sha256':sha(p),'transformation':'NONE_BYTE_COPY'})
for p,names,prefix in [
 (G,['RESULT_FREEZE.json','PLP_REFERENCE.csv','ALL_EVENT_ROLES.csv','QUARTER_CELLS.csv','QUARTER_NEAREST_ONSETS.csv','QUARTER_CONTEXT_EVENTS.csv','SELECTED_STATISTICS.csv','SECTIONS.json','CONFIGURATION.json','INPUT_LINEAGE.json'],'global'),
 (C,['RESULT_FREEZE.json','SOURCE_CONDITIONED_ASSIGNMENTS.csv','SOURCE_CANDIDATES.csv','TIMING_STATISTICS.csv','SECTION_COVERAGE.csv','CONFIGURATION.json'],'source'),
 (S,['RESULT_FREEZE.json','EVENT_MATCHING.csv','UNIQUE_MATCHES.csv','MATCHING_EDGES.csv','BASS_EVENTS.csv','DRUMS_EVENTS.csv','STEM_ASSIGNMENTS.csv','STEM_EVENT_ROLES.csv','STEM_PAIRS.csv','DUAL_AUDIT.csv','SECTION_COMPARISON.csv','STATISTICS.csv','SUMMARY.json','SEPARATION_RESULT.json','PREREGISTRATION.json'],'hybrid')]:
    for n in names:copy(p/n,'data/'+prefix+'__'+n)
copy(H/'DECISION_FREEZE.json','data/JGA_V1_DECISION_FREEZE.json')
figs=[(C,'REVISED_GLOBAL_SOURCE_SHAPED_CONTEXT','FIGURE_1_GLOBAL'),(C,'SOURCE_CONDITIONED_WHOLE','FIGURE_2_SOURCE_CONDITIONED'),(S,'FULLMIX_VS_STEMS','FIGURE_3_HYBRID'),(C,'SOURCE_CONDITIONED_ZOOM','FIGURE_4_REFERENCE_ZOOM'),(S,'PIANO_BASS_EXCHANGES','FIGURE_5_PIANO_BASS')]
for p,n,dest in figs:
    for ext in ['png','pdf']:copy(p/(n+'.'+ext),'figures/'+dest+'.'+ext)

fm=rows(G/'ALL_EVENT_ROLES.csv');matches=rows(S/'EVENT_MATCHING.csv');unique=rows(S/'UNIQUE_MATCHES.csv')
idx={(x['stem'],x['event_id']):x for x in matches if x['side']=='FULL_MIX'}
links={(x['stem'],x['full_mix_id']):x for x in unique}
provenance=[]
for x in fm:
    y=dict(x,operational_timestamp=x['native_timestamp'],timestamp_origin='ORIGINAL_FULL_MIX_NATIVE',physical_attack_accuracy='NOT_ESTABLISHED',source_asset_sha256=source['sha256'])
    for k in ['bass','drums']:
        m=idx[k,x['JGA_EVENT_ID']];edge=links.get((k,x['JGA_EVENT_ID']))
        supported=x['source_state'] in (['BASS_SUPPORTED','BASS_AND_DRUM_SUPPORTED'] if k=='bass' else ['DRUM_SUPPORTED','BASS_AND_DRUM_SUPPORTED'])
        y[k+'_matching_state']=m['status'];y[k+'_stem_ids']=m['partner_ids']
        y[k+'_complementary_support']='SEPARATOR_DERIVED' if edge else 'NOT_ESTABLISHED'
        y[k+'_provenance_class']='FULL-MIX + STEM CONFIRMED' if edge else ('FULL-MIX SOURCE-SUPPORTED ONLY' if supported and m['status']=='FULL_MIX_ONLY' else 'UNKNOWN / AMBIGUOUS')
        y[k+'_original_source_support_agrees']=supported
        y[k+'_evidence_note']='Compatible native observability plus separator hypothesis; not independent identity truth. Original source state is retained.' if edge else 'No compatible separator support established; retain original source evidence.'
        y[k+'_FM_minus_stem_ms']=edge['FM_MINUS_STEM_ms'] if edge else ''
    provenance.append(y)
csvout('data/HYBRID_EVENT_PROVENANCE.csv',provenance)
stem_only=[]
for k in ['bass','drums']:
    only={x['event_id'] for x in matches if x['stem']==k and x['side']=='STEM' and x['status']=='STEM_ONLY'}
    for x in rows(S/(k.upper()+'_EVENTS.csv')):
        if x['event_id'] in only:stem_only.append(dict(x,provenance='SEPARATOR_DERIVED / STEM_ONLY',operational_timestamp=x['timestamp_s'],timestamp_origin='SEPARATOR_STEM',full_mix_event_id='NOT_ESTABLISHED'))
csvout('data/STEM_ONLY_PROVENANCE.csv',stem_only)

q=rows(G/'PLP_REFERENCE.csv');t=np.array([float(x['time_seconds']) for x in q]);intervals=np.diff(t);bpm=60/intervals
tempo={'value':float(np.median(bpm)),'units':'BPM','statistic':'median raw/discrete inter-reference interval BPM','N_intervals':len(intervals),'formula':'median(60 / diff(frozen_reference_seconds)); only adjacent references inside [0,330)','range':[float(bpm.min()),float(bpm.max())],'mean_raw_interval_bpm':float(bpm.mean()),'aggregate_reference_rate_bpm':float(60*len(intervals)/(t[-1]-t[0])),'qualification':'Timestamp-lattice affected; not continuous performer tempo or a new tempo estimate'}
csvout('data/RAW_PLP_INTERVALS.csv',[{'left_reference_index':i,'left_seconds':float(t[i]),'right_seconds':float(t[i+1]),'interval_seconds':float(v),'raw_discrete_bpm':float(bpm[i])} for i,v in enumerate(intervals)])
gs=rows(G/'SELECTED_STATISTICS.csv');cs=rows(C/'TIMING_STATISTICS.csv');coverage=rows(C/'SECTION_COVERAGE.csv');hybrid=rows(S/'SECTION_COMPARISON.csv');sections=load(G/'SECTIONS.json')
global_whole=[numeric(x) for x in gs if x['method']=='PLP' and x['section']=='WHOLE']
source_stats={k:numeric(next(x for x in cs if x['section']=='WHOLE' and x['source']==k and x['cohort']==('DISTINCT_PAIRS_ONLY' if k=='DRUM_MINUS_BASS' else 'PRIMARY_NONSHARED'))) for k in ['BASS','DRUM','DRUM_MINUS_BASS']}
section_table=[]
for sec in sections:
    a=numeric(next(x for x in gs if x['method']=='PLP' and x['section']==sec['id'] and x['category']=='ALL_SELECTED'))
    c=numeric(next(x for x in coverage if x['section']==sec['id']));h=numeric(next(x for x in hybrid if x['section']==sec['id']))
    section_table.append(dict(sec,global_statistics=a,source_coverage=c,hybrid_coverage=h))
counts=Counter(x['source_state'] for x in fm);union={x['full_mix_id'] for x in unique}
confirmed={x['full_mix_id'] for x in unique if x['full_mix_state'] in (['BASS_SUPPORTED','BASS_AND_DRUM_SUPPORTED'] if x['stem']=='bass' else ['DRUM_SUPPORTED','BASS_AND_DRUM_SUPPORTED'])}
summary={'schema':'JGA_HISTORICAL_REPORT_SUMMARY_v1','template':'JGA HISTORICAL REPORT TEMPLATE v1','report_id':'JGA HISTORICAL REPORT 001','artist_ensemble':'Ray Brown Trio','track':'Exactly Like You','source':source,'bibliography':{'album':None,'session_date':None,'personnel':None,'label':None,'status':'NOT AVAILABLE in the evidence assembled for this report; later bibliographic enrichment'},'duration_seconds':source['frames']/source['sample_rate'],'analyzed_region_seconds':[0,330],'analyzed_duration_seconds':330,'excluded_region_seconds':[330,source['frames']/source['sample_rate']],'primary_meter_domain':{'value':'4/4','authority':'PI operational recording/domain annotations; not inferred from onset geometry'},'central_internal_bpm':tempo,'quarter_cells':905,'native_events':1606,'event_coverage':{'selected':891,'denominator_cells':905,'percent':891/905*100,'context':715,'EMPTY':14},'original_source_states':dict(counts),'Bass_observability':{'inclusive_native_events':205,'covered_cells':203,'denominator_cells':905,'primary_nonshared_N':23,'stem_events':827,'stem_covered_cells':672},'Drum_observability':{'inclusive_native_events':1091,'covered_cells':834,'denominator_cells':905,'primary_nonshared_N':654,'stem_events':1227,'stem_covered_cells':868},'dual_ambiguity':{'native_Dual_events':196,'native_denominator':1606,'native_Dual_percent':196/1606*100,'shared_Dual_cells':180,'cell_denominator':905,'shared_Dual_percent':180/905*100,'shared_without_distinct_alternative':135,'distinct_selected_fullmix_pairs':21,'UNKNOWN_events':506,'UNKNOWN_native_percent':506/1606*100,'ambiguous_temporal_matches':0,'qualification':'No ambiguous temporal match does not mean no source-identity uncertainty'},'source_timing_primary_nonshared':source_stats,'global_timing_statistics':global_whole,'sections':section_table,'hybrid_provenance':{'unique_native_events_matched_to_any_stem':len(union),'unique_native_events_with_original_source_support_and_corresponding_stem':len(confirmed),'Bass_supported_matches':148,'Drum_supported_matches':923,'Bass_supported_fullmix_only':57,'Drum_supported_fullmix_only':168,'Bass_stem_only':279,'Drum_stem_only':156,'Bass_all_state_matches':548,'Drum_all_state_matches':1071,'native_timestamps_preferred':True,'original_source_states_unchanged':True,'geometry':'Frozen original-support geometry reused; additive evidence join is not relabelled/reselected geometry'},'narrowest_dispersion':{'section':'Final theme / turnaround','statistic':'global ALL_SELECTED IQR','IQR_ms':next(x['global_statistics']['IQR_ms'] for x in section_table if x['id']=='M56')},'widest_dispersion':{'section':'Piano–Drum exchanges','statistic':'global ALL_SELECTED IQR','IQR_ms':next(x['global_statistics']['IQR_ms'] for x in section_table if x['id']=='M4')},'primary_musical_observation':'Piano–Drum exchanges show the widest selected-landmark dispersion; final theme/turnaround the narrowest. This is reference-dependent observable geometry, not performer intention.','primary_limitation':'Sparse non-shared Bass support and shared Dual ambiguity constrain Bass–Drum interpretation; stem labels are not independent identity truth.','methodology_changed':False,'methodology_freeze_sha256':sha(H/'DECISION_FREEZE.json'),'parent_freezes':parents}
put('SUMMARY.json',summary);put('LINEAGE.json',lineage)
put('PARENT_VERIFICATION.json',{'source':'PASS','six_stem_assets':'PASS','parent_manifests':parents,'v1_decision_sha256':sha(H/'DECISION_FREEZE.json'),'v1_members_verified_before_current_status_update':True,'historical_files_verified':1112,'historical_document_version_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'note':'Later authorized current project/session/bootstrap completion entries do not rewrite the frozen decision or its historical document version.'})

form=table(['Section','Start–end (s)','Independent PI description'],[[s['label'],f"{s['start']}–{s['end']}",s['label']] for s in sections])
population=table(['Original full-mix state','Native events','Global selected'],[['Bass only',9,3],['Drum only',895,593],['Dual (one timestamp)',196,174],['UNKNOWN',506,121],['Total',1606,891]])
globaltab=table(['Global selected population','N','Median Δt ms','Mean ms','IQR ms','SD ms'],[[x['category'],int(x['N']),fmt(x['median_ms']),fmt(x['mean_ms']),f"{x['IQR_ms']:.2f}",f"{x['SD_ms']:.2f}"] for x in global_whole])
sourcetab=table(['Source-conditioned population','N','Median Δt ms','IQR ms','Negative / positive / exact'],[[k+' — '+x['cohort'],int(x['N']),fmt(x['median_ms']),f"{x['IQR_ms']:.2f}",f"{int(x['negative'])} / {int(x['positive'])} / {int(x['exact_zero'])}"] for k,x in source_stats.items()])
sectab=table(['Section','Selected / cells','Median ms','IQR ms','Bass / Drum covered cells','Distinct pairs'],[[s['label'],f"{int(s['global_statistics']['N'])}/{int(s['global_statistics']['reference_N'])}",fmt(s['global_statistics']['median_ms']),f"{s['global_statistics']['IQR_ms']:.2f}",f"{int(s['source_coverage']['Bass_covered'])} / {int(s['source_coverage']['Drum_covered'])}",int(s['source_coverage']['distinct_selected_pairs'])] for s in section_table])
hybtab=table(['Evidence count','Bass','Drum'],[['Original source-supported native events, inclusive',205,1091],['Corresponding stem-compatible support',148,923],['Source-supported full-mix-only',57,168],['Stem-only, unmatched to any native event',279,156],['All-state full-mix/stem matches',548,1071],['Stem events',827,1227],['Covered cells: full mix → stem','203 → 672','834 → 868']])
section_sources=table(['Section','Non-shared Bass N / median ms','Non-shared Drum N / median ms','Distinct pair N / Drum−Bass median ms'],[[s['label'],f"{int(s['source_coverage']['BASS_primary_N'])} / {fmt(s['source_coverage']['BASS_primary_median_ms'])}",f"{int(s['source_coverage']['DRUM_primary_N'])} / {fmt(s['source_coverage']['DRUM_primary_median_ms'])}",f"{int(s['source_coverage']['distinct_selected_pairs'])} / {fmt(s['source_coverage']['pair_median_ms'])}"] for s in section_table])
block=[['REPORT ID',summary['report_id']],['ARTIST / ENSEMBLE',summary['artist_ensemble']],['TRACK',summary['track']],['ANALYZED DURATION','330 s; [0,330)'],['PRIMARY METER DOMAIN','4/4 — PI operational domain'],['CENTRAL INTERNAL BPM',f"{tempo['value']:.2f}; median raw/discrete interval BPM, N=904"],['QUARTER CELLS',905],['EVENT COVERAGE','891/905 — 98.45%'],['BASS OBSERVABILITY','205 inclusive events; 203/905 cells; 23 non-shared observations; stem 672/905 cells'],['DRUM OBSERVABILITY','1,091 inclusive events; 834/905 cells; 654 non-shared observations; stem 868/905 cells'],['DUAL / AMBIGUITY RATE',f"196/1,606 native events ({196/1606*100:.2f}%); 180/905 shared cells ({180/905*100:.2f}%); 0 ambiguous temporal matches"],['BASS MEDIAN Δt','−34.83 ms; PRIMARY_NONSHARED N=23'],['DRUM MEDIAN Δt','+11.61 ms; PRIMARY_NONSHARED N=654'],['BASS↔DRUM MEDIAN','Drum − Bass +46.44 ms; 21 distinct selected pairs'],['SECTION WITH NARROWEST DISPERSION','Final theme / turnaround — global selected IQR 34.83 ms'],['SECTION WITH WIDEST DISPERSION','Piano–Drum exchanges — global selected IQR 69.66 ms'],['PRIMARY MUSICAL OBSERVATION',summary['primary_musical_observation']],['PRIMARY LIMITATION',summary['primary_limitation']]]
put('HUMAN_SUMMARY_FIELDS.json',dict(block))
report=f'''# JGA HISTORICAL REPORT 001

## Ray Brown Trio — “Exactly Like You”

**Historical jazz corpus analysis · JGA v1 · USABLE_WITH_QUALIFICATION**

This report consolidates completed, frozen evidence into the adopted historical-analysis format. No model, detector, separation or PLP execution was repeated. The findings describe observable onset geometry in this recording.

## 1. Recording identification

Artist/ensemble: **Ray Brown Trio**. Title: **Exactly Like You**. Original registered source: `{source['path']}`.

SHA-256: `{source['sha256']}`. Decoded duration: **{summary['duration_seconds']:.6f} s**; 44,100 Hz, two channels, 15,338,496 frames. Analysis: **[0,330) s**. Excluded free/open ending: **[330,{summary['duration_seconds']:.6f}) s**. The original commercial full mix remains primary; separator audio is a derived representation.

Album, session date, label and detailed personnel: **NOT AVAILABLE in the evidence assembled for this report**. These remain for later bibliographic enrichment; none is inferred from a filename or timing result. The report uses the PI's 4/4 operational scope, not a new meter analysis.

## 2. JGA analysis method — short form

JGA places a frozen PLP temporal ruler over the original full mix and measures the positions of existing native onset landmarks around it. Qualified source evidence supports Bass, generic Drum, Dual or UNKNOWN interpretations. Authorized Demucs stems provide complementary source evidence; they do not supply an independent tempo ruler or physical truth.

When a stem observation matches a native full-mix event under the frozen rule, the report's provenance layer retains the **full-mix timestamp**, original source support and complementary stem evidence separately. Unmatched stem observations remain SEPARATOR_DERIVED / STEM_ONLY. This is a join of existing evidence, not a new classifier: the frozen global and source-conditioned assignments below are reused without relabelling or reselection.

`Δt = observable source-associated onset − PLP temporal reference`. Negative is before; positive after. Neither coordinate is snapped. These are acoustic landmarks, not exact finger release or stick contact. No numerical ON tolerance is imposed.

## 3. Musical form

**Table 1. Independently supplied PI form map.** Boundaries are approximate listening annotations, preserved from the operational study; they were not inferred from timing geometry.

{form}

The final-theme/turnaround subdivision within 232–330 s is not independently resolved and is not invented here.

## 4. Internal tempo / PLP

The 905 frozen references yield 904 adjacent intervals entirely within the analysis domain. Their **median RAW / DISCRETE PLP INTER-PEAK BPM is {tempo['value']:.2f} BPM**. The raw interval range is {tempo['range'][0]:.2f}–{tempo['range'][1]:.2f} BPM; the aggregate reference rate over the first-to-last reference span is {tempo['aggregate_reference_rate_bpm']:.2f} BPM. These different summaries answer different arithmetic questions.

This is a central operational pulse-rate description, not a continuous reconstruction of performer tempo. Much short-scale jaggedness reflects the 512-sample timestamp lattice (approximately 11.61 ms at 44.1 kHz). The figures label this limitation explicitly; saw-tooth appearance is not evidence of alternating performer acceleration/deceleration. No smoothing or new tempo estimate was introduced. Exact interval arithmetic is preserved in `data/RAW_PLP_INTERVALS.csv`.

## 5. Observable event population

**Table 2. Original full-mix source states and global selection.**

{population}

905 reference cells contain **891 selected landmarks (98.45%)**, **14 EMPTY** and **715 non-selected CONTEXT events**. UNKNOWN remains eligible for selection. Inclusive native support is Bass **205 = 9 + 196** and Drum **1,091 = 895 + 196**; these counts overlap through Dual and must not be added as independent attacks.

The source-conditioned view covers **203 Bass cells** and **834 Drum cells**. Both support types occur in 201 cells: 21 have distinct selected timestamps, 180 share one Dual winner. Of the latter, 135 lack any distinct supported full-mix alternative. 69 cells contain neither source support.

The additive provenance join identifies **{len(union)} unique native events with at least one compatible stem observation** and **{len(confirmed)} unique native events whose original source support is also compatible with the corresponding stem**. These are compatibility counts, not independent identity validation. UNKNOWN remains 506 original events; no original state is overwritten. Zero ambiguous temporal matches does not mean zero source ambiguity.

## 6. Global quarter-nearest geometry

Each frozen midpoint-defined cell selects its nearest existing native onset. No event is borrowed or reused across cells. All other native events remain gray context, with source-specific shapes in this source-aware rendering.

![Figure 1. Whole-performance global quarter-nearest geometry.](figures/FIGURE_1_GLOBAL.png)

**Figure 1.** Byte-preserved source-aware global figure. Colored markers are global winners; light-gray markers retain source shapes. EMPTY and independent form boundaries retain the frozen styling. The raw/discrete PLP panel contains lattice effects, not a literal continuous tempo trace.

**Table 3. Global selected-landmark statistics.** Milliseconds; SD is sample SD. These populations differ from source-conditioned selections in section 7.

{globaltab}

All-selected MAD is 23.22 ms; median absolute displacement 23.22 ms; range −116.10 to +81.27 ms. Full category statistics, including MAD and ranges, are preserved in `data/global__SELECTED_STATISTICS.csv`. Only three global winners are Bass-only: losing global competition is not absence of Bass evidence.

## 7. Quarter-centered Bass / Drum geometry

Source-conditioned selection independently asks for the nearest Bass-supported and Drum-supported native event within the same cell. Shared Dual is one event, not two simultaneous attacks. Primary timing distributions exclude shared or same-timestamp unresolved winners; all-support slots are reported separately.

![Figure 2. Quarter-centered Bass and Drum geometry.](figures/FIGURE_2_SOURCE_CONDITIONED.png)

**Figure 2.** Frozen source-conditioned view. Additional source-supported observations can be visible even when they were gray context in the global view. Shared Dual and distinct pair semantics are preserved.

{sourcetab}

For the 21 distinct pairs, positive `Drum − Bass` means Bass precedes Drum: **14 positive, 7 negative**, median **+46.44 ms**, IQR **185.76 ms**. This small, dispersed subset does not support a universal ordering claim.

Including shared support changes the Bass population substantially: ALL_SUPPORT_SLOTS N=203 has median **+11.61 ms**, rather than the non-shared subset's −34.83 ms. Drum ALL_SUPPORT_SLOTS N=834 also has median +11.61 ms. Those shared slots are not independent timed attacks. The non-shared Bass tendency must not be generalized to all Bass activity.

## 8. Hybrid full-mix / stem evidence

**Table 5. Hybrid provenance and coverage.** Corresponding-support matches differ from matches to any full-mix state. Stem-only means no compatible native event, not independently verified new instrumental activity.

{hybtab}

Matching reuses the inclusive one-hop bound, **512 samples / 11.61 ms**, and mutual unique compatibility; no PLP-proximity filtering. Bass-stem matches comprise 6 Bass-only, 142 Dual, 312 Drum-only and 88 UNKNOWN full-mix events. Drums-stem matches comprise 2 Bass-only, 167 Dual, 756 Drum-only and 146 UNKNOWN. Additive separator hypotheses retain their provenance; different original support is not erased.

![Figure 3. Aligned full-mix and separated-stem comparison.](figures/FIGURE_3_HYBRID.png)

**Figure 3.** Both representations use the same frozen PLP ruler. Source-associated native timing remains primary when matched. Unmatched-event lanes do not prove physical absence.

Among 180 shared-Dual cells, stems show Bass only in 3, Drums only in 18, one distinguishable candidate per stem in 29, unresolved single candidates in 57, neither in 0, and multiple candidates in 73. The 29 distinguishable cases are diagnostic model-derived observations, not automatically two full-mix attacks. Full-mix Dual labels remain unchanged.

The stem Bass median is +23.22 ms (N=672 selected); stem Drum median +11.61 ms (N=868). Their 340 pairs resolved beyond one hop have Drum−Bass median −23.22 ms. These are different populations and representations from the 21 full-mix pairs, not a correction of them. Conditional matched full-mix-minus-stem medians are zero for both sources; the matching window truncates that distribution and cannot prove global timing preservation.

## 9. Section-by-section groove analysis

**Table 4a. Global selected distributions and original source coverage.** Quarter-level statistics use reference-time section membership; event-level provenance retains original event time.

{sectab}

**Table 4b. Non-shared source-conditioned and distinct-pair timing.** NOT AVAILABLE is missing support, not a zero-ms result.

{section_sources}

- **Opening:** selected median +23.22 ms, with 128/131 occupied cells. The eight non-shared Bass observations are sparse; their negative median and seven pair observations cannot define the whole ensemble's placement.
- **Piano / walking Bass:** global coverage is complete, median +11.61 ms. Bass support covers 82/257 cells, but only seven non-shared selections remain after shared Dual is excluded. The independent walking-Bass annotation is not a claim that every Bass note was identified.
- **Piano–Bass exchanges:** 124/125 global cells are occupied, yet original Bass support is zero. This is a source-support limitation, not evidence that Bass is absent. The Bass stem contains 159 onsets across 111/125 cells: 113 match non-Bass-supported native events and 46 are stem-only. Their identity remains separator-derived.
- **Piano–Drum exchanges:** widest global IQR, 69.66 ms; median −11.61 ms; ten EMPTY cells. The lone distinct Bass/Drum pair is insufficient for a section-level relationship claim. This is the least densely occupied global section (117/127).
- **Final theme / turnaround:** all 265 cells are occupied, with the narrowest global IQR, 34.83 ms, and median +11.61 ms. Six distinct pairs remain too few to establish a general ensemble timing law.

![Figure 4. Established source-conditioned reference zoom.](figures/FIGURE_4_REFERENCE_ZOOM.png)

**Figure 4.** Existing independently defined 122–128.5 s reference window in the piano/walking-Bass section. It was reused, not selected for favorable results. Original timestamps, selected roles, shared evidence and gray context remain intact.

![Figure 5. Piano–Bass exchange observability diagnostic.](figures/FIGURE_5_PIANO_BASS.png)

**Figure 5.** Existing 141–186 s comparison explains the gap between full-mix Bass support and separator-derived activity. More Bass-labelled activity does not independently establish true Bass identity or exclude piano leakage.

## 10. Musical interpretation

**OBSERVATION:** most global sections have modestly positive selected-landmark medians, while the Piano–Drum exchange section has a negative median and the widest distribution. Final-theme/turnaround landmarks occupy every cell with the narrowest spread. **INTERPRETATION:** the observable event field is more dispersed during the independently labelled exchanges and more concentrated relative to this ruler in the returning theme. Reference placement and nearest-selection geometry contribute; these are not claims about deliberate ahead/behind playing.

**OBSERVATION:** non-shared Bass selections lean negative (15/23), non-shared Drum selections positive (407/654), while shared-Dual inclusion changes the Bass median's sign. **INTERPRETATION:** a limited Bass-before/Drum-after pattern is visible in a small qualified subset, not a general characteristic of all instrumental attacks. The wide pair dispersion and different stem ordering argue against a stronger conclusion.

**OBSERVATION:** separator-derived Bass activity is present during Piano–Bass exchanges despite absent original Bass support. **INTERPRETATION:** the hybrid record makes a source-coverage blind spot visible. It does not establish whether each added candidate is Bass, leakage or another separator-dependent landmark. No performer intention, causal account of swing or universal jazz rule is inferred.

## 11. Limitations

Commercial full-mix landmarks have unquantified physical-attack uncertainty; they are not physical attack Ground Truth. Source states are qualified/provisional; generic Drum does not establish Ride or Hi-Hat. Separation may leak, suppress or alter activity, and STEM_ONLY is separate provenance. DUAL is unresolved shared support. The approximately 11.61-ms detector/reference lattice and nearest-selection geometry affect offsets and raw BPM; displayed decimal precision is arithmetic, not physical accuracy. No ON tolerance or numerical confidence interval is invented. Findings are recording-specific development evidence. Open ending and unavailable historical metadata remain explicit exclusions/gaps. The historical independent PLP FAIL is unchanged by the later bounded v1 operational adoption.

## 12. JGA result summary

{table(['Field','Value'],block)}

Exact numeric values, units and cohort definitions are in [SUMMARY.json](SUMMARY.json). Full per-event provenance and frozen parent tables are in `data/`; no huge event table is inserted into the reading report. [LINEAGE.json](LINEAGE.json) records every reused figure/table hash; PNG figures have accompanying PDF originals. [Validation](VALIDATION.json) and [report freeze](REPORT_FREEZE.json) seal the report, template, summaries and evidence.

**Next action:** Select/prepare Historical Report 002 using the frozen JGA Historical Report Template v1. Not executed here.
'''
(O/'REPORT.md').write_text(report)
print('Report assembled; unique any-stem native',len(union),'original-support confirmed native',len(confirmed),'lineage records',len(lineage))
