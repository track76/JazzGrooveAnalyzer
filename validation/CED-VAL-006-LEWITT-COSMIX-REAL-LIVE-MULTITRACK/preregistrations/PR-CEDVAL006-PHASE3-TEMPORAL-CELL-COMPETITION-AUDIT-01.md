# PR-CEDVAL006-PHASE3-TEMPORAL-CELL-COMPETITION-AUDIT-01

Status: **PREREGISTERED — NOT EXECUTED**

This read-only audit reconstructs the complete unprocessed and processed Bass
candidate inventories inside the already frozen original-EME Voronoi cells.
It uses the frozen scorer's exact half-open boundaries and selection order:
minimum absolute original-time displacement, then earlier timestamp, then
native observation index. This rule is evaluated only to reproduce historical
assignments; it is not a production proposal.

Candidate identity is exact 44.1-kHz producer sample coordinate. The audit
records retained, new and disappeared coordinates, candidate counts, selected
coordinates, existing serialized onset evidence and original-time distance.
The canonical reports do not serialize candidate strength; absence is recorded
rather than inferred.

Timing contribution is summarized for the mutually exclusive processed-match
groups B, E and A-minus-E using displacement distributions and squared-error
share. A future intervention is `YES` only if the dominant mechanism also has
a serialized candidate attribute available without original Ground Truth that
supports a bounded principle. It is `INDETERMINATE` when a mechanism is shown
but no such discriminating attribute is preserved, and `NO` when no stable
mechanism is shown. No intervention is designed or executed.

Full authority, categories, metrics, replay requirements and firewalls are in
the adjacent JSON.
