# Cached/streaming equivalence — bounded synthetic evidence

PASS: CACHED_STREAMING_PERIODICITY_EVALUATOR_EQUIVALENCE_VALIDATED.
Two executions (original plus fresh-process replay), each with a fresh naive worker
followed by a fresh optimized worker. Exactly 21 queries per worker; 236 checks
passed per execution, zero failed. No subsequent evaluation or source changes.

The naive worker calls the unchanged historical evaluate() function. Line tracing
counts actual Hann/term executions without modifying it. Optimized code retains
the arithmetic expressions, precision and ordered accumulation, including boundary
terms. Scoring compares complete expanded records and independently checks frozen
membership/pair/interval tables. Canonical encoding and numeric serialization helpers
are shared; no optimized cache/membership oracle is shared with the scorer.

Source and input hashes were frozen before execution. The bound numerical environment
and all installed binary hashes were verified inside each worker. Full bulk artifacts
remain at JGA_EXTERNAL_ROOT/experiments/H-VAL001-CACHED-STREAMING-EQUIVALENCE-01/.
No bulk shards or expanded logical records are committed. result.json and the copied
optimized_index.json retain content fingerprints, external checksums and replay status.

Canonical bytes: naive 63,085; optimized manifests/index/shards 42,150, identical
between runs. Worker scientific_bytes counters also included filesystem-created
AppleDouble sidecars; those original counters are preserved unchanged. Separate
serialized_sizes.json reports exact preregistered JSON sizes from named files.
This is a descriptive filesystem accounting distinction, not scientific retuning.

Runtime includes naive line-tracing overhead and does not support an uninstrumented
speedup claim. RSS includes interpreter/libraries. Performance records are operational
and intentionally excluded from scientific replay equality. Cache counters match:
naive exponentials/Hann/amplitudes/accumulations=68 each, membership builds=21;
optimized=17/26/26/68, membership builds=9. Parsed cache=9. Six optimized shards
contain 4,4,4,4,4,1 records; maximum buffered result rows=4.

PASS is limited to these synthetic queries, environment, caching, provenance expansion
and deterministic streaming contract. It does not authorize real Drum execution,
recurrence, period selection, BeatReference, musical phase, tactus, meter/downbeat,
BPM, accompaniment correspondence or visualization. No real Fourier response evaluated.
