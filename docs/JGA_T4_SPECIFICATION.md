# Jazz Groove Analyzer

# T4 – Musical Analysis Services

## Objective

The objective of T4 is to transform the Domain Model developed during T3
into a complete musical analysis pipeline.

No new domain entities should be introduced unless strictly necessary.

All services operate on existing domain objects.

---

# Global Pipeline

AudioRecording
        │
        ▼
Stem Separation
        │
        ▼
AudioStem
        │
        ▼
Source Identification
        │
        ▼
SoundSource
        │
        ▼
Musical Function Assignment
        │
        ▼
Metric Contributor Resolution
        │
        ▼
Pulse Construction
        │
        ▼
Metric Cluster Construction
        │
        ▼
Internal Metric Timeline
        │
        ▼
Temporal Analysis
        │
        ▼
Analysis Report

---

## Services

### SourceIdentificationService

Input

- AudioStem

Output

- SoundSource

---

### MusicalFunctionAssignmentService

Input

- SoundSource

Output

- MusicalFunction

---

### MetricContributorResolver

Input

- SoundSource
- MusicalFunction

Output

- MetricContributor

---

### PulseBuilder

Input

- MetricCluster

Output

- Pulse

---

### MetricClusterBuilder

Input

- ElementaryMetricEvent

Output

- MetricCluster

---

### InternalMetricTimelineBuilder

Input

- Pulse

Output

- InternalMetricTimeline

---

## Development Workflow

Theory

↓

Tests

↓

Implementation

↓

Validation

↓

Refactoring