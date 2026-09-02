# Bass Research Authority-Gap Audit

Date: 2026-09-02

Scope cutoff: synthesis commit
`782bd89e313d2fb2c90a5f8f54c9922e341c8f0d`

Status: **COMPLETE — BOTH GAPS REMAIN UNRESOLVED**

## Question

Can either authority gap recorded by the Bass-recovery synthesis be closed
from an already-finalized repository or external scientific-storage artifact?

The two requested records are:

1. a standalone finalized CED-VAL-009 report; and
2. a separately named maximum-recoverable-evidence result.

## Read-only audit scope

The audit searched:

- all reachable Git refs and commit paths;
- local Git reflogs;
- unreachable commits and trees still present in the local object database;
- the established external JGA scientific-storage tree at
  `/Volumes/SSD Track/JGA`; and
- existing repository references to CED-VAL-009 and maximum-recoverable
  evidence.

No raw audio, Ground Truth population, event coordinate, outcome distribution
or dense scientific representation was opened. No result was reconstructed,
recomputed or inferred from conversational memory.

## CED-VAL-009 standalone finalized report

**Audit result: NOT RECOVERED.**

No standalone finalized protocol/report/result authority was found in Git
history, reflogs, unreachable Git trees or external scientific-storage. The
external tree contains the CED-VAL-009 raw dataset directory, but raw dataset
presence is not finalized result authority and was not inspected.

The repository does contain the finalized cross-dataset characterization,
which serializes a CED-VAL-009 population of 624 PRESERVED and 1,011 MISSED
observations and the effect sizes explicitly reported there. That record
remains authoritative only for its own cross-dataset claims:
[cross-dataset report](../CROSS-DATASET-BASS-PRESERVATION/preserved_missed_characterization_20260901_01/REPORT.md).
It cannot substitute for, or reconstruct, a standalone CED-VAL-009 record.

## Maximum-recoverable-evidence result

**Audit result: NOT RECOVERED.**

No separately named finalized protocol/report/result authority was found in
Git history, reflogs, unreachable Git trees or external scientific-storage.
Existing reports contain retrospective or oracle combined-coverage quantities,
but explicitly classify those quantities as explanatory only. They are not a
maximum-recoverable-evidence authority and are not reinterpreted as one.

## Authority decision

Both gaps remain explicitly unresolved. Nothing is restored because no
artifact met the repository's finalized-authority and provenance requirements.
This negative audit changes no prior result, fingerprint, checksum,
classification or interpretation.
