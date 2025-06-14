from enum import unique, StrEnum


@unique
class DetectionStatus(StrEnum):

    PENDING = "pending"
    """
    Pending to be executed
    """

    EXECUTED = "executed"
    """
    Detection algorithm executed
    """
