# AD-041 — Direct-Input AudioStem and Metric Source Identity

Status: PROPOSED CLARIFICATION — NOT IMPLEMENTED

## Decision Scope

This decision defines provenance identity only. It clarifies the identity of
an observational source instance entering JGA and keeps that identity distinct
from the checksum-bound identity of the audio asset used in an execution. It
does not change observation, timing, localization, role assignment or musical
interpretation.

## Canonical Identity Semantics

`source_identity` identifies the authoritative observational/source instance
propagated through `AudioStem`, `MetricSource` and the analytical chain. It is
not a display name, instrument label, file path or audio checksum.

`asset_identity` identifies the exact audio bytes used by an execution. Its
canonical value remains the full lowercase SHA-256 digest represented by the
existing asset-provenance fields, including `input_asset_sha256` and
`source_asset_sha256` where applicable.

A source may be associated with more than one asset only when an explicit
authority declares that relationship. Conversely, two assets do not acquire
the same source identity merely because their display or stem names match.

## Direct-Input Derivation Rule

Direct ingestion MUST receive an authority-issued `source_instance_key` that
is unique within its `source_authority_id`. Both values are opaque provenance;
they MUST NOT be inferred from audio, instrument expectations, population
counts or Ground Truth.

The direct-input source UUID is:

```text
uuid5(
  NAMESPACE_URL,
  canonical_json({
    "rule": "jga-direct-input-source-identity/v1",
    "source_authority_id": <non-empty authoritative identifier>,
    "source_instance_key": <non-empty authority-issued key>
  })
)
```

`canonical_json` means UTF-8 JSON with keys sorted lexicographically, no
insignificant whitespace, and separators `,` and `:`. Values are strings and
JSON escaping is normative. The rule identifier is part of the UUID name.

The ingestion authority may supply the authority identifier and instance key,
and must bind them in provenance to the input asset SHA-256. The asset SHA-256,
local path, display name, inferred instrument and execution order are excluded
from the UUID name. Thus source identity is not silently redefined as asset
identity.

For multiple independent direct inputs, the ingestion authority MUST provide
distinct `(source_authority_id, source_instance_key)` pairs unless it
explicitly declares that the inputs are representations of the same
observational/source instance. Distinct authoritative assets MUST NOT collapse
to one Metric Source identity merely because they share a generic name such as
`Mix`.

Replaying the same authoritative direct input with the same identity rule,
authority identifier and source-instance key MUST reproduce the same Metric
Source UUID. The separately verified asset SHA-256 establishes whether the
same exact bytes were replayed.

## Path Policy

Filesystem paths are provenance locators only. Absolute paths,
repository-relative paths, filenames and basenames are excluded from canonical
source-identity derivation because relocation or renaming must not change
source identity. A provider may record a path while assigning an opaque
source-instance key, but JGA MUST NOT implicitly promote that path or filename
to the key.

## Separated-Stem Policy

A separator output is a derived observational/source instance, not another
direct input. Its source UUID is:

```text
uuid5(
  NAMESPACE_URL,
  canonical_json({
    "output_source_key": <stable key declared by the separator contract>,
    "parent_source_identity": <canonical UUID string>,
    "rule": "jga-separated-source-identity/v1",
    "separator_authority_id": <method/configuration authority identifier>
  })
)
```

Each output of one separation MUST have a distinct stable output-source key.
The key may encode a semantic output identity only when that semantic identity
is explicitly declared by the separator contract; downstream content analysis
must not invent it. Parent-asset SHA-256, output-asset SHA-256, separator
execution identity, model/configuration provenance and labels remain separately
recorded. A deterministic replay under the same parent identity, separator
authority and output key reproduces the same source UUID.

## Required Invariants

1. Distinct directly ingested authoritative assets MUST NOT collapse to the
   same Metric Source identity merely because they share a generic display or
   stem name.
2. Replaying the same authoritative direct input under the same identity
   semantics MUST reproduce the same Metric Source identity.
3. Source identity and checksum-bound asset identity MUST remain separately
   serialized and independently verifiable.
4. Source identity MUST be assigned at ingestion or the separation boundary
   and preserved downstream; Translation and reporting MUST NOT reconstruct it.
5. No musical, detector or Ground-Truth evidence may participate in identity
   assignment.

## Compatibility and Migration

The legacy rule `uuid5(NAMESPACE_URL, stem.name)` remains part of historical
execution provenance. Existing reports, fingerprints, commits and scientific
results MUST NOT be rewritten or silently relabelled.

Prospective remediation uses the versioned rules above. A remediation record
must identify the legacy execution and identity rule, the corrected execution
and identity rule, and the unchanged asset authorities. Corrected source UUIDs
may deterministically change source-dependent candidate, contributor, EME,
localization, profile and report identities and their fingerprints. Such
changes are provenance-identity changes only; they MUST NOT be interpreted as
changes in observed event count, timestamp, strength, temporal geometry or
scientific outcome. Those quantities require explicit invariant comparison.

## Minimum Future Implementation Surface

Implementation is not authorized by this clarification. The minimum later
repair is confined to:

1. the ingestion contract, to require the authority identifier and
   source-instance key while retaining the independent asset checksum;
2. `AudioStem` identity construction, to accept the resulting explicit source
   UUID instead of deriving it from `name`;
3. `NullSeparator`, to preserve the direct-input UUID rather than manufacture
   identity from `Mix`;
4. source-understanding/semantic bridging, to propagate that UUID rather than
   reconstruct it from a display name; and
5. focused identity, collision, replay and downstream-invariance tests.

No report-only workaround is valid. AD-037, AD-038 and AD-040 already preserve
the source and asset fields they receive and require no change to their timing
or scientific algorithms. Their source-dependent record identities and
fingerprints may change prospectively, while EME materialization behavior,
absolute timestamps, Drum-relative geometry, boundary/tie rules and
`GEOMETRIC_ONLY` semantics remain invariant.

## Scientific Firewall

This decision does not authorize instrument inference, musical labels derived
from audio, Ground Truth access, BPM, meter, beat/downbeat inference,
groove/swing interpretation, timing correction, missing-event recovery or new
detector behavior. Expected controlled-population counts are validation
invariants only and never identity inputs.

## Relationship to Existing Authority

- AD-015 remains authoritative: Metric Source identity is preserved rather
  than reconstructed by Translation.
- AD-037 remains authoritative for EME materialization and lineage.
- AD-038 remains authoritative for neutral Drum-relative geometry.
- AD-040 remains authoritative for provenance-bound role assignment keyed by
  source and asset identity.

This clarification supplies the previously missing identity rule at the
ingestion/separation boundary; it does not revise those decisions.
