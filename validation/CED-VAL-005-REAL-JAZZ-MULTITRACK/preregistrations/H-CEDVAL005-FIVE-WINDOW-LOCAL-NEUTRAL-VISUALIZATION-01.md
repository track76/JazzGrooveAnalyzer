# H-CEDVAL005-FIVE-WINDOW-LOCAL-NEUTRAL-VISUALIZATION-01

Status: **PREREGISTERED — NOT RENDERED**

## Frozen authority and scientific question

This protocol is bound exclusively to frozen execution
`EXEC-CEDVAL005-REAL-AUDIO-20260824-112305`, scientific fingerprint
`074d84768f508e6ceee9c9225c34e9ea881ce50d88e0d5f930525b92e87bd9d6`,
and its immutable AD-037 EME, AD-038 `GEOMETRIC_ONLY` localization, and
AD-040 `RhythmSectionTimingProfile` artifacts. It performs no new
observational computation.

Scientific question: can five prospectively selected local windows provide a
reproducible, unbiased visual inspection of the frozen CED-VAL-005 Drums and
Double Bass observations and neutral Drum-relative geometry across the
recording?

## Scope and frozen window selection

The exact distributed-file scope is 10,068,072 frames at 44,100 Hz, indexed
from 0 through 10,068,071 inclusive. Divide that scope into five equal temporal
strata. For stratum `i = 0, 1, 2, 3, 4`, define:

`center_i = floor((2*i + 1) * 10,068,072 / 10)`.

Every window is exactly 220,500 frames (5 seconds). Because the length is
even, its deterministic bounds are
`start_i = center_i - 110,250` and `end_i = start_i + 220,500`, with
start-inclusive/end-exclusive membership.

| Window | Stratum | Center frame | Center time (s) | Frame interval `[start,end)` | Time interval `[start,end)` (s) |
|---|---:|---:|---:|---:|---:|
| `CEDVAL005-LOCAL-WINDOW-00` | 0 | 1,006,807 | 22.830090702947846 | `[896557,1117057)` | `[20.330090702947846,25.330090702947846)` |
| `CEDVAL005-LOCAL-WINDOW-01` | 1 | 3,020,421 | 68.49027210884354 | `[2910171,3130671)` | `[65.99027210884354,70.99027210884354)` |
| `CEDVAL005-LOCAL-WINDOW-02` | 2 | 5,034,036 | 114.15047619047618 | `[4923786,5144286)` | `[111.65047619047618,116.65047619047618)` |
| `CEDVAL005-LOCAL-WINDOW-03` | 3 | 7,047,650 | 159.81065759637187 | `[6937400,7157900)` | `[157.31065759637187,162.31065759637187)` |
| `CEDVAL005-LOCAL-WINDOW-04` | 4 | 9,061,264 | 205.47083900226758 | `[8951014,9171514)` | `[202.97083900226758,207.97083900226758)` |

Frame coordinates are authoritative. Decimal seconds equal frame/44,100 and
are display representations; implementations shall calculate from the integer
coordinates rather than parse the displayed decimals.

Window selection consumes only the frozen total file scope. EME or
PulseCandidate counts, displacement values, exact-zero coincidences, AD-038
statuses, extremes, musical content, audio playback, waveform features and
visual inspection are forbidden selection inputs. A sparse, dense, empty or
visually unremarkable window remains in the population unchanged.

## Event inclusion and connector rules

For each window include every frozen Drums and Double Bass EME whose
authoritative producer-frame coordinate is in `[start_i, end_i)`. Preserve its
immutable EME identity, producer frame, timestamp, source identity, lineage and
provenance. Do not thin, filter, rank, suppress, interpolate or recompute any
observation.

A neutral connector may be rendered only when all of the following are true:

1. the displayed Double Bass EME has an existing frozen AD-038 localization;
2. that localization has an existing frozen nearest Drum EME reference; and
3. both the Double Bass EME and that exact referenced Drum EME are inside the
   same displayed window.

Never recompute nearest geometry or replace the frozen reference with another
visible Drum EME. If the Bass EME is inside but its frozen nearest Drum EME is
outside, omit the connector and record `DISPLAY_BOUNDARY_CENSORING`. This is a
display status only and cannot be counted or interpreted as unresolved
scientific geometry. Frozen nearest ties remain explicitly identified; their
existing serialized nearest reference is not new correspondence authority.

## Visualization contract

Later execution shall generate exactly five figures with identical dimensions,
axis scaling within each five-second span, lane positions, marker vocabulary,
connector styling and labeling rules:

- X axis: absolute distributed-file time in seconds;
- Y lanes: `Drums` and `Double Bass`;
- every in-window EME plotted at its immutable timestamp;
- only the connector population authorized above; and
- visible labels `OBSERVATIONAL / FRAME-RESOLVED` and `GEOMETRIC_ONLY`.

No beat grid, BPM, measure number, meter, score, chord symbol, musical form,
swing label, rushing/dragging label, synchronization language or performance
judgment is permitted.

JGA timing has producer-frame authority on a lattice of 512/44,100 seconds
(approximately 11.609977324263 ms). No sub-frame onset interpolation is
authorized, and the figures must not imply sample-level timing precision.

## Future window records and replay

Each future window record shall preserve: window ID; stratum index; center
frame and time; exact start/end frames and seconds; Drums, Double Bass and total
EME counts; eligible frozen AD-038 localization count; rendered connector
count; `DISPLAY_BOUNDARY_CENSORING` count; nearest-tie cases present; exact
included EME and localization identities; source authority; scientific
provenance; and a visualization fingerprint. Counts describe detector output
only.

Require at least two complete visualization executions with exact agreement of
the five definitions, included EME/localization identities, counts, connector
and boundary-censoring decisions, rendered scientific content, per-window
fingerprints and aggregate visualization fingerprint. If nondeterministic image
container metadata prevents byte-identical PNG replay, preserve and compare a
canonical metadata-free scientific-content representation and report PNG-byte
identity separately. Scientific-content replay may not be weakened.

## Meaning and firewalls

The figures may support descriptive inspection of local observation density,
local temporal distribution, same-frame or nearby frame-resolved observations,
gaps, neutral nearest-Drum geometry and variation in observational structure
across absolute file time.

They do not establish physical onset, event correspondence, shared beat
identity, synchronization, rushing, dragging, swing, groove, timing intention,
performance quality, acquisition-time human microtiming or
calibration-corrected timing.

Acquisition authority remains `ACQUISITION_AUTHORITY_PARTIAL`. That status does
not block neutral visualization on the common distributed-file coordinate, but
does block acquisition-time and human-microtiming interpretation.
Correspondence remains `GEOMETRIC_ONLY`; `AUTHORIZED_EVENT_RELATION` is not
created or implied.

No JGA rerun, H02, PulseCandidate strength, BPM, meter, measure, symbolic
information, musical-form knowledge, audio inspection or calibration transfer
is permitted. Historical authorities, raw assets, architecture and production
code remain unchanged. Rendering is not authorized by this preregistration
task.
