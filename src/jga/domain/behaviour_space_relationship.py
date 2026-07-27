from enum import Enum


class BehaviourSpaceRelationship(str, Enum):

    COINCIDENT = "coincident"

    PARALLEL = "parallel"

    CONVERGENT = "convergent"

    DIVERGENT = "divergent"

    INTERSECTING = "intersecting"

    PARTIALLY_OVERLAPPING = (
        "partially_overlapping"
    )

