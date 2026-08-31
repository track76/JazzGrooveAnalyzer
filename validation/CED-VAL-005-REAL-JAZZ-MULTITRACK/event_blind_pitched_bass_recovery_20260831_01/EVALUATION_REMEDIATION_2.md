# Second evaluation schema-key remediation

The second evaluation launch passed authority verification and performed the
frozen evaluation calculations in memory. It then failed with
`KeyError: 'interpretation_firewall'` before result serialization,
fingerprinting, or printing.

No outcome value was displayed, logged, written, or inspected, and no
`result_1.json` was created. The frozen 661-candidate authority remained
unchanged.

The protocol stores the unchanged interpretation text under
`scientific_firewall`; the evaluator attempted to read the absent key
`interpretation_firewall`. The bounded correction replaces exactly:

`p['interpretation_firewall']`

with:

`p['scientific_firewall']`

No candidate, authority, scientific parameter, threshold, matching rule,
pitch rule, metric, decision gate, or interpretation changed.
