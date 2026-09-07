# Accepted ANALYZABLE timing — PI inspection package

Open these two PNG files first:

1. [Absolute analyzable timeline](absolute_timeline.png): 2880 × 1080 pixels.
2. [Drum-relative analyzable timing](drum_relative_timing.png): 2880 × 1260 pixels.

Vector versions: [timeline SVG](absolute_timeline.svg) and
[Drum-relative SVG](drum_relative_timing.svg). Figure dimensions are 16 × 6 inches
and 16 × 7 inches respectively, rendered at 180 dpi; SVG viewports are
1152 × 432 and 1152 × 504 points.

Both graphs show **GEOMETRIC_ONLY — ANALYZABLE OBSERVATIONS ONLY**.
Absence of a plotted event does not establish musical absence. These figures
are inspection aids, not new scientific evidence; the accepted canonical data
remain authoritative. The observable subset does not establish complete
performance coverage.

The timeline contains exactly 63 Drums, 49 Piano and 27 Double Bass EME
(139 total), in explicit source lanes against absolute recording seconds.
The relative graph contains exactly 49 Piano and 27 Double Bass points
(76 total). Its vertical coordinate is the report's recorded signed displacement
in milliseconds from the selected nearest Drum reference. Negative means only
before that selected reference; positive means only after it. The dashed line
is 0 ms. Time-axis guides are ordinary seconds ticks, not beat or bar grids.

Points are never connected, smoothed, interpolated, selected again, or shifted.
Ten Piano/Bass pairs share exact coordinates in the relative graph. Larger
hollow orange Bass diamonds surround smaller blue Piano circles so both marks
remain visible without jitter. SVG zoom supports inspection. Graphic resolution
cannot replace exact numeric coordinates; use plot-data for numeric inspection.
Drum-relative fields for Drum observations are null: no self-relative Drum
relationship is manufactured. Graph 3 was omitted.

## Authority and traceability

The sole data input is the accepted
[canonical report](../ad041_direct_input_acceptance_20260907/canonical_report_run_1.json).
Its checksum and scientific fingerprint are pinned in the renderer and provenance
manifest. No audio asset, detector, source-separation, or scientific-analysis
pipeline is loaded. Existing milliseconds are copied; Drum absolute milliseconds
are only their accepted seconds multiplied by 1000.

[plot_data.json](plot_data.json) retains canonical record and EME identifiers,
canonical JSON pointers, source and asset identity, lanes, absolute seconds and
milliseconds, and the report's applicable nearest-Drum references and signed/
absolute displacements. Each graph point references exactly one plot-data record.
Each SVG point's stable group ID links to that graph point and hence to the
canonical EME. The PNG uses the same coordinate-verified Matplotlib artists.
Records intentionally occur in both graphs when applicable, but never duplicate
within either graph.

[provenance_manifest.json](provenance_manifest.json) preserves input/output
hashes, dimensions, software/font versions and traceability policy.
[inspection_verification.json](inspection_verification.json) records the independent
canonical-field and SVG membership audit (`verify.py`).
[acceptance_result.json](acceptance_result.json) records exact count, coordinate,
membership and fresh-process replay checks. [resume_record.json](resume_record.json)
records the interrupted artifact inventory and the specific display/provenance
completions; work was not restarted because of the interruption.

## Regeneration

From the repository root, use a fresh explicit output directory:

```sh
.venv/bin/python validation/VAL-001/analyzable_timing_visualization_20260907/render.py --output-dir /private/tmp/jga-timing-visualization-replay
```

The renderer refuses to overwrite preserved outputs, checks the immutable input,
then performs two isolated rendering runs. Plot-data, PNG, SVG and provenance
must replay byte-identically in the recorded environment. Rendering checks the
actual artist coordinates, one SVG marker per point, and exact record membership.
The scientific acceptance is not rerun. Font/software changes may change figure
bytes; the source report remains authoritative.
