from __future__ import annotations

from dataclasses import dataclass

from jga.source_understanding.rules.classification_rule import ClassificationRule


@dataclass(frozen=True, slots=True)
class RuleSet:
    """
    Immutable collection of classification rules.
    """

    rules: tuple[ClassificationRule, ...]
