
from dataclasses import dataclass

from jga.domain.behaviour_observation import (
    BehaviourObservation,
)

from jga.domain.behaviour_profile import (
    BehaviourProfile,
)


@dataclass(frozen=True, slots=True)
class BehaviourConstructionResult:
    """
    Explicit output contract for behaviour construction.

    Contains only domain behaviour objects.

    It must not depend on runtime context
    or pipeline structures.
    """

    behaviour_observations: (
        tuple[BehaviourObservation, ...]
    )

    behaviour_profile: (
        BehaviourProfile | None
    )
