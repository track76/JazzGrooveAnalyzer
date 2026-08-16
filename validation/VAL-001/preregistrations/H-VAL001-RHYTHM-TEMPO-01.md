# H-VAL001-RHYTHM-TEMPO-01 — Rhythm-Section Common-Period Preregistration

Status: PREREGISTERED — NOT EXECUTED

Authority: JGA Scientific Research Constitution, SVP-001, F-032, AD-035 and
AD-037

## Scientific question

Can complete, independently preserved Drums, Double Bass and Piano EME
timestamp populations support one or more common recurrent physical periods
without declared tempo, meter, metric timeline, normalized phase, symbolic
evidence or musical-role assumptions?

This experiment supplies genuinely new evidence relative to the former
33/66/132 work: source-specific complete AD-037 EME populations are evaluated
independently and each rhythm-section contributor receives one equal evidence
vote. No pooled full-mix recurrence population is used.

## Frozen blind input

Timestamp-only input:
`validation/VAL-001/run_20260816_192519/blind_input.json`

SHA-256: `25ee4d610f6a3130f0b4f001b1908c8dad443d34ee30413905f6fd377202c9e8`

| Contributor | EME | Population fingerprint |
|---|---:|---|
| Drums | 63 | `bdd609584ae58c3897691b1c400a3829b45dd637fe1fcc432cbdadc574b251ed` |
| Double Bass | 27 | `80896b766d87b9a6d820223dfee5b928adab76397960fe2b728b6a8e158b6164` |
| Piano | 49 | `357be2d0c1ad88d8dccf4513c1aab165d7b48286861fff62ea954a62d99f72a2` |

Only EME identity, absolute timestamp, contributor/source identity,
supporting-observation lineage and asset provenance are present. Tenor Sax,
Voice, full mix, symbolic sources, declared BPM/meter/timeline, normalized
phase, Ground Truth and AI evidence are excluded. Voice remains `DEFERRED`.

## Source-independent recurrence

Apply the existing AD-035 minimum recurrence rule independently to each
ordered contributor population:

1. project every timestamp to its nearest 512-sample frame at 44.1 kHz and
   preserve its signed quantization residual;
2. compute every consecutive positive frame interval;
3. retain every exact interval occurring at least twice; and
4. preserve every supporting adjacent EME pair and its temporal position.

No event is removed. A retained duration is observation-derived Candidate
Period evidence only. It is not beat, tempo, tactus or subdivision.

The measurement duration is exactly `512/44100` seconds per frame. Each
measured interval has uncertainty of ±1 frame because both endpoint timestamps
are independently rounded within ±1/2 frame.

## Source-level reproducibility and persistence

A source candidate is reproducible when a second deterministic execution
returns the byte-identical duration, occurrence identities and fingerprint.

Define each source's observed temporal scope from its first through last EME
timestamp and divide it at its exact midpoint. An occurrence is assigned by
its temporal midpoint. A source candidate is `PERSISTENT` only when it has at
least one occurrence in each half. Otherwise it remains a supported candidate
with status `LIMITED_SCOPE`. Only reproducible, persistent candidates enter
cross-source consensus. All other candidates remain preserved and reported.

## Cross-source correspondence and consensus

For candidate frame duration `d`, its measurement interval is `[d-1,d+1]`.
Two independently estimated periods correspond only when these closed
intervals overlap, equivalently when their frame counts differ by at most two.
No additional tolerance is permitted.

After every source population is independently frozen, enumerate every
maximal tuple containing at most one persistent candidate per source whose
measurement intervals have a non-empty common intersection. A common-period
candidate requires at least two distinct contributors. Raw occurrence count
does not weight a source. Its descriptive point estimate is the equal-source
arithmetic mean of tuple frame durations; preserve the full tuple and common
uncertainty intersection.

Overlapping tuples are not merged. If one source candidate participates in
several defensible tuples, every tuple remains. Candidate identity is the
sorted set of contributor and source-candidate identities.

## Hierarchy and ambiguity

Preserve an exact `1:2` hierarchical relation when doubling the shorter
candidate's measurement interval overlaps the longer candidate's measurement
interval. Neither member is privileged. All other candidates remain preserved
without a role label.

Consensus classification is frozen as:

- `UNIQUE_COMMON_PERIOD`: exactly one common tuple;
- `MULTIPLE_COMMON_PERIODS`: more than one common tuple;
- `SOURCE_DISAGREEMENT`: at least two sources have persistent candidates but
  no cross-source correspondence;
- `NO_COMMON_PERIOD`: source candidates exist but no two sources supply a
  persistent candidate;
- `INSUFFICIENT_EVIDENCE`: input integrity or deterministic replay fails.

## Temporal-stability audit

For every common tuple report, per source, early/late occurrence counts,
first/last occurrence midpoint and support span. `FULL_SCOPE_PERSISTENT` means
every supporting candidate occurs in both source-scope halves. This audit may
describe persistence or region limitation only. It shall not construct a
local BPM trajectory or infer drift not measured by this recurrence protocol.

## Blind freeze and Ground Truth firewall

Freeze and checksum all source candidates, consensus tuples, hierarchy,
classification and corresponding rates before Ground Truth access. A rate is
reported only as `60 / period_seconds` and is labelled `CORRESPONDING_RATE`,
not quarter-note BPM.

SVP-001 permits post-blind Ground Truth evaluation after this immutable freeze.
Only then may the authoritative controlled tempo be loaded and compared with
the frozen candidates. Ground Truth shall not select, rerank or remove any
candidate, and no rerun or parameter change is permitted.

## Interpretation and architecture firewall

Source periodicity, common physical period, metric-reference role and BPM are
separate conclusions. Cross-source recurrence alone does not assign musical
metric role. Meter, measures, downbeats, accents, groove and behaviour are not
analysed.

Execution is experiment-local downstream of AD-037. It introduces no
production component, dependency, detector, AI model or architectural layer.
