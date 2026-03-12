from dataclasses import dataclass

from domain.errors import DomainError, ErrorCodes


@dataclass(slots=True, frozen=True)
class PriceVO:
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise DomainError(ErrorCodes.MUST_BE_MORE_THAN_ZERO)

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __le__(self, other) -> bool:
        return self.value <= other.value

    def __gt__(self, other) -> bool:
        return self.value > other.value

    def __ge__(self, other) -> bool:
        return self.value >= other.value
