# H-CEDVAL006-RX11-BASS-SEPARATION-BENCHMARK-01-R1

Status: **PROSPECTIVELY CORRECTED — AWAITING MANUAL RX EXPORT**

## Evidence Conflict and resolution

Before rendering, the PI observed that RX 11.2.0 exposes all four Music
Rebalance Sensitivity controls on an integer 0–100 scale and that Reset sets
Vocal, Bass, Drums and Other to 50. The original preregistration encoded `5.0`.
No render or output analysis occurred.

The original scientific intent was the untouched reset/default midpoint, not
a sensitivity below the midpoint. Revision R1 therefore corrects only the
scale representation: every Sensitivity is frozen at UI value `50` on the
verified `[0,100]` scale and state `RESET_DEFAULT_MIDPOINT`. The original
protocol, commit and fingerprint remain preserved as historical evidence.

All other authorities, gains, Bass-only Solo state, Best quality, export
format, operator steps, evaluation metrics, decision gates, reproducibility
requirements and scientific firewalls remain unchanged.

## Corrected operator step

After opening Music Rebalance, press Reset and verify—not merely assume—that
Vocal, Bass, Drums and Other each display Sensitivity `50`. Do not change
those four values. If any value or scale differs, stop without rendering.

Continue with the original operator protocol except that its sensitivity
step is superseded by this corrected step. No render is authorized from the
superseded `5.0` representation.
