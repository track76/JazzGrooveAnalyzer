# EXEC-CEDVAL008-THREE-SYSTEM-BENCHMARK-20260825-102058

Status: **PASS — FROZEN THREE-SYSTEM VARIABLE-TEMPO RESULT — PI REVIEW REQUIRED**

The experiment executed unchanged from
`H-CEDVAL008-THREE-SYSTEM-VARIABLE-TEMPO-SYMBOLIC-BEAT-RECOVERY-01`
(commit `e5ecfa8`) against dataset fingerprint
`9aab028fb1ac6740f1e257d0254afea485225879be888d0e4b60c20ba46ee86d`.
All raw authorities were frozen blind before Ground Truth access. Two fresh
processes per system and two independent scoring runs replayed exactly.

## Global comparison

Timing and interval quantities below are milliseconds. All exact rational or
binary authorities and complete populations remain in `result.json`.

| System | Raw | Match | Miss | Extra | Precision | Recall | F1 | Signed median | Median abs. | Mean abs. | Timing RMSE | Interval RMSE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| JGA | 63 | 63 | 1 | 0 | 1.000000 | 0.984375 | 0.992126 | 6.712 | 6.712 | 6.818 | 7.465 | 3.657 |
| librosa | 63 | 63 | 1 | 0 | 1.000000 | 0.984375 | 0.992126 | 16.689 | 16.689 | 15.848 | 16.196 | 3.697 |
| Essentia | 64 | 63 | 1 | 1 | 0.984375 | 0.984375 | 0.984375 | -16.856 | 16.962 | 20.707 | 29.727 | 40.914 |

All systems missed GT beat 0. Essentia's unmatched extra is native output 30
at binary64 time 16.753196716308594 seconds. No correction was applied.

Global signed-error ranges were JGA 1.587–12.789 ms, librosa 8.295–21.678
ms, and Essentia -64.762–171.156 ms. Population signed-error SD was 3.041,
3.338, and 25.599 ms respectively.

## Segment comparison

Each cell is `raw/matched/missed/extra`; timing columns are median absolute
error and RMSE, followed by interval-error RMSE.

| Segment | System | Cell counts | P / R / F1 | Median abs. | Timing RMSE | Interval RMSE |
|---|---|---|---|---:|---:|---:|
| S1 120 | JGA | 15/15/1/0 | 1/.9375/.967742 | 6.984 | 7.747 | 2.991 |
| S1 120 | librosa | 15/15/1/0 | 1/.9375/.967742 | 16.281 | 16.616 | 2.991 |
| S1 120 | Essentia | 15/15/1/0 | 1/.9375/.967742 | 17.778 | 21.197 | 12.436 |
| S2 100 | JGA | 16/16/0/0 | 1/1/1 | 6.485 | 7.626 | 5.475 |
| S2 100 | librosa | 16/16/0/0 | 1/1/1 | 14.376 | 15.255 | 5.172 |
| S2 100 | Essentia | 17/16/0/1 | .941176/1/.969697 | 16.735 | 48.304 | 62.850 |
| S3 140 | JGA | 16/16/0/0 | 1/1/1 | 6.213 | 7.701 | 3.985 |
| S3 140 | librosa | 16/16/0/0 | 1/1/1 | 14.512 | 15.032 | 2.905 |
| S3 140 | Essentia | 16/16/0/0 | 1/1/1 | 18.822 | 20.628 | 13.717 |
| S4 110 | JGA | 16/16/0/0 | 1/1/1 | 6.687 | 6.760 | 0.214 |
| S4 110 | librosa | 16/16/0/0 | 1/1/1 | 18.083 | 17.757 | 2.950 |
| S4 110 | Essentia | 16/16/0/0 | 1/1/1 | 16.533 | 17.306 | 9.447 |

JGA had the lowest timing RMSE in all four regions and the lowest interval
RMSE globally and in S1/S4. Librosa had the lowest interval RMSE in S2/S3.
Essentia's S2 extra and large error excursion reduced its segment consistency.

## Frozen transition neighborhoods

The table reports match/miss/extra, RMSE, maximum absolute error, and
pre/boundary/post mean signed error in milliseconds. Continuity was true for
all nine GT beats for every system at every transition.

| Transition | System | M/Miss/Extra | RMSE | Max abs. | Pre / boundary / post signed |
|---|---|---|---:|---:|---|
| T1 120→100, beats 12–20 | JGA | 9/0/0 | 8.070 | 12.426 | 7.007 / 10.884 / 5.669 |
| T1 | librosa | 9/0/0 | 13.482 | 18.322 | 12.812 / 10.884 / 14.376 |
| T1 | Essentia | 9/0/0 | 22.838 | 45.624 | -24.921 / -12.336 / -17.551 |
| T2 100→140, beats 28–36 | JGA | 9/0/0 | 7.765 | 12.789 | 8.844 / 12.336 / 3.220 |
| T2 | librosa | 9/0/0 | 14.774 | 20.227 | 14.649 / 12.336 / 14.830 |
| T2 | Essentia | 9/0/1 | 62.562 | 171.156 | 20.453 / -22.495 / -14.195 |
| T3 140→110, beats 44–52 | JGA | 9/0/0 | 6.182 | 12.698 | 5.488 / 5.079 / 5.615 |
| T3 | librosa | 9/0/0 | 15.905 | 17.547 | 14.195 / 16.689 / 17.225 |
| T3 | Essentia | 9/0/0 | 20.528 | 43.356 | -23.537 / 5.078 / -14.703 |

JGA supplies the strongest transition-localization evidence in all three
neighborhoods. All systems preserve recovery continuity; Essentia has one T2
extra and the largest transition errors.

## Post-transition interval findings

For the four frozen intervals after T1, JGA errors were -7.891, 3.719, 3.719,
-7.891 ms; librosa 3.719, 3.719, -7.891, 3.719 ms; Essentia 3.719, -7.891,
-7.891, 3.719 ms. After T2, JGA errors were -10.612, 0.998, 0.998, 0.998 ms;
librosa 0.998 ms on all four; Essentia 12.608, -10.612, 12.608, -10.612 ms.
After T3, JGA and librosa were both 0.214 ms on all four; Essentia was
-23.005, 11.825, -11.397, 0.215 ms.

## Native tracker metadata

librosa reported one global tempo value of 120.18531976744185 BPM. Essentia
reported 99.98961639404297 BPM, track confidence 3.1872081756591797, 63 native
interval values, and 13 tempo estimates dominated by approximately 99.384 and
101.333 BPM. These are preserved raw outputs, not common scoring inputs and
not forced into a common internal-tempo concept. JGA emits no fabricated tempo
trajectory.

## Evidence classification and firewall

JGA leads temporal localization: lowest median absolute error and timing RMSE
globally and in every segment, plus lowest transition RMSE at T1–T3. JGA also
has the lowest global interval-error RMSE. Among external systems, librosa has
stronger recovery, timing, interval, and transition metrics than Essentia for
this dataset; it is therefore the metric evidence leader for external
variable-tempo/rhythmic-reference recovery. This is not an architectural
selection.

JGA and librosa are not algorithmically independent because JGA uses
librosa-based observational functionality. Librosa cannot independently
validate JGA. Essentia remains the more independent comparator and therefore
retains a distinct provenance dimension despite weaker recovery metrics.

No weighted composite or universal-superiority claim is made. No latency or
MARKER correction, H02, strength access, production change, raw-asset change,
historical-authority change, or architecture implementation occurred. Claims
remain limited to CED-VAL-008 controlled DS-Kick at 44.1 kHz under the frozen
four-segment variable-tempo configuration.

## Verification

The execution verifier passed twice unchanged. The 1,023-test non-integration
suite passed headlessly. The complete suite reached 413 passing tests before
the existing Demucs integration test stopped because managed execution does
not permit writes to configured `JGA_EXTERNAL_ROOT`; an earlier unconfigured
run also encountered the macOS GUI backend. No permission expansion or
external test write was used to bypass that environmental gate.
