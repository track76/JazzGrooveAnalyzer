# JGA M32 START CONTEXT

## Milestone

M32 — Source Understanding Integration


## Starting Point

M31 completed.

JGA can now transform a real jazz recording into separated audio sources.


Current flow:

Audio File

↓

Demucs Separation

↓

AudioStemCollection

↓

JGA Core


## Scientific Goal

Move from:

"separated audio signals"

to:

"interpreted musical entities"


## Target Architecture


AudioStem

↓

Source Identification

↓

SoundSource

↓

MusicalFunction

↓

MetricContributor


## Existing Domain Objects

Available:

- SoundSource
- MusicalFunction
- MetricContributor


## Existing Services

To audit:

- SourceIdentificationService
- RuleBasedMusicalFunctionAssignmentService
- RuleBasedMetricContributorAssignmentService


## First Development Task

Perform architectural audit.

Do not implement immediately.

Define:

- input contract
- output contract
- transformations
- provenance preservation
- validation strategy


## Constraints

JGA must remain:

- scientifically interpretable
- modular
- backend independent
- test driven


Every transformation must be explicit.
