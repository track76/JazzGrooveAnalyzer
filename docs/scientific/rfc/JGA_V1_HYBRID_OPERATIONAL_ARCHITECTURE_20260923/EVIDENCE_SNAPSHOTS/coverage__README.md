# Quarter-nearest candidate-coverage sensitivity audit

Additive noncanonical study JGA-QUARTER-NEAREST-ONSET-COVERAGE-SENSITIVITY-001, 2026-09-22. Track: Ray Brown Trio, Exactly Like You.

Start with [RESULT.md](RESULT.md), [preregistration](JGA_QUARTER_NEAREST_ONSET_COVERAGE_PREREGISTRATION.json), [validation](INDEPENDENT_VALIDATION.json), and [result freeze](JGA_QUARTER_NEAREST_ONSET_COVERAGE_SENSITIVITY_RESULT_FREEZE.json). Parent selections and all contextual candidates remain immutable.

`preregister.py` records parent integrity and freezes rules before results; `analyze.py` implements diagnostic loss only; `verify.py` independently checks selection and window arithmetic using SciPy; `figures.py` generates the six requested figures in PNG/SVG/PDF. These preparation scripts have freeze guards and must not be rerun over frozen artifacts. They do not run models or change canonical code.

QUARTER_COVERAGE_METRICS contains every quarter, including EMPTY. SELECTION_MARGIN has NA when no second candidate exists. LEAVE_ONE_SELECTED_OUT removes one parent winner at a time. THINNING_DEFINITIONS preserves exact removed IDs for all 35 periodic phases. THINNING_RESULTS preserves all 946 quarters per scenario. WINDOW_COVERAGE_SENSITIVITY retains all fixed windows, including unchanged ones; local leave-one-out conclusions use affected scenarios only. REFERENCE/RECURRENCE audit files contain record types separating baseline coverage and perturbation results. SOURCE_COVERAGE_COMPARISON and COVERAGE_ASSOCIATIONS preserve descriptive comparisons. SUMMARY.json carries full-precision aggregates.

Result freeze precedes all authoritative documentation edits. ARTIFACT_HASHES inventories this package except itself; documentation outside the package is bound separately in DOCUMENTATION_UPDATE_MANIFEST. No staging, commit or push.
