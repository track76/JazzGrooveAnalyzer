# Drum periodicity recurrence-sufficiency research design

Identifier: DRUM-RECURRENCE-SUFFICIENCY-DESIGN-01. Date: 2026-09-10. Status: **AUDIT / PROPOSED DESIGN FOR PI REVIEW; NO EXECUTION AUTHORIZATION**.

## 1. Decision brief and authority boundary

The accepted finite map is reusable for exact, lineage-aware descriptive relations and a bounded recurrence-witness audit. It does **not** already identify cross-center recurrent structures. There is **INSUFFICIENT AUTHORITY** for a defensible PASS criterion promoting its responses to RECURRENCE_SUFFICIENCY_ESTABLISHED. A map coordinate appearing at several centers is automatic enumeration, not evidence. Multiple period alternatives must survive. No musical reference is selected.

The PI now explicitly reopens only RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED. This supersedes the bootstrap’s earlier no-new-task permission boundary, not any scientific conclusion. Repository evidence agrees with its accepted-map snapshot. The Double-Bass work and frozen Bass-recovery conclusions are independent and unchanged. No BPM, beat trackers, score/reference timeline or accompaniment values enter the proposed discovery. No audio, Fourier operator, recurrence algorithm or experimental control was executed during this audit.

Evidence classes: **Observed Fact** = inspected records/hash verification, not independent revalidation of their scientific claims; **Logical Inference** = consequence of the preserved mathematical contract; **Proposed Design** = requires PI approval; **UNKNOWN** = authority absent. Sufficiency classifications below describe requirements for a stated claim, not newly binding architecture. This is not a preregistration ready for execution.

## 2. Authoritative starting state and verification

Canonical starting package: `validation/VAL-001/complete_real_drum_periodicity_20260908/`. Its README records PI acceptance of **PASS — VAL001_COMPLETE_REAL_DRUM_LOCAL_COMPLEX_PERIODICITY_MAP_OBSERVED**. Preregistration: `validation/VAL-001/preregistrations/H-VAL001-COMPLETE-REAL-DRUM-PERIODICITY-01.md`, with `.inputs.json` and `.authorities.json` siblings. `implementation_binding.json` freezes driver, validator and transitive dependencies. The historical preregistration’s pre-execution wording is not the current run status; README, scores and replay establish acceptance.

| Accepted quantity | Authority-verified value per run |
|---|---:|
| Centers | 63 |
| Period coordinates | 1,056 |
| Center-specific scales | 3,864 |
| Queries | 4,080,384 |
| Ordered event accumulations, including boundaries | 133,195,392 |
| Distinct unordered event-ID pairs in coordinate generation | 1,953 |
| Validator passed checks / failures | 126,506,686 / 0 |
| Replay passed checks / failures | 1,007 / 0 |
| Byte-identical bulk files recorded by acceptance | 1,003, including 997 response shards |

These counts were verified in the input freeze, implementation assertions, accepted README, score and replay records. No coordinate population or response was regenerated to count it. Queries are not independent samples; run_2 is not a second performance.

Scientific fingerprint: `03146e8794151bb91faa938eb3f0f8ea1cfda34a12faaaf84158e820c39e96fc`.
Logical-record fingerprint: `1e5030acfa48d976832c31ebff220c5094ff14a7567bc67648cdbd01de8d54a9`.
Root hash: `0e9290e7cf47f9c87abfbadf5df92e1099b4c870429b6cb3723df2d8d85df4d2`.
Replay hash: `0360779603ffc1b3982d06cc01da00ae428e205fc95e52106bd1b433e15733cb`.
Implementation binding hash: `e91b5d2b961f0274706732f46e0ec274fd0b839b921ebaaf7e7e71ce87dcb2f5`.

External source exists at `/Volumes/SSD Track/JGA/experiments/H-VAL001-COMPLETE-REAL-DRUM-PERIODICITY-01/`, `run_1/production/` and `run_2/production/`. This audit rehashed every file listed in the bounded package SHA256SUMS, all entries of the input authorities and implementation binding, both external roots/indexes and all their shared catalogues (`inputs.json`, `periods.json`, `windows.jsonl`). One run_1 response shard was hash-verified and one row inspected for schema. **The entire 30-GB two-run shard population was not rehashed or byte-compared here.** Complete equality remains the accepted replay record’s result; this audit is not a fresh full replay. Future execution must verify every consumed shard before using it. No accepted preservation/validation program was run.

### Existing successor designs, not completed recurrence evidence

`validation/VAL-001/preregistrations/H-VAL001-DRUM-RECURRENCE-STRUCTURE-01.md` already defines lossless period profiles, exact-(T,L) temporal edges, scale edges, support overlap and narrowly descriptive phase comparisons. It explicitly remains BLOCKED FOR RECURRENCE CLAIM. Its authority manifest hash is `73f8415d4fd6234be276acc2158e498aadbdb0c7b1caa9248882a89e256a9136`; its 13 authority-file bindings were verified. No scientific permission is inferred from its filename.

`H-VAL001-DRUM-STRUCTURAL-TRANSITION-01.md` and its manifest define a separate descriptive spacing/strength channel, not transition significance or texture identity. Its 10 file bindings were verified. `H-VAL001-TEMPORAL-CELL-SINGLETON-01.md` is an unexecuted accompaniment correspondence design with missing independent scoring authority; it is not a recurrence authority and is excluded from the proposed inputs. This audit does not silently execute or revise these designs.

## 3. What the map actually measures

Let e denote a preserved EME, with unique supporting PulseCandidate, exact accepted dyadic timestamp t_e, native AD-032 strength s_e and source lineage. Exactness means preservation of producer binary64 values; it does not mean exact physical contact time. Define:

- **Center u:** a distinct accepted event timestamp. All coincident EME identities would remain attached; the center is not an independently chosen fixed-time observation or musical position.
- **Period T:** a distinct positive all-pairs separation |t_j−t_i| for two different EME IDs. Every generating pair and parent lineage is retained. Frequency f=1/T is a query coordinate. These 1,056 coordinates are **not automatically F-032 Candidate Periods**, nor interchangeable with AD-035 consecutive-frame candidates.
- **Center-specific scale L:** a distinct positive 2|t_e−u|. Requested support is [u−L/2,u+L/2]. Its center/boundary generation pairs, contained/boundary/positive members, clipping and unavailable pieces are preserved. L is full window width, not a period or normalized scale index.
- **Query:** (population ID,u,L,T); loops u then L then T. All global T occur at every admitted (u,L). No ranking, selected maxima or inferred period trajectory exists.

The accepted mathematical operator is

C(u,L,T) = Σ_{|t_e−u|≤L/2} s_e · [1+cos(2π(t_e−u)/L)]/2 · exp(−2π i t_e/T).

Only the frozen in-scope events are available; requested support is intersected with asset/scope without padding or fabricated silence. Boundary events remain in accumulation even though their ideal Hann weight is zero. The bound implementation preserves expression order, timestamp/ID reduction order and 128-bit certified arithmetic. This formula describes existing evidence; it is not evaluated here.

**Values:** real/imaginary interval balls, magnitude bounds, zero-containment flag, phase interval/status and contributing IDs. Coefficients are weighted sparse detector-strength responses, not audio spectra, acoustic energy, loudness, likelihoods, statistical significance or recurrence confidence. `score_1.json` is contract-validation scoring, not a period quality score. Large magnitude can reflect support/strength/density; a single positive-weight event yields nonzero response at every frequency. Zero containment is not proof of exact cancellation; phase may be unresolved or conservatively cover the branch cut. Numerical enclosures do not quantify detector error, missed events or source-separation error.

**Variable:** u, L, T, f, memberships, generation/evaluation overlap, requested/available support, clipping and numeric responses. **Fixed:** one source-instance population and asset, 63 observations, producer measurements, scope/origin, strength semantics, query rule, Hann family, operator, arithmetic/ordering, environment binding and serialization. Scope is closed [0, accepted binary64 42.30675736961451 s]; the 1,865,728 samples at 44,100 Hz are diagnostics and must not replace that duration. Global exponential phase uses absolute t; do not independently rephase each center.

**Missing versus zero:** distinguish NOT_IN_QUERY_DOMAIN (especially absent L at another center), unavailable/truncated support, no positive-weight contributors, exact numerical zero if certified, zero-containing enclosure, unresolved/branch phase, and physical events never observed. No state proves musical absence. No interpolation or manufactured cycles across gaps.

## 4. Source, event identity and architecture

Source UUID: `c46d6cb9-b99c-5bd6-8d81-656dc1ad48ec`; source authority `VAL-001-DIRECT-INPUT-SOURCE-AUTHORITY-V1`; opaque key `VAL001_SOURCE_001`. Asset hash: `d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd`. The AD-041 authority binds that key to the existing `rendered_stems.Drums` asset-authority entry. Its historical storage key and the accepted “real Drum” experiment title do not certify a microphone-isolated physical Drum component. UUID derivation excludes filename, instrument label and asset hash. The canonical producer report hash is `eeb189217a722679d5f40bef4d809e2b38ab381e9dea81057023dfd3d80e05c7`.

The legitimate common characteristic is **membership in the same explicitly bound source-instance observation population under the same measurement/representation contract**. It is not “all these are Ride,” “same timbre,” or “same function.” AD-037 preserves each PulseCandidate-supported EME independently; parent ID, timestamp/strength field pointers, producer bits, source and asset references permit audit. The 63 EME have 63 unique supporting PulseCandidate identities. Reusing an EME in several windows does not create a new occurrence.

AD-015 requires source identity preservation through Core and Translation. AD-037 materialization precedes metric localization and does not establish note identity. AD-038 geometric Drum-relative localization and AD-040 timing profiles preserve relations without musical authority; neither supplies this study with a beat or accompaniment correspondence. AD-041’s accepted htdemucs_6s operational path has its own parent/separator/output-key binding and prepared/native-asset distinction. It is **not** the direct-input map’s identity derivation and supplies no Drum-component labels here. No source identity is reconstructed from “Drums.”

Core → Translation → Domain remains unchanged. Proposed derived recurrence relations are research objects over immutable observations, not a new production component. Translation must not infer missing identity. Future metric meaning requires Domain authority; names such as EME, MetricSource and TEMPORAL_REFERENCE do not themselves grant it.

## 5. Operational recurrence taxonomy

F-032 §3.1 defines recurrence as repeated occurrence of a temporal relation in a declared population/scope, while supplying no equality tolerance or statistical method. The following **proposed narrow operationalization** uses existing exact coordinate equality and lineage, not a new acoustic similarity metric:

For T>0, an occurrence is a distinct unordered pair of EME identities {i,j} in this frozen source population, with |t_j−t_i|=T as exact accepted ratios. Its support is [min(t_i,t_j),max(t_i,t_j)]. **Exact observed-relation recurrence** means more than one distinct occurrence supports that same T; duplicate serialization/window reuse counts once. “More than one” describes repetition, not a numerical sufficiency PASS threshold or transfer of AD-035’s algorithm. Retain shared-endpoint and event-disjoint occurrences separately. Event-disjoint does not mean statistically independent. This scope says nothing about physical-time tolerance or recurrence beyond detection.

| Concept | Input / mathematical object / temporal conditioning | Equality and uncertainty/missingness | Counterexample / falsification |
|---|---|---|---|
| A. Event recurrence | Distinct EME-pair occurrences and their full temporal spans; optionally ordered event motifs | Exact pair separation under source/measurement freeze; same EME ID reused is exact identity, not repeated physical event. Physical uncertainty remains unquantified | One pair shown in many windows is not repetition. Claimed exact T witness falsified if its different-ID endpoints do not have T separation |
| B. Source-conditioned recurrence | Occurrence collection restricted to the explicit UUID, asset/scope and measurement contract | Same authority/key qualifies shared source context, not same instrument component; cross-source identity not supplied | Two files labelled Drums lack common authorized identity. A witness with an alien/missing source binding is inadmissible |
| C. Period recurrence | P_T, the catalogue’s distinct generating pairs for exact T; temporal extent and endpoint-overlap retained | Repeated pair support, not appearance of the query label. Near T values remain separate; missed pairs/events outside scope UNKNOWN | All centers query T even if its sole generating pair is elsewhere. Fewer than two valid occurrences falsifies only the proposed exact repeated-relation assertion |
| D. Local-structure recurrence | Proposed signature of ordered (t_e−u,s_e,lineage-role) within declared equal-L, equally clipped windows; alternatively interval-only signature explicitly typed | Exact translation correspondence is definable; inclusion of strength changes the proposition. No distance, rescaling or approximate match authorized; finite enclosures are not physical similarity | Equal count/mean/response may mask different timestamp patterns. No bijection preserving declared exact fields falsifies exact signature equality, not approximate recurrence |
| E. Cross-center structural recurrence | Existing successor’s temporal edges at identical exact (T,L), plus endpoints’ memberships, generating pairs and support intersection/differences | These edges index comparable queries; they do not yet assert recurrence. Exact witness incidence can be derived by pair containment in positive members; shared evidence flagged, absent L remains missing | Repeated response caused by the same two EME is reused support. A claimed new local witness falsified if identical pair is counted twice or endpoints are outside declared support |
| F. Multiscale / hierarchical recurrence | Existing typed scale edges and exact period ratios with witness sets across centers | Every L retained; exact integer/doubling relation is arithmetic only. Hierarchical co-organization/equality criterion UNKNOWN; no low-denominator clustering | All dyadic periods have rational ratios, so rational connectedness is tautological. Missing exact ratio falsifies that arithmetic claim; no hierarchy claim is authorized to test yet |

A scalar recurrence flag for D/E/F beyond these narrowly typed facts is **not defined**. Approximate timing/strength/timbre recurrence needs independent measurement-aware correspondence authority. Counterexamples can invalidate a stated exact relation without disproving a broader physical recurrence hypothesis. This taxonomy does not relabel uncertainty as FAIL.

## 6. What “same/comparable characteristics” can mean

| Category | Admissible meaning | Present representation / limit |
|---|---|---|
| EXACT IDENTITY | Same EME/PulseCandidate/query/source identity under authority | YES for tracing one observation or replay. Not an independent occurrence; indices alone never match separate detection runs |
| MEASUREMENT EQUIVALENCE | Same source/input/producer/coordinate/strength/precision contract; compare identical T,L with declared coverage | Contract metadata present. Different centers have different memberships; different L are different operators. Equal numbers/enclosure overlap do not prove same physical event or underlying response |
| STRUCTURAL SIMILARITY | A declared relation-preserving map between different event configurations | Exact temporal translation signature can be proposed from saved timestamps/lineage. No accepted approximate/acoustic distance, invariance rule or tolerance exists. New relation representation is required, not new audio for the exact case |
| SOURCE-CONDITIONED COMPARABILITY | Same bound UUID and measurement population, while retaining each event’s own identity | YES within the single source. Does not imply same Ride/Hi-Hat/Snare, attack morphology or performance role |
| MUSICAL/SEMANTIC SIMILARITY | Same expected beat, instrument role, rhythm or metric position | EXCLUDED; no manual class, filename, symbolic schedule or metric localization joins |

No event-local spectrum, transient envelope, timbral feature, physical-contact label or independently validated Drum-component identity is present in the map. Native onset strength is one detector quantity, not a sufficient “same sound” signature. The minimum is comparable **temporal observations**, not comparable physical Drum articulations. F-032 and C1-07/C1-10 prohibit silently filling this gap with numerical proximity.

## 7. Periodicity versus recurrence and multiple alternatives

1. Large response at one center is a local operator value; “strong” has no threshold/normalization authority here.
2. Repeated exact T across centers is query-domain identity. Repeated **distinct pair support** at exact T is a different, auditable proposition. A period can be generated outside a window and queried inside it.
3. Exact T ratios preserve arithmetic relationships, not recurring family organization. The existing successor correctly notes that unrestricted rational relations connect every pair of rational periods; connected components cannot discover families that way.
4. Timing-variation stability requires an authorized tolerant correspondence rule and error/control model; the accepted exact dyadics cannot supply it merely by being precise.
5. Coincidental numerical proximity cannot be rejected by nonzero scores, count, exact repeat or response-enclosure intersection alone. Shared event support, frame quantization and all-pairs generation matter.

C1-07 found numerical proximity without authorized exact cross-condition correspondence and retained EVIDENCE INSUFFICIENT. C1-10’s measurement-origin perturbation changed the detection population; shared durations did not preserve supporting-event correspondence. Deterministic replay is not perturbation invariance. These remain negative limits; no approximate fallback, indexwise matching or half/double repair is introduced.

Preserve an unranked evidence collection: period ID, exact T/f, occurrence pairs, centers/windows containing each pair, shared/nonshared event support, coverage, unchanged response references, exact coordinate-relation types, uncertainty and missingness. One pair can participate in multiple overlapping motif descriptions without becoming multiple independent events. No strength/duration/count/ratio preference selects a root.

The desired future outcome vocabulary remains **ONE RECURRENCE FAMILY / MULTIPLE COEXISTING RECURRENCE FAMILIES / NO SUFFICIENT RECURRENCE / UNRESOLVED**. Until a family criterion and sufficiency authority exist, a period-witness catalogue is not such a classifier: its family assessment remains UNRESOLVED. Exact period classes and alternatives may nevertheless all be preserved. Local persistence, transitions and nested support can be described; stability, significance and hierarchy cannot yet be claimed.

## 8. Requirements for recurrence sufficiency

Sufficiency must specify **sufficient for what**. Recoverability of an exact observed relation, physical recurrence robust to detection variability, and readiness to investigate a metric hypothesis are three different claims. No authority inspected defines a rule for the requested general RECURRENCE_SUFFICIENCY_ESTABLISHED state. Consequently no numerical PASS rule is frozen.

| Candidate requirement | Classification | Reason / needed authority |
|---|---|---|
| Explicit population, relation, source, scope, lineage and equality semantics | SCIENTIFICALLY_REQUIRED | F-032 traceability/falsifiability; cannot assess an unspecified proposition |
| More than one distinct occurrence | SCIENTIFICALLY_REQUIRED | Logical repetition requirement; not sufficient count or guaranteed independence |
| Avoid counting overlapping windows/shared pairs as independent evidence | SCIENTIFICALLY_REQUIRED | Same data reused by construction; all overlap must be retained |
| Persistence across time appropriate to claimed span | SCIENTIFICALLY_REQUIRED | A local witness cannot establish whole-scope persistence; minimum duration/count UNKNOWN |
| Independent checker and deterministic replay | SCIENTIFICALLY_REQUIRED | F-032 recoverability/reproducibility and scientific validation governance; replay is not physical validation |
| Account for accidental structure if claiming recurrence beyond chance | SCIENTIFICALLY_REQUIRED | Null/effect/decision authority must match that claim; none supplied by map scores |
| Null probability model and numerical significance cutoff for every descriptive relation | NOT_REQUIRED | Exact descriptive equality can be audited without inferential probability |
| Statistically independent centers as units | NOT_REQUIRED | Centers are generally dependent; correctly model dependence instead of asserting independence |
| Disjoint evidence, independent temporal blocks or held-out population | POTENTIALLY_REQUIRED — NEEDS AUTHORITY | Design depends on target claim; event-disjointness is not enough for independence |
| Robustness to missing observations, local density and local timing variation | POTENTIALLY_REQUIRED — NEEDS AUTHORITY | Necessary if such robustness is claimed; perturbations, tolerances and admissible controls not fixed |
| Independence from arbitrary absolute time origin | SCIENTIFICALLY_REQUIRED for translation-invariant recurrence | Differences are translation-invariant; global complex phase is covariant, not numerically invariant |
| Resolve all harmonic/subharmonic alternatives to one winner | NOT_REQUIRED | Recurrence multiplicity is legitimate; metric selection is later |
| Preserve and distinguish alternate exact period/scale support | SCIENTIFICALLY_REQUIRED | F-031/F-032; ratios alone do not explain organization |
| Several source instances or identified Drum components | NOT_REQUIRED for bounded single-source temporal claim | Would need independent identity and data for cross-source/component claims |
| Independent validation dataset | POTENTIALLY_REQUIRED — NEEDS AUTHORITY | Required for a future generalization claim, not to verify one frozen-map exact witness |
| Minimum effect size, repetition count beyond repetition, coverage and tolerance | UNKNOWN | No supported threshold available; do not choose after viewing responses |
| Physical-onset accuracy, complete musical coverage | NOT_REQUIRED for stated observation-domain claim | Remain unestablished; required only for stronger physical-event conclusions |
| Beat/tactus/metric interpretation | NOT_REQUIRED | Explicitly excluded and not supplied by sufficient recurrence |

Missing authority: target sufficiency proposition; relation/family correspondence; physical measurement uncertainty; dependence-aware occurrence/evaluation units; justified null/exchangeability and effect criterion; multiplicity/selection policy; drift/missingness perturbation scope; independent reference/custody; reviewed implementation/capacity/replay bindings for any derived execution. Existing September 9 design does not close these gaps.

## 9. Smallest falsifiable successor (proposal, not execution)

**Conclusion:** a decisive experiment for the broad sufficiency state cannot presently be designed without inventing its criterion. Do not disguise descriptor production as that experiment. The smallest useful prior step is **DRUM-EXACT-RELATION-WITNESS-AUDIT-01**, a bounded audit of the narrower F-032 repeated-relation proposition using preserved catalogues only. No new audio or periodicity evaluation is needed.

Proposed question: do the catalogue’s distinct-ID pairs supply recoverable repeated occurrences of any exact temporal relation, and can their local support be distinguished from reused evidence? This tests lineage-aware observed recurrence, not strength-profile recurrence, accidental-structure rejection or sufficiency for metric research.

Inputs: authenticated run_1 inputs/periods/windows catalogues and their existing authority/root chain. Numeric response shards are unnecessary for this minimum; no 4-million-row reindexing merely for completeness. Use all 1,056 T entries and all their declared pairs, not handpicked strong periods or favorable windows. Run_2 is replay provenance, not another sample. Preserve rejected/missing witnesses and singleton classes as well as repeated classes.

Prospective outputs: each T with original pair/parent IDs, exact endpoint coordinates and span, duplicate/reuse checks; separate shared-endpoint/event-disjoint relations; each window’s exact containment of those pair endpoints in contained/positive membership, with boundary/clipping status. This incidence is a **new prospective relational representation**, never claimed already measured in this audit. No response threshold, similarity distance or new Fourier result. Pair membership provides local evidence even when there is no equal-L comparison edge; that does not prove cross-center structural equivalence.

Independent evaluator reconstructs each asserted separation from the immutable timestamp authority and checks ID/source lineage, without consuming a generator’s “correct” labels. It checks duplicate suppression by ID, complete catalogue coverage, window membership and witness distinctions against the existing definitions. The generation/evaluation dependence is explicit: pair coordinates were generated from these same events, so recovery is a contract/witness test, not an independent discovery dataset. Freeze outputs before independent evaluation; one deterministic replay checks serialization. Concrete checker/transport binding and resources require later preregistration and PI authorization, not implementation here.

No result of this audit changes the accepted map status or declares a metric reference. If it finds support, its maximum claim is **EXACT_REPEATED_TEMPORAL_RELATIONS_RECOVERABLE_IN_FROZEN_SOURCE_POPULATION**, with every exact class and support retained. If none qualifies, the result is useful: no exact repetition under this rule, with approximate recurrence still unknown. If the PI instead wants response-profile recurrence beyond this scope, first resolve Section 8 rather than automatically executing the larger September 9 descriptive plan.

## 10. Null and control logic (unexecuted)

| Control | Preserves | Breaks / diagnoses | Disposition |
|---|---|---|---|
| Opaque ID renaming and serialization permutation with inverse lineage map | All times/strengths/support/relations | Accidental reliance on lexical IDs or file order | Positive invariance/control for future checker, not chance null; canonical output compared after inverse renaming |
| Duplicate one witness reference without a new endpoint pair | Original relation evidence | Inflated counts caused by repeated representation | Negative contract fixture: no extra occurrence permitted |
| Claim a pair with distinct exact separation as a T witness | Valid source/event tokens otherwise | Exact relation membership | Negative contract fixture; evaluator must reject; not real audio manipulation |
| Translate every time and scope by common delta | Exact intervals, source, incidence, duration | Arbitrary origin dependence | Algebraic control for exact relations; C changes by exp(−2π i delta/T), magnitude unchanged. No numerical rephasing/operator run required or authorized here |
| Shuffle complete center/window profiles across centers | Some marginal payloads | Source-time/membership geometry and temporal order | NOT an automatically valid null; breaks the accepted generative contract and may guarantee apparent success |
| Permute period labels independently of responses/pairs | Marginal labels/responses | T–pair–frequency coherence | Integrity corruption test only, not an accidental-recurrence baseline |
| Permute observed intervals or strengths | Selected marginal distributions | Serial organization and often density/support/generation relations | POTENTIALLY_REQUIRED for a separately stated model; exchangeability not established. Cannot relabel the old map as responses to new events |
| Source-conditioned null | Could preserve source/measurement scope | Intended temporal dependence | UNKNOWN stochastic model; one source-instance label is not a null distribution |
| Randomly thin event evidence | Retained-event identity where explicit | Completeness, pair/query generation, local density | Future missingness sensitivity, not chance null. Existing full-map responses cannot represent thinned input; no recomputation now |
| Independent synthetic null event populations | Chosen finite-scope/frame/density/strength process | Specified non-recurrence property | Needs external scientific model/calibration authority. A uniform-noise/Poisson baseline chosen for convenience is not justified |

No accepted null currently supports an above-chance PASS. Conditional permutation of entire units is legitimate only if exchangeability and retained conditioning are independently justified; overlapping windows violate a naive independent-unit assumption. All-pairs query generation introduces selection dependence. A held-out period proposal must be generated solely from its declared discovery subset; the full global catalogue is not a blind held-out proposal set. The map cannot be quietly reused as a new-map response under permuted timestamps. Full sufficiency may require additional independent observations or periodicity computation, but **whether these are necessary remains unresolved**, not authorization to acquire or compute them now.

## 11. Prospective outcome logic

| Outcome | Narrow witness audit | Broader recurrence sufficiency |
|---|---|---|
| PASS | Complete, reproducible audit with at least one valid repeated exact relation and independent checker agreement; “repeated” is definitional, not statistical significance | NOT AVAILABLE until Section 8 authority is approved; narrow PASS cannot promote this state |
| FAIL | Falsification of an asserted exact witness/recoverability or broken lineage/replay contract, with failure type recorded | Only once a specific sufficiency hypothesis exists; no rejection of all physical recurrence from implementation failure |
| INSUFFICIENT_EVIDENCE | Complete admissible inventory contains no repeated exact relation; or scope cannot support the specifically requested independent evidence | Existing authority cannot decide sufficient recurrence; exact absence is not approximate absence |
| INDETERMINATE | Unresolvable lineage/coverage/physical correspondence prevents the proposed comparison; interruption is separately incomplete execution | Approximate/family/metric interpretation unresolved; preserve all alternatives and uncertainty |

Separate machine contract status from scientific evidence outcome. A passing hash check with no witnesses is not scientific PASS. A failed resource run is STOP_INCOMPLETE, not scientific FAIL. No optional stopping, top-period selection or post-result threshold adjustment.

## 12. Recurrence → BeatReference firewall and next decision

Even a later valid recurrence-sufficiency claim cannot by itself privilege one metric level: the same observed population can support several periods and alternate interpretations. A symmetry/evidence tie is information that must survive, not something to break by largest response, shortest duration or simplest ratio. Additional **independently justified metric interpretation/discrimination authority**, evaluated on blind frozen JGA alternatives, would be required: evidence capable of distinguishing metric assignments rather than merely verifying repeating intervals, with an allowed abstention outcome. F-031/F-032 reserve this musical interpretation for later Domain authority. This document does not design that inference, use external beats to discover recurrence, or calculate any BPM.

RECURRENCE != BEATREFERENCE. BEATREFERENCE != BPM. Neither source-instance identity nor successful interval prediction establishes a perceptual beat, musical role, groove, swing, meter/downbeat or physical onset coverage. Bass/Piano correspondence is excluded. No pending Double-Bass capture is a dependency.

**Recommended next scientific action requiring PI authorization:** review and authorize a separate bounded preregistration for DRUM-EXACT-RELATION-WITNESS-AUDIT-01 with the maximum claim in Section 9, or explicitly require the broader sufficiency-authority question to be resolved first. Recommendation: the narrow witness preregistration, because it reuses compact existing evidence and can reject tautological support without computing any new periodicity map. Do not implement or execute it from this report. It cannot close RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED.

## 13. Consulted record index and reproducible document hashes

Repository paths below are authoritative navigation, not external citations or inferred conversational history. The complete-map source manifest recursively binds producer sources; this audit verified the named integration/input bindings, not every historical producer source file or installed executable. Environment identity is the accepted bound CPython 3.13.14 / python-flint 0.9.0 / FLINT 3.6.0 record, not a claim that this audit ran in that environment. No tests or experiments were rerun.

| Record | SHA-256 |
|---|---|
| `artifacts/JGA_BOOTSTRAP.md` | `d7debbe70e4b36e3e6d7d84d77de0a3f18ba3d2f493713de1894f3e0ca433760` |
| `docs/JGA_DECISIONS.md` | `18a00cf68330f33bcb9ddf5349f84d96f4260c631ccf669044409047ac5051e6` |
| `docs/scientific/JGA_SCIENTIFIC_RESEARCH_CONSTITUTION.md` | `ee64ab7988141cdfb56ac816d9441b4f8c5d3bff538f48db132ff1c031b1d778` |
| `docs/scientific/JGA_SCIENTIFIC_VALIDATION_PROTOCOL.md` | `35f0ae4fadfd8fe66e0605108ca801c7a544b198570d9611bb98d7fa8af62a8b` |
| `docs/scientific/foundations/F-031_HIERARCHICAL_METRIC_PERIODICITY.md` | `9c2c5235a1c9b6bcbbec964adab8a1cc6eea7ccfbe47cf0c6b3d411187fe98f2` |
| `docs/scientific/foundations/F-032_CANDIDATE_PERIODS.md` | `d8a17444e89d87ac5d00239fb2325ac7c61ec62e877ee257d2a89221261af29a` |
| `docs/architecture/AD-032_M89_PULSE_STRENGTH_PRESERVATION.md` | `ea80d6703010327480cfd4552bb230c5ea1ba8b793e55bc0d682051d55bb09fc` |
| `docs/architecture/AD-037_EME_MATERIALIZATION_METRIC_LOCALIZATION.md` | `d8df29981d7c0bdae9ea422b620151ee0138159fbb2a38ef47a77ab349ae4729` |
| `docs/architecture/AD-038_DRUM_RELATIVE_EME_LOCALIZATION.md` | `3dff7713a6197f8791c1edb79e8304a647f6d789496c81805053381d2941e2a0` |
| `docs/architecture/AD-040_RHYTHM_SECTION_TIMING_PROFILE.md` | `e45e9e80f0ebabf01eaed12287560e06cdd1e7b1a8e9fd52bb8c87460f61904a` |
| `docs/architecture/AD-041_DIRECT_INPUT_AUDIOSTEM_METRIC_SOURCE_IDENTITY.md` | `30836a0b40722c460324931a2c2cc828afcf34bf7765996a8d2da53ab02684a3` |
| `docs/architecture/AD-041_HTDEMUCS6S_OPERATIONAL_BINDING.md` | `af7a6c4962478bc39048a0be963df9c00e2d6213ef111a66a24b826d6c5711ea` |
| `validation/VAL-001/authorities/AD-041_DIRECT_INPUT_SOURCE_INSTANCE_AUTHORITY_V1.json` | `b3a76361f30a0dbbc0b79cd15b4a7485ec66b95c42d2cd2c076cb783ee9da347` |
| `validation/VAL-001/preregistrations/H-VAL001-COMPLETE-REAL-DRUM-PERIODICITY-01.md` | `d36995de8fa9c24046eb1d4a56dd81abe7d6ad367238bba4006d98d1391130e0` |
| `validation/VAL-001/preregistrations/H-VAL001-COMPLETE-REAL-DRUM-PERIODICITY-01.inputs.json` | `ba21b73d7fe122b29b522f442a3724a89b8fec96549a34b39db62bb7830b29e7` |
| `validation/VAL-001/preregistrations/H-VAL001-COMPLETE-REAL-DRUM-PERIODICITY-01.authorities.json` | `6ac578c7ea5e8f9367682ca3a46e8ce0e7d0733c1b95eab9ad8937c91575c9b4` |
| `validation/VAL-001/complete_real_drum_periodicity_20260908/README.md` | `7d6176a50fdb9972663978ffcfa2948d5afa6d870a28e20f71ba67838f3f8d59` |
| `validation/VAL-001/complete_real_drum_periodicity_20260908/implementation_binding.json` | `e91b5d2b961f0274706732f46e0ec274fd0b839b921ebaaf7e7e71ce87dcb2f5` |
| `validation/VAL-001/complete_real_drum_periodicity_20260908/score_1.json` | `09dd82b496d1ee2a0fc9484bc0dbc58b9fb4942ffe2a6f905177ba286ae6f80f` |
| `validation/VAL-001/complete_real_drum_periodicity_20260908/score_2.json` | `09dd82b496d1ee2a0fc9484bc0dbc58b9fb4942ffe2a6f905177ba286ae6f80f` |
| `validation/VAL-001/complete_real_drum_periodicity_20260908/replay.json` | `0360779603ffc1b3982d06cc01da00ae428e205fc95e52106bd1b433e15733cb` |
| `validation/VAL-001/preregistrations/H-VAL001-DRUM-RECURRENCE-STRUCTURE-01.md` | `a5c4caf9db3979f363e9776bcb274b9ee95be6c6961c97e6a8a511844479c82b` |
| `validation/VAL-001/preregistrations/H-VAL001-DRUM-STRUCTURAL-TRANSITION-01.md` | `9a67ea26debd7119abe28712495e88cb6d89df6b9da5353d55771fd89d104d7e` |
| `validation/VAL-001/preregistrations/H-VAL001-TEMPORAL-CELL-SINGLETON-01.md` | `6507a69c33247da87afe6f5445db0f4d475e7de8386c97b7b6b4fc61fda56ac8` |
| `validation/VAL-001/run_20260809_192908/report.md` | `238380b1a5dca4377fb58ba1f6e1a0b2802a29b87df9dd4dee2d2b1ef53e89eb` |
| `validation/VAL-001/run_20260810_065939/report.md` | `5a210f669f03c30735f5e467f29aa127fae9bf993e15793d1d103e4853f6fe52` |

Only this new RFC is written. Accepted timing/Double-Bass files remain unchanged. No commit or push. STOP for PI review.

ACCEPTED PERIODICITY MAP REUSABLE:
PARTIALLY

RECURRENCE OPERATIONALLY DEFINED:
YES

RECURRENCE-SUFFICIENCY TEST DESIGNABLE:
INSUFFICIENT AUTHORITY

NEW AUDIO REQUIRED:
NO

NEW PERIODICITY COMPUTATION REQUIRED:
NO

BEATREFERENCE AUTHORIZED:
NO

BPM AUTHORIZED:
NO

NEXT STEP REQUIRES PI AUTHORIZATION:
YES
