from uuid import UUID

from jga.domain.metric_contributor import MetricContributor


class MetricContributorResolver:
    """
    Resolves the MetricContributor associated
    with a SoundSource.

    Mapping:

        SoundSource.id
              |
              ▼
        MetricContributor.sound_source_id
              |
              ▼
        MetricContributor.id
    """

    def resolve(
        self,
        sound_source_id: UUID,
        contributors: tuple[MetricContributor, ...],
    ) -> MetricContributor:

        if sound_source_id is None:
            raise ValueError(
                "sound_source_id cannot be None."
            )

        if contributors is None:
            raise ValueError(
                "contributors cannot be None."
            )

        for contributor in contributors:

            if contributor.sound_source_id == sound_source_id:
                return contributor

        raise ValueError(
            f"No MetricContributor found for SoundSource "
            f"{sound_source_id}."
        )
