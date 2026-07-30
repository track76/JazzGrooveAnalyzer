# Instrument Classification Decision Table

| Feature | Bass | Chordal | Percussion | Wind | Voice |
|----------|------|----------|-------------|------|-------|
| RMS | medium-high | medium | high transient peaks | medium | medium |
| Zero Crossing Rate | low | medium | high | medium | medium |
| Spectral Centroid | low | medium | high | medium-high | medium |
| Spectral Bandwidth | narrow | medium | wide | medium | medium |
| Spectral Rolloff | low | medium | high | medium-high | medium |
| Duration | sustained | sustained | short | sustained | sustained |

---

# Interpretation

## Bass

- low-frequency dominant
- low spectral centroid
- low rolloff
- low zero crossing rate
- sustained notes

## Chordal

- harmonic spectrum
- medium centroid
- medium bandwidth
- sustained events

## Percussion

- transient attacks
- high centroid
- high bandwidth
- high rolloff
- high zero crossing rate
- short duration

## Wind

- sustained energy
- medium-high centroid
- medium bandwidth
- moderate rolloff

## Voice

- sustained signal
- medium centroid
- moderate bandwidth
- harmonic content
