# Classification Scoring

## Purpose

The classification scoring system quantifies how strongly the observable
features support a given instrument family.

The score is **not** a probability and **not** the output of a statistical
model.

It is an interpretable measure of evidence accumulation.

---

## Scientific Principles

The scoring system shall satisfy the following principles:

1. Deterministic.
2. Explainable.
3. Reproducible.
4. Independent of machine learning.
5. Based only on observable acoustic evidence.

---

## Rule Evaluation

Each classification rule produces a RuleResult.

A rule may be:

- satisfied
- not satisfied

Each satisfied rule contributes one independent piece of evidence.

---

## Confidence

Confidence expresses the proportion of expected evidence that has been
observed.

Let

S = number of satisfied rules

T = total number of rules

Then

confidence = S / T

Properties:

- 0.0 → no supporting evidence
- 1.0 → all expected evidence observed

Examples

RuleSet size = 2

0 satisfied -> 0.0

1 satisfied -> 0.5

2 satisfied -> 1.0

RuleSet size = 5

0 satisfied -> 0.0

1 satisfied -> 0.2

2 satisfied -> 0.4

3 satisfied -> 0.6

4 satisfied -> 0.8

5 satisfied -> 1.0

---

## Interpretation

Confidence measures the completeness of the observed evidence,
not the certainty of the classification.

Additional rules increase confidence only when they are independently
satisfied.

---

## Future Extensions

Future versions may introduce weighted rules.

The aggregation mechanism may change from

confidence = S / T

to

confidence = weighted_sum / total_weight

without changing the public architecture.

---

## Range Based Rules

Some instrument families are characterized by intermediate values.

Example:

- medium spectral centroid
- medium spectral bandwidth

These cases cannot be represented by only high/low comparisons.

A range rule expresses:

lower_bound <= feature <= upper_bound

Range rules remain deterministic and interpretable.
