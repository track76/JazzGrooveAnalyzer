# H-VAL001-EME-CARDINALITY-01

Status: **PASS**

AD-037 corrects the former AD-018 movement-dependent EME cardinality rule.
Source-observation event EME are materialized before the authorized quarter
timeline is reconstructed. Localization then relates every existing EME to
its preceding quarter reference without suppressing, merging or creating EME.

Controlled cardinalities are preserved exactly:

| Source | PulseCandidates | EME before localization | EME after localization | MetricPoints |
|---|---:|---:|---:|---:|
| Drums | 63 | 63 | 63 | 63 |
| Piano | 49 | 49 | 49 | 49 |
| Double Bass | 27 | 27 | 27 | 27 |
| Tenor Sax | 16 | 16 | 16 | 16 |

Multiple events per contributor and quarter interval are preserved. The
maximum populations are 2, 3, 2 and 3 respectively. Exact-boundary events
belong to that reference at phase zero; distinct evidence at an identical
timestamp remains distinct; the final in-scope interval remains localizable
without an in-scope following reference.

Every normalized phase lies in `[0,1)`. Raw phase populations are preserved in
`result.json` without clustering, tolerance, subdivision or musical labels.

Each EME has deterministic asset-bound identity and complete supporting
PulseCandidate, source and contributor lineage. Metric localization preserves
declared timeline and asset provenance. Core observations are unchanged.

The EME populations represent physical temporal events supported by the
current source observations; they do not assert symbolic note identity. Voice
remains deferred.
