# CL-H-CEDVAL005-FIVE-WINDOW-COORDINATE-AUTHORITY-01

Status: **FROZEN COORDINATE-AUTHORITY CLARIFICATION**

## Scientific-history record

This clarification is downstream of and does not replace
`H-CEDVAL005-FIVE-WINDOW-LOCAL-NEUTRAL-VISUALIZATION-01`, frozen at commit
`7d9273e8f5ae350e349a85799e3a4949f1d97764`. The original preregistration
remains unchanged and recoverable.

Before rendering, an Evidence Conflict was identified: the preregistered
window bounds are distributed-file/WAV sample-frame coordinates, while the
phrase “producer-frame coordinate” could be read as the JGA analysis-frame
field `producer_frame`. Directly applying the sample-frame bounds to that
analysis-frame index would be dimensionally invalid and would not express the
approved window authority. Execution stopped before rendering or inspection
of window contents.

The PI subsequently clarified that all five visualization windows are and
remain expressed in the frozen CED-VAL-005 WAV/sample coordinate at 44,100 Hz.
This record freezes that coordinate meaning before rendering.

## Frozen coordinate authority

- `producer_frame` is the immutable JGA analysis-frame index. In the frozen
  CED-VAL-005 result its authority is on the JGA frame lattice, whose observed
  population spans approximately 33 through 19,211.
- `producer_sample_coordinate` is the exact projection of that identity onto
  the distributed-file/WAV sample coordinate:
  `producer_sample_coordinate = 512 * producer_frame`.
- `timestamp_seconds` is the corresponding absolute distributed-file time:
  `timestamp_seconds = producer_sample_coordinate / 44,100`, represented by
  the frozen binary64 timestamp and its hexadecimal encoding.
- Visualization centers, bounds and membership are expressed exclusively in
  the distributed-file/WAV sample coordinate, not in JGA analysis-frame-index
  units.

The final EME inclusion rule is therefore:

`start_sample_frame <= producer_sample_coordinate < end_sample_frame`.

The bounds must never be compared directly with `producer_frame`.

Both authorities remain preserved simultaneously: `producer_frame` supplies
the immutable JGA frame identity, while `producer_sample_coordinate` supplies
its exact file-coordinate projection for window inclusion and visualization.
This projection does not create sub-frame or sample-accurate detector
precision. The visualization remains `OBSERVATIONAL / FRAME-RESOLVED` with
frame spacing 512/44,100 seconds (approximately 11.609977324263 ms).

## Unchanged preregistered method

This clarification changes no scientific method or observation. The five
centers, five start/end bounds, 220,500-frame duration, five-stratum selection
formula, EME populations, AD-038 geometry, connector rules, selection-bias
firewall, acquisition status `ACQUISITION_AUTHORITY_PARTIAL`, and
correspondence status `GEOMETRIC_ONLY` remain unchanged.

The frozen sample-frame bounds remain:

1. `[896557, 1117057)`
2. `[2910171, 3130671)`
3. `[4923786, 5144286)`
4. `[6937400, 7157900)`
5. `[8951014, 9171514)`

No window was moved, resized, replaced or selected after observation. No
window membership, EME density, displacement, localization pattern, musical
content, audio, waveform, strength or visual appearance was inspected to make
this clarification.

## Pre-render validation requirement

Before rendering, mechanical authority validation must confirm without
enumerating or inspecting window contents that:

1. every frozen bound lies inside the 10,068,072-sample scope and every window
   is exactly 220,500 samples;
2. the execution membership predicate uses `producer_sample_coordinate`;
3. every frozen EME record satisfies
   `producer_sample_coordinate = 512 * producer_frame` exactly; and
4. every frozen EME timestamp is the exact binary64 representation produced
   by `producer_sample_coordinate / 44,100`, including hexadecimal round-trip.

No rendering, JGA rerun, observation recomputation, AD-038 recomputation, H02,
PulseCandidate strength, production-code change or historical-authority change
is authorized by this clarification.
