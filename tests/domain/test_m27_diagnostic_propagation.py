
from jga.domain.behaviour_analytics_result import (
    BehaviourAnalyticsResult,
)

from jga.domain.behaviour_diagnostic_result import (
    BehaviourDiagnosticResult,
)

from jga.domain.services.behaviour_analytics_builder import (
    BehaviourAnalyticsBuilder,
)

from jga.domain.descriptor_set import DescriptorSet


def test_m27_diagnostic_propagation():

    diagnostic = object()

    builder = BehaviourAnalyticsBuilder()

    result = builder.build(
        DescriptorSet(
            descriptors=()
        ),
        diagnostic,
    )

    assert (
        result.behaviour_diagnostic_result
        is diagnostic
    )
