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

        previous_timestamp = None

        for pulse in pulses:

            if pulse is None:
                raise ValueError(
                    "Pulse sequence cannot contain None values."
                )

            if not isinstance(pulse, Pulse):
                raise TypeError(
                    "All elements must be Pulse instances."
                )

            if (
                previous_timestamp is not None
                and pulse.timestamp < previous_timestamp
            ):
                raise ValueError(
                    "Pulse sequence is not chronologically ordered."
                )

            previous_timestamp = pulse.timestamp
