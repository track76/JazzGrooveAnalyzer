# Jazz Groove Analyzer (JGA)

# Reference Validation Cases

Version 1.0

---

## RC-001

### Perfect Metronome

Description

Perfect periodic sequence with constant intervals.

Expected Result

- Regularity: Maximum
- Persistence: Maximum
- Continuity: Maximum
- Metric Compatibility: Maximum

---

## RC-002

### Walking Bass

Description

Walking bass performed by an experienced jazz bassist with natural micro-variations.

Expected Result

- Very high Regularity
- Maximum Persistence
- Maximum Continuity
- Maximum Metric Compatibility

---

## RC-003

### Ride Swing

Description

Ride cymbal with natural human timing.

Expected Result

- Very high Regularity
- Maximum Persistence
- Maximum Continuity
- Maximum Metric Compatibility

---

## RC-004

### Random Events

Description

Completely irregular sequence.

Expected Result

- Low Regularity
- Low Persistence
- Low Continuity

---

## RC-005

### Walking → Bass Solo

Description

Walking bass stops functioning as metric reference and starts a solo.

Expected Result

- Progressive decrease of Periodicity Score
- Automatic loss of Metric Role

---

## RC-006

### Ride → Brushes

Description

Ride stops and brushes become the rhythmic reference.

Expected Result

- Metric Role transferred
- Beat continuity preserved

---

## RC-007

### Triplet Subdivision

Description

Triplet subdivision inside one beat.

Expected Result

- High Metric Compatibility
- Beat continuity preserved

---

## RC-008

### Quintuplet Subdivision

Description

Quintuplet subdivision inside one beat.

Expected Result

- High Metric Compatibility
- Beat continuity preserved

---

## RC-009

### Metric Modulation

Description

Temporary metric transformation without loss of pulse.

Expected Result

- Periodicity preserved
- Metric Compatibility evaluated

---

## RC-010

### Ensemble Consensus

Description

Several metric sources converge toward the same pulse.

Expected Result

- Ensemble Metric Event generated
- High Confidence