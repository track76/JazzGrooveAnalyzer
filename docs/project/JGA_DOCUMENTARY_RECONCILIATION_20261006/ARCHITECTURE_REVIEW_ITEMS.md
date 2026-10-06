# Open architecture/governance review items

No normative rule changed; options are descriptive, no recommendation grants authority.

## Recovery and blind execution

CURRENT RULE: AGENTS/startup requires root bootstrap and canonical sync

OBSERVED BEHAVIOR: Recovery summaries may expose current target information; mixed population metadata contains timing boundary details

CONFLICT / FRICTION: Blind independence can conflict with complete recovery sync

EVIDENCE: Qualification HUMAN_FIREWALL_FAILURE.json and AUTHORITY_INSPECTION_RECORD.json

PI QUESTION: Should PI define a blind execution view distinct from full recovery authority?

POSSIBLE OPTIONS: Separate views; redacted metadata; explicit phase-specific access contracts — descriptive options only

## TASK versus PHASE

CURRENT RULE: Infrastructure requires task-specific admission and exact writer scope

OBSERVED BEHAVIOR: Preparatory subtasks repeatedly triggered registration and lease cycles

CONFLICT / FRICTION: Scientific task versus internal phase boundary is unclear

EVIDENCE: Qualification admission, packet/documentary preparation blockers in conversation and ledger

PI QUESTION: Which phases can remain within one admitted scientific task?

POSSIBLE OPTIONS: One admitted task with bounded phases; separately admitted preparatory tasks — no option adopted

## Backup exception execution

CURRENT RULE: Continuous backup helper synchronously writes old HD after relevant writes

OBSERVED BEHAVIOR: Exact-file I/O error reproduced despite PI-reported volume check; PI prohibits old-HD writes

CONFLICT / FRICTION: Normal helper cannot be invoked without violating current PI instruction

EVIDENCE: Preservation retry on PRINCIPAL_AUTHORITY_VERIFICATION.json; decision PI-DOCUMENTARY-RECONCILIATION-BACKUP-DEBT-20261006

PI QUESTION: How should explicit debt be represented and settled when replacement arrives?

POSSIBLE OPTIONS: Scoped debt ledger and guarded local adapter; future authorized replacement target — no policy rewrite here

## Bootstrap deferral

CURRENT RULE: Root bootstrap is generated from canonical sources and required at startup

OBSERVED BEHAVIOR: PI asks to review changed sources before regeneration

CONFLICT / FRICTION: Root will intentionally lag reconciled current sources

EVIDENCE: Current PI instruction; source documents and untouched bootstrap digest

PI QUESTION: How should next sessions recognize this reviewed source-over-generated deferral?

POSSIBLE OPTIONS: Explicit current coordination/debt gate; later regeneration after PI review — no change to root here

## External scientific registration

CURRENT RULE: External manifest indexes individual authorities, exact hashes and backup evidence

OBSERVED BEHAVIOR: Earlier October4–6 packages were not in the current index; old HD cannot now be certified

CONFLICT / FRICTION: Prior verification and current certification must remain distinct

EVIDENCE: SSD-only registrations in external manifest and authority inventory

PI QUESTION: What verification milestone is required on replacement device?

POSSIBLE OPTIONS: Registered-scope full hash verification plus original-namespace preservation — descriptive only

