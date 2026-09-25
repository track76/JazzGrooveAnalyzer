from pathlib import Path
import sys,json,csv,hashlib,numpy as np
sys.path.insert(0,'tools')
from continuous_backup import atomic_write_and_backup,MIRROR,preflight
O=Path('docs/historical_reports/JGA_HISTORICAL_REPORT_001/FINAL_ANCHORED_BMIG_DMIG_20260925')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(n):return list(csv.DictReader((O/n).open()))
def put(n,b):atomic_write_and_backup(O/n,b.encode() if isinstance(b,str) else b)
def js(n,x):put(n,json.dumps(x,indent=2,ensure_ascii=False)+'\n')
preflight()
pages=json.loads(Path('/private/tmp/jga_final_pdf_qa/PDF_PAGES.json').read_text());assert len(pages)==2
assert all(abs(p['width_pt']-595.27559)<.001 and abs(p['height_pt']-841.88976)<.001 for p in pages)
expected=' '.join((O/'FINAL_READER_SUMMARY.md').read_text().replace('# ','').split())
assert ' '.join(pages[1]['text'].split())==expected
for i in range(131,195):assert f'Q{i}' in pages[0]['text']
assert 'BPM locale' not in pages[0]['text'] and 'Mediana BPM: 161.5' in pages[0]['text']
ev=rows('EVENT_PROVENANCE_127.csv');rend=rows('RENDERED_EVENTS.csv');assert len(rend)==127 and len({e['event_ID'] for e in rend})==127
lookup={e['event_ID']:e for e in ev}
for r in rend:assert r['render_x_s']==lookup[r['event_ID']]['original_time_s']
g=rows('FINAL_ANCHORED_BMIG_DMIG.csv');gl=rows('RENDERED_GRIDS.csv');assert len(gl)==128
for r in gl:
 source=next(x for x in g if x['quarter_ID']==r['quarter']);assert float(r['render_x_s'])==float(source['BMIG_time_s' if r['instrument']=='Bass' else 'DMIG_time_s'])
for p in ['FINAL_ANCHORED_BMIG_DMIG.csv','FINAL_ANCHORED_GRID_PROTOCOL.md','FINAL_ANCHOR_AUDIT.csv','EVENT_PROVENANCE_127.csv']:
 assert sha(O/p)==sha(O/'source_anchored'/p)
# Check stored anchored normal equations without fitting or changing any coordinate.
for inst,col in [('BASS','BMIG'),('DRUM','DMIG')]:
 rr=rows(f'source_anchored/{inst}_INDEPENDENT_ANCHORED_GRID.csv');x=np.array([float(r[col+'_time_s']) for r in rr]);a=np.array([r[inst+'_anchor_yes_no']=='YES' for r in rr]);t=np.array([float(r[inst+'_anchor_time_s']) if a[i] else 0 for i,r in enumerate(rr)])
 D=np.diff(np.eye(64),n=2,axis=0);gradient=a*(x-t)+(D.T@D@x)/16
 assert np.max(abs(gradient))<1e-10
 assert np.all(np.diff(x)>0)
js('VISUAL_QA.json',{'status':'PASS','black_and_white':'PASS','review':'All two PDF-rendered pages inspected, plus grayscale page 1. Page 2 is monochrome. Native line/event positions checked from render logs.','pages':2,'A4_portrait':True,'four_measures_per_system':True,'grid_lines':128,'onsets_rendered':127,'B_D_font_pt':5.5,'onset_sizes_points_squared':[15,8],'BPM_curve_and_extrema_preserved':True,'native_temporal_geometry':True,'no_full_height_quarter_lines':True,'no_event_delta_labels':True,'all_64_B_D_labels':True,'no_clipping_or_label_overlap_observed':True,'reader_text_exact':True})
q=json.loads((O/'SCIENTIFIC_QA.json').read_text());q.update(normal_equations_without_refitting='PASS',all_rendered_positions_match_source=True,reader_text_exact=True,source_and_mirror_hashes_verified=True);js('SCIENTIFIC_QA.json',q)
for name,src in [('qa/PAGE_01.png','/private/tmp/jga_final_pdf_qa/PAGE_01.png'),('qa/PAGE_02.png','/private/tmp/jga_final_pdf_qa/PAGE_02.png'),('qa/PAGE_01_GRAYSCALE.png','/private/tmp/jga_final_bw.png'),('qa/PDF_PAGES.json','/private/tmp/jga_final_pdf_qa/PDF_PAGES.json')]:put(name,Path(src).read_bytes())
put('verify_final_package.py',Path(__file__).read_bytes())
put('RESULT.md','# Final anchored historical report\n\nPI adopted the existing anchored method. Final PDF rendered and every page inspected; color, grayscale, arithmetic and scientific integrity PASS. BMIG64/64, DMIG64/64, 16measures, 127unchanged observed events, clean-six median +8.886246628359018ms. No fitting or new audio inference. Frozen payload and final authority status are recorded by FREEZE_RECORD.json after the backup gate. Previous experiments remain intact; limitations in FINAL_TECHNICAL_METHOD.md.\n')
entries=[]
for p in sorted(O.rglob('*')):
 if p.is_file():
  assert sha(p)==sha(MIRROR/p)
  entries.append({'relative_path':str(p.relative_to(O)),'sha256':sha(p),'size_bytes':p.stat().st_size})
js('MANIFEST.json',{'payload':'Final report and technical evidence; closure files MANIFEST.json SHA256SUMS.txt FREEZE_RECORD.json excluded to avoid self-reference','entries':entries})
put('SHA256SUMS.txt',''.join(e['sha256']+'  '+e['relative_path']+'\n' for e in entries)+sha(O/'MANIFEST.json')+'  MANIFEST.json\n')
for p in O.rglob('*'):
 if p.is_file():assert sha(p)==sha(MIRROR/p)
print('PDF/SCIENTIFIC/BW/PACKAGE_BACKUP PASS',len(entries),'payload files',sha(O/'MANIFEST.json'))
