# H-VAL001-BINARY64-CERTIFIED-INPUT-01

Date: 2026-09-08
Status: FROZEN DESIGN — EXECUTION REQUIRES PI AUTHORIZATION
Conversion authority: JGA-ACCEPTED-BINARY64-OBSERVATION-INPUT-V1 (prospective PI decision).

## Purpose and preserved authorities

Validate only lossless reconstruction of accepted binary64 observation fields,
conversion to certified Arb input, and explicit numerical scope binding.
No audio, detector, Fourier operator, real Drum population, or query workload is run.
No historical authority is amended. The producer-lineage audit supports Python
binary64 timestamp/strength fields and their hexadecimal observation-ID inputs.
Integer sample/frame coordinates remain diagnostics, not replacement seconds.
Original JSON tokens are serialization provenance, not exact decimal coordinates.

Reuse CPython 3.13.14, python-flint 0.9.0 / FLINT 3.6.0, macOS arm64 from
../certified_query_environment_20260907/binding.json, SHA-256
5242ca974311694e7bf0d20e4459e25336232fc201bc55f80e43e58f7166f468.
Set precision=128 bits, threads=1; verify linked flint_get_num_threads()==1.
No precision escalation, alternate package or empirical tolerance.
The earlier seven-query numerical PASS is not validation of this new adapter.

## Frozen fixtures and independent expected table

Hex bit patterns below are 16 lowercase hexadecimal digits, most-significant
byte first (IEEE-754 binary64); not machine-native byte order. Rational pairs
are reduced with positive denominator. Every row is a separate field invocation.
A-H are eight finite inputs; I1-I3 are three rejected inputs: total eleven.

| ID / field | Producer binary64 bits | Python float.hex() | Exact rational n/d | Original and canonical JSON numeric token |
|---|---|---|---|---|
| A timestamp | 3fb999999999999a | 0x1.999999999999ap-4 | 3602879701896397/36028797018963968 | 0.1 |
| B timestamp | 3ff8000000000000 | 0x1.8000000000000p+0 | 3/2 | 1.5 |
| C native_strength | 3fb99999a0000000 | 0x1.99999a0000000p-4 | 13421773/134217728 | 0.10000000149011612 |
| D generic_numeric | 3ff4000000000000 | 0x1.4000000000000p+0 | 5/4 | 1.25 |
| E generic_numeric | c004000000000000 | -0x1.4000000000000p+1 | -5/2 | -2.5 |
| F temporal_origin | 0000000000000000 | 0x0.0p+0 | 0/1 | 0.0 |
| G signed_zero_probe | 8000000000000000 | -0x0.0p+0 | 0/1 | -0.0 |
| H analysis_input_duration | 3fd3333333333333 | 0x1.3333333333333p-2 | 5404319552844595/18014398509481984 | 0.3 |

A construction diagnostic: integer sample coordinate=1, sample rate=10;
ideal sample rational=1/10. Round-to-nearest, ties-to-even binary64 division
produces frozen bits A. The accepted coordinate exceeds 1/10 by
1/180143985094819840. It must not be replaced by 1/10.

B construction: exact 3/2. D/E are exact 5/4 and -5/2. Negative E tests
conversion mechanics only, not negative Drum-strength admissibility.

C construction: IEEE-754 binary32 bits 3dcccccd, exact value
13421773/134217728; widening to binary64 is exact and produces the frozen C bits.
This is not recovery of exact 1/10 or earlier signal-processing information.

F/G are explicitly distinct bit identities. F is the scope origin fixture;
G is only a signed-zero preservation probe. Both have rational value zero.

H construction diagnostic: sample count=3, sample rate=10, ideal duration=3/10.
Binary64 division produces frozen H. Accepted duration is below 3/10 by
1/90071992547409920. Preserve this non-identity explicitly.

| ID | Raw binary64 bits | Expected classification | Scientific output |
|---|---|---|---|
| I1 | 7ff8000000000000 | NONFINITE_NAN | REJECTED_NONFINITE; no Arb input |
| I2 | 7ff0000000000000 | NONFINITE_POSITIVE_INFINITY | REJECTED_NONFINITE; no Arb input |
| I3 | fff0000000000000 | NONFINITE_NEGATIVE_INFINITY | REJECTED_NONFINITE; no Arb input |

Nonfinite values arrive as raw producer-bit fixtures, not JSON number literals.
Their original_json_numeric_token is null; valid JSON has no NaN/Infinity tokens.
Preserve the exact diagnostic bits and classification in rejection records only.
No nonfinite hex spelling, ratio or enclosure is required or authorized. The
single NaN payload does not validate every NaN payload or signalling behavior.

Each input has observation_id=SYNTHETIC-ADAPTER-<ID>, field as in the table
(I rows use generic_numeric), population_id=H-VAL001-BINARY64-CERTIFIED-INPUT-01.
Source and asset lineage are synthetic construction identifiers, not WAV assets
or AD-041 source instances. Input-manifest SHA-256 binds exact fixture bytes and
all diagnostic fields. For rows without sample/float32 diagnostics use null.

## Adapter contract

Input: original token when available, finite producer bits or reconstructed
producer value, field identity and provenance. Production code must not import
the expected table or dispatch on fixture ID.

1. Decode bits using explicit IEEE binary64 byte order. Reject exponent-all-ones
   inputs before attempting rational or Arb conversion. Classify NaN/infinity by
   exponent, fraction and sign; do not perform arithmetic on NaNs.
2. For finite token-bearing input, parsing its JSON numeric token must recover
   identical binary64 bits. Preserve the original token unchanged, even though
   it is not the exact rational authority. Do not replace it with a new spelling.
3. Record bits, float.hex(), float.as_integer_ratio(), sign-bit and zero status.
   Exact rational is the ratio of the reconstructed binary64 value, not Fraction
   of the JSON token. Preserve the ratio even when it differs from diagnostics.
4. Construct Arb directly from exact integer numerator and denominator, e.g.
   arb(n)/arb(d); neither operand passes through decimal float or binary64 again.
   At the fixed precision, require a finite ball containing the exact dyadic.
   The certification check is containment, not decimal agreement or epsilon.
5. Export exact Arb midpoint/radius dyadics using mid()/rad()/man_exp(), normalized
   odd mantissa for nonzero values, canonical zero (0,0). Derive rational interval
   endpoints exactly for scoring. No approximate printed Arb strings as authority.
6. Preserve numerical_authority_status=EXACT_ACCEPTED_BINARY64_RECONSTRUCTION
   and measurement_authority_status=NOT_ESTABLISHED_BY_ADAPTER. Record conversion
   authority, runtime/build hashes, input-manifest hash, observation and field ID,
   original token, upstream diagnostics and actual certified enclosure.

Signed-zero fields: sign_bit is 0/1 encoded as strings; zero_status is
POSITIVE_ZERO, NEGATIVE_ZERO, or NONZERO. Arb and rational zero need not retain
signed zero; the separate original-bit/sign provenance MUST retain it. Comparing
only rational equality is insufficient. No physical uncertainty is inferred from
an exact or narrow numerical enclosure.

## Explicit scope contract (uses F and H, no additional adapter invocations)

For the synthetic analysis_input scope:
- temporal_origin and observation_scope_start reference adapted F (+0.0);
- accepted analysis_input_duration references adapted H;
- observation_scope_end and clipping asset upper bound reference H directly;
- clipping lower bound references F; interval is closed [F,H];
- sample_count=3 and sample_rate=10 remain exact diagnostic integers;
- diagnostic duration is exact 3/10 and is not the clipping coordinate.

Independent boundary witnesses: 0 and accepted H are included; exact diagnostic
3/10 is excluded because it exceeds H. These are rational set-membership checks,
not further adapter calls or periodicity queries. No offset addition is needed
or authorized: nonzero-origin end construction is outside this experiment.

Prospective VAL-001 binding, not an input fixture: temporal origin is the accepted
0.0; analysis_input is the full accepted input, with end/clipping bound equal to
its accepted binary64 duration. Preserve original duration token and bits together
with asset sample count/sample rate diagnostics. Do not recompute end from their
exact quotient. Application to real records requires separate PI authorization.
This synthetic PASS does not independently verify actual asset length or scope.

## Independent oracle and tests

Scorer receives frozen output only after adapter generation completes. It must not
call the adapter to derive expected bits, hex, ratio, sign, classification or scope.
Use the literal expected tables above. Independently decode finite IEEE values as
(-1)^sign * (2^52+fraction) * 2^(exponent-1023-52) for normal numbers and
(-1)^sign * fraction * 2^(-1074) for subnormal/zero encodings; use integer/rational
arithmetic only. This decoder verifies table consistency before scientific run
without treating adapter output as oracle. No nonzero subnormal fixture is included;
no subnormal-coverage claim follows from this decoder's general formula.

Exact checks for each finite fixture:
- input token/diagnostics/identity unchanged;
- output bits, hex, reduced ratio and signed-zero status equal frozen table;
- canonical producer JSON serialization via CPython json.dumps(value,
  allow_nan=False) equals frozen canonical token and parses back to identical bits;
- exact dyadic value is inside exported certified rational endpoints;
- finite enclosure, nonnegative radius, valid canonical dyadic encoding;
- conversion, numerical/measurement authority and provenance fields are correct.

Additional checks: A/H signed differences from diagnostic rationals equal the
frozen differences; C binary32 widening is exact; scope aliases/bounds and all
three membership witnesses agree; I1-I3 yield the exact rejection classification
with no scientific ratio/enclosure record. A/H division and C widening may be
verified during the authorized test, never used to overwrite a mismatching table.
Any inconsistent frozen table is a failure/authority issue, not permission to fix.

## Canonical output and replay

All artifacts: UTF-8 JSON, sorted keys, compact separators (',',':'), ensure_ascii=True,
no trailing newline. Scientific numeric payloads use strings: bits as fixed-width
lowercase hex, ratios as [n,d] decimal integer strings, reduced with positive d,
hex values as frozen above. Original JSON numeric token is a string field. Arb
midpoint/radius use [mantissa,exponent] strings. Booleans and null remain JSON values.
Ordering A,B,C,D,E,F,G,H,I1,I2,I3; diagnostics and authority maps sort by key.
No actual NaN/Infinity floats or decimal-only scientific identifiers in artifacts.
No wall-clock times/randomness/filesystem paths in canonical scientific output.

Before execution freeze input manifest, adapter/scorer source hashes and bound
environment identity. Preserve adapter accepted-input records, separate rejection
records, scope binding and provenance, plus all scoring outcomes. One full eleven-
fixture execution and one fresh-process replay only. Require byte-identical canonical
adapter, scope/provenance and scoring artifacts and record SHA-256 values. Exact
runtime/build mismatch blocks execution; no version substitution. No precision tuning.

## Failure, maximum claim and readiness

Every frozen equality, containment, rejection, scope, provenance, serialization
and replay check must pass. Any mismatch -> FAIL, preserve evidence and stop.
No epsilon, precision escalation, fixture repair or repair-and-rerun without PI.
No statistical success percentage. Expected nonfinite rejection is a passing test
of the rejection contract, not an experimental failure.

Maximum future PASS: BINARY64_CERTIFIED_OBSERVATION_INPUT_ADAPTER_VALIDATED,
limited to these eleven fixtures and zero-origin scope-binding semantics under
the bound numerical environment. It is not proof for all binary64 encodings.

No physical timing/onset truth, recovery of earlier information, recurrence,
periodicity sufficiency, discovery, window optimization, real Drum execution,
trajectory/level selection, half/double resolution, BeatReference, musical phase,
tactus, meter/downbeat, BPM, accompaniment correspondence or visualization authority.

Specification is ready for PI review and subsequent execution authorization.
No adapter implementation, fixture evaluation, Arb execution or real-data query
was performed in this design task. No essential numerical/scope choice remains
unresolved for this bounded, zero-origin synthetic contract.
