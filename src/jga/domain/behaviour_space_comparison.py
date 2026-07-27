from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BehaviourSpaceComparison:

    comparable: bool

    reason: str

