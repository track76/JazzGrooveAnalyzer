# F-017 — Physical Offset Comparison

Status

Draft

------------------------------------------------------------

Purpose

Determine whether two consecutive observation
frames belong to the same Stable Region.

------------------------------------------------------------

Current Measurement

Physical Offset (milliseconds)

------------------------------------------------------------

Decision Rule

If the absolute difference between two
consecutive physical offsets is smaller than
the configured tolerance, the Stable Region
continues.

Otherwise a new Stable Region starts.

