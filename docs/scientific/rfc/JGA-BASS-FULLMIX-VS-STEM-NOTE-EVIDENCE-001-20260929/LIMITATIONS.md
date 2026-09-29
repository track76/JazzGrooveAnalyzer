# Limitations — JGA-BASS-FULLMIX-VS-STEM-NOTE-EVIDENCE-001-20260929

## What this evidence is
Convergent computational evidence that bass note candidates found in the isolated bass stem
also appear in the full mix within fixed temporal tolerances (T0/T1/T2/T4), and that where both
arms yield a finite F0 the two estimates often agree.

## What this evidence is NOT
- Not verified or "true" notes. No Ground Truth, no human annotation, no independent label exists in this project.
- Not independent confirmation. Every artifact was produced by one agent using one codebase.
  The FULLMIX 458-event reproduction is a code-port check, not a replication.
- Not an accuracy measure. There is nothing here to compare a detection against.
- Not `STEM_BETTER` or `FULLMIX_BETTER`. Coverage differences between arms are descriptive.
- Not a separator leakage measurement. See SEPARATOR_PROVENANCE.json.

## Method limitations
- Temporal matching only. No pitch threshold, no nearest-neighbour choice, no one-to-one
  assignment, no candidate deletion. All events, matched or not, are retained in every family.
- Connected components merge transitively. At T2 and T4 a component can contain several events
  per arm, so component counts are not pair counts and the two must not be compared directly.
- Tolerance families are not nested in their conclusions. Widening T0->T4 raises coverage and
  raises ambiguity simultaneously; the direction of travel is the only safe statement.
- The 43.06640625 Hz boundary is a fixed reporting descriptor, not an acceptance criterion.
  No pair is accepted or rejected on pitch anywhere in this analysis.

## Population limitations
- 255 of 328 T1 pairs have finite F0 in both arms. The remaining 73 are pitch-free and are
  reported as absence of a pitch estimate, not as disagreement.
- Low-register pairs number 17 at T1. This is far too small a group to characterise, and is
  reported only because the preregistration fixed the boundary in advance.
- Both arms are the same performance through a separator. Shared upstream artifacts (mixing,
  performance, tuning) are expected in both populations and are not controlled for.

## Process limitations
- Six process deviations (DEV-1..DEV-6) are recorded in EXECUTION_PROVENANCE.json. They were
  detected by cross-checks rather than review, and one (DEV-6) was a governance breach.
- Artifacts are large JSON/CSV files; they are generated deterministically but this run
  provides no bit-reproducibility guarantee across platforms or library versions.
