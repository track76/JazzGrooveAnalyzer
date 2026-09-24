from pathlib import Path
import json
import numpy, scipy, soundfile
res=[]
try:
 p=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/scientific/rfc/JGA_SPOTIFY_BASIC_PITCH_BASS_M33_M48_20260923/TARGET_NOTES.csv')
 if p.is_dir():list(p.iterdir())
 else:p.open('rb').read(1)
 raise RuntimeError('PROHIBITED READ SUCCEEDED')
except PermissionError:res.append('/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/scientific/rfc/JGA_SPOTIFY_BASIC_PITCH_BASS_M33_M48_20260923/TARGET_NOTES.csv')
try:
 p=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/scientific/rfc/JGA_V1_OPERATIONAL_PLP_QUARTER_NEAREST_001_20260922/PLP_REFERENCE.csv')
 if p.is_dir():list(p.iterdir())
 else:p.open('rb').read(1)
 raise RuntimeError('PROHIBITED READ SUCCEEDED')
except PermissionError:res.append('/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/scientific/rfc/JGA_V1_OPERATIONAL_PLP_QUARTER_NEAREST_001_20260922/PLP_REFERENCE.csv')
try:
 p=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/historical_reports/JGA_HISTORICAL_REPORT_001/FINAL_SCORE_V1/METRIC_REFERENCE.csv')
 if p.is_dir():list(p.iterdir())
 else:p.open('rb').read(1)
 raise RuntimeError('PROHIBITED READ SUCCEEDED')
except PermissionError:res.append('/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/historical_reports/JGA_HISTORICAL_REPORT_001/FINAL_SCORE_V1/METRIC_REFERENCE.csv')
try:
 p=Path('/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/historical_reports/JGA_HISTORICAL_REPORT_001/SCORE_V1_1_REVIEW')
 if p.is_dir():list(p.iterdir())
 else:p.open('rb').read(1)
 raise RuntimeError('PROHIBITED READ SUCCEEDED')
except PermissionError:res.append('/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/historical_reports/JGA_HISTORICAL_REPORT_001/SCORE_V1_1_REVIEW')
Path('/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/scientific/rfc/JGA_BASIC_PITCH_HARMONIC_FAMILY_20260924/crosscheck/output/ISOLATION_PROBE.json').write_text(json.dumps({'denied':res,'passed':True}))
print('ISOLATION PROBE PASS',len(res))
