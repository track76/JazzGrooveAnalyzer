# AD-032 — M89 PulseCandidate Strength Preservation

Status: LOCKED

## Context

The Development Constitution places Scientific Theory and the Observation
Model above Architecture and Implementation. The active theoretical framework
and the stable Representation Translation contract require observable
information to survive Translation unless an explicit theoretical
justification authorizes its removal.

AD-026 defined Core PulseCandidate input with `strength`, but omitted that
quantity from its Domain PulseCandidate output. No authoritative supersession
or theoretical justification for that omission exists.

## Decision

`PulseCandidate.strength` is preserved as an immutable observational quantity.

Its preservation introduces no musical, metrical, accentual, behavioural or
interpretative semantics.

M89 restores the observation-preservation invariant only.

The Translation boundary copies the observed numeric value exactly from Core
PulseCandidate to Domain PulseCandidate. It does not normalize, aggregate,
reinterpret or use the value in downstream computation.

## Supersession

This decision explicitly supersedes only the incomplete output mapping in
AD-026 — Domain Pulse Candidate Translation Boundary. All other AD-026
responsibilities, dependency directions and non-responsibilities remain in
force.

The corrected mapping is:

Core PulseCandidate:

- time;
- strength;
- confidence.

Domain PulseCandidate:

- id;
- sound source identity;
- timestamp;
- strength;
- confidence;
- creation metadata.

## Scope

This decision changes only preservation across the Translation boundary. It
does not modify Behaviour analysis, Metric reconstruction, Comparator, Ground
Truth, Immutable Analysis Representation or Scientific Validation Record.

It introduces no new scientific quantity and no new interpretation of the
existing observation.

## Validation

Validation requires focused immutable-domain and Translation tests, exact
strength preservation through both translation paths, and real VAL-001 audio
pipeline evidence.
