# CED-VAL-006 Canonical Report Acceptance Result

Acceptance validation ID:
`ACC-CEDVAL006-CANONICAL-RHYTHM-SECTION-REPORT-01`

Status: **FAIL — SCIENTIFIC_INTEGRATION_CONFLICT — STOPPED WITHOUT REPAIR**

The frozen dataset, analytical inputs, implementation commit, historical
result, source paths, roles, checksums and technical properties all verified.
Two fresh-process canonical CLI executions succeeded and produced byte-identical
JSON with report fingerprint
`e804977be05d0f9eba8f578be495d796c3549464ff620fa7574e73dc54f51ddb`.

All preregistered numerical invariants match the immutable historical result:
909 Drums EME, 1,055 Double Bass EME, 1,055/1,055/0 AD-038
eligible/localized/unresolved records, four ties, and 1,964 AD-040 represented
EME. All 1,055 accompaniment relationships remain `GEOMETRIC_ONLY` and no
timestamp correction is applied.

Acceptance nevertheless fails because the report does not preserve two
dataset-critical authorities:

1. CED-VAL-006 calibration applicability is `UNESTABLISHED`, while the report
   records only the distinct application status `NOT_APPLIED`.
2. CED-VAL-006 explicitly forbids acquisition-clock synchrony claims, while
   the report's serialized unsupported-claim firewall omits that claim.

These are provenance/firewall losses. `NOT_APPLIED` cannot be reinterpreted as
`UNESTABLISHED`, and a dataset-specific limitation cannot be inferred into a
serialized report after execution. Production code was not patched. The
workflow is not real-audio accepted and the first-release gate is not ready.
