# H-VAL001-RHYTHM-CORRESPONDENCE-01

Status: **FROZEN — NOT EXECUTED**

Authority: PI decision, AD-037, AD-038, AD-040, F-030 and SVP-001.

## Frozen Scientific Question

Can JGA identify defensible candidate temporal relations between accompaniment
EME and Drum EME without BPM, meter, symbolic timing or an arbitrary
millisecond threshold?

A successful candidate means only that sufficient blind observational
structure exists to justify temporal comparison of two physical events. It
does not establish musical equivalence, intended synchronization or shared
metric identity.

## Execution State and Hypothesis Freeze

This preregistration freezes one Ground-Truth-blind experiment before blind
candidate calculation or access to symbolic correspondence outcomes. The
experiment shall not execute without a separate PI decision. The rule,
classifications and validation metrics shall not be relaxed, retuned or
extended after result access.

The frozen hypothesis is:

> An accompaniment EME and Drum EME form a blind candidate temporal relation
> only when they are mutual unique geometric nearest neighbours, possess the
> same exact two-sided within-source integer-frame interval signature, that
> signature recurs at least twice independently within each source, and
> neither event is a boundary or tie case.

## Exact Blind Input Authority

Execution shall fail closed unless it binds exactly to:

- source revision `05ac8cee40958902b3bef69c30abf4d7f2497379`;
- AD-040 authority revision `b8983e8280a1077130acb420767e02b51de4551c`;
- existing timestamp-only blind input
  `validation/VAL-001/run_20260816_192519/blind_input.json`, SHA-256
  `25ee4d610f6a3130f0b4f001b1908c8dad443d34ee30413905f6fd377202c9e8`;
- blind-input source-record SHA-256
  `04468297cb6bf70e56af00d73c4071a96fabc429cfbabad1f81e302e7088ca02`;
- AD-038 result
  `validation/VAL-001/run_20260823_060808/result.json`, SHA-256
  `92baa58ed69032af8f6ef59b94e36bd7504774e947a96a7ada174658b82a1da7`
  and scientific fingerprint
  `92a6b2e467d0b0b7fe465e9ccb8d9eb6d6e03ed9fb3e7435a2f0fd53bb4c2c62`;
- AD-038 localization rule `observed-drum-eme-relative-localization/v1`;
- AD-040 profile rule `rhythm-section-timing-profile/v1`;
- sample rate 44,100 Hz and frame length 512 samples; and
- the following complete population bindings:

| Source | AD-040 role | EME | Population fingerprint | Asset SHA-256 |
|---|---|---:|---|---|
| Drums | `TEMPORAL_REFERENCE` | 63 | `bdd609584ae58c3897691b1c400a3829b45dd637fe1fcc432cbdadc574b251ed` | `d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd` |
| Double Bass | `ACCOMPANIMENT` | 27 | `80896b766d87b9a6d820223dfee5b928adab76397960fe2b728b6a8e158b6164` | `31d6f2e34d360c6f8f75362187433f2a2c1f5eb5cbbfe627305e99d07d8be6c5` |
| Piano | `ACCOMPANIMENT` | 49 | `357be2d0c1ad88d8dccf4513c1aab165d7b48286861fff62ea954a62d99f72a2` | `26fa1158f375598cc7c01e04379c00547ef1787f6862eb2f29a36aafd9007c7e` |

Tenor Sax is outside the current Rhythm Section Timing Core. Voice remains
`DEFERRED`. Both are excluded from input without altering their observations.

Execution shall materialize the AD-040 profile from the bound AD-037 EME and
AD-038 localization evidence using explicit PI-authorized roles. Before any
candidate calculation, preserve the profile identity, fingerprint, complete
EME/localization identity inventory and an input-manifest checksum.

PulseCandidate strength, Calibration Zero results, full mix, symbolic sources,
MusicXML, MIDI, BeatReference, declared metric information and all existing
post-freeze Ground Truth outcomes are excluded from blind input.

## Exact Frame Identity

`PulseCandidate.observation_index` is sequence ordinal and shall not be treated
as onset-frame identity.

For an immutable runtime EME timestamp `t`, define `frame(E)` as the unique
non-negative integer `k` within the declared audio scope for which the exact
IEEE-754 hexadecimal value of `t` equals the exact IEEE-754 hexadecimal output
of the frozen observation producer's configured
`frames_to_time(k, sr=44100, hop_length=512)` operation.

No nearest-integer projection, rounding, tolerance or residual-based selection
is permitted. If zero or more than one `k` satisfies exact equality, input
status is `INSUFFICIENT_FRAME_AUTHORITY` and blind execution stops before any
signature or candidate relation is calculated.

The checksum-bound historical blind-input serialization binds population and
identity. Exact frame identity is established only from the immutable runtime
timestamp and frozen producer operation; its lower-precision JSON projection
shall not be used to infer a frame.

## Ordered Source Populations

Treat Drums, Double Bass and Piano independently. Within each source, order all
EME by `frame(E)`, then EME identity. Preserve duplicate-frame observations.
An event sharing its frame with another same-source event is non-unique for
local signature ownership and remains unresolved; identity ordering is for
serialization only and shall not make the event eligible.

No event is removed from the audit population.

## Exact Two-Sided Interval Signature

For ordered source event `E_i`, a signature exists only when:

- `E_(i-1)` and `E_(i+1)` exist;
- `E_i` and both neighbours occupy unique source frames; and
- both consecutive intervals are strictly positive.

Define exactly:

```text
left_interval(E_i)  = frame(E_i)     - frame(E_(i-1))
right_interval(E_i) = frame(E_(i+1)) - frame(E_i)
signature(E_i)      = (left_interval(E_i), right_interval(E_i))
```

The signature is an ordered pair of exact positive integers. No tolerance,
rounding, approximate equality, reversal, scaling or interval swapping is
permitted.

The first and last source events, duplicate-frame events and events adjacent
to a non-positive or non-unique interval have no valid two-sided signature.

## Exact Recurrence Rule

For source `S`, recurrence count for signature `q` is the number of distinct
eligible center EME in the complete ordered `S` population whose exact
two-sided signature equals `q`.

`q` is recurrent in `S` if and only if that count is at least two. Each
supporting center EME and its two neighbouring EME identities shall be
preserved. Overlapping signatures are permitted because their center EME are
distinct. Duplicate evidence records for one center are prohibited.

For target `A` in accompaniment source `S` and Drum event `D`, the recurrence
condition passes only when:

```text
signature(A) == signature(D) == q
recurrence_count(S, q) >= 2
recurrence_count(Drums, q) >= 2
```

Double Bass and Piano are evaluated separately and may not borrow recurrence
support from each other.

## Exact Mutual-Unique-Nearest Rule

For accompaniment event `A` in source `S`:

1. AD-038 must report `nearest_selection_status == UNIQUE` and a non-null
   `nearest_drum_eme`; call it `D`.
2. Independent arithmetic replay over the complete Drum population must show
   that `D` alone minimizes `abs(timestamp(A) - timestamp(drum))`.
3. Over the complete accompaniment population `S`, `A` alone must minimize
   `abs(timestamp(D) - timestamp(source_event))`.

Any exact equal-distance candidate in either direction makes the relation
non-unique. No identity-order tie breaking is permitted for correspondence.
Piano and Double Bass nearest searches remain contributor-separated.

The timestamp geometry used by this rule remains raw AD-038 evidence. No
millisecond cutoff, calibration adjustment or maximum-distance condition is
introduced.

## Frozen Candidate-Relation Criterion

One and only one blind candidate relation `(A, D)` is produced when all of the
following hold:

1. `A` belongs to the complete Piano or Double Bass AD-040 accompaniment
   population and `D` belongs to the complete Drum temporal-reference
   population;
2. `(A, D)` passes the exact mutual-unique-nearest rule;
3. both events possess valid exact two-sided signatures;
4. `signature(A) == signature(D)`;
5. the shared signature recurs at least twice independently in `A`'s source
   and at least twice in Drums; and
6. no frame-authority, boundary, duplicate-frame, tie, identity, provenance or
   deterministic-replay conflict affects either event.

All other accompaniment/Drum geometry remains `GEOMETRIC_ONLY` with blind
candidate status `UNRESOLVED` and every failed condition recorded. A blind
candidate is not promoted to AD-040 `AUTHORIZED_EVENT_RELATION` before
post-freeze validation.

## Blind Freeze Procedure

Execution order is mandatory:

1. verify all checksums, revisions, populations, assets and configuration;
2. materialize and fingerprint the exact AD-040 profile;
3. establish exact frame authority or stop fail-closed;
4. freeze ordered populations, every signature and recurrence inventory;
5. freeze both-direction nearest audits and all tie/boundary statuses;
6. freeze the complete candidate and unresolved populations independently for
   Piano–Drums and Double Bass–Drums;
7. write complete machine-readable event-level evidence and failure reasons;
8. repeat blind execution from identical inputs and require exact replay; and
9. freeze an artifact manifest, blind scientific fingerprint and completion
   record before any Ground Truth access.

The blind fingerprint covers input identities, profile fingerprint, frame
inventory, ordered EME identities, signatures, recurrence support, both
nearest directions, candidate relations and unresolved reasons. Execution
timestamps and local paths are excluded from scientific content.

## Ground Truth Firewall and Future Reveal

Blind construction shall not open or derive from symbolic score, MusicXML,
MIDI, symbolic timing, symbolic pairing, declared BPM/meter, measures,
BeatReference or any existing Ground Truth outcome.

Only after the blind artifact and fingerprint are frozen may a separately
authorized validation stage verify and open the existing checksum-bound
Calibration Zero symbolic-event authority, absolute correspondence artifact
and symbolic-pair authority. Ground Truth may score the frozen population only;
it shall not create, remove, rematch, rank or modify a blind relation.

A blind pair is scorable only when both EME have unique frozen symbolic-event
correspondences. It is a true recovered relation only when those exact symbolic
events form an authorized symbolic pair under the already-frozen Calibration
Zero pair authority. A scorable blind pair that does not form that exact pair
is false. Symbolic relations are missed when their two uniquely corresponding
EME form no frozen blind candidate. Non-unique or unavailable symbolic
correspondence is ambiguous/unscorable and reported separately.

No parameter, outcome criterion or matching rule may change after reveal.

## Frozen Validation Metrics

Report overall, Piano–Drums and Double Bass–Drums separately:

- complete accompaniment and Drum input counts;
- blind candidate count;
- unresolved count by exact failed condition;
- scorable and ambiguous/unscorable blind candidates;
- true authorized symbolic relations recovered (`TP`);
- false candidate relations (`FP`);
- scorable authorized symbolic relations missed (`FN`);
- ambiguous/unscorable symbolic relations;
- `precision = TP / (TP + FP)` when defined;
- `recall = TP / (TP + FN)` when defined;
- `F1 = 2 * precision * recall / (precision + recall)` only when both metrics
  are defined and their sum is positive;
- complete event-level score records; and
- exact deterministic replay and scientific fingerprints.

Undefined metrics remain null and shall not be replaced by zero. No event or
ambiguous evidence is suppressed.

## Frozen Allowed Outcomes

Apply the first matching rule in this order:

1. `FAIL`: checksum, authority, firewall, raw-immutability or deterministic
   replay failure.
2. `INSUFFICIENT_CANDIDATES`: no scorable blind candidate overall, or either
   accompaniment source has no scorable blind candidate.
3. `HIGH-PRECISION_USEFUL_CANDIDATE_RULE`: overall and contributor-specific
   precision are exactly `1.0`, with at least one scorable candidate for each
   accompaniment source. Recall is reported but does not disqualify this
   outcome because sparse reliable candidates are explicitly acceptable.
4. `LOW_PRECISION`: overall precision is defined and `FP >= TP`.
5. `LOW_RECALL`: overall precision is greater than `0.5`, overall recall is
   defined, and `FN >= TP`.
6. `PARTIAL_CORRESPONDENCE_EVIDENCE`: scorable candidates exist for both
   accompaniment sources but none of the preceding outcome rules applies.

Contributor-specific metrics and limitations remain mandatory even when the
overall outcome is singular. Negative and sparse outcomes are valid scientific
results. Coverage shall not be optimized after reveal.

## Raw Immutability and Interpretation Firewall

The experiment may create experiment-local evidence records only. It shall not
modify EME, PulseCandidates, AD-038 localizations, AD-040 profiles, Calibration
Zero artifacts or existing visualizations. PulseCandidate strength is not
loaded or used. Calibration evidence is measurement context only and does not
create, select or correct a relation.

No blind candidate implies a shared beat, subdivision, note, synchronization
intent, groove role or musical equivalence. The experiment uses no threshold,
clustering, AI, BPM, meter, measures or musical interpretation.

## Determinism, Architecture and Production

Two executions from identical frozen inputs must reproduce byte-identical
frame authority, signature inventories, recurrence support, nearest audits,
candidate/unresolved populations and scientific fingerprint. Any mismatch is
`FAIL`.

The experiment is local to scientific validation. A later accepted result may
support a downstream Analysis projection over AD-037, AD-038 and AD-040. No
new architectural layer is introduced. Production impact is **NONE**; no
production implementation is authorized.
