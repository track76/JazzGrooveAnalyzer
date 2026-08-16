# H-VAL001-RHYTHM-ROLE-01 — Rhythm-Section Metric-Role Preregistration

Status: PREREGISTERED — NOT EXECUTED

Authority: JGA Scientific Research Constitution, SVP-001, F-032, AD-035 and
AD-037

## Scientific question

Can neutral temporal organization of complete Drums, Double Bass and Piano EME
populations discriminate the two already-frozen hierarchical common-period
families without Ground Truth or musical-role assumptions?

No new period is discovered. Input is the immutable blind result of
`H-VAL001-RHYTHM-TEMPO-01`, SHA-256
`0f6d8162053142893d4f938f32c73174b26dd8c783a457ad98e6e491ecb369cd`.

## Frozen EME populations

| Contributor | EME | Fingerprint |
|---|---:|---|
| Drums | 63 | `bdd609584ae58c3897691b1c400a3829b45dd637fe1fcc432cbdadc574b251ed` |
| Double Bass | 27 | `80896b766d87b9a6d820223dfee5b928adab76397960fe2b728b6a8e158b6164` |
| Piano | 49 | `357be2d0c1ad88d8dccf4513c1aab165d7b48286861fff62ea954a62d99f72a2` |

Every EME identity and timestamp is retained. Voice remains `DEFERRED`; Tenor
Sax, full mix, symbolic evidence, declared BPM/meter/timeline, normalized
phase, Ground Truth and AI evidence are excluded.

## Frozen candidate families

The SHORT family consists of these frozen common-period identities:

- `RCP-d5ffc083c273a55acad93186be4b3190150babb558a247c1bc626811139e3d7d`;
- `RCP-c953167752e31df8a6822d7f8228819c8c85eb90fe97423476770d8d20ff21cb`;
- `RCP-49fac2900de54fd737e4b6ce57177fab0e68f3e2145e70197d8ed6ff1da8eeb9`;
- `RCP-cb42f47c336f7a91b8b578d72b5282a356f08c849423d1d4c94d327ba21e7ea0`.

The LONG family consists of:

- `RCP-e1f164f0c17452afde41470ffd078bc18a624e92111780eca8e709b4c3a99660`;
- `RCP-a0e4cbece9254e5af4bd0364e04ee6b537d3a7bc5c5e5361dfd25eae82b448c5`;
- `RCP-aa3105c88891efbae9adcd9efffd5ae96a77dcb022d0a2a4c16ad6afed3b7780`;
- `RCP-7c1efed257ebb311645aaf5a2b574bc320da23b5640fe870b3d8f06207218cdf`.

Family names are geometric identifiers only. The frozen measurement interval
of every candidate is imported unchanged.

## Nuisance origin and period uncertainty

For each candidate, evaluate every integer period frame inside its frozen
measurement interval. For each period `P`, evaluate every integer origin
residue `o` in `[0,P)`. This exhaustive one-frame grid derives solely from the
512-sample observation resolution and is identical for both families.

No origin is interpreted. For each statistical model, period and origin are
nuisance values selected only by maximum likelihood. Preserve all likelihoods
and the selected nuisance values. Exact ties select smaller period then smaller
origin. Non-identifiability is reported when several combinations share the
same serialized optimum.

## Neutral organization measurements

For each source and candidate independently:

1. assign every EME to its candidate cycle for each nuisance period/origin;
2. retain partial edge-cycle exposure so no EME is discarded;
3. count EME occupancy in every successive cycle;
4. fit Poisson occupancy models whose rate repeats every `L` cycles; and
5. preserve phase concentration `R = |mean(exp(2πit/P))|`, circular center and
   pairwise source-center differences as descriptive geometry only.

The origin changes the reported center but not `R`; cross-source center
differences are invariant to a common origin shift. Use 2,000 deterministic
nonparametric EME bootstraps for 95% intervals of `R` and center differences.
These descriptive phase quantities do not decide metric role.

## Higher-order recurrence search

For each candidate and temporal scope, test every integer `L` beginning at 1
for which at least four complete `L`-length recurrences fit in that scope:

`L = 1 .. floor(complete_cycle_count / 4)`.

No particular length is inserted or privileged. A model has one Poisson rate
per cycle class, with exposure offsets for partial edge cycles. Select the
period, origin and `L` combination having minimum
`BIC = parameter_count * ln(cycle_count) - 2 ln(likelihood)`. Period and origin
are counted as two nuisance parameters. Exact BIC ties select smaller `L`,
then smaller period and origin. Preserve every tested model and rejected
insufficient-cycle reason.

## Temporal partition and source decision

Run the identical search over the full source timestamp scope and its exact
early/late temporal halves. A candidate's selected organization length is
`PERSISTENT` only when full, early and late scopes select the same `L`.

For one source:

- `SHORT_FAMILY_PREFERRED` only when every SHORT candidate persistently
  selects `L=1`;
- `LONG_FAMILY_PREFERRED` only when every SHORT candidate persistently
  selects `L=2`;
- otherwise `EQUIVALENT_OR_UNRESOLVED`.

LONG-family higher-order lengths are all reported but do not create a slower
automatic preference. The 1:2 relation alone contributes no vote.

## Equal-source consensus

Each contributor has one vote:

- final `SHORT_FAMILY_PREFERRED` when at least two sources prefer SHORT and no
  source prefers LONG;
- final `LONG_FAMILY_PREFERRED` when at least two sources prefer LONG and no
  source prefers SHORT;
- `SOURCE_DISAGREEMENT` when at least one source prefers each family;
- `EQUIVALENT_HIERARCHICALLY_UNRESOLVED` when no family reaches two votes and
  input/replay remain valid; or
- `INSUFFICIENT_EVIDENCE` when input integrity or deterministic replay fails.

No raw event count weights a vote. Ambiguous sources abstain. Deterministic
replay must reproduce all model selections, measurements and the final
scientific fingerprint exactly.

## Blind freeze, allowed outcomes and firewall

Freeze the complete result and checksum before Ground Truth access. Allowed
outcomes are SHORT, LONG, EQUIVALENT/HIERARCHICALLY UNRESOLVED, SOURCE
DISAGREEMENT and INSUFFICIENT EVIDENCE.

Only after freeze may SVP-001 Ground Truth validation report whether the blind
family classification agrees with the authoritative controlled context.
Ground Truth cannot alter inputs, models, nuisance choices, votes or outcome.

This experiment assigns no beat, quarter note, downbeat, meter, measure,
subdivision, timing-behaviour or groove meaning during blind execution. It is
experiment-local and introduces no production or architectural change.
