from __future__ import annotations

from dataclasses import dataclass

from jga.core.stability_curve import StabilityCurve

from jga.domain.behaviour_profile import BehaviourProfile


@dataclass(frozen=True, slots=True)
class BehaviourQuantificationContext:
    """
    Explicit input contract for Behaviour Quantification.

    M5 transforms validated representations and analytical
    measurements into BehaviourDescriptor objects.

    It does not recompute metric analysis.
    """

    behaviour_profile: BehaviourProfile
    stability_curve: StabilityCurve

    def __post_init__(self) -> None:

        if self.behaviour_profile is None:
            raise ValueError(
                "BehaviourProfile is required"
            )

        if self.stability_curve is None:
            raise ValueError(
                "StabilityCurve is required"
            )
