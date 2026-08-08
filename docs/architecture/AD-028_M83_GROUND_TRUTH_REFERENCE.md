# AD-028 — M83 Ground Truth Reference

Status: LOCKED

## Context

M81 defines Ground Truth as an immutable scientific representation constructed
from an authoritative symbolic source and kept independent from JGA analysis.

M83 introduces the minimum Ground Truth reference required for later scientific
validation of VAL-001.

## Identity and Dataset Binding

The Ground Truth identity is:

`GT-VAL-001-v1`

The Validation Dataset identity is:

`VAL-001`

They are distinct scientific entities. The Ground Truth reference preserves the
explicit binding between them.

## Authoritative Source

The authoritative symbolic source is:

`recordings/validation/ground_truth/03 THE COST OF LIVING versione intro + 8 bar.musicxml`

Its SHA-256 checksum is:

`809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778`

Repository-relative path and content checksum establish source identity. Source
repository revision remains absent until the source has been committed and
shall not be fabricated.

## Schema and Normalization Identity

The M83 Ground Truth schema version is `1`.

The approved normalization version is `1`.

Both identities are preserved in Ground Truth provenance.

## Mandatory Scientific Quantities

M83 Ground Truth contains only:

- time signature;
- tempo;
- sections;
- instrumentation; and
- the minimum metric-position mapping required for pickup normalization and
  section boundaries.

GroundTruthBeat and GroundTruthEvent remain candidate concepts. They are not
part of M83 Ground Truth.

## Pickup Normalization

MusicXML measure `1` is an explicit pickup. It is preserved, precedes the Intro,
and is excluded from ordinary full-measure numbering and the four-measure Intro
count.

The twelve complete MusicXML measures `2` through `13` are normalized as full
measures `1` through `12`.

MusicXML measure `6` maps to normalized full measure `5`. Section A begins at
normalized full measure `5`.

The original MusicXML measure identity and normalized measure identity remain
traceable.

## Sections

- Intro: normalized full measures `1` through `4`;
- Section A: normalized full measures `5` through `12`.

The pickup is not part of either section.

## Instrument Normalization

The original MusicXML part and instrument designations are preserved alongside
the canonical VAL-001 category.

- `Voce` / `Voice (2)` → `Voice`
- `Sax Tenore` / `Tenor Saxophone (2)` → `Saxophone`
- `Piano` → `Piano`
- `Basso Verticale` / `Upright Bass` → `Double Bass`
- `Set di batteria` / `Drum Set (Jazz)` → `Drum Set`

## Ownership and Independence

The Ground Truth Layer owns source loading, approved normalization, provenance,
and construction of the immutable Ground Truth model.

Ground Truth generation has no dependency on `AnalysisContext`, Immutable
Analysis Representation, Comparator, validation outputs, or JGA Domain objects.
No JGA-derived value may influence Ground Truth.

## Dependency Direction

Authoritative MusicXML Source

↓

Ground Truth Loader

↓

Immutable Ground Truth Model

## Governing References

- `docs/scientific/m81/M81_GROUND_TRUTH_MODEL.md`
- `docs/scientific/JGA_SCIENTIFIC_VALIDATION_PROTOCOL.md`
- `docs/scientific/VAL-001_REFERENCE_DATASET.md`
- `docs/scientific/foundations/F-030_SCIENTIFIC_KNOWLEDGE_RECORD.md`
