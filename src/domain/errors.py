from enum import StrEnum


class DomainError(Exception):
    def __init__(self, error_code: str):
        super().__init__(error_code)


class ErrorCodes(StrEnum):
    MUST_BE_MORE_THAN_ZERO = "MUST_BE_MORE_THAN_ZERO"
    LESS_THAN_CURRENT_PRICE = "LESS_THAN_CURRENT_PRICE"
    LOT_ALREADY_EXISTS = "LOT_ALREADY_EXISTS"
    LOT_NOT_FOUND = "LOT_NOT_FOUND"
    LOT_IS_ENDED = "LOT_IS_ENDED"

    BID_NOT_MORE_THAN_EXISTENCE = "BID_NOT_MORE_THAN_EXISTENCE"
    TOO_SMALL_STEP = "TOO_SMALL_STEP"
