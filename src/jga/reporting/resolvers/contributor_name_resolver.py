from uuid import UUID

from jga.domain.metric_contributor import (
    MetricContributor,
)

from jga.domain.sound_source import (
    SoundSource,
)


class ContributorNameResolver:
    """
    Resolves a contributor identifier into a
    human-readable sound source name.

    Reporting translation only.
    No musical interpretation is performed.
    """

    def resolve(
        self,
        contributor_id: UUID,
        contributors: tuple[MetricContributor, ...],
        sound_sources: tuple[SoundSource, ...],
    ) -> str:

        contributor = next(
            (
                item
                for item in contributors
                if item.id == contributor_id
            ),
            None,
        )

        if contributor is None:
            return "Unknown"

        source = next(
            (
                item
                for item in sound_sources
                if item.id == contributor.sound_source_id
            ),
            None,
        )

        if source is None:
            return "Unknown"

        return source.name
