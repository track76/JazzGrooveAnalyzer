# H-VAL001-RHYTHM-CORRESPONDENCE-02

Status: **FROZEN — NOT EXECUTED**

Authority: PI decision, AD-037, AD-038, AD-040, F-030 and SVP-001.

## Scientific History and Question

`H-VAL001-RHYTHM-CORRESPONDENCE-01` remains frozen and unchanged as the valid
negative result `INSUFFICIENT_CANDIDATES`. Its blind failure-mode audit found
that exact cross-source equality of two-sided interval signatures was not
scientifically required for temporal comparability and made the rule
structurally inapplicable to the differing source patterns.

This second experiment asks whether JGA can identify defensible candidate
temporal relations between accompaniment EME and Drum EME using mutual unique
geometry plus independently recurrent local temporal context within each
source, without BPM, meter, symbolic timing or a millisecond threshold.

## Frozen Hypothesis and Single Change

An accompaniment EME `A` and Drum EME `D` form a blind candidate temporal
relation if and only if:

1. `A` and `D` are mutual unique geometric nearest neighbours;
2. `A` has a valid exact two-sided within-source integer-frame interval
   signature;
3. `A`'s exact signature recurs at least twice independently within `A`'s own
   accompaniment source;
4. `D` has a valid exact two-sided within-source integer-frame interval
   signature;
5. `D`'s exact signature recurs at least twice independently within Drums;
6. neither event is a boundary, duplicate-frame or non-positive-interval case;
7. neither nearest relation is tied or frame-authority ambiguous; and
8. all frozen identity, provenance and deterministic-replay checks pass.

The only candidate-rule condition removed from Hypothesis 01 is:

```text
signature(A) == signature(D)
```

The two signatures need not be equal. Each is independent evidence that its
event occupies a recurrent local temporal context within its own source. No
other definition, criterion or scoring rule changes.

## Exact Blind Input Authority

Execution fails closed unless it binds exactly to:

- source revision `05ac8cee40958902b3bef69c30abf4d7f2497379`;
- AD-040 authority revision `b8983e8280a1077130acb420767e02b51de4551c`;
- blind input
  `validation/VAL-001/run_20260816_192519/blind_input.json`, SHA-256
  `25ee4d610f6a3130f0b4f001b1908c8dad443d34ee30413905f6fd377202c9e8`;
- blind source-record SHA-256
  `04468297cb6bf70e56af00d73c4071a96fabc429cfbabad1f81e302e7088ca02`;
- AD-038 result `validation/VAL-001/run_20260823_060808/result.json`,
  SHA-256
  `92baa58ed69032af8f6ef59b94e36bd7504774e947a96a7ada174658b82a1da7`
  and fingerprint
  `92a6b2e467d0b0b7fe465e9ccb8d9eb6d6e03ed9fb3e7435a2f0fd53bb4c2c62`;
- AD-038 rule `observed-drum-eme-relative-localization/v1`;
- AD-040 rule `rhythm-section-timing-profile/v1`;
- sample rate 44,100 Hz and hop length 512 samples; and
- populations Drums 63, Piano 49 and Double Bass 27 with frozen population
  fingerprints and asset checksums below.

| Source | Role | EME | Population fingerprint | Asset SHA-256 |
|---|---|---:|---|---|
| Drums | `TEMPORAL_REFERENCE` | 63 | `bdd609584ae58c3897691b1c400a3829b45dd637fe1fcc432cbdadc574b251ed` | `d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd` |
| Piano | `ACCOMPANIMENT` | 49 | `357be2d0c1ad88d8dccf4513c1aab165d7b48286861fff62ea954a62d99f72a2` | `26fa1158f375598cc7c01e04379c00547ef1787f6862eb2f29a36aafd9007c7e` |
| Double Bass | `ACCOMPANIMENT` | 27 | `80896b766d87b9a6d820223dfee5b928adab76397960fe2b728b6a8e158b6164` | `31d6f2e34d360c6f8f75362187433f2a2c1f5eb5cbbfe627305e99d07d8be6c5` |

Tenor Sax is excluded from the current Rhythm Section Timing Core. Voice is
`DEFERRED`. Neither observation population is altered.

## Frozen Frame, Signature, Recurrence and Nearest Definitions

All definitions are incorporated unchanged from
`H-VAL001-RHYTHM-CORRESPONDENCE-01`:

- `PulseCandidate.observation_index` is not onset-frame identity.
- `frame(E)` is the unique non-negative integer `k` within audio scope whose
  frozen `frames_to_time(k, sr=44100, hop_length=512)` IEEE-754 hexadecimal
  value exactly equals the immutable runtime EME timestamp hexadecimal value.
  No rounding, projection or tolerance is allowed. Zero or multiple matches
  stop execution as `INSUFFICIENT_FRAME_AUTHORITY`.
- Events are ordered independently per source by frame, then EME identity;
  identity ordering never resolves duplicate-frame eligibility.
- For an eligible non-boundary event `E_i`, with unique frames and positive
  intervals:

```text
left_interval  = frame(E_i) - frame(E_(i-1))
right_interval = frame(E_(i+1)) - frame(E_i)
signature(E_i) = (left_interval, right_interval)
```

- A signature recurs within one source only when the exact ordered pair occurs
  for at least two distinct eligible center EME in that source. Piano and
  Double Bass recurrence is independent and cannot be pooled.
- `D` must be the sole raw-distance-minimizing Drum EME for `A`, consistent
  with AD-038 `UNIQUE`; independently, `A` must be the sole raw-distance-
  minimizing EME in its accompaniment source for `D`. Any tie is unresolved;
  identity ordering cannot break it.

No distance, strength, density or tolerance condition exists.

## Blind Gates and Freeze

Preserve independent and cumulative survivors for:

1. valid accompaniment signature;
2. unique target-to-Drum nearest;
3. unique Drum-to-target reverse nearest;
4. mutual unique nearest;
5. recurrent Drum signature;
6. recurrent accompaniment signature; and
7. complete candidate criterion.

Before Ground Truth access, freeze complete candidates and unresolved records,
both EME identities and timestamps, both independent signatures and recurrence
support, both-direction nearest evidence, contributor, provenance, input and
profile fingerprints, scientific fingerprint and artifact checksums. Execute
twice from identical inputs and require byte-identical scientific content.

Any failed condition remains `UNRESOLVED / GEOMETRIC_ONLY`. A candidate is not
an AD-040 `AUTHORIZED_EVENT_RELATION`.

## Ground Truth Firewall and Scoring

Blind execution shall not open symbolic score, MusicXML, MIDI, symbolic
timing/pairing, declared BPM/meter, measures, BeatReference or existing Ground
Truth outcomes. Only after blind freeze and deterministic replay may the
checksum-bound Calibration Zero absolute correspondence and symbolic-pair
authorities score frozen candidates. Ground Truth cannot create, remove,
rematch or modify any blind evidence.

A candidate is scorable only when both EME have unique frozen symbolic-event
correspondences. It is TP only when those exact symbolic events form an
authorized frozen symbolic pair; a scorable non-pair is FP. A scorable
authorized symbolic relation without a candidate is FN. Non-unique or absent
correspondence is ambiguous/unscorable.

Report Piano–Drums, Double Bass–Drums and overall candidate, unresolved,
scorable, ambiguous/unscorable, TP, FP, FN, precision, recall and F1. Undefined
metrics remain null. Preserve complete event-level scoring records and the
exact comparison to Hypothesis 01's zero candidates.

## Frozen Classification

Apply the first matching outcome:

1. `FAIL`: integrity, firewall, raw-immutability or replay failure.
2. `INSUFFICIENT_CANDIDATES`: no scorable candidate overall or either source
   has no scorable candidate.
3. `HIGH_PRECISION_USEFUL_CANDIDATE_RULE`: overall and each source precision
   equal exactly 1.0 with at least one scorable candidate per source.
4. `LOW_PRECISION`: overall precision is defined and `FP >= TP`.
5. `LOW_RECALL`: overall precision exceeds 0.5, recall is defined and
   `FN >= TP`.
6. `PARTIAL_CORRESPONDENCE_EVIDENCE`: both sources have scorable candidates
   and no earlier outcome applies.

Recall does not disqualify the high-precision outcome. No post-reveal tuning is
permitted.

## Immutability and Interpretation Firewall

The experiment creates validation-local evidence only. EME, PulseCandidates,
AD-038 localizations, AD-040 profiles, Calibration Zero and Hypothesis 01 are
immutable. No production promotion or correction is authorized.

A validated candidate supports only controlled temporal comparison. It does
not establish beat, subdivision, musical equivalence, synchronization intent,
groove, swing or performance quality. The experiment uses no BPM, meter,
threshold, clustering, strength, Drum classification or AI.
