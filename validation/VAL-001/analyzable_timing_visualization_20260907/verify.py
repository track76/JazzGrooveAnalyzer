"""Independent inspection of preserved plot-data and SVG membership; no analysis."""
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
REPORT = ROOT/'validation/VAL-001/ad041_direct_input_acceptance_20260907/canonical_report_run_1.json'
EXPECTED_SHA = 'eeb189217a722679d5f40bef4d809e2b38ab381e9dea81057023dfd3d80e05c7'
EXPECTED_FP = 'e3d73705306ccc0e96ec78020a54f34aa4e8f267337afa6b7bd56b74fc4fdc4d'


def verify(directory):
    assert sha256(REPORT.read_bytes()).hexdigest() == EXPECTED_SHA
    report = json.loads(REPORT.read_bytes())
    assert report['scientific_fingerprint'] == EXPECTED_FP
    data = json.loads((directory/'plot_data.json').read_bytes())
    manifest = json.loads((directory/'provenance_manifest.json').read_bytes())
    events = {x['eme_id']:x for x in report['elementary_metric_events']}
    locs = {x['target_eme_id']:x for x in report['ad038_localizations']}
    sources = {x['source_identity']:x for x in report['source_authorities']}
    records = data['records']
    assert len(records) == len({x['canonical_eme_identifier'] for x in records}) == 139
    assert {x['canonical_eme_identifier'] for x in records} == set(events)
    for record in records:
        eid = record['canonical_eme_identifier']
        event = events[eid]
        assert record['canonical_record_identifier'] == eid
        assert report['elementary_metric_events'][int(record['canonical_record_pointer'].rsplit('/',1)[1])] == event
        assert record['source_identity'] == event['sound_source_id']
        assert record['asset_identity'] == event['source_asset_sha256']
        assert record['source_lane'] == sources[event['sound_source_id']]['label']
        assert record['absolute_time_seconds'] == event['timestamp_seconds']
        assert record['absolute_time_ms'] == event['timestamp_seconds'] * 1000.0
        if eid in locs:
            loc = locs[eid]
            assert record['nearest_drum_reference'] == loc['nearest_reference']
            assert record['nearest_drum_reference_identifier'] == loc['nearest_reference']['eme_id']
            assert record['nearest_drum_time_seconds'] == loc['nearest_reference']['timestamp_seconds']
            assert record['nearest_drum_time_ms'] == loc['nearest_reference']['timestamp_ms']
            assert record['signed_displacement_seconds'] == loc['nearest_displacement_seconds']
            assert record['signed_displacement_ms'] == loc['nearest_displacement_ms']
            assert record['absolute_displacement_ms'] == loc['nearest_absolute_displacement_ms']
            assert report['ad038_localizations'][int(record['localization_pointer'].rsplit('/',1)[1])] == loc
        else:
            assert record['source_lane'] == 'Drums'
            for field in ('nearest_drum_reference', 'nearest_drum_reference_identifier', 'nearest_drum_time_seconds', 'nearest_drum_time_ms', 'signed_displacement_seconds', 'signed_displacement_ms', 'absolute_displacement_ms'):
                assert record[field] is None
    overlap_pairs = []
    for name, points in data['graphs'].items():
        expected = set(events) if name == 'absolute_timeline' else set(locs)
        assert len(points) == len({x['canonical_record_identifier'] for x in points}) == len(expected)
        assert {x['canonical_record_identifier'] for x in points} == expected
        groups = {element.attrib['id']:element for element in ET.parse(directory/f'{name}.svg').iter() if element.attrib.get('id','').startswith(name+'__')}
        assert len(groups) == len(points)
        positions = defaultdict(list)
        for point in points:
            record = records[point['plot_data_record_index']]
            assert point['canonical_record_identifier'] == record['canonical_eme_identifier']
            assert point['x_seconds'] == record['absolute_time_seconds']
            group = groups[point['svg_artist_id']]
            uses = [x for x in group.iter() if x.tag.endswith('}use')]
            paths = [x for x in group if x.tag.endswith('}path')]
            assert len(uses)+len(paths) == 1
            if name == 'absolute_timeline':
                assert point['y_lane'] == {'Drums':2,'Piano':1,'Double Bass':0}[record['source_lane']]
            else:
                assert point['y_signed_displacement_ms'] == record['signed_displacement_ms']
                positions[(point['x_seconds'],point['y_signed_displacement_ms'])].append(record['source_lane'])
                if record['source_lane']=='Double Bass':
                    assert len(paths)==1 and 'fill: none' in paths[0].attrib['style']
        if name == 'drum_relative_timing':
            overlap_pairs = [labels for labels in positions.values() if len(labels)>1]
            assert all(sorted(pair)==['Double Bass','Piano'] for pair in overlap_pairs)
        with Image.open(directory/f'{name}.png') as image:
            assert list(image.size) == manifest['figures'][name]['png_pixels']
    for filename,metadata in manifest['artifacts'].items():
        assert sha256((directory/filename).read_bytes()).hexdigest()==metadata['sha256']
    assert sha256((directory/'plot_data.json').read_bytes()).hexdigest()==manifest['plot_data_sha256']
    return dict(canonical_coordinate_and_field_equality='PASS', complete_membership_and_no_duplicates='PASS',
                source_and_asset_provenance='PASS', svg_point_traceability='PASS',
                exact_overlapping_piano_bass_pairs=len(overlap_pairs), hollow_bass_markers_verified=True,
                png_dimensions='PASS', artifact_checksums='PASS', canonical_report_unchanged=True)

if __name__=='__main__':
    directory=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
    print(json.dumps(verify(directory),sort_keys=True,separators=(',',':')))
