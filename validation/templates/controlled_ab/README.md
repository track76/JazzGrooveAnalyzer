# Controlled A/B Experiment Package Template

This operational template prepares the existing JGA structures for a matched
rhythmic-density experiment. It introduces no scientific entity, production
contract, Ground Truth quantity, Comparator behaviour, or interpretation.

## Preparation

Copy this directory to a new, human-approved Controlled Dataset location and
remove `.template` from each template filename. Replace every
`__REQUIRED_*__` value with externally supplied scientific content.

Required layout:

```text
controlled_ab_manifest.json
symbolic/condition_a.musicxml
symbolic/condition_b.musicxml
ground_truth/condition_a.ground_truth.json
ground_truth/condition_b.ground_truth.json
audio/condition_a.wav
audio/condition_a_repeat.wav
audio/condition_b.wav
audio/condition_b_repeat.wav
audio/condition_a.mp3
audio/condition_b.mp3
provenance/dataset_generation_record.md
provenance/event_removal_inventory.json
validation/run_<timestamp>/
```

The WAV files are the controlled observation assets. The MP3 files satisfy the
existing schema-1 Validation Item binding and are not substitutes for the WAV
evidence. Each condition becomes an ordinary Validation Item only after its
human-approved data is added to `recordings/validation/catalog.json`.

## Validation gate

Run:

```bash
python tools/validate_controlled_ab_package.py <package-root>
```

The gate rejects unresolved placeholders, missing assets, checksum mismatch,
non-PCM WAV, unequal audio measurement conditions, ambiguous event identity,
an empty removal set, and any retained-event timing change.

The gate does not decide which events to remove, infer musical identity,
execute analysis, or load Ground Truth during blind discovery.

## Execution order

1. Validate the completed package.
2. Create a new non-overwriting SVP-001 run directory.
3. Record repository revision, bootstrap revision, identities, checksums, and
   configuration in `experiment_manifest.json`.
4. Analyze neutralized Condition A and B WAV identities blind.
5. Freeze both CandidatePeriodPopulation representations and their
   fingerprints in `blind_results.json`.
6. Only then reveal condition assignment, load each existing-schema Ground
   Truth reference, and write `post_blind_evaluation.json`.
7. Execute the existing catalogue-bound immutable validation chain for each
   registered Validation Item and preserve the identities and fingerprints in
   `validation_chain_results.json`. The immutable representations, Comparator
   results, and Scientific Validation Records remain ordinary existing-schema
   artifacts rather than fields of a new A/B model.

No placeholder package is scientifically executable.
