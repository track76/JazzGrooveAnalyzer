# Evaluation schema-key remediation

The first evaluation launch failed with
`KeyError: 'authorities_locked_until_evaluation'` before either Bass-reference
authority or any Bass-reference outcome was opened, computed, printed, logged,
or inspected.

The evaluator expected the prior CED-VAL-006 protocol key
`authorities_locked_until_evaluation`; this preregistration names the same
authority block `authorities_locked_until_candidate_commit`.

The bounded correction replaces exactly:

`auth=p['authorities_locked_until_evaluation']`

with:

`auth=p['authorities_locked_until_candidate_commit']`

No candidate, authority, scientific parameter, threshold, matching rule,
metric, pitch rule, decision gate, or interpretation changed.
