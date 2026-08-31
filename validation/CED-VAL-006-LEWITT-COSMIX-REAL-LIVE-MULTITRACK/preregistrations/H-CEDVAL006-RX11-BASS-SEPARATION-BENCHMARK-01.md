# H-CEDVAL006-RX11-BASS-SEPARATION-BENCHMARK-01

Status: **PREREGISTERED — AWAITING MANUAL RX EXPORT**

This benchmark compares one prospectively frozen iZotope RX 11.2.0 Music
Rebalance Bass export with the frozen deterministic htdemucs_ft Bass result.
It evaluates only preservation of the authorized original-Bass JGA event
population and temporal localization. It does not evaluate perceptual quality
or commercial superiority.

## Frozen operator protocol

1. Confirm RX About/Info reports `RX 11 Audio Editor 11.2.0`, build
   `11.2.0.4231`. If not, stop.
2. Verify the controlled mix SHA-256 is
   `32845a5d05538524b19c8f857b0a908f6618cc4b95110a14169f1e450ddfe6e0`.
3. Open only `CED-VAL-006-CONTROLLED-MIXDOWN-v0.1.wav` in RX.
4. Select the complete file, sample scope `[0,11912868)`.
5. Open **Music Rebalance** and reset the module.
6. Set Quality to **Best**.
7. Set Vocals, Bass, Percussion and Other gains to exactly `0.0 dB`.
8. Set all four sensitivities to exactly `5.0`.
9. Enable **Solo** for Bass only. Leave every Mute control off and every other
   Solo control off. Do not use **Stem Split**.
10. Capture a screenshot showing the complete module configuration.
11. Do not Preview, audition, listen, compare, or change settings. Render once.
12. Export once as stereo RIFF/WAVE, 48,000 Hz, IEEE 32-bit float; disable
    normalization, dither and sample-rate conversion.
13. Save exactly as
    `CED-VAL-006-RX11.2.0-MUSIC-REBALANCE-BASS-v0.1.wav` at the path frozen in
    the adjacent JSON. Capture the export-dialog screenshot.
14. Do not open or analyze the export. Record its SHA-256 and technical
    properties, plus operator identity and UTC operation time, then provide
    those records to Codex.

If any named control or exact value is unavailable, or any additional
processing control cannot be neutralized, stop without rendering and report
the discrepancy. No substitute setting is authorized.

The full input, output, evaluation, decision, reproducibility and firewall
authorities are frozen in the adjacent JSON.
