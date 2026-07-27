from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class InternalMetricSignature:
    """
    Scientific representation of the reconstructed
    internal metric signature.
    """

    numerator: int

    denominator: int

    @property
    def beats_per_measure(
        self,
    ) -> int:

        return self.numerator

    def __str__(
        self,
    ) -> str:

        return (
            f"{self.numerator}/{self.denominator}"
        )

