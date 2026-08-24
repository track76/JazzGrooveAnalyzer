# CL-PR-CEDVAL006-DATASET-FINGERPRINT-BASIS-01

Status: **DATASET_FINGERPRINT_BASIS_RECOVERED**

## Scope and preserved history

This clarification records only the historical verification mechanics of
dataset authority
`PR-CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK-001` at authority commit
`0ac756e1abef8e1c25fe4cc501db008e064210b1`.

It does not alter the dataset identity, frozen fingerprint, manifest, asset
population, analytical-input authority, observational preregistration,
acquisition claims or scientific semantics. The aborted pre-execution gate for
`EXEC-CEDVAL006-REAL-LIVE-AUDIO-20260824-183116` remains preserved as an
execution-harness verification mismatch. JGA did not execute.

## Recovered canonical basis

The historical `derive()` implementation constructs `manifest_basis` with
exactly these six fields, inserted in this order:

1. `schema`;
2. `dataset_id`;
3. `external_root`;
4. `directory_structure`;
5. `scientifically_relevant_assets`;
6. `filesystem_metadata_sidecars`.

The authoritative population is the complete six-field `manifest_basis`
mapping shown by the historical verifier.

`scientifically_relevant_assets` contains all 17 non-AppleDouble supplied
assets with their deterministic inventory, checksums and type-specific
technical metadata. `filesystem_metadata_sidecars` contains all 17 AppleDouble
records, including filename, relative path, type, byte size, checksum and
`scientific_authority: false`. AppleDouble files therefore participate in the
dataset fingerprint as checksum-bound filesystem-metadata inventory, while
remaining excluded from the scientifically relevant asset population.

Within each population, records retain the order produced by sorting all raw
files on `relative_path.as_posix().encode()` and then preserving the order of
the filtered scientific or AppleDouble sequence. Nested lists retain their
stored order. JSON object-key insertion order is not hash-significant because
canonical serialization sorts keys recursively.

## Excluded expanded-authority fields

The following expanded manifest fields do not enter `manifest_basis` and are
therefore excluded from the dataset fingerprint:

- `authority_id`, `status`, `scientifically_relevant_asset_count`,
  `wav_asset_count`, `appledouble_sidecar_count` and `dataset_fingerprint`;
- `provenance` and `rights_authority`;
- `source_population` and `technical_scope`;
- `acquisition_authority_audit` and `bounded_use_authority`;
- `analytical_source_decision`; and
- `firewalls`.

These fields were assembled outside `manifest_basis` in the same original
authority construction. They are part of the expanded frozen authority record,
but not part of the historical fingerprint input.

## Exact canonicalization and hashing

Future verification must:

1. parse the frozen UTF-8 JSON manifest;
2. construct a new mapping containing exactly the six basis fields named
   above, taking their frozen values without normalization or reinterpretation;
3. serialize that mapping with Python `json.dumps` using
   `sort_keys=True`, `separators=(",", ":")`, and `ensure_ascii=False`;
4. encode the resulting JSON string as UTF-8 with `.encode()`;
5. hash those bytes with SHA-256; and
6. compare the lowercase hexadecimal digest exactly with
   `9d837f710fbf3292c80490d499bc96df0a8fe1140bc9139b65de8a553c4c2eca`.

The independently reconstructed canonical byte population is 15,160 bytes and
reproduces the frozen fingerprint exactly.

## Reason for the aborted mismatch

The aborted harness copied the full expanded manifest, removed only
`dataset_fingerprint`, canonicalized everything else and hashed that larger
record. That is not the historical `manifest_basis`. It incorporates fields
explicitly assembled after the fingerprint was calculated and yields
`ea421ed48b5a45ea40352c7606c1be53dc998c046eed0cb1da67e9a9a0924840`.
The disagreement is a harness implementation mismatch, not evidence of raw
asset change or a defect in the frozen authority.

## Independent verification

Independent reconstruction from the frozen manifest reproduced
`9d837f710fbf3292c80490d499bc96df0a8fe1140bc9139b65de8a553c4c2eca`.
The original frozen verifier also re-derived the complete authority from the
external dataset and returned `PASS`, confirming all frozen raw-asset and
AppleDouble checksums and `raw_assets_unchanged: true`.

Future CED-VAL-006 execution harnesses must use the six-field historical basis
above or invoke the frozen verifier. They must not hash the expanded manifest
minus only its `dataset_fingerprint` field.

No scientific evidence, raw asset, production code or historical authority
changed. No JGA, external tracker, H02, strength, BPM or musical interpretation
was executed or accessed in this forensic review.
