# H-VAL001-EME-DISPLACEMENT-01

Status: **PASS**

The controlled validation used the authorized 55-reference quarter timeline
and the four in-scope authoritative WAV stems. Voice remained deferred.

The measured quantity was only `EME timestamp - associated BeatReference
timestamp`. Every authorized EME retained one explicit association; no EME was
missing, duplicated or reassigned to a different movement. Two executions per
source produced identical scientific fingerprints.

The audit found that `MetricClusterBuilder` recomputed nearest-reference
projection instead of consuming the movement identity already authorized by
the AD-018 association. All controlled results happened to agree, but the
second decision was unauthorized and could diverge. The minimal correction
uses `EME.beat_reference_id` when available and rejects an identity outside the
supplied timeline. Legacy EME without explicit lineage retain their existing
deterministic nearest projection.

No inclusion threshold is active. Exact midpoint ties in the legacy nearest
projection resolve to the earlier ordered reference. The controlled authorized
path does not make a second tie decision.

Raw quarter-normalized phase values are preserved in `result.json`. Drums,
Double Bass and Tenor Sax contain values numerically close to both zero and
minus one-half of the quarter period. Piano values occupy a narrow positive
range close to zero. No tolerance, subdivision grid or musical label was
introduced, so these are descriptive numerical populations only—not timing
errors or subdivision interpretations.

The exact limitation is that quarter-only displacement cannot distinguish
performance displacement from an event occupying another metric phase.
Subdivision-aware interpretation remains unauthorized.
