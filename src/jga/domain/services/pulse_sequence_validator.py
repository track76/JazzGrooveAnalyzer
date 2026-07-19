from jga.domain.pulse import Pulse


class PulseSequenceValidator:
    """
    Validates a Pulse sequence before higher-level metric reconstruction.
    """

    def validate(
        self,
        pulses: tuple[Pulse, ...],
    ) -> None:

        if not pulses:
            raise ValueError(
                "At least one Pulse is required."
            )

        for pulse in pulses:

            if pulse is None:
                raise ValueError(
                    "Pulse sequence cannot contain None values."
                )

            if not isinstance(pulse, Pulse):
                raise TypeError(
                    "All elements must be Pulse instances."
                )
