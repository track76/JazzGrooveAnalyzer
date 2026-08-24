# H-CEDVAL006-FIVE-WINDOW-LOCAL-NEUTRAL-VISUALIZATION-01

Status: **PREREGISTERED — NOT RENDERED**

## Frozen authority and scientific question

This protocol is bound exclusively to frozen execution
`EXEC-CEDVAL006-REAL-LIVE-AUDIO-20260824-183919`, result commit
`d89524ff544f19b95815e2f86efaf8dcbbf3f3ce`, and scientific-content
fingerprint
`8c5723fbeabe2031516b2eeee0c83fb42ad84f46824cf65f5d485c6cf6c82b5c`.
The execution's independent verifier passes its artifact, fingerprint, native
48 kHz mapping, AD-037 lineage, AD-038 geometry/statistics, AD-040 profile,
replay and firewall checks.

Scientific question: can prospectively selected local windows provide
reproducible, selection-unbiased visual inspection of the frozen CED-VAL-006
Drums and Double-Bass EME populations and their existing AD-038 neutral
geometry on the common distributed-file coordinate?

No JGA observation or AD-038 geometry may be recomputed. Only the existing
frozen 909 Drums EME, 1,055 Double Bass EME and 1,055 AD-038 localization
records are eligible input.

## Systematic window selection

The sole selection authority is the frozen common distributed-file scope
`[0, 11912868)` at 48,000 Hz: 11,912,868 source-file sample frames, exactly
`992739/4000` seconds (`248.18475` seconds).

For stratum index `i = 0, 1, 2, 3, 4`, define the integer center:

`center_i = floor((2*i + 1) * 11912868 / 10)`.

Each window is exactly 240,000 sample frames. Because its length is even,
define:

`start_i = center_i - 120000`

`end_i = start_i + 240000`

with membership convention `[start_i, end_i)`. The five frozen definitions
are:

| Window | Stratum | Center sample | Center seconds | Sample window | Exact time window | Decimal time window (s) |
|---|---:|---:|---:|---|---|---|
| W1 | 0 | 1,191,286 | `595643/24000` | `[1071286, 1311286)` | `[535643/24000, 655643/24000)` | `[22.318458333333332, 27.318458333333332)` |
| W2 | 1 | 3,573,860 | `178693/2400` | `[3453860, 3693860)` | `[172693/2400, 184693/2400)` | `[71.95541666666666, 76.95541666666666)` |
| W3 | 2 | 5,956,434 | `992739/8000` | `[5836434, 6076434)` | `[972739/8000, 1012739/8000)` | `[121.592375, 126.592375)` |
| W4 | 3 | 8,339,007 | `2779669/16000` | `[8219007, 8459007)` | `[2739669/16000, 2819669/16000)` | `[171.2293125, 176.2293125)` |
| W5 | 4 | 10,721,581 | `10721581/48000` | `[10601581, 10841581)` | `[10601581/48000, 10841581/48000)` | `[220.86627083333335, 225.86627083333335)` |

All bounds lie inside the frozen source-file scope. No bound may be moved,
resized, replaced or adjusted after observation.

## Selection-bias firewall

Window construction consumes only total sample scope, number of strata and
fixed duration. It must not consume EME or PulseCandidate counts, localization
density, displacement, ties, extremes, music, audio playback, waveform
inspection, beat structure, BPM, tracker output or visual appearance. Sparse
or empty windows remain selected. No replacement window is permitted.

This preregistration freezes the windows before querying their EME membership.
No in-window observation or localization population was inspected in their
selection or in this record.

## Frozen coordinate and EME membership

For every frozen EME preserve:

`producer_sample_coordinate = 512 * producer_frame`

`timestamp_seconds = producer_sample_coordinate / 48000`.

Include the EME in a window if and only if:

`start_sample_frame <= producer_sample_coordinate < end_sample_frame`.

Never compare sample-window bounds directly with `producer_frame`. Do not
interpolate. The JGA observation lattice is exactly `512/48000 = 4/375`
seconds, approximately 10.6666666666667 ms. Rendering remains
`OBSERVATIONAL / FRAME-RESOLVED` and does not claim sub-frame or sample-level
detector precision.

Every frozen in-window Drums and Double Bass EME must be displayed. No
filtering, thinning, ranking, aggregation or visual suppression is permitted.

## Frozen AD-038 connector rule

Use only the existing frozen AD-038 nearest-reference record. Draw a connector
for an in-window Double Bass EME only when its exact frozen nearest Drum EME is
also inside that same window. Do not recompute nearest geometry and do not
substitute another visible Drum EME.

If the Double Bass EME is inside but its frozen nearest Drum EME is outside,
omit the connector and record `DISPLAY_BOUNDARY_CENSORING`. This is display
censoring only; it does not change or create unresolved scientific geometry.

Exact nearest ties retain their frozen AD-038 tie authority and frozen
serialization/reference state. Rendering must neither resolve a tie nor
replace its frozen reference.

## Visualization contract

Future execution must produce exactly five figures using identical dimensions,
axis conventions, lane positions, marker semantics, connector semantics,
labels and styling.

- X axis: absolute distributed-file seconds, with the exact window bounds.
- Y axis: exactly two fixed lanes, `Drums` and `Double Bass`.
- Plot every authorized in-window EME at its immutable timestamp.
- Display only connectors authorized by the rule above.
- State visibly: `OBSERVATIONAL`, `FRAME-RESOLVED`, and `GEOMETRIC_ONLY`.

No BPM, beat grid, downbeat, meter, measure, form, score, symbolic note,
rushing/dragging, swing, groove or performance-judgment label is permitted.

## Window-level future authority

For each window preserve its ID, stratum, center, exact sample/time bounds,
Drums EME count, Double Bass EME count, total EME count, eligible frozen
Double Bass localization count, connector count,
`DISPLAY_BOUNDARY_CENSORING` count, frozen nearest-tie count, exact included
EME identities, exact included localization identities, source and execution
provenance, scientific-content fingerprint and PNG SHA-256.

Freeze a per-window scientific-content fingerprint and one aggregate
visualization fingerprint over all five window records and artifact identities.

## Deterministic replay

Perform two complete visualization executions. Require exact agreement of
window definitions, included EME/localization identities, counts, connector and
boundary-censoring decisions, tie preservation, scientific rendering content,
per-window fingerprints and aggregate fingerprint. Any scientific-content
disagreement is `FAIL / STOP`; do not repair or replace a window. Report PNG
byte identity separately from scientific-content identity.

## Meaning and authority limits

The figures may show only local frozen-observation distribution,
source-specific observation density, temporal gaps, frame-level coincidence or
proximity, frozen neutral Drum-relative geometry and descriptive variation
across distributed-file time.

They must not establish or imply physical onset, musical-event correspondence,
shared beat identity, common acquisition clock, synchronization, rushing,
dragging, swing, groove, performer intention, performance quality or calibrated
human microtiming.

Live performance is `SUPPORTED BY PRIMARY LEWITT PROVIDER DECLARATION`.
`RAW / no editing / no tuning` is supported exactly to the extent declared by
LEWITT. Shared hardware clock and common session-time origin remain
`UNESTABLISHED`; physical onset remains `NOT ESTABLISHED`; calibration
applicability remains `UNESTABLISHED`; correspondence remains
`GEOMETRIC_ONLY`.

No JGA rerun, external tracker, BPM, H02, strength access, production change,
raw-asset change, historical-authority change or musical interpretation is
authorized by this protocol.
