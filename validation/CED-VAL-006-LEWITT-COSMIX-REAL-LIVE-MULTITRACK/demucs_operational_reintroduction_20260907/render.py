"""Render only the prospective canonical operational observations."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
LANES={'Drums':2,'Piano':1,'Double Bass':0}
COLORS={'Drums':'#404040','Piano':'#1769aa','Double Bass':'#d46b08'}


def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()+b'\n'


def plot_data(report):
    sources={s['source_identity']:s for s in report['source_authorities']}
    localizations={r['target_eme_id']:r for r in report['ad038_localizations']}
    rows=[]
    for i,event in enumerate(report['elementary_metric_events']):
        source=sources[event['sound_source_id']];loc=localizations.get(event['eme_id'])
        rows.append({'point_id':'eme-'+event['eme_id'],'canonical_record':'/elementary_metric_events/'+str(i),
            'eme_id':event['eme_id'],'source_identity':event['sound_source_id'],
            'asset_sha256':event['source_asset_sha256'],'lane':source['label'],
            'time_seconds':event['timestamp_seconds'],'time_ms':event['timestamp_seconds']*1000,
            'nearest_reference':None if loc is None else loc['nearest_reference'],
            'signed_displacement_ms':None if loc is None else loc['nearest_displacement_ms'],
            'absolute_displacement_ms':None if loc is None else loc['nearest_absolute_displacement_ms']})
    assert len({r['eme_id'] for r in rows})==len(rows)
    assert sum(r['lane']!='Drums' for r in rows)==len(localizations)
    return rows


def render(report_path,output):
    report=json.loads(report_path.read_text());rows=plot_data(report)
    assert canonical(rows)==canonical(plot_data(report))
    output.mkdir(parents=True,exist_ok=True)
    (output/'plot_data.json').write_bytes(canonical(rows))
    matplotlib.rcParams.update({'font.family':'DejaVu Sans','svg.hashsalt':'jga-demucs-operational-v1','font.size':11})
    counts={label:sum(r['lane']==label for r in rows) for label in LANES}
    figures={}
    for graph,name,height in [(1,'absolute_timeline',7),(2,'drum_relative_timing',8)]:
        fig,ax=plt.subplots(figsize=(18,height),dpi=180)
        fig.subplots_adjust(left=.14 if graph==1 else .09,right=.98,top=.81,bottom=.2)
        if graph==2:ax.axhline(0,color='#333333',linewidth=1.0,zorder=0)
        selected=[r for r in rows if graph==1 or r['lane']!='Drums']
        for row in selected:
            y=LANES[row['lane']] if graph==1 else row['signed_displacement_ms']
            artist,=ax.plot([row['time_seconds']],[y],linestyle='None',
                marker='D' if row['lane']=='Double Bass' else 'o',
                markersize=4.5 if row['lane']=='Double Bass' else 3,
                markerfacecolor='none',markeredgecolor=COLORS[row['lane']],markeredgewidth=.8)
            artist.set_gid(f'graph{graph}-'+row['point_id'])
        ax.set_xlabel('Absolute recording time (seconds)')
        ax.set_xlim(0,max(r['time_seconds'] for r in rows)+2)
        if graph==1:
            ax.set_yticks([2,1,0],[f'{label}  (n={counts[label]})' for label in LANES]);ax.set_ylim(-.5,2.5)
            title='Absolute analyzable timeline — Demucs-derived observations'
        else:
            ax.set_ylabel('Signed displacement from selected nearest Drum (ms)')
            title='Drum-relative analyzable timing — Demucs-derived observations'
            for label in ['Piano','Double Bass']:
                ax.plot([],[],linestyle='None',marker='D' if label=='Double Bass' else 'o',
                    markerfacecolor='none',markeredgecolor=COLORS[label],label=f'{label} (n={counts[label]})')
            ax.legend(loc='upper right',frameon=False)
        ax.spines[['top','right']].set_visible(False)
        fig.suptitle(title,y=.96,fontsize=17)
        fig.text(.5,.9,'GEOMETRIC_ONLY  •  ANALYZABLE OBSERVATIONS ONLY',ha='center',fontsize=12)
        fig.text(.5,.09,'Absence of a plotted event does not establish musical absence.',ha='center')
        fig.text(.5,.045,('Each marker is one observable EME; overlaps retained without jitter.' if graph==1 else
            'Negative: before selected Drum reference. Positive: after selected Drum reference. Piano preservation NOT_ESTABLISHED.'),ha='center',fontsize=10)
        fig.savefig(output/(name+'.png'),metadata={'Software':'JGA deterministic operational visualization'})
        fig.savefig(output/(name+'.svg'),metadata={'Date':None,'Creator':'JGA deterministic operational visualization'})
        svg_path=output/(name+'.svg')
        svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text().splitlines())+'\n')
        plt.close(fig)
        svg=ET.parse(output/(name+'.svg'))
        ids={node.attrib.get('id') for node in svg.iter()}
        expected={f'graph{graph}-'+r['point_id'] for r in selected}
        assert expected.issubset(ids)
        actual={x for x in ids if x and x.startswith(f'graph{graph}-eme-')}
        assert actual==expected
        figures[name]={'point_count':len(selected),'width_pixels':3240,'height_pixels':height*180,'svg_point_ids_verified':True}
    proof={'canonical_sha256':sha256(report_path.read_bytes()).hexdigest(),
           'plot_data_sha256':sha256(canonical(rows)).hexdigest(),'counts':counts,'figures':figures,
           'coordinate_equality_and_membership':'PASS','plot_data_replay':'BYTE_IDENTICAL',
           'traceability':'SVG point ID -> plot_data point_id -> canonical_record JSON pointer and EME ID'}
    (output/'visualization_verification.json').write_bytes(canonical(proof))
    print(json.dumps(proof))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();render(HERE/'canonical_operational_report.json',args.output)
