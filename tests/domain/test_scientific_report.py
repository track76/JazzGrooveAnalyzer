from jga.domain.scientific_report import (
    ScientificReport,
)

from jga.domain.descriptor_set import (
    DescriptorSet,
)


def test_scientific_report_creation():

    report = ScientificReport(
        descriptor_set=DescriptorSet(
            descriptors=(),
        ),
        analytical_structure=None,
        scientific_evidence=None,
    )

    assert report is not None
