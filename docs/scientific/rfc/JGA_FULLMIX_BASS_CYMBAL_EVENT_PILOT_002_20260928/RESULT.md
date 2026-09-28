# Pilot 002 — full-mix Bass/Cymbal candidate evidence

Status: EXPERIMENTAL / DIAGNOSTIC / PI REVIEW REQUIRED / NOT PROMOTED. Engineering execution and saved-artifact verification PASS. This is not a scientific accuracy/identity validation. No candidate freeze, commit or push.

## Input and scope

Original full mix: `docs/scientific/rfc/JGA_TARGETED_PITCH_ONSET_20260924/inference/input/FULLMIX.wav`. SHA-256 `c890658d8c8f67e0d295d7ab334712227c2c2c999283a1fdb5cf32e6af7a467f`.
Verified WAV FLOAT32, 44,100 Hz, stereo; arithmetic channel mean. M33–M56, Q131–Q226; chorus identity NOT ESTABLISHED. Native admission [2107392, 3643392) samples, [47.786666666667, 82.616598639456) s. Requested decimal endpoints rounded to nearest integer (half-even), exclusive end. Full source context extends on both sides; only final candidate admission is restricted to this interval. Canonical quarter mapping is verified only after extraction, for interval metadata.

## Independently recomputed saved counts/statistics

| Metric | Bass | Cymbal |
|---|---:|---:|
| all_local_maxima | 939 | 709 |
| peak_qualified | 659 | 405 |
| deduplicated | 458 | 302 |
| rejected | 280 | 304 |
| merged_members | 201 | 103 |
| clusters | 458 | 302 |
| multi_member_clusters | 137 | 83 |
| clusters_span_exceeds_tolerance | 44 | 15 |
| evaluation_boundary_crossed | 2 | 8 |
| source_support_truncated | 0 | 0 |
| cluster_span_ms median | 0.000000 | 0.000000 |
| dedup_spacing_ms median | 69.659864 | 81.269841 |
| flux median | 11.537758 | 4.551651 |
| prominence median | 8.486923 | 2.208010 |

All cluster-span statistics include singleton clusters (span zero). Flux/prominence units are uncalibrated magnitude-change units. Boundary-crossing means local evidence crosses the evaluation interval, not missing source audio. Whole-context algorithms have explicitly wider support for every candidate.

| Arm | Deduplicated state | N |
|---|---|---:|
| bass | BASS_COMPATIBLE | 350 |
| bass | BASS_POSSIBLE | 0 |
| bass | AMBIGUOUS | 108 |
| bass | UNRESOLVED | 0 |
| cymbal | CYMBAL_COMPATIBLE | 17 |
| cymbal | OTHER_PERCUSSIVE_COMPATIBLE | 279 |
| cymbal | AMBIGUOUS | 6 |
| cymbal | UNRESOLVED | 0 |

Bass cluster-size distribution: `{"1": 321, "2": 93, "3": 30, "4": 9, "5": 4, "6": 1}`; cluster span maximum 174.149660 ms.
Cymbal cluster-size distribution: `{"1": 219, "2": 68, "3": 11, "4": 3, "5": 1}`; cluster span maximum 127.709751 ms.
Deduplicated candidate density: 19.083 Bass-arm candidates/measure and 12.583 Cymbal-arm candidates/measure. These are computational evidence densities, not note/hit counts.

## Timestamp and evidence semantics

Synthetic STFT impulses at native samples 1024, 2048 and 4096 recover frame centers exactly: 0-sample coordinate error. center=True maps frame k to processing-start + k×512; no half-window subtraction. At 44,100 Hz the hop is 11.609977 ms and window 46.439909 ms. This verifies indexing, not physical onset accuracy. Spectral-flux maxima are frame-derived positive-change landmarks. Zero-phase filtering has no nominal interior phase delay but can deform transients or introduce pre-ringing; filtering does not certify unchanged physical onset location. SOS coefficients, response, included bin centers and synthetic symmetry/tail descriptors are saved.

Classification-local intervals differ from whole-context algorithm support. Offline filtering, adaptive flux percentiles and pYIN sequence decoding require the processing context; evidence-available-until and decision time therefore use context end. No post-event observation moves a landmark.

## Scientific limitations — no tuning

45–350 Hz is a mixture-evidence region, not Bass identity. F0 is conditioned on that band; harmonic-bin magnitudes come from the unfiltered full mix and may include other instruments. Fundamental and overtones are stored separately; summed magnitude does not establish multiple distinct harmonics belonging to Bass. Continuity is only a measured previous voiced-frame F0 difference, not note/source tracking. The harmonic/flux classification inequality is heuristic and uncalibrated. The present states do not establish independent instrument attribution.

pYIN emitted a preserved warning: frame_length=2048 at 44,100 Hz contains fewer than two periods at fmin=41.2 Hz. Low-register pitch evidence is consequently limited. No parameter was adjusted after observing this output. Voiced probability is a model output, not a calibrated probability of Bass identity.

2–10 kHz features are band-conditioned. The contrast-like descriptor is correctly named six-subband energy coefficient of variation, not standard spectral contrast. Post-event energy is a finite-support sum of squared STFT magnitudes, not an estimated decay constant. Conjunctive Cymbal rules and any Ride/HiHat subtype are tentative heuristics; simultaneous piano, snare, noise and other sources remain unresolved. OTHER_PERCUSSIVE_COMPATIBLE is not an independently confirmed confuser.

Deduplication chains neighboring qualified candidates within 35 ms, preserving all member evidence and selecting the earliest landmark independently of class. Total chains can exceed 35 ms and can merge distinct attacks; conversely a musical attack can generate multiple clusters. No cluster is certified as one physical event. All local maxima, rejected candidates and merged members remain recoverable.

## Independence and preservation

Producer reads only configuration and the verified original full mix. No stem, human/expert annotation, old onset table or Global/PLP coordinate informs generation, timing, features, thresholds, class or deduplication. Quarter mapping is metadata-only post-extraction validation. No grid, 96-position completion, microtiming or groove analysis exists. Source audio, Pilot 001, canonical scientific records and unrelated worktree bytes remain unchanged. OpenCode partial JSON provenance is preserved in PREEXISTING_INPUTS.json.

## Artifacts and verification

Three inventories per arm are distinct: ALL_LOCAL_MAXIMA, PEAK_QUALIFIED_CANDIDATES and DEDUPLICATED_CANDIDATES; DEDUP_CLUSTERS contains complete member records. JSON uses null/status rather than invented zero evidence. NPZ NaN pitch/harmonic entries explicitly mean unavailable measurements. Full context spectra/flux/maxima/F0/waveform are in the SSD artifact referenced and hashed by EXTERNAL_ARRAYS.json.

All six PNG figures were generated from saved arrays/tables only; PLOT_DATA.json identifies plotted candidate IDs/times/states. Representative zooms use chronological first/middle/last examples, not expert success labels. No independently labeled confuser examples exist. Visual inspection and programmatic membership checks are separate from source-identity validation.

REPRODUCTION/validate.py independently checks arithmetic, raw maxima, configured qualification/classes, harmonic values, dedup membership, coordinates, plot references and hashes without rerunning extraction. VALIDATION.json records the pre-manifest checks; final manifest-aware verification is recorded in the task ledger. Report counts, displayed medians and boundary counts are checked against saved/recomputed data.

Producer/configuration/environment hashes are in EXECUTION_PROVENANCE.json; matplotlib/renderer provenance is in PLOT_DATA.json. The executed producer is preserved verbatim. Do not rerun it in this completed namespace: reproduction requires a separately authorized fresh output scope and writer lease. External disposable caches are TEMPORARY_NO_BACKUP, reconstructible and not scientific evidence.

MANIFEST.json lists every other package file with hash, size, role and generation step, counts itself explicitly, and does not attempt an impossible self-hash. Its own hash is recorded in the external backup log and final task ledger. BACKUP_VERIFICATION.json is a scoped pre-manifest receipt; final package and governance equality are checked at closure. Historical SSD inventory remains NOT FULLY CERTIFIED.

STOP FOR PI REVIEW. No further experiment is authorized.
