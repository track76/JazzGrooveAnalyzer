"""Render only the immutable accepted canonical report; no JGA analysis imports."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
REPORT = ROOT / 'validation/VAL-001/ad041_direct_input_acceptance_20260907/canonical_report_run_1.json'
REPORT_SHA = 'eeb189217a722679d5f40bef4d809e2b38ab381e9dea81057023dfd3d80e05c7'
FINGERPRINT = 'e3d73705306ccc0e96ec78020a54f34aa4e8f267337afa6b7bd56b74fc4fdc4d'
BASELINE_HEAD = '8cf4bed84e79912cc788aca712e25dfef353d26b'
COUNTS = {'Drums': 63, 'Piano': 49, 'Double Bass': 27}
LANES = {'Drums': 2, 'Piano': 1, 'Double Bass': 0}
COLORS = {'Drums': '#374151', 'Piano': '#1766a3', 'Double Bass': '#b85b16'}
MARKERS = {'Drums': 'o', 'Piano': 'o', 'Double Bass': 'D'}
STATUS = 'GEOMETRIC_ONLY  |  ANALYZABLE OBSERVATIONS ONLY'
ABSENCE = 'Absence of a plotted event does not establish musical absence.'
FIGURES = {'absolute_timeline': (16, 6), 'drum_relative_timing': (16, 7)}
DPI = 180


def canonical(value):
    return (json.dumps(value, ensure_ascii=True, allow_nan=False,
                       sort_keys=True, separators=(',', ':')) + '\n').encode('ascii')


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read_authority():
    assert digest(REPORT) == REPORT_SHA, 'Canonical report checksum mismatch'
    report = json.loads(REPORT.read_bytes())
    assert report['scientific_fingerprint'] == FINGERPRINT
    content = deepcopy(report)
    content.pop('scientific_fingerprint')
    assert sha256(canonical(content).rstrip(b'\n')).hexdigest() == FINGERPRINT
    assert report['scientific_status']['default_correspondence_status'] == 'GEOMETRIC_ONLY'
    return report


def extract(report):
    sources = {x['source_identity']: x for x in report['source_authorities']}
    assert len(sources) == 3
    assert {x['label'] for x in sources.values()} == set(COUNTS)
    events = {x['eme_id']: (i, x) for i, x in enumerate(report['elementary_metric_events'])}
    assert len(events) == len(report['elementary_metric_events']) == 139
    localizations = {x['target_eme_id']: (i, x) for i, x in enumerate(report['ad038_localizations'])}
    assert len(localizations) == len(report['ad038_localizations']) == 76
    records = []
    graphs = {name: [] for name in FIGURES}
    for eid, (index, event) in events.items():
        source = sources[event['sound_source_id']]
        label = source['label']
        assert event['source_asset_sha256'] == source['sha256']
        record = dict(
            canonical_record_identifier=eid,
            canonical_eme_identifier=eid,
            canonical_record_pointer=f'/elementary_metric_events/{index}',
            source_identity=event['sound_source_id'],
            asset_identity=event['source_asset_sha256'],
            absolute_time_seconds=event['timestamp_seconds'],
            absolute_time_ms=event['timestamp_seconds'] * 1000.0,
            source_lane=label,
            nearest_drum_reference=None,
            signed_displacement_ms=None,
            signed_displacement_seconds=None,
            absolute_displacement_ms=None,
            nearest_drum_reference_identifier=None,
            nearest_drum_time_seconds=None,
            nearest_drum_time_ms=None,
            nearest_drum_record_pointer=None,
            nearest_drum_asset_identity=None,
            localization_pointer=None,
            relative_fields_status='NOT_APPLICABLE_TEMPORAL_REFERENCE',
        )
        if label != 'Drums':
            loc_index, loc = localizations[eid]
            assert loc['target_source_identity'] == record['source_identity']
            assert loc['target_asset_sha256'] == record['asset_identity']
            assert loc['target_timestamp_seconds'] == record['absolute_time_seconds']
            assert loc['target_timestamp_ms'] == record['absolute_time_ms']
            assert loc['correspondence_status'] == 'GEOMETRIC_ONLY'
            assert loc['nearest_displacement_ms'] == loc['nearest_displacement_seconds'] * 1000.0
            assert loc['nearest_absolute_displacement_ms'] == loc['nearest_absolute_displacement_seconds'] * 1000.0
            nearest = loc['nearest_reference']
            assert nearest is not None
            ref_index, ref_event = events[nearest['eme_id']]
            assert sources[nearest['source_identity']]['label'] == 'Drums'
            assert nearest['source_identity'] == ref_event['sound_source_id']
            assert nearest['timestamp_seconds'] == ref_event['timestamp_seconds']
            assert nearest['timestamp_ms'] == nearest['timestamp_seconds'] * 1000.0
            record.update(
                absolute_time_ms=loc['target_timestamp_ms'],
                nearest_drum_reference=deepcopy(nearest),
                nearest_drum_record_pointer=f'/elementary_metric_events/{ref_index}',
                nearest_drum_asset_identity=ref_event['source_asset_sha256'],
                signed_displacement_ms=loc['nearest_displacement_ms'],
                signed_displacement_seconds=loc['nearest_displacement_seconds'],
                absolute_displacement_ms=loc['nearest_absolute_displacement_ms'],
                nearest_drum_reference_identifier=nearest['eme_id'],
                nearest_drum_time_seconds=nearest['timestamp_seconds'],
                nearest_drum_time_ms=nearest['timestamp_ms'],
                localization_pointer=f'/ad038_localizations/{loc_index}',
                relative_fields_status='COPIED_FROM_ACCEPTED_LOCALIZATION',
            )
            graphs['drum_relative_timing'].append(dict(
                canonical_record_identifier=eid,
                plot_data_record_index=len(records),
                svg_artist_id=f'drum_relative_timing__{eid}',
                x_seconds=loc['target_timestamp_seconds'],
                y_signed_displacement_ms=loc['nearest_displacement_ms'],
                source_category=label,
            ))
        else:
            assert eid not in localizations
        graphs['absolute_timeline'].append(dict(
            canonical_record_identifier=eid,
            plot_data_record_index=len(records),
            svg_artist_id=f'absolute_timeline__{eid}',
            x_seconds=event['timestamp_seconds'],
            y_lane=LANES[label],
            source_category=label,
        ))
        records.append(record)
    assert Counter(x['source_lane'] for x in records) == COUNTS
    assert Counter(x['source_category'] for x in graphs['drum_relative_timing']) == {'Piano': 49, 'Double Bass': 27}
    assert {x['canonical_record_identifier'] for x in graphs['drum_relative_timing']} == set(localizations)
    for name, points in graphs.items():
        assert len(points) == len({x['canonical_record_identifier'] for x in points})
        for point in points:
            record = records[point['plot_data_record_index']]
            assert point['canonical_record_identifier'] == record['canonical_record_identifier']
            assert point['x_seconds'] == record['absolute_time_seconds']
            assert point['source_category'] == record['source_lane']
    return dict(
        schema='JGA_ACCEPTED_ANALYZABLE_TIMING_PLOT_DATA_V1',
        canonical_report_path=str(REPORT.relative_to(ROOT)),
        canonical_report_sha256=REPORT_SHA,
        accepted_scientific_fingerprint=FINGERPRINT,
        scientific_status='GEOMETRIC_ONLY',
        observation_scope='ANALYZABLE OBSERVATIONS ONLY',
        absence_statement=ABSENCE,
        lane_coordinates=LANES,
        recording_duration_seconds={x['label']: x['technical_audio']['duration_seconds'] for x in sources.values()},
        coordinate_policy='Copy accepted seconds and milliseconds. Drum EME milliseconds, absent from the report EME record, are only seconds * 1000.0. No reference selection or displacement calculation.',
        records=records, graphs=graphs,
    )


def render_once(output):
    # A private cache removes dependence on user matplotlib configuration.
    with tempfile.TemporaryDirectory(prefix='jga-timing-mpl-') as cache:
        os.environ['MPLCONFIGDIR'] = cache
        os.environ['XDG_CACHE_HOME'] = cache
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib import font_manager, ft2font
        from matplotlib.lines import Line2D
        from PIL import Image
        plt.rcdefaults()
        plt.rcParams.update({
            'font.family': 'DejaVu Sans', 'font.size': 12,
            'svg.hashsalt': REPORT_SHA, 'svg.fonttype': 'none',
            'axes.spines.top': False, 'axes.spines.right': False,
            'axes.labelcolor': '#252b33', 'xtick.color': '#374151',
            'ytick.color': '#374151', 'figure.facecolor': 'white',
        })
        report = read_authority()
        data = extract(report)
        output.mkdir(parents=True, exist_ok=True)
        with (output/'plot_data.json').open('xb') as stream:
            stream.write(canonical(data))
        artifacts = {}
        for name, dimensions in FIGURES.items():
            fig, ax = plt.subplots(figsize=dimensions, dpi=DPI)
            fig.subplots_adjust(left=0.105, right=0.975, bottom=0.22, top=0.75)
            title = 'Absolute analyzable timeline' if name == 'absolute_timeline' else 'Drum-relative timing'
            fig.text(0.105, 0.92, title, fontsize=23, weight='bold', color='#20262e')
            fig.text(0.105, 0.85, STATUS, fontsize=12, color='#374151')
            duration = max(data['recording_duration_seconds'].values())
            ax.set_xlim(0.0, duration)
            ax.set_xlabel('Absolute recording time (seconds)', labelpad=12)
            ax.grid(axis='x', color='#e4e7eb', linewidth=0.7)
            ax.set_axisbelow(True)
            points = data['graphs'][name]
            if name == 'absolute_timeline':
                ax.set_ylim(-0.55, 2.55)
                ax.set_yticks([2, 1, 0], ['Drums  (63)', 'Piano  (49)', 'Double Bass  (27)'])
                ax.tick_params(axis='y', length=0, pad=12)
                ax.spines['left'].set_visible(False)
            else:
                ax.set_ylabel('Signed displacement from nearest Drum (ms)', labelpad=14)
                ax.axhline(0.0, color='#737b85', linewidth=1.0, linestyle='--', zorder=1)
                handles = [Line2D([], [], marker=MARKERS[label], linestyle='None',
                                  color=COLORS[label], markersize=8 if label == 'Double Bass' else 5,
                                  markerfacecolor='none' if label == 'Double Bass' else COLORS[label],
                                  markeredgewidth=1.2, label=f'{label}  ({COUNTS[label]})')
                           for label in ('Piano', 'Double Bass')]
                ax.legend(handles=handles, loc='upper right', frameon=False)
                fig.text(0.105, 0.105, 'Negative: before selected Drum reference.  Positive: after selected Drum reference.', fontsize=11, color='#374151')
            for point in points:
                record = data['records'][point['plot_data_record_index']]
                y = point['y_lane'] if name == 'absolute_timeline' else point['y_signed_displacement_ms']
                hollow_bass = name == 'drum_relative_timing' and record['source_lane'] == 'Double Bass'
                artist = ax.scatter([point['x_seconds']], [y],
                                    s=70 if hollow_bass else 28,
                                    marker=MARKERS[record['source_lane']],
                                    facecolors='none' if hollow_bass else COLORS[record['source_lane']],
                                    edgecolors=COLORS[record['source_lane']],
                                    linewidths=1.2 if hollow_bass else 0,
                                    clip_on=False, zorder=4 if hollow_bass else 3)
                artist.set_gid(point['svg_artist_id'])
                offsets = artist.get_offsets()
                assert offsets.shape == (1, 2)
                assert float(offsets[0, 0]) == record['absolute_time_seconds']
                assert float(offsets[0, 1]) == (LANES[record['source_lane']] if name == 'absolute_timeline' else record['signed_displacement_ms'])
            assert len(ax.collections) == len(points)
            # No point-connecting lines: only the explicitly requested zero reference.
            assert len(ax.lines) == (0 if name == 'absolute_timeline' else 1)
            fig.text(0.105, 0.05, ABSENCE, fontsize=11, color='#374151')
            for extension in ('png', 'svg'):
                path = output/f'{name}.{extension}'
                assert not path.exists()
                metadata = {'Software': 'JGA accepted timing visualization'} if extension == 'png' else {'Date': None, 'Creator': 'JGA accepted timing visualization'}
                fig.savefig(path, dpi=DPI, metadata=metadata)
                artifacts[path.name] = dict(sha256=digest(path), byte_size=path.stat().st_size)
            with Image.open(output/f'{name}.png') as image:
                assert image.size == (dimensions[0]*DPI, dimensions[1]*DPI)
            svg = ET.parse(output/f'{name}.svg')
            ids = [element.attrib['id'] for element in svg.iter() if element.attrib.get('id', '').startswith(name+'__')]
            assert len(ids) == len(set(ids)) == len(points)
            assert set(ids) == {x['svg_artist_id'] for x in points}
            for point in points:
                artist_group = next(x for x in svg.iter() if x.attrib.get('id') == point['svg_artist_id'])
                uses = [x for x in artist_group.iter() if x.tag.endswith('}use')]
                # Hollow markers serialize as one direct path; filled markers use one SVG instance.
                direct_paths = [x for x in artist_group if x.tag.endswith('}path')]
                assert len(uses) + len(direct_paths) == 1
            text = (output/f'{name}.svg').read_text()
            assert STATUS in text and ABSENCE in text
            plt.close(fig)
        font_path = Path(font_manager.findfont('DejaVu Sans'))
        manifest = dict(
            schema='JGA_ANALYZABLE_TIMING_VISUALIZATION_PROVENANCE_V1',
            input_report=str(REPORT.relative_to(ROOT)), input_sha256=REPORT_SHA,
            scientific_fingerprint=FINGERPRINT, authoritative_head=BASELINE_HEAD,
            plot_data_sha256=digest(output/'plot_data.json'),
            render_script_sha256=digest(Path(__file__)),
            figures={name: dict(inches=list(size), png_pixels=[size[0]*DPI, size[1]*DPI],
                                svg_points=[size[0]*72, size[1]*72],
                                point_counts=dict(Counter(x['source_category'] for x in data['graphs'][name])),
                                total_points=len(data['graphs'][name])) for name,size in FIGURES.items()},
            artifacts=artifacts,
            environment=dict(python=sys.version.split()[0], matplotlib=matplotlib.__version__,
                             freetype=ft2font.__freetype_version__,font='DejaVu Sans',font_sha256=digest(font_path)),
            traceability='SVG point group ID -> graph point -> plot-data record -> canonical JSON pointer and EME ID. PNG uses the same verified artist coordinates.',
            point_coordinates='EXACT_ACCEPTED_COORDINATES_NO_JITTER_NO_SMOOTHING',
            drum_relative_fields_for_drums='NULL_NOT_APPLICABLE_NO_SELF_REFERENCE_INVENTED',
            scientific_transformation='NONE; rendering and explicit seconds-to-ms unit projection only',
            optional_graph_3='NOT_CREATED',
            overlap_display='Exact coordinates retained; hollow larger Bass diamonds surround smaller filled Piano circles at coincident coordinates. No jitter; glyph clipping disabled.',
        )
        (output/'provenance_manifest.json').write_bytes(canonical(manifest))
        assert digest(REPORT) == REPORT_SHA


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--render-once', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.render_once:
        render_once(args.output_dir)
        return
    read_authority()
    with tempfile.TemporaryDirectory(prefix='jga-timing-visualization-replay-') as tmp:
        runs = [Path(tmp)/'first', Path(tmp)/'second']
        for run in runs:
            subprocess.run([sys.executable, str(Path(__file__).resolve()), '--render-once', '--output-dir', str(run)], check=True)
        files = sorted(p.name for p in runs[0].iterdir())
        assert files == sorted(p.name for p in runs[1].iterdir())
        for filename in files:
            assert (runs[0]/filename).read_bytes() == (runs[1]/filename).read_bytes(), filename
        assert digest(REPORT) == REPORT_SHA
        result = dict(
            classification='PASS_ANALYZABLE_TIMING_VISUALIZATION_ACCEPTED',
            traceability='PASS', no_duplicates='PASS', no_omissions='PASS',
            exact_rendered_coordinates='PASS', svg_point_membership='PASS',
            graph_1_counts=COUNTS, graph_2_counts={'Piano':49,'Double Bass':27,'total':76},
            plot_data_sha256=digest(runs[0]/'plot_data.json'),
            canonical_report_sha256=REPORT_SHA, scientific_fingerprint=FINGERPRINT,
            canonical_report_unchanged=True, detection_or_scientific_acceptance_rerun=False,
            fresh_process_plot_data_replay='BYTE_IDENTICAL',
            fresh_process_png_svg_replay='BYTE_IDENTICAL',
            provenance_manifest_sha256=digest(runs[0]/'provenance_manifest.json'),
        )
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for filename in files+['acceptance_result.json']:
            assert not (args.output_dir/filename).exists(), 'Preserved output already exists'
        for filename in files:
            shutil.copyfile(runs[0]/filename,args.output_dir/filename)
        (args.output_dir/'acceptance_result.json').write_bytes(canonical(result))
        print(canonical(result).decode(),end='')

if __name__ == '__main__':
    main()
