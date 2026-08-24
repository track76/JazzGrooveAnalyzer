# PR-JGA-REAL-AUDIO-ACQUISITION-AUTHORITY-01

Status: **PREREGISTERED — NOT APPLIED**

## Purpose and frozen scientific question

Scientific question: what minimum prospective evidence is sufficient to
establish that Drums and Double Bass waveforms preserve a common
acquisition-time coordinate suitable for later inter-source timing analysis?

This is a dataset-independent gate applied before JGA analysis and, wherever
possible, before acquisition or download. It establishes only provenance for
the relative sampled timeline. It does not establish physical onset, detector
accuracy, event correspondence, calibration applicability, musical beat
identity, human microtiming, synchronization, rushing/dragging, swing or
groove.

CED-VAL-005 motivates this gate but is not reassessed or upgraded by it.

## Frozen authority dimensions

### 1. Common acquisition system

Accept only provenance-bound primary evidence identifying the recording
session, recorder/DAW, relevant input channels, and their routing during the
captured performance. The evidence must explicitly place the selected Drums
and Double Bass channels in the same identified session and acquisition
system. A later file collection, shared folder or common export application is
insufficient.

### 2. Shared hardware clock

Primary evidence must state that the relevant A/D channels were governed by
one sampling clock during capture, or identify multiple devices and the
documented hardware word-clock/digital synchronization relationship that made
them one clock domain. Acceptable evidence includes recorder/interface clock
configuration preserved in the original session or recorder metadata, or a
direct attributable engineer/provider declaration identifying the clock
arrangement. Equal nominal sample rates, lengths or timestamps cannot
substitute.

### 3. Simultaneous capture

Primary evidence must explicitly state or contemporaneously record that the
authorized Drums and Double Bass takes were performed and recorded
simultaneously. It must distinguish the chosen takes from overdubs,
comped/replaced takes and independently recorded performances. If any source
was overdubbed, the dataset fails this gate for inter-source performance
timing even if later aligned to the same session grid.

### 4. Common timeline origin

Primary evidence must define how each selected file's sample zero maps to the
same session timeline: preferably all files begin at the same declared session
location, or each file carries an exact integer-sample offset from one common
session origin. The mapping must be frozen before JGA output. Independent
trims without preserved exact offsets fail this dimension.

### 5. Timing-edit history

For each selected channel, a primary record must declare either `NONE` or a
complete event-independent account of every timing-changing operation between
capture and authority-bound WAV. It must cover manual shifts, alignment,
warp/time-stretch, quantization, elastic audio, transient correction,
destructively rendered latency compensation, independently trimmed origins,
sample insertion/deletion, comping or replacement, and resampling that can
alter inter-track timing. Any operation is acceptable only if its exact
sample/time mapping is documented and deterministically reversible to the
common acquisition coordinate; otherwise PASS is prohibited.

### 6. Export authority

The record must identify the exported files, export/bounce method, session
start and end locations, sample rate, bit depth, channel handling and whether
all selected tracks were exported with one common range and without
post-export timing modification. If separate ranges were used, exact
integer-sample offsets to the common origin must be supplied. Each distributed
asset must be checksum-bound, readable and technically consistent with the
declaration.

### 7. Source identity

Primary or session evidence must map each selected channel to the intended
recorded Drums or Double Bass source and identify microphone, DI or stem status
at the available level. Multiple channels remain observation channels, not
independent instruments. Bleed does not fail acquisition authority, but known
bleed, replacement, re-amping, submixing or source ambiguity must be recorded
and may limit later source-attribution claims.

## Processing distinction

Amplitude-domain processing is non-blocking for the common sampled-coordinate
claim only when it preserves sample count and the exact sample-to-session-time
mapping. Gain, polarity, channel routing, fixed panning and sample-synchronous
mix coefficients may be accepted when documented. EQ, compression, limiting,
gating, denoising, fades and other waveform-altering processing do not by
themselves change the coordinate, but must be disclosed because they may
affect later onset observation and calibration applicability. Raw or
pre-fader/pre-processing tracks remain preferable.

Processing with lookahead, plugin delay, rendered latency compensation,
convolution latency or any other delay is timing-relevant unless exact latency
and mapping are documented. Manual shifts, independent alignment, warp,
quantization, elastic audio, transient correction, trimming with different
origins, sample insertion/deletion, timing-altering comping, unsynchronized
resampling and undocumented latency rendering are timing-changing and must be
excluded or completely authority-bound.

## Evidence hierarchy

### A. Primary acquisition authority

At least one attributable, checksum- or identity-bound primary record is
mandatory for PASS:

1. an original DAW/recorder session plus acquisition metadata, routing and
   edit/export history sufficient to establish every required dimension; or
2. contemporaneous session/recorder documentation with clock, take, channel,
   origin and export records; or
3. a direct dated declaration from the recording engineer, producer, archive
   or dataset provider who has first-hand authority, explicitly answering the
   frozen checklist.

Multiple primary records may be combined. Every claim retains its status as a
declared procedure or documented record; file agreement does not transform a
declaration into direct physical observation.

### B. Supporting technical evidence

Supporting evidence includes asset SHA-256 values, readable PCM properties,
sample rates, exact frame counts, channel layouts, BWF/iXML or DAW timestamps,
common file scope, creation/export metadata, directory/package structure,
first-nonzero diagnostics and waveform continuity checks. It must corroborate
the primary account and expose conflicts, but cannot independently establish
the acquisition clock, simultaneity or edit history.

### C. Insufficient evidence by itself

None of the following alone can establish PASS: identical file lengths;
identical nominal sample rates; common bit depth; near-zero first-nonzero
frames; matching creation dates; similar waveform starts; apparent musical
synchronization by ear; filenames or instrument labels; common folder/archive;
general “raw multitrack” or “recorded live” wording; a Readme without clock,
take, origin and edit details; later alignment to one grid; or successful JGA
replay.

## Frozen status rules

### `ACQUISITION_AUTHORITY_PASS`

Assign PASS if and only if all seven dimensions have primary authority, the
selected assets are checksum-bound, technical evidence agrees with the primary
record, all source-to-common-origin mappings are exact, and no unresolved
conflict exists. PASS decisions occur before JGA results and cannot depend on
detector behavior.

### `ACQUISITION_AUTHORITY_PARTIAL`

Assign PARTIAL when assets and source labels are provenance-bound and a common
distributed-file coordinate is established, but one or more of hardware
clock, simultaneity, session origin, timing-edit history or export mapping
lacks sufficient primary evidence. PARTIAL may authorize separately reviewed
neutral file-coordinate observation; it cannot authorize acquisition-time
inter-source claims.

### `ACQUISITION_AUTHORITY_FAIL`

Assign FAIL when required assets are unreadable/unbound, selected sources were
not captured simultaneously, clocks were independent and unsynchronized,
origins cannot be mapped, timing-changing operations destroyed or obscured the
mapping, or source identity cannot be established. Dataset attractiveness or
musical quality cannot override FAIL.

### `AUTHORITY_CONFLICT`

Assign AUTHORITY_CONFLICT when primary records disagree with one another or
with technical evidence on any required dimension. Preserve both claims and
stop; do not resolve the conflict by inference or JGA output.

## Minimum sufficient documentation package

The simplest sufficient package is:

1. one dated, attributable engineer/provider acquisition declaration covering
   the recording/session identity, selected channels, one clock domain,
   simultaneous take, common origin mapping, timing-edit history and export
   procedure;
2. a channel/source and take list identifying Drums and Double Bass;
3. an export manifest giving exact filenames, common range or exact offsets,
   sample rate, bit depth, channel handling and SHA-256 values; and
4. independent read-only technical verification of those files and claims.

An original session is not mandatory when this smaller package supplies
equivalent evidence. Conversely, possession of a session alone is
insufficient if clock, take or edit history remains ambiguous.

## Provider / recording-engineer checklist

Before selection, obtain explicit answers and supporting records for:

1. What recording, date/session, recorder/DAW and interface(s) produced the
   candidate tracks?
2. Which exact channels/files are Drums and Double Bass, and are they original
   microphones, DI, submixes, re-amps or replacements?
3. Did their A/D channels share one hardware clock? If multiple devices were
   used, how were they hardware-synchronized?
4. Are the selected takes from one simultaneous performance, without an
   overdubbed or replaced source?
5. What session location corresponds to sample zero in every distributed
   file? If origins differ, what is each exact integer-sample offset?
6. Were any tracks shifted, aligned, warped, quantized, elastically edited,
   transient-corrected, independently trimmed, resampled, comped or altered by
   sample insertion/deletion?
7. Was latency compensation rendered? If yes, what exact per-track mapping
   remains to the acquisition timeline?
8. What amplitude/waveform processing was printed, including processing with
   lookahead or delay?
9. Were all files exported over the same session range and sample rate, with
   no later temporal modification?
10. Can the provider supply the file manifest, technical properties,
    checksums and an attributable declaration for these answers?

## Firewalls and scientific consequence

PASS authorizes only the statement that the selected source recordings have a
defensible common acquisition-time coordinate under the frozen provenance. It
allows a later separately preregistered study to measure inter-source
file-coordinate timing while retaining all detector, physical-onset,
calibration, correspondence and interpretation limitations.

PASS does not authorize physical onset, source isolation, detector accuracy,
event correspondence, calibration applicability, beat identity, human
microtiming conclusions, synchronization quality, rushing/dragging, swing,
groove, production correction or generalization.

No dataset was searched or selected. JGA, H02, strength and physical-onset
measurement were not executed. CED-VAL-005 and production code remain
unchanged. Architecture impact: **NONE**. Production impact: **NONE**.
