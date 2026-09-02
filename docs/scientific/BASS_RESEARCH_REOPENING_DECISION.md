# Bass Research Reopening Decision

Status: **WAIT — NEW AUTHORITY REQUIRED**

Date: 2026-09-02

Authority context:

- JGA v1.0 scope: Drums, Double Bass and Piano timing relationships;
- frozen Bass branch: commit
  `93dfddbf8fc4ea59c62e53064529c819b0882d8e`;
- current branch decision: `STOP — MAXIMUM DEFENSIBLE OBSERVATION BOUNDARY
  REACHED WITH CURRENT CED DATASETS AND REPRESENTATIONS`.

This record selects an evidence-acquisition path. It is not a protocol and
authorizes no experiment, processing, production change or Ground Truth use.

## REQUIRED_NEW_EVIDENCE

JGA needs an independently authoritative observation of the same jazz
performance in two forms:

1. original, sufficiently isolated Drums, Double Bass and Piano recordings on
   a defensibly common sample-time coordinate; and
2. the contemporaneous full mixture on that same coordinate.

This pairing is required to distinguish three currently confounded questions:

- whether source-local acoustic evidence exists at a coordinate;
- whether it remains measurable in the simultaneous mixture; and
- whether separation plus JGA observation preserves, transforms or loses it.

For the historical mission, the authority must also preserve recording date,
performers, piece/take identity, venue/session provenance and the limits of any
historical-period claim. One recording can reopen and validate the observation
method; reconstruction of historical evolution ultimately requires independent
recordings spanning justified historical strata.

## CANDIDATE_PATHS

### New common-clock original multitrack

Directly supplies independent source identity, mixture context and shared-time
authority. It is the only listed path that can simultaneously address source
attribution, timing preservation and ecological rhythm-section performance.

### Qualified JTD access

Potentially highly relevant to jazz timing and historical comparison, but the
repository contains no JTD provenance or access authority. It does not establish
whether JTD exposes original microphone/DI tracks, source-separated estimates,
only a mixture, a common clock, preserved temporal origin or auditable editing
history. JTD is therefore an unqualified candidate, not an authorized dataset.
Source-separated estimates must not be treated as original stems.

### Improved source-separation technology

Feasible to benchmark prospectively, but it transforms the same kind of mixture
evidence and supplies no independent Bass identity or timing authority. It may
improve engineering performance without resolving the scientific bottleneck.

### Independently justified temporal/source priors

Could constrain interpretation, but no independent authority for such priors is
currently recorded. Derivation from existing CED outcomes would risk leakage
and circular attribution.

### Controlled physical-acoustic recording

Can provide strong common-clock, source-presence and physical-action authority.
It is valuable for causal calibration, but an isolated or scripted laboratory
performance has lower direct information about ecologically performed and
historically situated jazz rhythm-section timing than a documented real
multitrack take.

### Independently aligned evidence modality

Contact pickup, MIDI/action sensing or synchronized video could strengthen
source identity and action timing. It introduces alignment and modality-to-audio
correspondence questions and, alone, does not provide the complete three-source
audio comparison required by JGA.

## RANKING

Ranks are prospective judgments based on repository authority, not experimental
outcomes. `Low` leakage risk is preferable.

| Rank | Path | Information gain | v1.0 relevance | Independence | Feasibility | Leakage risk | Resolves attribution bottleneck |
|---:|---|---|---|---|---|---|---|
| 1 | Provider-authoritative common-clock original multitrack | Very high | Direct | High | Moderate | Low | Directly |
| 2 | Controlled physical-acoustic Drums/Bass/Piano recording | High | Direct but less ecological/historical | High | Moderate | Low | Directly within its condition |
| 3 | Independently aligned modality paired with multitrack audio | High | Direct if all three sources are covered | High | Low–moderate | Low | Potentially, subject to alignment authority |
| 4 | Qualified JTD access | Potentially high | Potentially direct/historical | Unknown | Unknown | Unknown | Unknown until provenance audit |
| 5 | Prospectively evaluated improved separation | Moderate | Indirect | Moderate | High | Low if frozen prospectively | No independent source authority |
| 6 | Independently justified source/temporal priors | Unknown | Indirect | Currently unestablished | Low | High if derived from present outcomes | Only if truly independent and validated |

JTD's rank reflects missing authority, not a negative judgment about the
dataset. A provider package proving original common-clock stems and suitable
provenance would cause it to be re-ranked as a form of the selected path.

## SELECTED_PATH

**Obtain and qualify a provider-authoritative, common-clock original
Drums–Double Bass–Piano jazz multitrack with its contemporaneous mixture and
preserved timing provenance.**

The preferred acquisition is an existing real performance/take with original
recorder exports. A newly recorded session is acceptable when it preserves
ecological trio performance and complete acquisition authority. A separator's
estimated stems do not satisfy this path.

## WHY_IT_IS_GENUINELY_NEW

The selected path adds independent physical recording channels, source labels
and shared-time provenance from a new performance. It does not create another
deterministic view of CED spectra. It supplies the missing counterfactual
comparison between source-local evidence, simultaneous mixture evidence and
separated/JGA evidence at the same native coordinate.

## WHAT_SCIENTIFIC_UNCERTAINTY_IT_CAN_RESOLVE

Within the acquired performance, the new authority can prospectively test:

- whether source-local Double Bass observations exist where mixture/separated
  observations are absent;
- whether loss first appears in the mixture, separation output or JGA
  observation stage;
- whether Piano- and Drum-associated simultaneous activity explains apparent
  Bass-compatible mixture evidence;
- whether any prospective recovery preserves neutral timing relationships
  among Drums, Double Bass and Piano; and
- whether the observation method transfers to a genuinely independent jazz
  performance.

It cannot by itself establish historical evolution, universal separator
causality, physical onset or general production validity.

## REQUIRED_AUTHORITY

Before preregistration, the candidate dataset must provide and permit freezing
of:

1. **Asset identity:** lossless original files, exact filenames, byte sizes,
   cryptographic checksums, sample formats and rights/usage terms.
2. **Same-take identity:** attributable provider confirmation that all three
   source tracks and the mixture represent the same performance/take.
3. **Simultaneous acquisition:** recorder/session evidence that the relevant
   channels were captured simultaneously, not assembled from different takes.
4. **Common timebase:** one hardware clock or an independently documented
   synchronization system, including sample rate and any clock conversion.
5. **Temporal origin:** exact file/session start relationship, export ranges,
   offsets, latency compensation and preserved frame-zero mapping.
6. **Editing history:** documented edits, comping, time-stretching, quantizing,
   sample replacement, overdubs, tuning, alignment, resampling and export
   operations; unknown operations must remain explicitly unknown.
7. **Independent source identity:** track sheet/provider declarations for
   Drums, Double Bass and Piano, including microphone, DI/contact-pickup and
   routing identities where available.
8. **Original-source status:** explicit confirmation that the source tracks are
   recorder/mix-session channels or declared microphone sums—not source-
   separation estimates. Any derived submix must retain its recipe and inputs.
9. **Isolation evidence:** enough direct/close-source separation to serve as
   source-local observational authority, with bleed measured and retained
   rather than assumed absent.
10. **Mixture authority:** a contemporaneous mix or a prospectively defined,
    exactly reproducible unity-gain mix from all authorized same-take tracks,
    preserving the common coordinate.
11. **Timing suitability:** uninterrupted regions with simultaneous rhythm-
    section performance, no undocumented timing edits, and sufficient duration
    and event population for separately preregistered timing analysis.
12. **Historical metadata:** attributable recording date, personnel,
    performance context and provenance adequate to bound—not infer—the
    historical comparison represented.
13. **Independence:** no selection of the dataset, excerpts or channels based on
    JGA Bass outcomes. Dataset acceptance must use authority/technical criteria
    frozen before JGA execution.

Provider declarations and measured file properties must remain separately
classified. Equal file length or shared frame zero alone does not prove a
common acquisition clock.

## NEXT_ACTION

Do not preregister a signal experiment. First obtain a candidate provider
package and conduct a read-only **dataset authority qualification** limited to
provenance, rights, checksums, technical compatibility, source identity,
same-take/simultaneity, clock/origin and editing history.

For JTD specifically, request its authoritative dataset documentation and
asset description before access is treated as useful. The minimum answer must
state whether each offered stem is an original recording channel, a provider
submix or a source-separated estimate, and must document its temporal relation
to the distributed mixture. If that cannot be established, JTD does not reopen
this problem.

No existing authorized local resource meets the selected path's genuinely new
authority requirement. Existing CED assets remain frozen and must not be used
as a substitute.

## GO / WAIT decision

**WAIT — OBTAIN NEW DATA AND AUTHORITY FIRST.**

GO is permitted only for a provenance-only qualification after a candidate
package and its provider documentation are available. A Bass-observability
experiment may be proposed only after that qualification passes. Until then,
the Bass-recovery branch remains stopped.
