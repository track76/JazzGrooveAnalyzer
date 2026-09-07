# AD-041 — prospective htdemucs_6s operational binding

PI authorization: 2026-09-07. Scope: provenance and the explicitly authorized
historical per-file signal preparation; no new scientific interpretation.

The [parent and separator authority package](../../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/demucs_operational_reintroduction_20260907/README.md)
binds the PI-issued mixture source instance, frozen M2 model/configuration, and
six model-declared output keys. The UUID rule is unchanged from
[AD-041](AD-041_DIRECT_INPUT_AUDIOSTEM_METRIC_SOURCE_IDENTITY.md).
The earlier non-null deferral remains historical; this authorization applies
only to this explicitly bound htdemucs_6s path. Other non-null configurations
remain UNAUTHORIZED absent their own prospective authority.

DemucsSeparator.separate_authorized uses AuthorizedDemucsRunner to execute the
pinned backend and preserve every native WAV externally. It assigns source
identity at the separation boundary from parent UUID, separator authority ID,
and model output key. Paths, display labels, asset SHA-256 and execution order
are excluded from UUID derivation.

DemucsTimingReportService independently passes each role-authorized output to
AnalysisPipeline.analyze_audio. This reuses the existing per-file analysis:
AudioPreprocessor channel mean and peak normalization, then NullSeparator
identity preservation, Source Understanding, unchanged detector and AD-037.
Each context retains its own original WAV checksum. Existing AD-038 and AD-040
builders compose the selected Drums, Piano and Double Bass populations.
This avoids assigning the mixture asset hash to all output observations.
No AD-037/038/040 algorithm or Candidate Period logic changes.

The preparation provenance names the source UUID, original WAV SHA-256,
method/version, channel count, exact existing averaging/normalization rules,
frame count and index preservation, and prepared float32 little-endian sample
checksum. The prepared checksum identifies a representation, never a replacement
source or WAV asset. Native WAV bytes remain untouched.

The canonical service validates derived UUID and asset/lineage consistency;
it never reconstructs source identity from a label. Role mappings are explicit
PI authority, not instrument inference. Six native outputs receive identities;
only the three role-authorized outputs enter this report. Piano preservation
has no independent denominator under current authority.

Acceptance and limits are governed by the prospective PROTOCOL.json in the
linked package. GEOMETRIC_ONLY means temporal geometry of analyzable
observations relative to the authorized Drum observations. It does not establish
complete performance coverage, musical absence, physical onsets or BPM.
