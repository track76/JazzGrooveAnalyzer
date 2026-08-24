# PR-CED-VAL-007-CONTROLLED-BEAT-BENCHMARK-001

Status: **CONTROLLED_BEAT_REFERENCE_PARTIAL**

This record freezes the supplied raw assets, the checksum-bound Ableton Live
Set, its prospective symbolic temporal schedule, and the mapping from the
arrangement render range to the exported WAV coordinate. It does not execute
JGA or an external tracker and does not establish rendered-response onset.

## Source authority and PI clarification

The canonical source definition is the checksum-bound Ableton Live Set listed
in `input_authority_manifest.json`. Direct inspection supersedes the earlier
descriptive statement that both tracks used MIDI note C2:

- `DRUM GT` uses MIDI key 48;
- `MARKER GT` uses MIDI key 60; and
- both tracks contain 64 enabled events at identical arrangement beat
  positions 0 through 63, with velocity 100, velocity deviation 0,
  probability 1 and groove ID -1.

The pitch difference is accepted by the PI and has no effect on the identity
of the symbolic temporal population. No source file was changed.

## Symbolic temporal authority

The Live Set freezes tempo 120 BPM and meter 4/4. Its target tracks each
contain sixteen consecutive four-beat arrangement clips beginning at
arrangement time 0, with events at local clip times 0, 1, 2 and 3. The PI's
prospective export declaration freezes render start 1.1.1 and length 16.0.0
bars. Every exported WAV has exactly 1,411,200 frames at 44,100 Hz, or 32
seconds, matching sixteen 4/4 bars at 120 BPM. Together these authorities map
arrangement time 0 / 1.1.1 to exported sample zero without ambiguity for this
bounded dataset.

The 64 positions in `symbolic_beat_reference.json` are therefore
`SYMBOLIC_BEAT_GROUND_TRUTH`: for beat index `i` from 0 through 63,
`sample(i) = 22050 * i` and `time(i) = i / 2` seconds. This authority concerns
the prospectively authored symbolic positions only. It is independent of JGA,
librosa and Essentia.

## Separate rendered objects

The following objects remain distinct:

1. the symbolic beat position;
2. the rendered `MARKER GT` waveform response; and
3. the rendered `DRUM GT` waveform response.

The CED-VAL-004 first-nonzero physical-response rule is not applicable
unchanged. That rule requires checksum-bound source-specific digital-silence
controls, exact-zero two-second pre-marker baselines, isolated ten-second
slots and fixed eight-second causal windows. CED-VAL-007 supplies neither the
required control renders nor that event geometry. Consequently no marker or
drum response onset, latency, displacement, physical onset or uncertainty is
authorized here. No substitute threshold or onset rule was invented.

## Asset roles

- `DRUM GT.wav`: candidate controlled benchmark audio input.
- `MARKER GT.wav`: candidate rendered temporal-reference channel; not the
  symbolic Beat Ground Truth and not physical-onset authority.
- Master render: supporting render only.
- `A-Reverb`: non-scientific return render for this benchmark.
- `B-Delay`: non-scientific return render for this benchmark.

AppleDouble files are inventoried as filesystem metadata and excluded from
scientific asset identity and the dataset fingerprint. Ableton backups and
filesystem metadata are supporting inventory only; the named canonical Live
Set is the sole source-definition authority.

## Firewalls

JGA, Essentia, librosa, H02 and strength were not executed or accessed.
No detector comparison, musical interpretation, production change, raw-asset
change, correction, shift, render or derived asset is authorized by this
record.
